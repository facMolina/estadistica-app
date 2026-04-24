"""
Tests del modo `inclusive_classes=True` de GroupedData + prob_conditional
generalizado. Los números de referencia salen del Modelo Primer Parcial
1C 2026 (Serebrisky), verificados contra la hoja oficial.

Ejecutar desde APP/:
    python tests/test_grouped_data_inclusive.py
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

from data_processing.grouped_data import GroupedData


TOL = 1e-3


def _approx(got: float, expected: float, tol: float = TOL) -> bool:
    return abs(got - expected) <= tol


def _assert_close(label: str, got: float, expected: float, tol: float = TOL) -> None:
    if _approx(got, expected, tol):
        print(f"  OK  {label}: got={got:.4f} expected={expected:.4f}")
    else:
        raise AssertionError(f"{label}: got={got:.6f} expected={expected:.6f} (tol={tol})")


def test_inclusive_enunciado():
    """Clases cátedra '0 a 3 / 4 a 7 / 8 a 11 / 12 a 15' con freq del enunciado."""
    print("\n[1] inclusive_classes=True con freq del enunciado [210,60,53,33]")
    gd = GroupedData(
        [(0, 3), (4, 7), (8, 11), (12, 15)],
        [210, 60, 53, 33],
        inclusive_classes=True,
    )
    assert gd.n == 356
    _assert_close("μ",          gd.mean().final_value,       4.4775)
    _assert_close("Sn²",        gd.variance_n().final_value, 16.7074)
    _assert_close("Sn",         gd.std_dev_n().final_value,  4.0875)
    _assert_close("S²n-1",      gd.variance_n1().final_value,16.7544)
    _assert_close("Sn-1",       gd.std_dev_n1().final_value, 4.0932)
    _assert_close("fractil .80",gd.fractile(0.80).final_value, 8.8377)


def test_inclusive_oficial():
    """Reproduce los números oficiales (que usaron freq=69 por typo)."""
    print("\n[2] inclusive_classes=True con freq de la hoja oficial [210,69,53,33]")
    gd = GroupedData(
        [(0, 3), (4, 7), (8, 11), (12, 15)],
        [210, 69, 53, 33],
        inclusive_classes=True,
    )
    assert gd.n == 365
    _assert_close("μ oficial",       gd.mean().final_value,       4.5027)
    _assert_close("Sn² oficial",     gd.variance_n().final_value, 16.3205)
    _assert_close("S²n-1 oficial",   gd.variance_n1().final_value,16.3654)
    _assert_close("Sn-1 oficial",    gd.std_dev_n1().final_value, 4.0454)
    _assert_close("fractil .80 of.", gd.fractile(0.80).final_value, 8.7358)


def test_continuous_backward_compat():
    """inclusive_classes=False (default) mantiene los números históricos."""
    print("\n[3] inclusive_classes=False (default) — backward compat")
    gd = GroupedData(
        [(0, 4), (4, 8), (8, 12), (12, 16)],
        [210, 60, 53, 33],
    )
    # Con Ci = 2/6/10/14, μ histórico es 4.9775
    _assert_close("μ histórico",    gd.mean().final_value,        4.9775)
    _assert_close("fractil histórico",gd.fractile(0.80).final_value, 9.1170)


def test_prob_conditional_4_borders():
    """prob_conditional con 4 bordes independientes (Ej 2b del modelo)."""
    print("\n[4] prob_conditional(num_lower=8, num_upper=15, cond_lower=4)")
    gd = GroupedData(
        [(0, 3), (4, 7), (8, 11), (12, 15)],
        [210, 60, 53, 33],
        inclusive_classes=True,
    )
    res = gd.prob_conditional(
        num_lower=8, num_upper=15, cond_lower=4,
    )
    _assert_close("P(8≤x≤15 | x≥4)", res.final_value, 0.5890)


def test_prob_conditional_legacy():
    """Forma posicional vieja: mismo comportamiento que antes del cambio."""
    print("\n[5] prob_conditional(given_above, find_below) — forma legacy")
    gd = GroupedData(
        [(0, 4), (4, 8), (8, 12), (12, 16)],
        [210, 60, 53, 33],
    )
    # P(x < 12 | x > 4) = P(4 < x < 12) / P(x > 4)
    f4 = gd._F_at(4)
    f12 = gd._F_at(12)
    expected = (f12 - f4) / (1 - f4)
    res = gd.prob_conditional(4, 12)
    _assert_close("legacy forma", res.final_value, expected)


def test_parser_hint_detection():
    """Parser NL detecta 'X a Y' como inclusivo y 'X-Y' como continuo."""
    print("\n[6] _infer_inclusive_classes hint del parser NL")
    from interpreter.nl_parser import NLParser
    p = NLParser()
    assert p._infer_inclusive_classes("0 a 3 | 210 ; 4 a 7 | 60") is True
    assert p._infer_inclusive_classes("0-4 | 210 ; 4-8 | 60") is False
    assert p._infer_inclusive_classes("solo texto sin intervalos") is None
    print("  OK  hints: inclusivo / continuo / None según separador")


if __name__ == "__main__":
    tests = [
        test_inclusive_enunciado,
        test_inclusive_oficial,
        test_continuous_backward_compat,
        test_prob_conditional_4_borders,
        test_prob_conditional_legacy,
        test_parser_hint_detection,
    ]
    for t in tests:
        t()
    print(f"\n{'='*60}")
    print(f"RESULTADO: {len(tests)}/{len(tests)} OK")
    print("="*60)
