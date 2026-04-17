"""
Tests de Sprint 7: motor de aproximaciones.

Ejecutar desde APP/:
    C:\\Python314\\python -m tests.test_approximations
o bien:
    C:\\Python314\\python tests/test_approximations.py
"""

from __future__ import annotations

import os
import sys

# Forzar UTF-8 en stdout/stderr para que los ≤/≥ no rompan el test en Windows
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# Permitir correr como script independiente desde APP/
_HERE = os.path.dirname(os.path.abspath(__file__))
_APP = os.path.dirname(_HERE)
if _APP not in sys.path:
    sys.path.insert(0, _APP)

from approximations.approximator import try_approximations, ApproximationResult


TOL_STRICT = 1e-9
TOL_LOOSE = 0.05    # 5% error absoluto aceptable para aproximaciones con condiciones apenas cumplidas


def _find(results: list[ApproximationResult], to_model: str) -> ApproximationResult:
    for r in results:
        if r.to_model == to_model:
            return r
    raise AssertionError(f"No se encontró aproximación a {to_model} en {[r.to_model for r in results]}")


def _assert_close(approx, exact, tol, label):
    assert approx is not None, f"{label}: approx es None"
    assert exact is not None, f"{label}: exact es None"
    err = abs(approx - exact)
    assert err <= tol, f"{label}: |{approx:.6f} - {exact:.6f}| = {err:.6f} > tol={tol}"
    print(f"  OK {label}: approx={approx:.6f} exact={exact:.6f} err={err:.6e}")


# ------------------------------------------------------------------
# 1. Hipergeometrico -> Binomial
# ------------------------------------------------------------------

def test_hiper_to_binomial():
    print("\n[1] Hipergeometrico -> Binomial")
    # N grande, n chico; n/N = 5/1000 = 0.005 <= 0.01 (cumple)
    params = {"N": 1000, "R": 50, "n": 5}
    query_type = "cdf_left"
    query_params = {"r": 2}

    results = try_approximations("Hipergeometrico", params, query_type, query_params)
    r = _find(results, "Binomial")

    assert r.condition_met, f"Condición debería cumplirse: {r.condition_str}"
    _assert_close(r.approx_value, r.exact_value, TOL_LOOSE, "Hiper->Binomial P(X<=2)")
    # p = R/N = 0.05
    assert abs(r.target_params["p"] - 0.05) < 1e-12
    print(f"  condición: {r.condition_str}")


def test_hiper_to_binomial_no_cumple():
    print("\n[1b] Hipergeometrico -> Binomial (condición no cumplida)")
    # n/N = 10/20 = 0.5 > 0.01 (no cumple, pero aun así devuelve resultado)
    params = {"N": 20, "R": 5, "n": 10}
    results = try_approximations("Hipergeometrico", params, "cdf_left", {"r": 3})
    r = _find(results, "Binomial")
    assert not r.condition_met
    print(f"  condición: {r.condition_str} (OK, marca como no cumple)")


# ------------------------------------------------------------------
# 2. Binomial -> Normal
# ------------------------------------------------------------------

def test_binomial_to_normal():
    print("\n[2] Binomial -> Normal (con corrección de continuidad)")
    # np=60, n(1-p)=40 => cumple
    params = {"n": 100, "p": 0.6}
    results = try_approximations("Binomial", params, "cdf_left", {"r": 65})
    r = _find(results, "Normal")

    assert r.condition_met, f"Condición debería cumplirse: {r.condition_str}"
    # Referencia: P(X<=65 | Bi(100,0.6)) ≈ 0.8697 exacto; Normal aprox con cc ≈ 0.8749
    _assert_close(r.approx_value, r.exact_value, TOL_LOOSE, "Bi->N P(X<=65)")
    print(f"  condición: {r.condition_str}")
    print(f"  μ={r.target_params['mu']:.4f} σ={r.target_params['sigma']:.4f}")


# ------------------------------------------------------------------
# 3. Binomial -> Poisson
# ------------------------------------------------------------------

def test_binomial_to_poisson():
    print("\n[3] Binomial -> Poisson (eventos raros)")
    # p=0.003 <= 0.005 (cumple); m = np = 0.6
    params = {"n": 200, "p": 0.003}
    results = try_approximations("Binomial", params, "cdf_right", {"r": 1})
    r = _find(results, "Poisson")

    assert r.condition_met, f"Condición debería cumplirse: {r.condition_str}"
    assert abs(r.target_params["m"] - 0.6) < 1e-12
    _assert_close(r.approx_value, r.exact_value, 1e-3, "Bi->Po P(X>=1)")
    print(f"  condición: {r.condition_str}")


# ------------------------------------------------------------------
# 4. Poisson -> Normal
# ------------------------------------------------------------------

def test_poisson_to_normal():
    print("\n[4] Poisson -> Normal (m>=15)")
    params = {"m": 25}
    results = try_approximations("Poisson", params, "cdf_left", {"r": 27})
    r = _find(results, "Normal")

    assert r.condition_met, f"Condición debería cumplirse: {r.condition_str}"
    assert abs(r.target_params["mu"] - 25) < 1e-12
    assert abs(r.target_params["sigma"] - 5.0) < 1e-9
    _assert_close(r.approx_value, r.exact_value, TOL_LOOSE, "Po->N P(X<=27)")
    print(f"  condición: {r.condition_str}")


# ------------------------------------------------------------------
# 5. Gamma -> Normal (Wilson-Hilferty)
# ------------------------------------------------------------------

def test_gamma_to_normal_wh():
    print("\n[5] Gamma -> Normal (Wilson-Hilferty)")
    # Guía: Fg(20/4;0.3) => r=4, lam=0.3, x=20. Exacto ≈ 0.8488 (= Gpo(4/6))
    params = {"r": 4, "lam": 0.3}
    results = try_approximations("Gamma", params, "cdf_left", {"x": 20})
    r = _find(results, "Normal")

    assert r.condition_met  # WH siempre "aplicable"
    # WH es aproximación, admite error más grande para r pequeño
    _assert_close(r.approx_value, r.exact_value, 0.02, "Gamma->N WH Fg(20/4;0.3)")
    # valor conocido por la guía
    assert abs(r.exact_value - 0.8488) < 0.01, f"exact Fg(20/4;0.3) debería ser 0.8488 ± 0.01, fue {r.exact_value}"
    print(f"  condición: {r.condition_str}")


def test_gamma_to_normal_wh_large_r():
    print("\n[5b] Gamma -> Normal (Wilson-Hilferty, r grande -> menor error)")
    params = {"r": 30, "lam": 1.0}
    results = try_approximations("Gamma", params, "cdf_left", {"x": 28})
    r = _find(results, "Normal")
    _assert_close(r.approx_value, r.exact_value, 5e-4, "Gamma->N WH r=30")


# ------------------------------------------------------------------
# Entry point
# ------------------------------------------------------------------

def main():
    tests = [
        test_hiper_to_binomial,
        test_hiper_to_binomial_no_cumple,
        test_binomial_to_normal,
        test_binomial_to_poisson,
        test_poisson_to_normal,
        test_gamma_to_normal_wh,
        test_gamma_to_normal_wh_large_r,
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
