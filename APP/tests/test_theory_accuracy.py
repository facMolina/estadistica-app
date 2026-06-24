"""Tests de exactitud del modo Consultas Teóricas.

Tres niveles:
  [1] Consistencia de fichas (theory/cards.py) — puro, sin Ollama, SIEMPRE corre.
      Bloquea regresiones en el grounding (fórmulas/signos/taxonomía correctos).
  [2] Detección de tópico — puro, verifica que detect_topics mapea bien.
  [3] Invariantes end-to-end por answer() — requiere Ollama, skip si está abajo.
      Aserta must_contain / must_not_contain (no fraseo exacto) con temp 0.

Ejecutar desde APP/:
    C:\\Python314\\python tests/test_theory_accuracy.py
"""

from __future__ import annotations

import os
import sys
import unicodedata

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

_HERE = os.path.dirname(os.path.abspath(__file__))
_APP = os.path.dirname(_HERE)
if _APP not in sys.path:
    sys.path.insert(0, _APP)

from theory.cards import detect_topics, all_cards, get_card
from config.model_catalog import IMPLEMENTED_MODELS


def _norm(text: str) -> str:
    t = (text or "").lower()
    t = unicodedata.normalize("NFKD", t)
    return "".join(c for c in t if not unicodedata.combining(c))


# Modelos implementados → clave de ficha. CustomPMF es una PMF casera sin ficha
# teórica fija (no aplica).
_MODEL_TO_TOPIC = {
    "Binomial": "Binomial", "Poisson": "Poisson", "Pascal": "Pascal",
    "Hipergeometrico": "Hipergeometrico", "Hiper-Pascal": "Hiper-Pascal",
    "Multinomial": "Multinomial", "Normal": "Normal", "Log-Normal": "LogNormal",
    "Exponencial": "Exponencial", "Gamma": "Gamma", "Weibull": "Weibull",
    "Gumbel Max": "GumbelMax", "Gumbel Min": "GumbelMin", "Pareto": "Pareto",
    "Uniforme": "Uniforme",
}


# ---------------------------------------------------------------------------
# [1] Consistencia de fichas
# ---------------------------------------------------------------------------

def test_cards_cover_implemented_models():
    print("\n[1a] cada modelo implementado tiene ficha")
    missing = []
    for model in IMPLEMENTED_MODELS:
        if model == "CustomPMF":
            continue
        topic = _MODEL_TO_TOPIC.get(model)
        if topic is None or get_card(topic) is None:
            missing.append(model)
    assert not missing, f"Modelos sin ficha: {missing}"
    print(f"  OK {len(_MODEL_TO_TOPIC)} modelos con ficha")


def test_cards_critical_formulas():
    """Tokens canónicos que NO pueden estar mal (atacan los errores observados)."""
    print("\n[1b] fórmulas/signos canónicos en las fichas")
    checks = [
        # (topic, substrings que DEBEN estar, substrings PROHIBIDOS)
        ("GumbelMax", ["e^{-e^{-(x-\\mu)/\\alpha}}", "tipo i"], ["tipo ii", "tipo 2"]),
        ("GumbelMin", ["e^{-e^{+(x-\\mu)/\\alpha}}", "tipo i"], ["tipo ii", "tipo 2"]),
        ("Pareto", ["f(x)=1-(\\delta/x)^{b}".replace(" ", ""), "(\\delta/x)^{b}"], []),
        ("Exponencial", ["g(x)=e^{-\\lambda x}"], []),
        ("Binomial", ["\\binom{n}{r}p^{r}(1-p)^{n-r}"], []),
        ("Poisson", ["e^{-m}m^{r}}{r!}"], []),
        ("TCL", ["varianzas"], []),
        ("Normal", ["(x-\\mu)/\\sigma"], []),
    ]
    for topic, musts, forbids in checks:
        card = get_card(topic)
        assert card is not None, f"falta ficha {topic}"
        body = _norm(card.body).replace(" ", "")
        for m in musts:
            assert _norm(m).replace(" ", "") in body, f"{topic}: falta '{m}'"
        body_spaced = _norm(card.body)
        for fb in forbids:
            assert _norm(fb) not in body_spaced, f"{topic}: contiene prohibido '{fb}'"
    print(f"  OK {len(checks)} fichas con fórmulas/signos correctos")


def test_gumbel_signs_distinct():
    """El signo del exponente distingue Máx (−) de Mín (+) — el bug original."""
    print("\n[1c] Gumbel Máx (−) ≠ Mín (+)")
    maxb = _norm(get_card("GumbelMax").body)
    minb = _norm(get_card("GumbelMin").body)
    assert "e^{-e^{-(x-\\mu)/\\alpha}}" in maxb.replace(" ", ""), "Máx debe llevar signo −"
    assert "e^{-e^{+(x-\\mu)/\\alpha}}" in minb.replace(" ", ""), "Mín debe llevar signo +"
    print("  OK signos distintos y correctos")


# ---------------------------------------------------------------------------
# [2] Detección de tópico
# ---------------------------------------------------------------------------

def test_topic_detection():
    print("\n[2] detección de tópico por pregunta")
    casos = [
        # (pregunta, topic que debe aparecer, debe ser el primero?)
        ("Para la ruptura de las correas de distribución, ¿uso Gumbel de Máximo?",
         "GumbelMin", True),
        ("Modelar la elongación máxima de un hilo hasta la rotura", "GumbelMax", True),
        ("¿Cómo calculo la media en datos agrupados?", "DatosAgrupados", True),
        ("Explicame el teorema de Bayes", "ProbabilidadBayes", True),
        ("En una suma de variables, ¿se suman los desvíos o las varianzas?", "TCL", True),
        ("Gamma con media y varianza, ¿cómo saco r y lambda?", "Gamma", True),
        ("¿Qué distribución para el tiempo hasta la primera falla de un fusible?",
         "Exponencial", True),
        ("Pareto para siniestros de seguro", "Pareto", True),
    ]
    fails = []
    for q, topic, first in casos:
        topics = [c.topic for c in detect_topics(q)]
        if topic not in topics:
            fails.append(f"{q[:40]!r}: esperaba {topic}, dio {topics}")
        elif first and topics[0] != topic:
            fails.append(f"{q[:40]!r}: {topic} no quedó primero ({topics})")
    assert not fails, "Fallos de detección:\n  " + "\n  ".join(fails)
    # Negativo: pregunta no estadística → sin tópico
    assert detect_topics("¿Cuál es la capital de Francia?") == []
    print(f"  OK {len(casos)} detecciones + 1 negativo")


# ---------------------------------------------------------------------------
# [3] Invariantes end-to-end (requiere Ollama)
# ---------------------------------------------------------------------------

def _ollama_up() -> bool:
    try:
        from llm.ollama_client import OllamaClient
        return OllamaClient().is_available()
    except Exception:
        return False


def test_answer_invariants():
    print("\n[3] invariantes end-to-end por answer() (Ollama)")
    if not _ollama_up():
        print("  SKIP: Ollama no está corriendo")
        return
    from theory.answerer import answer, _FALLBACK_TEXT

    casos = [
        {
            "q": "Para estudiar la ruptura de una correa de distribución por esfuerzo, "
                 "¿es correcto usar la distribución Gumbel de Máximo?",
            "must": ["minim"],          # debe orientar a Mínimo
            "forbid": ["tipo ii", "tipo 2"],
        },
        {
            "q": "¿Cuál es la fórmula de la distribución binomial?",
            "must": ["binom", "p^"],
            "forbid": [],
        },
        {
            "q": "En una suma de variables aleatorias independientes, ¿se suman los "
                 "desvíos o las varianzas?",
            "must": ["varianz"],
            "forbid": [],
        },
        {
            "q": "¿Qué significan F(x) y G(x) en la notación de la cátedra?",
            "must": ["f(x)", "g(x)"],
            "forbid": [],
        },
    ]
    fails = []
    for case in casos:
        try:
            ans = answer(case["q"]).text
        except Exception as e:
            fails.append(f"{case['q'][:40]!r}: EXC {e}")
            continue
        if ans == _FALLBACK_TEXT:
            print(f"  SKIP item (fallback): {case['q'][:40]!r}")
            continue
        n = _norm(ans)
        for m in case["must"]:
            if _norm(m) not in n:
                fails.append(f"{case['q'][:40]!r}: falta '{m}'")
        for fb in case["forbid"]:
            if _norm(fb) in n:
                fails.append(f"{case['q'][:40]!r}: contiene prohibido '{fb}'")
    assert not fails, "Fallos de invariantes:\n  " + "\n  ".join(fails)
    print(f"  OK {len(casos)} respuestas cumplen invariantes")


if __name__ == "__main__":
    tests = [
        test_cards_cover_implemented_models,
        test_cards_critical_formulas,
        test_gumbel_signs_distinct,
        test_topic_detection,
        test_answer_invariants,
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
    print(f"RESULTADO: {len(tests) - failures}/{len(tests)} OK")
    sys.exit(1 if failures else 0)
