"""Gate de invisibilidad — ningún artefacto del stack técnico debe aparecer
en la UI final (archivos que el usuario abre o render HTML).

Escanea archivos Python de UI + prompts + código que llega al render y verifica
que no contengan strings prohibidas (case-insensitive).
"""

from __future__ import annotations

import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

_HERE = os.path.dirname(os.path.abspath(__file__))
_APP = os.path.dirname(_HERE)
if _APP not in sys.path:
    sys.path.insert(0, _APP)


# Strings que NO deben aparecer en strings de UI visibles
# (literales — se buscan con .lower() in contents.lower())
_FORBIDDEN_LITERALS = [
    "ollama",
    "qwen",
    "nomic-embed",
    "llm",
    "ia local",
    "modelo de lenguaje",
    "inteligencia artificial",
    "según el material",
    "segun el material",
    "[fuente",
    "📚",
]


# Archivos que el usuario ve directo (UI layer): NO pueden mencionar nada del stack
_UI_FILES = [
    "app_streamlit.py",
    "ui/components/theory_ui.py",
    "ui/components/data_processing_ui.py",
    "ui/components/probability_ui.py",
    "ui/components/continuous_ui.py",
    "ui/components/multinomial_ui.py",
    "ui/components/tcl_ui.py",
    "ui/components/compound_ui.py",
    "ui/components/approximations_ui.py",
    "ui/components/step_display.py",
    "ui/components/summary_panel.py",
    "ui/components/table_panel.py",
    "ui/components/graph_panel.py",
    "ui/components/detail_selector.py",
]


def _scan_file(path: str) -> list[str]:
    """Devuelve lista de violaciones encontradas en el archivo."""
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        contents = f.read()
    lower = contents.lower()
    violations: list[str] = []
    for kw in _FORBIDDEN_LITERALS:
        if kw.lower() in lower:
            # Permitir si aparece en un comentario de docstring (no es user-facing)
            # Regla simple: violación solo si está dentro de un string literal.
            matches = re.findall(rf'["\'].*?{re.escape(kw)}.*?["\']', contents, re.IGNORECASE)
            if matches:
                violations.append(f"{kw} → {matches[0][:80]}")
    return violations


def test_ui_files_contain_no_stack_mentions():
    print("\n[1] Archivos de UI no mencionan el stack técnico")
    all_violations: dict[str, list[str]] = {}
    for rel in _UI_FILES:
        full = os.path.join(_APP, rel)
        v = _scan_file(full)
        if v:
            all_violations[rel] = v
    if all_violations:
        for f, vv in all_violations.items():
            print(f"  FAIL {f}:")
            for line in vv:
                print(f"    - {line}")
        raise AssertionError(f"Archivos con violaciones: {list(all_violations.keys())}")
    print(f"  OK {len(_UI_FILES)} archivos UI limpios")


def test_theory_prompt_prohibits_citations():
    print("\n[2] theory_answer.txt prohíbe citas y menciones de fuentes")
    path = os.path.join(_APP, "llm", "prompts", "theory_answer.txt")
    assert os.path.exists(path), f"No existe {path}"
    with open(path, encoding="utf-8") as f:
        content = f.read().lower()
    for kw in ("prohibido", "fuente", "pdf", "material"):
        assert kw in content, f"Prompt no menciona '{kw}' en las reglas"
    print("  OK prompt incluye cláusula de invisibilidad")


def test_fallback_text_is_generic():
    print("\n[3] El texto de fallback es genérico y no explica el error")
    from theory.answerer import _FALLBACK_TEXT
    assert "Respuesta no disponible" in _FALLBACK_TEXT
    for kw in _FORBIDDEN_LITERALS:
        assert kw.lower() not in _FALLBACK_TEXT.lower()
    print(f"  OK fallback = '{_FALLBACK_TEXT}'")


def test_parser_source_field_is_private():
    print("\n[4] El campo `source` del parser usa prefijo `_` (interno)")
    from interpreter.nl_parser import NLParser
    p = NLParser()
    r = p.parse("Fb(4/12;0.45)")
    # Debe tener _source, no source (que es público)
    assert "_source" in r, "Falta _source en el resultado"
    assert "source" not in r, "'source' expuesto como campo público (debe ser _source)"
    print(f"  OK _source={r['_source']} (campo interno)")


if __name__ == "__main__":
    tests = [
        test_ui_files_contain_no_stack_mentions,
        test_theory_prompt_prohibits_citations,
        test_fallback_text_is_generic,
        test_parser_source_field_is_private,
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
