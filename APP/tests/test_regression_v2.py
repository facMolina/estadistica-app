"""Orquestador de la suite de regresión Sprint v2.

Corre los tests existentes más los del Sprint v2 en secuencia. Los tests que
dependen de Ollama se saltean silenciosamente si el servicio no está arriba.

Uso:
    C:\\Python314\\python tests/test_regression_v2.py
"""

from __future__ import annotations

import os
import subprocess
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

_HERE = os.path.dirname(os.path.abspath(__file__))
_APP = os.path.dirname(_HERE)

PY = sys.executable  # usa el mismo Python que ejecuta este orquestador

SUITES: list[tuple[str, str]] = [
    ("Sprint 7  — approximations", "test_approximations.py"),
    ("Sprint 9  — guide index",    "test_guide_index.py"),
    ("Sprint 10 — multinomial/TCL", "test_sprint10.py"),
    ("Sprint 10 — guide corpus",   "test_guide_corpus.py"),
    ("Sprint v2 — ollama client",  "test_ollama_client.py"),
    ("Sprint v2 — parser LLM",     "test_parser_llm_fallback.py"),
    ("Sprint v2 — theory flow",    "test_theory_flow.py"),
    ("Sprint v2 — UI invisibility", "test_ui_invisibility.py"),
]


def run_one(name: str, script: str) -> tuple[bool, str]:
    path = os.path.join(_HERE, script)
    if not os.path.exists(path):
        return False, f"(archivo {script} no existe)"
    proc = subprocess.run(
        [PY, path],
        cwd=_APP,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    output = proc.stdout + proc.stderr
    ok = proc.returncode == 0
    # Extraer línea de resultado
    tail = ""
    for line in reversed(output.splitlines()):
        if "RESULTADO" in line or "OK" in line or "FAIL" in line:
            tail = line.strip()
            break
    return ok, tail or "(sin output)"


def main() -> int:
    print("=" * 70)
    print("Regresión Sprint v2 — orquestador")
    print("=" * 70)
    results: list[tuple[str, bool, str]] = []
    for name, script in SUITES:
        print(f"\n[{name}] {script} ...", flush=True)
        ok, tail = run_one(name, script)
        mark = "OK" if ok else "FAIL"
        print(f"   [{mark}] {tail}")
        results.append((name, ok, tail))
    print("\n" + "=" * 70)
    passed = sum(1 for _, ok, _ in results if ok)
    print(f"RESUMEN: {passed}/{len(results)} suites OK")
    for n, ok, t in results:
        mark = "OK" if ok else "FAIL"
        print(f"  [{mark}] {n}: {t}")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
