"""Tests del flujo de Consultas Teóricas.

Los tests que requieren Ollama son skip si el servicio no está arriba.
"""

from __future__ import annotations

import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

_HERE = os.path.dirname(os.path.abspath(__file__))
_APP = os.path.dirname(_HERE)
if _APP not in sys.path:
    sys.path.insert(0, _APP)

from llm.ollama_client import OllamaClient
from theory.machete_builder import build_machete
from theory.rag_index import RAGIndex
from theory.answerer import answer, _FALLBACK_TEXT
from config.settings import MACHETE_PATH


def _skip(reason: str) -> None:
    print(f"  SKIP: {reason}")


def _ollama_up() -> bool:
    try:
        return OllamaClient().is_available()
    except Exception:
        return False


def test_machete_builder():
    print("\n[1] Machete: build genera MACHETE.md con temas I..VII")
    path = build_machete(force=True)
    assert os.path.exists(path), f"MACHETE.md no existe en {path}"
    with open(path, encoding="utf-8") as f:
        content = f.read()
    for tema in ("Tema I", "Tema II", "Tema III", "Tema IV",
                 "Tema V", "Tema VI", "Tema VII"):
        assert tema in content, f"Falta '{tema}' en machete"
    print(f"  OK machete con todos los temas ({len(content)} chars)")


def test_rag_index_build_and_search():
    print("\n[2] RAG Index: build + search (fallback textual sin embeddings)")
    idx = RAGIndex()
    n = idx.build(force=True)
    assert n > 0, "El índice quedó vacío — sin PDFs ni machete?"
    results = idx.search("binomial media y varianza", top_k=5)
    assert len(results) > 0, "search no devolvió chunks"
    print(f"  OK índice con {n} chunks, {len(results)} resultados relevantes")


def test_answerer_fallback_when_ollama_down():
    print("\n[3] Answerer: fallback silencioso si Ollama no responde")
    if _ollama_up():
        _skip("Ollama está corriendo — skip (no podemos forzar el down)")
        return
    ans = answer("¿Qué es la binomial?")
    assert ans.text == _FALLBACK_TEXT
    print("  OK fallback texto invariable")


def test_answerer_produces_spanish_with_latex():
    print("\n[4] Answerer: respuesta con LaTeX cuando Ollama está arriba")
    if not _ollama_up():
        _skip("Ollama no está corriendo")
        return
    ans = answer("¿Qué es la distribución binomial?")
    assert ans.text and ans.text != _FALLBACK_TEXT
    # El prompt exige LaTeX — que haya al menos un delimitador
    has_latex = "$" in ans.text or "\\(" in ans.text
    assert has_latex, f"Respuesta sin LaTeX: {ans.text[:200]}"
    # Invisibilidad: no puede mencionar fuentes, páginas, Ollama, etc.
    forbidden_literal = [
        "ollama", "llm", "modelo de lenguaje", "segun el material",
        "según el material", "fuente:", "[fuente", "TEORIA/", "📚",
    ]
    lower = ans.text.lower()
    for kw in forbidden_literal:
        assert kw.lower() not in lower, (
            f"Respuesta menciona palabra prohibida '{kw}': {ans.text[:300]}"
        )
    print(f"  OK respuesta en español con LaTeX, {len(ans.text)} chars")


if __name__ == "__main__":
    tests = [
        test_machete_builder,
        test_rag_index_build_and_search,
        test_answerer_fallback_when_ollama_down,
        test_answerer_produces_spanish_with_latex,
    ]
    passed = 0
    failed: list[tuple[str, str]] = []
    for t in tests:
        try:
            t()
            passed += 1
        except AssertionError as e:
            failed.append((t.__name__, str(e)))
            print(f"  FAIL {t.__name__}: {e}")
        except Exception as e:
            failed.append((t.__name__, f"EXC {e}"))
            print(f"  FAIL {t.__name__}: {e}")
    print(f"\n{'='*60}")
    print(f"RESULTADO: {passed}/{len(tests)} OK")
    if failed:
        for n, err in failed:
            print(f"  {n}: {err}")
        sys.exit(1)
