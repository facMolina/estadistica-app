"""Indexador del PDF de la Guia de Problemas.

Flujo:
  load_or_build_index() -> dict con todos los ejercicios por tema
  get_exercise(index, tema, numero) -> {"tema", "numero", "text", "resp"}

El indice se cachea en guide_index/index.json y se reconstruye si el PDF
es mas nuevo o si se pasa force_rebuild=True.
"""

import json
import os
import re

from config.settings import GUIA_INDEX_CACHE, resolve_guia_path

_PAGE_HEADER_RE = re.compile(
    r"^\s*Ing\.\s*Sergio\s*An[ií]bal\s*Dopazo\s*\n"
    r"\s*.Gu[ií]a\s+de\s+Problemas.*\n"
    r"\s*\d+\s*de\s*\d+\s*\n?",
    re.MULTILINE,
)

_TEMA_HEADER_RE = re.compile(
    r"^TEMA\s+(I{1,3}|IV|VI{0,2}|VII)\s*[-\u2013]",
    re.MULTILINE,
)

_EXERCISE_START_RE = re.compile(r"^\s*(\d+)\)\s+", re.MULTILINE)

_ROMAN_MAP = {
    "1": "I", "I": "I", "UNO": "I",
    "2": "II", "II": "II", "DOS": "II",
    "3": "III", "III": "III", "TRES": "III",
    "4": "IV", "IV": "IV", "CUATRO": "IV",
    "5": "V", "V": "V", "CINCO": "V",
    "6": "VI", "VI": "VI", "SEIS": "VI",
    "7": "VII", "VII": "VII", "SIETE": "VII",
}


def _normalize_tema(tema) -> str | None:
    if tema is None:
        return None
    key = str(tema).strip().upper()
    return _ROMAN_MAP.get(key)


def _strip_page_headers(text: str) -> str:
    return _PAGE_HEADER_RE.sub("", text)


def _collect_pages(pdf_path: str) -> list[str]:
    import fitz
    doc = fitz.open(pdf_path)
    try:
        return [doc[i].get_text() for i in range(doc.page_count)]
    finally:
        doc.close()


def _find_tema_boundaries(pages: list[str]) -> dict[str, dict]:
    """Return {roman: {"page_start": physical_page_index, "title": str}} for the body pages.

    Skips the index (physical pages 1-2) by only accepting the FIRST occurrence
    of each TEMA in pages >= index 2 (physical page 3+).
    """
    boundaries: dict[str, dict] = {}
    for pi, raw in enumerate(pages):
        if pi < 2:
            continue
        match = _TEMA_HEADER_RE.search(raw)
        if not match:
            continue
        roman = match.group(1).upper()
        if roman in boundaries:
            continue
        title_start = match.end()
        title = raw[title_start:title_start + 200].strip().split("\n")[0].strip(" -\u2013")
        boundaries[roman] = {
            "page_start": pi,
            "title": title,
        }
    return boundaries


def _split_exercises(body: str) -> list[tuple[int, str, str]]:
    """Return list of (numero, enunciado, resp) for a tema body."""
    matches = list(_EXERCISE_START_RE.finditer(body))
    result: list[tuple[int, str, str]] = []
    for idx, m in enumerate(matches):
        numero = int(m.group(1))
        start = m.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(body)
        raw_block = body[start:end]
        text, resp = _split_enunciado_resp(raw_block)
        if not text.strip():
            continue
        result.append((numero, text, resp))
    return result


def _split_enunciado_resp(block: str) -> tuple[str, str]:
    m = re.search(r"\n\s*Resp\s*:\s*", block)
    if not m:
        return _clean_text(block), ""
    enunciado = block[: m.start()]
    resp = block[m.end():]
    return _clean_text(enunciado), _clean_text(resp)


def _clean_text(text: str) -> str:
    text = text.replace("\r\n", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    lines = [line.rstrip() for line in text.split("\n")]
    return "\n".join(lines).strip()


def build_index(pdf_path: str | None = None) -> dict:
    """Build a fresh index from the PDF. Does not touch disk."""
    if pdf_path is None:
        pdf_path = resolve_guia_path()
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"Guia PDF no encontrada: {pdf_path}")

    pages = _collect_pages(pdf_path)
    cleaned_pages = [_strip_page_headers(p) for p in pages]
    boundaries = _find_tema_boundaries(cleaned_pages)

    ordered_romans = sorted(
        boundaries.keys(),
        key=lambda r: boundaries[r]["page_start"],
    )

    temas_out: dict[str, dict] = {}
    for idx, roman in enumerate(ordered_romans):
        start_page = boundaries[roman]["page_start"]
        end_page = (
            boundaries[ordered_romans[idx + 1]]["page_start"] - 1
            if idx + 1 < len(ordered_romans)
            else len(cleaned_pages) - 1
        )

        first_page = cleaned_pages[start_page]
        header_match = _TEMA_HEADER_RE.search(first_page)
        body_parts = [first_page[header_match.end():]] if header_match else [first_page]
        for p in range(start_page + 1, end_page + 1):
            body_parts.append(cleaned_pages[p])
        body = "\n".join(body_parts)

        exercises: dict[str, dict] = {}
        for numero, text, resp in _split_exercises(body):
            exercises[str(numero)] = {
                "text": text,
                "resp": resp,
            }

        temas_out[roman] = {
            "title": boundaries[roman]["title"],
            "physical_page_start": start_page + 1,
            "physical_page_end": end_page + 1,
            "exercises": exercises,
        }

    return {
        "version": 1,
        "source_pdf": os.path.basename(pdf_path),
        "temas": temas_out,
    }


def load_or_build_index(
    pdf_path: str | None = None,
    cache_path: str | None = None,
    force_rebuild: bool = False,
) -> dict:
    pdf_path = pdf_path or resolve_guia_path()
    cache_path = cache_path or GUIA_INDEX_CACHE

    if not force_rebuild and os.path.exists(cache_path) and os.path.exists(pdf_path):
        if os.path.getmtime(cache_path) >= os.path.getmtime(pdf_path):
            try:
                with open(cache_path, "r", encoding="utf-8") as fh:
                    return json.load(fh)
            except (json.JSONDecodeError, OSError):
                pass

    index = build_index(pdf_path)
    try:
        os.makedirs(os.path.dirname(cache_path), exist_ok=True)
        with open(cache_path, "w", encoding="utf-8") as fh:
            json.dump(index, fh, ensure_ascii=False, indent=2)
    except OSError:
        pass
    return index


def get_exercise(index: dict, tema, numero) -> dict | None:
    roman = _normalize_tema(tema)
    if roman is None:
        return None
    tema_entry = index.get("temas", {}).get(roman)
    if not tema_entry:
        return None
    ex = tema_entry.get("exercises", {}).get(str(numero))
    if not ex:
        return None
    return {
        "tema": roman,
        "numero": int(numero),
        "text": ex["text"],
        "resp": ex.get("resp", ""),
        "tema_title": tema_entry.get("title", ""),
    }
