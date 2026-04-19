"""Indice RAG minimal sobre los PDFs de TEORIA/.

Estrategia:
- Extrae texto página a página con PyMuPDF (ya es dependencia de guide_index).
- Parte el contenido en chunks de ~400 palabras con solapamiento de ~80.
- Embeddea con Ollama (nomic-embed-text).
- Persiste en theory/_cache/rag_index.pkl.
- Busca por similitud coseno (numpy puro — faiss es opcional).

Invalidación por mtime de los PDFs + MACHETE.md.
"""

from __future__ import annotations

import hashlib
import os
import pickle
import re
from dataclasses import dataclass
from typing import Iterable

from config.settings import TEORIA_DIR, THEORY_CACHE_DIR, MACHETE_PATH


@dataclass
class Chunk:
    text: str
    source_pdf: str     # interno, nunca se muestra al usuario
    page: int           # interno
    score: float = 0.0


def _iter_pdfs() -> list[str]:
    if not os.path.isdir(TEORIA_DIR):
        return []
    out: list[str] = []
    for name in sorted(os.listdir(TEORIA_DIR)):
        if name.lower().endswith(".pdf"):
            out.append(os.path.join(TEORIA_DIR, name))
    return out


def _fingerprint(paths: list[str]) -> str:
    h = hashlib.sha256()
    for p in paths:
        try:
            h.update(p.encode("utf-8"))
            st = os.stat(p)
            h.update(str(int(st.st_mtime)).encode("utf-8"))
            h.update(str(st.st_size).encode("utf-8"))
        except FileNotFoundError:
            continue
    if os.path.exists(MACHETE_PATH):
        st = os.stat(MACHETE_PATH)
        h.update(str(int(st.st_mtime)).encode("utf-8"))
    return h.hexdigest()[:16]


def _extract_chunks_from_pdf(path: str) -> list[Chunk]:
    try:
        import fitz  # PyMuPDF
    except ImportError:
        return []
    chunks: list[Chunk] = []
    try:
        doc = fitz.open(path)
    except Exception:
        return []
    try:
        for page_idx in range(len(doc)):
            page = doc[page_idx]
            text = page.get_text("text") or ""
            text = re.sub(r"[ \t]+", " ", text)
            text = re.sub(r"\n{3,}", "\n\n", text).strip()
            if not text or len(text) < 80:
                continue
            # Partición por palabra: ~400 con overlap 80
            words = text.split()
            step = 320  # 400 - 80 overlap
            size = 400
            for i in range(0, len(words), step):
                piece = " ".join(words[i:i + size])
                if len(piece) < 120:
                    continue
                chunks.append(Chunk(text=piece, source_pdf=path, page=page_idx + 1))
    finally:
        doc.close()
    return chunks


def _extract_chunks_from_md(path: str) -> list[Chunk]:
    if not os.path.exists(path):
        return []
    try:
        with open(path, encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return []
    out: list[Chunk] = []
    # Partir por secciones "## "
    blocks = re.split(r"\n(?=##?\s)", content)
    for i, block in enumerate(blocks):
        block = block.strip()
        if len(block) < 60:
            continue
        out.append(Chunk(text=block, source_pdf=path, page=i + 1))
    return out


def _cosine(a, b):
    import math
    s = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0 or nb == 0:
        return 0.0
    return s / (na * nb)


class RAGIndex:
    def __init__(self, cache_dir: str = THEORY_CACHE_DIR):
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)
        self.cache_path = os.path.join(self.cache_dir, "rag_index.pkl")
        self._chunks: list[Chunk] = []
        self._embeds: list[list[float]] = []
        self._fp: str = ""

    def _load_cache(self) -> bool:
        if not os.path.exists(self.cache_path):
            return False
        try:
            with open(self.cache_path, "rb") as f:
                obj = pickle.load(f)
        except Exception:
            return False
        self._chunks = obj.get("chunks", [])
        self._embeds = obj.get("embeds", [])
        self._fp = obj.get("fp", "")
        return True

    def _save_cache(self):
        try:
            with open(self.cache_path, "wb") as f:
                pickle.dump(
                    {"chunks": self._chunks, "embeds": self._embeds, "fp": self._fp},
                    f,
                )
        except Exception:
            pass

    def build(self, *, force: bool = False) -> int:
        pdfs = _iter_pdfs()
        current_fp = _fingerprint(pdfs)

        if not force and self._load_cache() and self._fp == current_fp and self._chunks:
            return len(self._chunks)

        chunks: list[Chunk] = []
        for pdf in pdfs:
            chunks.extend(_extract_chunks_from_pdf(pdf))
        chunks.extend(_extract_chunks_from_md(MACHETE_PATH))
        self._chunks = chunks

        # Embed (si Ollama está — si no, dejamos sin embeds para fallback textual)
        try:
            from llm.ollama_client import OllamaClient, OllamaUnavailable
            client = OllamaClient()
            if client.is_available() and self._chunks:
                # batch en grupos de 32 para no saturar
                self._embeds = []
                batch = 32
                for i in range(0, len(self._chunks), batch):
                    texts = [c.text for c in self._chunks[i:i + batch]]
                    try:
                        embs = client.embed(texts)
                    except OllamaUnavailable:
                        embs = []
                    if not embs or len(embs) != len(texts):
                        self._embeds = []
                        break
                    self._embeds.extend(embs)
            else:
                self._embeds = []
        except Exception:
            self._embeds = []

        self._fp = current_fp
        self._save_cache()
        return len(self._chunks)

    def search(self, query: str, top_k: int = 6) -> list[Chunk]:
        if not self._chunks:
            self._load_cache()
        if not self._chunks:
            return []

        # Si tenemos embeddings, usamos similitud vectorial
        if self._embeds and len(self._embeds) == len(self._chunks):
            try:
                from llm.ollama_client import OllamaClient
                client = OllamaClient()
                q_emb = client.embed([query])[0]
            except Exception:
                q_emb = None
            if q_emb:
                scored: list[tuple[float, Chunk]] = []
                for c, e in zip(self._chunks, self._embeds):
                    s = _cosine(q_emb, e)
                    scored.append((s, c))
                scored.sort(key=lambda t: t[0], reverse=True)
                out = []
                for s, c in scored[:top_k]:
                    c2 = Chunk(text=c.text, source_pdf=c.source_pdf, page=c.page, score=s)
                    out.append(c2)
                return out

        # Fallback BM25-lite: conteo de términos
        q_terms = set(re.findall(r"\w{3,}", query.lower()))
        scored: list[tuple[float, Chunk]] = []
        for c in self._chunks:
            text_low = c.text.lower()
            s = sum(text_low.count(t) for t in q_terms)
            if s > 0:
                scored.append((float(s), c))
        scored.sort(key=lambda t: t[0], reverse=True)
        return [
            Chunk(text=c.text, source_pdf=c.source_pdf, page=c.page, score=s)
            for s, c in scored[:top_k]
        ]


_singleton: RAGIndex | None = None


def get_index() -> RAGIndex:
    global _singleton
    if _singleton is None:
        _singleton = RAGIndex()
        _singleton.build()
    return _singleton
