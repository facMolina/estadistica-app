"""Generador de respuestas teóricas — RAG + Ollama.

Contrato de invisibilidad: la respuesta devuelta al usuario es solo texto español +
LaTeX. NO incluye citas, fuentes, páginas, menciones a PDFs, Ollama o LLM.
Los chunks retrieved se usan internamente como grounding del prompt.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from theory.rag_index import get_index

_PROMPT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "llm", "prompts", "theory_answer.txt",
)

_FALLBACK_TEXT = "Respuesta no disponible momentáneamente."


@dataclass
class TheoryAnswer:
    text: str


def _load_prompt() -> str:
    try:
        with open(_PROMPT_PATH, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return (
            "Sos un experto en Estadística General. Respondé en español con "
            "LaTeX ($...$). No menciones fuentes ni PDFs."
        )


def answer(question: str, history: list[dict] | None = None,
           model: str | None = None) -> TheoryAnswer:
    """Pregunta teórica → TheoryAnswer(text).

    `model` permite forzar un modelo de Ollama por llamada (usado por el
    benchmark de WS6); si es None usa el default resuelto.

    Silencioso ante errores: si algo falla, devuelve _FALLBACK_TEXT.
    """
    if not question or not question.strip():
        return TheoryAnswer(text=_FALLBACK_TEXT)

    try:
        from llm.ollama_client import OllamaClient
        client = OllamaClient()
        if not client.is_available():
            return TheoryAnswer(text=_FALLBACK_TEXT)
    except Exception:
        return TheoryAnswer(text=_FALLBACK_TEXT)

    try:
        idx = get_index()
        chunks = idx.search(question, top_k=6)
    except Exception:
        chunks = []

    context_blob = ""
    if chunks:
        parts = []
        for i, c in enumerate(chunks, 1):
            snippet = c.text[:900]
            parts.append(f"[contexto {i}]\n{snippet}")
        context_blob = "\n\n".join(parts)

    # Ficha(s) canónica(s) por tópico detectado: fuente de verdad determinística,
    # antepuesta al contexto de coseno. Garantiza que la fórmula/método correctos
    # estén frente al modelo aunque el retrieval falle.
    cards_blob = ""
    try:
        from theory.cards import detect_topics, render_cards
        cards_blob = render_cards(detect_topics(question))
    except Exception:
        cards_blob = ""

    system = _load_prompt()
    user_parts = [question.strip()]
    if cards_blob:
        user_parts.append(
            "\n\n(FICHA AUTORITATIVA — fórmulas y criterio correctos; reproducí las "
            "fórmulas EXACTAS de acá, NO menciones que es una ficha):\n" + cards_blob
        )
    if context_blob:
        user_parts.append(
            "\n\n(Material técnico de fondo — NO mencionar al responder):\n" + context_blob
        )

    messages: list[dict] = [{"role": "system", "content": system}]
    if history:
        for m in history[-10:]:
            if m.get("role") in ("user", "assistant") and m.get("content"):
                messages.append({"role": m["role"], "content": m["content"]})
    messages.append({"role": "user", "content": "\n".join(user_parts)})

    try:
        text = client.chat(
            messages,
            json_mode=False,
            temperature=0.2,
            max_tokens=1200,
            model=model,
        )
    except Exception:
        return TheoryAnswer(text=_FALLBACK_TEXT)

    text = (text or "").strip()
    if not text:
        return TheoryAnswer(text=_FALLBACK_TEXT)
    return TheoryAnswer(text=text)
