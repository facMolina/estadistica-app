"""
Tests de Sprint 9: indexador de la Guía PDF + integración con el NL parser.

Ejecutar desde APP/:
    C:\\Python314\\python -m tests.test_guide_index
o bien:
    C:\\Python314\\python tests/test_guide_index.py
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

from guide_index import build_index, get_exercise, load_or_build_index
from interpreter.nl_parser import NLParser
from interpreter.streamlit_interpreter import interpret_turn


def test_build_index_smoke():
    print("\n[1] build_index: smoke + conteo por tema")
    index = build_index()
    temas = index["temas"]
    assert set(temas.keys()) == {"I", "II", "III", "IV", "V", "VI", "VII"}, \
        f"Temas inesperados: {list(temas.keys())}"
    total = sum(len(t["exercises"]) for t in temas.values())
    assert total >= 100, f"Esperaba >=100 ejercicios, obtuve {total}"
    print(f"  OK: {len(temas)} temas, {total} ejercicios totales")
    for roman, t in temas.items():
        print(f"    Tema {roman}: {len(t['exercises'])} ejercicios")


def test_known_exercise_tema2_ej23():
    print("\n[2] Tema II ej 23 (Bayes — proveedor honesto)")
    index = load_or_build_index()
    ex = get_exercise(index, "II", 23)
    assert ex is not None, "Tema II ej 23 no encontrado"
    assert "pieza vital" in ex["text"], f"Texto no contiene 'pieza vital': {ex['text'][:100]}"
    assert "0,4" in ex["resp"], f"Resp no contiene '0,4': {ex['resp'][:50]}"
    print(f"  OK: text starts with '{ex['text'][:60]}...'")
    print(f"  OK: resp='{ex['resp'][:40]}'")


def test_tema_normalization():
    print("\n[3] Normalización de tema (3 / 'III' / 'iii' / 'tres')")
    index = load_or_build_index()
    a = get_exercise(index, 3, 1)
    b = get_exercise(index, "III", 1)
    c = get_exercise(index, "iii", 1)
    d = get_exercise(index, "tres", 1)
    assert a is not None and a == b == c == d, \
        "get_exercise no es robusto a distintas representaciones de tema"
    print("  OK: todas las variantes devuelven el mismo ejercicio")


def test_invalid_tema_numero():
    print("\n[4] Tema inválido / número inválido devuelve None")
    index = load_or_build_index()
    assert get_exercise(index, "IX", 1) is None, "Tema IX debería devolver None"
    assert get_exercise(index, "III", 999) is None, "Tema III ej 999 debería devolver None"
    assert get_exercise(index, None, 1) is None, "tema=None debería devolver None"
    print("  OK")


def test_parser_detects_guide():
    print("\n[5] NLParser detecta 'tema X ejercicio Y'")
    parser = NLParser()
    for text, tema, num in [
        ("tema III ejercicio 8", "III", 8),
        ("Tema 2 ej 23", "2", 23),
        ("guia tema V problema 5", "V", 5),
        ("tema iv, ej. 3", "iv", 3),
    ]:
        r = parser.parse(text)
        assert r["status"] == "guide_exercise", \
            f"{text!r} -> status={r.get('status')}, esperaba guide_exercise"
        assert str(r["tema"]).upper() == tema.upper(), \
            f"{text!r} -> tema={r['tema']}, esperaba {tema}"
        assert r["numero"] == num, f"{text!r} -> numero={r['numero']}, esperaba {num}"
        print(f"  OK: {text!r} -> Tema {r['tema']} ej {r['numero']}")


def test_cache_persistence():
    print("\n[6] Cache en disco")
    from config.settings import GUIA_INDEX_CACHE
    # Forzar rebuild para asegurarse que escribe el cache
    load_or_build_index(force_rebuild=True)
    assert os.path.exists(GUIA_INDEX_CACHE), f"No se creó el cache en {GUIA_INDEX_CACHE}"
    import json
    with open(GUIA_INDEX_CACHE, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    assert data["version"] == 1
    assert "temas" in data
    print(f"  OK: cache en {GUIA_INDEX_CACHE}")


def test_end_to_end_guide_to_interpret():
    print("\n[7] End-to-end: interpret_turn con 'tema II ejercicio 23'")
    result = interpret_turn([], "tema II ejercicio 23")
    assert result.get("enunciado_from_guide") is True, \
        f"enunciado_from_guide debería estar en True, no: {result.get('enunciado_from_guide')}"
    assert result["tema"] == "II"
    assert result["numero"] == 23
    assert result["action"] in ("complete", "follow_up", "error"), \
        f"action inesperada: {result['action']}"
    # Debe haber al menos un mensaje del assistant con el enunciado
    assistant_msgs = [m for m in result["messages"]
                      if m.get("role") == "assistant"
                      and not m.get("content", "").startswith("__partial__")]
    assert len(assistant_msgs) >= 1, \
        "Faltó el mensaje del assistant con el enunciado"
    assert "pieza vital" in assistant_msgs[0]["content"], \
        "El mensaje del assistant no contiene el enunciado esperado"
    print(f"  OK: action={result['action']}, enunciado presente en messages")


def test_end_to_end_unknown():
    print("\n[8] End-to-end: Tema IX (no existe) devuelve error")
    result = interpret_turn([], "tema IX ejercicio 1")
    assert result["action"] == "error", f"action esperada 'error', obtuve {result['action']}"
    assert "Tema IX" in result["message"] or "ejercicio" in result["message"]
    print(f"  OK: {result['message']}")


def main() -> int:
    tests = [
        test_build_index_smoke,
        test_known_exercise_tema2_ej23,
        test_tema_normalization,
        test_invalid_tema_numero,
        test_parser_detects_guide,
        test_cache_persistence,
        test_end_to_end_guide_to_interpret,
        test_end_to_end_unknown,
    ]
    failures = 0
    for t in tests:
        try:
            t()
        except AssertionError as e:
            failures += 1
            print(f"  FAIL {t.__name__}: {e}")
        except Exception as e:
            failures += 1
            print(f"  ERROR {t.__name__}: {type(e).__name__}: {e}")

    print("\n" + "=" * 60)
    if failures == 0:
        print(f"TODOS LOS TESTS OK ({len(tests)}/{len(tests)})")
    else:
        print(f"{len(tests) - failures}/{len(tests)} OK, {failures} con falla")
    return failures


if __name__ == "__main__":
    sys.exit(main())
