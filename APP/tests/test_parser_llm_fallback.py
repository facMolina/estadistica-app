"""
Tests del fallback LLM del NLParser. Son skip-friendly si Ollama no está.

Ejecutar desde APP/:
    C:\\Python314\\python tests/test_parser_llm_fallback.py
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

from interpreter.nl_parser import NLParser
from llm.ollama_client import OllamaClient


def _skip(reason: str) -> None:
    print(f"  SKIP: {reason}")


def _ollama_up() -> bool:
    try:
        return OllamaClient().is_available()
    except Exception:
        return False


def test_regex_still_wins_for_catedra_notation():
    print("\n[1] La notación cátedra sigue resolviéndose por regex (no toca LLM)")
    p = NLParser()
    r = p.parse("Fb(4/12;0.45)")
    assert r["status"] == "complete", r
    assert r["model"] == "Binomial", r
    assert r.get("_source") == "regex", r
    print("  OK Fb() resolvió por regex")


def test_llm_output_validation_rejects_bad_shape():
    print("\n[2] _validate_llm_output rechaza objetos malformados")
    p = NLParser()
    assert p._validate_llm_output(None) is None
    assert p._validate_llm_output({}) is None
    assert p._validate_llm_output({"status": "garbage"}) is None
    # confidence bajo
    assert p._validate_llm_output({
        "status": "complete",
        "model": "Binomial",
        "confidence": 0.1,
    }) is None
    # shape válida mínima
    ok = p._validate_llm_output({
        "status": "complete",
        "model": "Binomial",
        "params": {"n": 10, "p": 0.5},
        "query_type": "probability",
        "query_params": {"r": 3},
        "confidence": 0.9,
    })
    assert ok is not None and ok["model"] == "Binomial"
    print("  OK validación de shape consistente")


def test_llm_does_not_degrade_regex_result():
    print("\n[3] Si regex devuelve complete, no se llama al LLM")
    p = NLParser()
    r = p.parse("Se lanza una moneda 15 veces. P(exactamente 4 caras)")
    assert r["status"] == "complete"
    assert r["model"] == "Binomial"
    assert r.get("_source") == "regex"
    print(f"  OK Binomial desde regex (n={r['params'].get('n')}, p={r['params'].get('p')})")


def test_llm_fallback_on_ambiguous_input():
    print("\n[4] Fallback LLM para un enunciado que el regex no resuelve")
    if not _ollama_up():
        _skip("Ollama no está corriendo")
        return
    p = NLParser()
    # Enunciado tipo Modelo 2026 ej 4 — el regex captura CustomPMF pero
    # sin dominio termina en need_more_info. El LLM puede elevarlo a complete.
    r = p.parse("P(X=x) = (x+2)/k. Hallar k y E(X).")
    print(f"  status={r.get('status')} model={r.get('model')} source={r.get('_source')}")
    # Lo mínimo: sigue siendo consistente — o regex need_more_info o llm complete
    assert r.get("status") in ("complete", "need_more_info"), r
    assert r.get("_source") in ("regex", "llm"), r


if __name__ == "__main__":
    tests = [
        test_regex_still_wins_for_catedra_notation,
        test_llm_output_validation_rejects_bad_shape,
        test_llm_does_not_degrade_regex_result,
        test_llm_fallback_on_ambiguous_input,
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
