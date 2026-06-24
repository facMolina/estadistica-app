"""Benchmark de modelos locales para Consultas Teóricas (WS6).

Corre un set multi-tema de preguntas por answer() con cada modelo de Ollama y
reporta exactitud (invariantes cumplidos) y latencia. Herramienta de decisión:
NO se encadena en la regresión.

Ejecutar desde APP/ con Ollama arriba:
    C:\\Python314\\python tests/bench_theory_models.py
    C:\\Python314\\python tests/bench_theory_models.py qwen3:8b qwen2.5:14b-instruct
"""

from __future__ import annotations

import os
import sys
import time
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

from theory.answerer import answer, _FALLBACK_TEXT
from llm.ollama_client import OllamaClient


def _norm(t: str) -> str:
    t = (t or "").lower()
    t = unicodedata.normalize("NFKD", t)
    return "".join(c for c in t if not unicodedata.combining(c))


# Set multi-tema con invariantes (must / forbid en forma normalizada).
QUESTIONS = [
    {"tema": "Gumbel", "q": "Para estudiar la ruptura de una correa de distribución por "
        "esfuerzo, ¿es correcto usar la distribución Gumbel de Máximo? Justificá y dame la fórmula.",
     "must": ["minim"], "forbid": ["tipo ii", "tipo 2"]},
    {"tema": "Discreto", "q": "¿Cuál es la fórmula de la distribución binomial y su esperanza?",
     "must": ["binom", "np"], "forbid": []},
    {"tema": "Poisson", "q": "¿Qué modela la distribución de Poisson y cuánto valen su media y varianza?",
     "must": ["m"], "forbid": []},
    {"tema": "TCL", "q": "En una suma de variables independientes, ¿se suman los desvíos o las varianzas?",
     "must": ["varianz"], "forbid": []},
    {"tema": "Notación", "q": "¿Qué significan F(x) y G(x) en la notación de la cátedra?",
     "must": ["f(x)", "g(x)"], "forbid": []},
    {"tema": "Pareto", "q": "¿Para qué se usa la distribución de Pareto y desde qué valor está definida?",
     "must": ["minim"], "forbid": []},
    {"tema": "Exponencial", "q": "¿Por qué la exponencial 'no tiene memoria'?",
     "must": ["memoria"], "forbid": []},
    {"tema": "Gamma", "q": "Si me dan la media y la varianza de una Gamma, ¿cómo obtengo r y lambda?",
     "must": ["lambda", "r"], "forbid": []},
]


def eval_model(model: str) -> dict:
    ok, total, secs = 0, 0, 0.0
    detail = []
    for case in QUESTIONS:
        total += 1
        t0 = time.time()
        try:
            txt = answer(case["q"], model=model).text
        except Exception as e:
            txt = f"__EXC__ {e}"
        dt = time.time() - t0
        secs += dt
        n = _norm(txt)
        passed = txt and txt != _FALLBACK_TEXT and not txt.startswith("__EXC__")
        if passed:
            for m in case["must"]:
                if _norm(m) not in n:
                    passed = False
            for fb in case["forbid"]:
                if _norm(fb) in n:
                    passed = False
        ok += 1 if passed else 0
        detail.append((case["tema"], passed, dt))
        print(f"    [{ '✓' if passed else '✗' }] {case['tema']:11} {dt:6.1f}s")
    return {"model": model, "ok": ok, "total": total, "secs": secs, "detail": detail}


def main() -> int:
    client = OllamaClient()
    if not client.is_available():
        print("Ollama no está corriendo — no se puede benchmarkear.")
        return 1
    pulled = client.list_models()
    requested = sys.argv[1:] or ["qwen3:8b", "qwen2.5:14b-instruct"]
    models = [m for m in requested if any(p.startswith(m.split(":")[0]) and m in p or p == m for p in pulled)]
    models = [m for m in requested if m in pulled] or requested

    results = []
    for model in models:
        if model not in pulled:
            print(f"\n[{model}] no está pulled — skip")
            continue
        print(f"\n[{model}]")
        results.append(eval_model(model))

    print("\n" + "=" * 60)
    print(f"{'Modelo':28} {'Exactitud':>10} {'Lat.media':>10}")
    print("-" * 60)
    for r in results:
        avg = r["secs"] / max(r["total"], 1)
        print(f"{r['model']:28} {r['ok']}/{r['total']:>8} {avg:>8.1f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
