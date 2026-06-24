"""
Test de regresión: desambiguación de modelo y conversión de tasa en el parser NL.

Caso real que motivó este test: un enunciado de Poisson que menciona
"averías" (palabra clave genérica de Binomial en MODELO_PATTERNS, chequeado
primero por orden de diccionario) se clasificaba mal como Binomial. Además,
una tasa dada en una unidad distinta a la de la consulta ("1 cada medio día"
vs. consulta "en una hora") no se convertía — ni el regex ni el fallback LLM
(qwen3:8b) la convertían bien (probado empíricamente: el LLM devolvía m=2 en
vez de ≈0,0833 para ese caso exacto).

Ejecutar desde APP/:
    C:\\Python314\\python tests/test_nl_parser_robustness.py
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

TOL = 1e-3


def test_averias_no_confunde_con_binomial():
    """"averías ... a razón de" debe resolver a Poisson via regex puro, sin LLM."""
    parser = NLParser()
    text = (
        "Se conoce por usos anteriores, que las averias ocurren a razon de "
        "1 cada medio dia. Cual es la probabilidad de que ningun generador "
        "falle en una hora particular?"
    )
    r = parser._parse_regex(text)
    assert r["model"] == "Poisson", f"esperaba Poisson, dio {r['model']}"
    assert r["status"] == "need_more_info"


def test_tasa_convertida_a_base_horaria():
    """La frase de tasa "1 cada medio día" debe convertirse a ≈0.0833/hora
    y dejar el follow-up determinístico (sin pasar por el fallback LLM)."""
    parser = NLParser()
    text = (
        "Se conoce por usos anteriores, que las averias ocurren a razon de "
        "1 cada medio dia. Cual es la probabilidad de que ningun generador "
        "falle en una hora particular?"
    )
    r = parser.parse(text)
    assert r["status"] == "need_more_info"
    assert r["model"] == "Poisson"
    assert r.get("_skip_llm") is True
    assert r.get("_source") == "regex"
    assert "0.0833" in r["question"]


def test_rate_phrase_helper_directo():
    parser = NLParser()
    casos = [
        ("1 cada medio dia", 1 / 12),
        ("4 averias por hora", 4.0),
        ("1 cada 2 horas", 0.5),
    ]
    for frase, esperado in casos:
        out = parser._detect_rate_per_hour(frase)
        assert out is not None, f"no detectó tasa en: {frase!r}"
        rate, _raw = out
        assert abs(rate - esperado) < TOL, f"{frase!r}: esperaba {esperado}, dio {rate}"


def test_binomial_explicito_sigue_funcionando():
    """No regresionar: un enunciado que sí es Binomial (sin tasa de Poisson)
    debe seguir resolviendo a Binomial."""
    parser = NLParser()
    text = "Se lanza una moneda 15 veces. Probabilidad de exactamente 4 caras."
    r = parser._parse_regex(text)
    assert r["model"] == "Binomial"


def main() -> int:
    print("\n[1] nl_parser_robustness: desambiguación averías->Poisson + conversión de tasa")
    tests = [
        test_averias_no_confunde_con_binomial,
        test_tasa_convertida_a_base_horaria,
        test_rate_phrase_helper_directo,
        test_binomial_explicito_sigue_funcionando,
    ]
    failures = 0
    for t in tests:
        try:
            t()
            print(f"  OK {t.__name__}")
        except AssertionError as e:
            failures += 1
            print(f"  FAIL {t.__name__}: {e}")
        except Exception as e:
            failures += 1
            print(f"  ERROR {t.__name__}: {type(e).__name__}: {e}")

    print("\n" + "=" * 60)
    if failures == 0:
        print(f"RESULTADO: {len(tests)}/{len(tests)} OK")
    else:
        print(f"RESULTADO: {len(tests) - failures}/{len(tests)} OK, {failures} con falla")
    return failures


if __name__ == "__main__":
    sys.exit(main())
