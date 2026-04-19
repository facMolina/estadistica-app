"""
Tests de Sprint 10: Multinomial + TCL (SumOfRVs).

Ejecutar desde APP/:
    C:\\Python314\\python tests/test_sprint10.py
"""

from __future__ import annotations

import math
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

from models.discrete.multinomial import Multinomial
from models.discrete.binomial import Binomial
from tcl.sum_of_rvs import SumOfRVs, Component

from scipy import stats as _st


TOL_STRICT = 1e-9
TOL_LOOSE = 5e-4


def _assert_close(got, expected, tol, label):
    err = abs(got - expected)
    assert err <= tol, f"{label}: |{got:.8f} - {expected:.8f}| = {err:.2e} > tol={tol}"
    print(f"  OK {label}: got={got:.6f} expected={expected:.6f}")


# ---------------------------------------------------------------------
# 1. Multinomial: probabilidad conjunta
# ---------------------------------------------------------------------

def test_multinomial_probability():
    print("\n[1] Multinomial.probability_value()")
    m = Multinomial(10, [0.2, 0.3, 0.5])
    got = m.probability_value([2, 3, 5])

    # Verificación manual: 10!/(2!·3!·5!) · 0.2^2 · 0.3^3 · 0.5^5
    coef = math.factorial(10) // (math.factorial(2) * math.factorial(3) * math.factorial(5))
    expected = coef * (0.2**2) * (0.3**3) * (0.5**5)
    _assert_close(got, expected, TOL_STRICT, "P(2,3,5) manual")
    _assert_close(got, 0.08505, 1e-5, "P(2,3,5) ≈ 0.08505")

    # CalcResult con steps
    res = m.probability([2, 3, 5])
    _assert_close(res.final_value, expected, TOL_STRICT, "CalcResult.final_value")
    assert len(res.steps) >= 3, f"Se esperaban ≥3 pasos, hubo {len(res.steps)}"
    print(f"  OK CalcResult tiene {len(res.steps)} pasos")


# ---------------------------------------------------------------------
# 2. Multinomial: momentos
# ---------------------------------------------------------------------

def test_multinomial_mean_variance():
    print("\n[2] Multinomial.mean_vector/variance_vector/covariance")
    m = Multinomial(10, [0.2, 0.3, 0.5])

    # E(X1)=2, E(X2)=3, E(X3)=5
    chars = m.characteristics_summary()
    _assert_close(chars[0]["E(Xi)"], 2.0, TOL_STRICT, "E(X1)")
    _assert_close(chars[1]["E(Xi)"], 3.0, TOL_STRICT, "E(X2)")
    _assert_close(chars[2]["E(Xi)"], 5.0, TOL_STRICT, "E(X3)")

    # V(X1) = 10·0.2·0.8 = 1.6
    _assert_close(chars[0]["V(Xi)"], 1.6, TOL_STRICT, "V(X1)")
    _assert_close(chars[1]["V(Xi)"], 2.1, TOL_STRICT, "V(X2)")
    _assert_close(chars[2]["V(Xi)"], 2.5, TOL_STRICT, "V(X3)")

    # Cov(X1, X2) = -10·0.2·0.3 = -0.6
    cov = m.covariance(1, 2)
    _assert_close(cov.final_value, -0.6, TOL_STRICT, "Cov(X1,X2)")

    # Cov(X1, X1) = V(X1) = 1.6
    cov_11 = m.covariance(1, 1)
    _assert_close(cov_11.final_value, 1.6, TOL_STRICT, "Cov(X1,X1) = V(X1)")


# ---------------------------------------------------------------------
# 3. Multinomial: marginal = Binomial
# ---------------------------------------------------------------------

def test_multinomial_marginal():
    print("\n[3] Multinomial.marginal_binomial()")
    m = Multinomial(10, [0.2, 0.3, 0.5])
    bi = m.marginal_binomial(2)  # X2 ~ Bi(10, 0.3)

    # Debe coincidir con Binomial(10, 0.3) puntual
    expected = Binomial(10, 0.3).probability_value(3)
    got = bi.probability_value(3)
    _assert_close(got, expected, TOL_STRICT, "P(X2=3) vs Bi(10,0.3).P(3)")


# ---------------------------------------------------------------------
# 4. SumOfRVs: 30 Bernoullis iid
# ---------------------------------------------------------------------

def test_sum_of_rvs_identical():
    print("\n[4] SumOfRVs: 30 copias de Bi(1,0.5)")
    s = SumOfRVs([Component("Bi", mean=0.5, variance=0.25, count=30)])
    _assert_close(s.expected_value_raw(), 15.0, TOL_STRICT, "E(S) = 15")
    _assert_close(s.variance_raw(), 7.5, TOL_STRICT, "V(S) = 7.5")

    # P(S ≤ 10) vía TCL  = Φ((10 − 15)/√7.5) ≈ 0.0339
    res = s.probability("cdf_left", s=10)
    expected = float(_st.norm.cdf((10 - 15) / math.sqrt(7.5)))
    _assert_close(res.final_value, expected, TOL_STRICT, "P(S ≤ 10) = Φ(-5/√7.5)")


# ---------------------------------------------------------------------
# 5. SumOfRVs: mezcla heterogénea
# ---------------------------------------------------------------------

def test_sum_of_rvs_mixed():
    print("\n[5] SumOfRVs: N(100,25) + N(50,16)")
    s = SumOfRVs([
        Component("X", mean=100, variance=25),
        Component("Y", mean=50, variance=16),
    ])
    _assert_close(s.expected_value_raw(), 150.0, TOL_STRICT, "E(S) = 150")
    _assert_close(s.variance_raw(), 41.0, TOL_STRICT, "V(S) = 41")

    res = s.probability("cdf_left", s=160)
    expected = float(_st.norm.cdf((160 - 150) / math.sqrt(41)))
    _assert_close(res.final_value, expected, TOL_STRICT, "P(S ≤ 160)")

    # Range query
    res_r = s.probability("range", a=140, b=160)
    expected_r = (float(_st.norm.cdf((160 - 150) / math.sqrt(41)))
                  - float(_st.norm.cdf((140 - 150) / math.sqrt(41))))
    _assert_close(res_r.final_value, expected_r, TOL_STRICT, "P(140 ≤ S ≤ 160)")

    # Fractile α=0.95
    res_f = s.probability("fractile", alpha=0.95)
    expected_f = 150 + float(_st.norm.ppf(0.95)) * math.sqrt(41)
    _assert_close(res_f.final_value, expected_f, TOL_STRICT, "s(0.95)")


# ---------------------------------------------------------------------
# 6. SumOfRVs: CalcResult de probabilidad tiene ≥3 niveles de detalle
# ---------------------------------------------------------------------

def test_sum_of_rvs_probability_steps():
    print("\n[6] SumOfRVs: CalcResult probability() steps")
    s = SumOfRVs([
        Component("X", mean=100, variance=25),
        Component("Y", mean=50, variance=16),
    ])
    res = s.probability("cdf_left", s=160)
    assert len(res.steps) >= 3, f"Se esperaban ≥3 pasos, hubo {len(res.steps)}"
    # Verificar que level=1 reduce pasos
    steps_l1 = res.get_steps_for_level(1)
    steps_l3 = res.get_steps_for_level(3)
    assert len(steps_l1) <= len(steps_l3), "level 1 debería tener ≤ pasos que level 3"
    expected = float(_st.norm.cdf((160 - 150) / math.sqrt(41)))
    _assert_close(res.final_value, expected, TOL_STRICT, "final_value == Φ(Z)")
    print(f"  OK steps L1={len(steps_l1)}, L3={len(steps_l3)}")


# ---------------------------------------------------------------------
# 7. SumOfRVs: from_model_instances
# ---------------------------------------------------------------------

def test_sum_of_rvs_from_models():
    print("\n[7] SumOfRVs.from_model_instances()")
    bi = Binomial(20, 0.4)  # E=8, V=4.8
    s = SumOfRVs.from_model_instances([bi], counts=[10])
    expected_E = 10 * 8.0
    expected_V = 10 * 4.8
    _assert_close(s.expected_value_raw(), expected_E, TOL_STRICT, "E(S) iid Bi")
    _assert_close(s.variance_raw(), expected_V, TOL_STRICT, "V(S) iid Bi")


# ---------------------------------------------------------------------
# 8. Multinomial: validación de parámetros
# ---------------------------------------------------------------------

def test_multinomial_validation():
    print("\n[8] Multinomial: validaciones")
    try:
        Multinomial(10, [0.2, 0.3, 0.4])  # suma != 1
        raise AssertionError("Debería haber fallado con suma != 1")
    except ValueError:
        print("  OK rechaza suma != 1")

    try:
        Multinomial(10, [0.5])  # k < 2
        raise AssertionError("Debería haber fallado con k < 2")
    except ValueError:
        print("  OK rechaza k < 2")

    m = Multinomial(10, [0.5, 0.5])
    try:
        m.probability([3, 3])  # suma != n
        raise AssertionError("Debería haber fallado con sum(r) != n")
    except ValueError:
        print("  OK rechaza sum(r) != n")


# ---------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------

if __name__ == "__main__":
    tests = [
        test_multinomial_probability,
        test_multinomial_mean_variance,
        test_multinomial_marginal,
        test_sum_of_rvs_identical,
        test_sum_of_rvs_mixed,
        test_sum_of_rvs_probability_steps,
        test_sum_of_rvs_from_models,
        test_multinomial_validation,
    ]
    passed = 0
    failed = []
    for t in tests:
        try:
            t()
            passed += 1
        except Exception as e:
            failed.append((t.__name__, repr(e)))
            print(f"  FAIL {t.__name__}: {e}")
    print(f"\n{'='*60}")
    print(f"RESULTADO: {passed}/{len(tests)} OK")
    if failed:
        for name, err in failed:
            print(f"  FAIL {name}: {err}")
        sys.exit(1)
