"""QA smoke — ejercita cada modo y flujo sin UI.

Recorre los 20 flujos del MANUAL_REGRESSION_CHECKLIST (los que no requieren
click manual) + edge cases. Un test se rompe si:
 - el parser no detecta el modo correcto,
 - el sc producido no pasa por apply_sc_to_session sin excepcion,
 - el modelo devuelve valor numerico lejos del esperado (> tol),
 - un flujo compound/approximation/multinomial/tcl explota.
"""
from __future__ import annotations

import math
import os
import sys
import traceback

_HERE = os.path.dirname(os.path.abspath(__file__))
_APP = os.path.dirname(_HERE)
if _APP not in sys.path:
    sys.path.insert(0, _APP)

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


RESULTS: list[tuple[str, bool, str]] = []


def _check(name: str, ok: bool, detail: str = "") -> None:
    RESULTS.append((name, ok, detail))
    mark = "OK" if ok else "FAIL"
    line = f"  [{mark}] {name}"
    if detail:
        line += f" — {detail}"
    print(line, flush=True)


def _close(got: float, exp: float, tol: float = 1e-3) -> bool:
    return abs(got - exp) < tol


# ---------------------------------------------------------------------------
# 1. Parser + mode dispatch
# ---------------------------------------------------------------------------
def qa_parser_and_mode():
    print("\n[1] Parser + mode switching")
    from interpreter.nl_parser import NLParser
    from interpreter.streamlit_interpreter import apply_sc_to_session, interpret_turn

    cases = [
        # (descripcion, texto, modo_esperado, extra_checks)
        ("Catedra Binomial bypass", "Fb(4/12;0.45)", "Modelos de Probabilidad", None),
        ("Catedra Pascal",          "Fpa(12/5;0.42)", "Modelos de Probabilidad", None),
        ("Catedra Hiper",           "Fh(3/10;30;8)", "Modelos de Probabilidad", None),
        ("Catedra Poisson",         "Fpo(4/6)", "Modelos de Probabilidad", None),
        ("Moneda NL",               "Se lanza una moneda 15 veces, exactamente 4 caras", "Modelos de Probabilidad", None),
        ("Datos Agrupados tabla",   "Tabla de frecuencias 10-20 5, 20-30 8, 30-40 7, calcular media y mediana", "Datos Agrupados", None),
        ("TCL NL",                  "suma de 30 variables con media 1 y varianza 0.25, calcular P(S<=20)", "TCL / Suma de VA", None),
        ("Multinomial NL",          "multinomial n=10 probabilidades 0.2;0.3;0.5 conteos 2;3;5", "Modelos de Probabilidad", None),
        ("Guide exercise",          "tema III ejercicio 8", None, "guide"),
        ("Compound hiper+bin",      "15 cajas de 10 piezas con 2 defectuosas. De cada caja se toma muestra de 2, se rechaza si hay alguna defectuosa. P(se rechacen menos de 3 cajas)", "Problema Compuesto", None),
    ]

    p = NLParser()
    # simulamos session_state como dict
    for desc, text, exp_mode, extra in cases:
        try:
            session: dict = {}
            msgs: list = []
            result = interpret_turn(msgs, text)
            action = result.get("action")
            sc = result.get("sc", {})
            if action != "complete":
                _check(desc, False, f"action={action} (no completo); msg={result.get('message','')}")
                continue

            apply_sc_to_session(sc, session)

            if extra == "guide":
                _check(desc, bool(result.get("enunciado_from_guide")), f"tema={result.get('tema')} num={result.get('numero')}")
                continue

            # modo: puede venir en sc['mode'] y se propaga via _pending_mode
            got_mode = session.get("_pending_mode") or sc.get("mode")
            if exp_mode == "Problema Compuesto":
                ok = sc.get("mode") == "Problema Compuesto"
                _check(desc, ok, f"sc.mode={sc.get('mode')}")
            else:
                ok = got_mode == exp_mode
                _check(desc, ok, f"mode={got_mode} (esperado {exp_mode})")
        except Exception as e:
            _check(desc, False, f"EXC {type(e).__name__}: {e}")


# ---------------------------------------------------------------------------
# 2. Valores conocidos de la guia
# ---------------------------------------------------------------------------
def qa_known_answers():
    print("\n[2] Valores conocidos de la guia")
    from models.discrete.binomial import Binomial
    from models.discrete.pascal import Pascal
    from models.discrete.poisson import Poisson

    # Binomial
    b = Binomial(n=12, p=0.45)
    _check("Fb(4/12;0.45)=0.3044", _close(b.cdf_left(4).final_value, 0.3044, 1e-3))
    b2 = Binomial(n=10, p=0.25)
    _check("Gb(3/10;0.25)=0.4744", _close(b2.cdf_right(3).final_value, 0.4744, 1e-3))
    b3 = Binomial(n=14, p=0.75)
    _check("Gb(10/14;0.75)=0.7415", _close(b3.cdf_right(10).final_value, 0.7415, 1e-3))

    # Pascal
    pa = Pascal(r=5, p=0.42)
    _check("Fpa(12/5;0.42)=0.6175", _close(pa.cdf_left(12).final_value, 0.6175, 1e-3))

    # Poisson
    po = Poisson(m=6)
    _check("Fpo(4/6)≈0.2851", _close(po.cdf_left(4).final_value, 0.2851, 1e-3))
    po2 = Poisson(m=5)
    _check("P(r=0/m=5)=0.0067", _close(po2.probability(0).final_value, 0.0067, 1e-3))


# ---------------------------------------------------------------------------
# 3. Multinomial + marginal
# ---------------------------------------------------------------------------
def qa_multinomial():
    print("\n[3] Multinomial")
    from models.discrete.multinomial import Multinomial

    m = Multinomial(n=10, p_vector=[0.2, 0.3, 0.5])
    _check("Multi P(2,3,5)=0.0851", _close(m.probability([2, 3, 5]).final_value, 0.08505, 1e-4))
    marg = m.marginal_binomial(1)
    _check("Marginal Bi(10,0.2).E=2", _close(marg.mean().final_value, 2.0, 1e-6))


# ---------------------------------------------------------------------------
# 4. TCL / Suma de VA
# ---------------------------------------------------------------------------
def qa_tcl():
    print("\n[4] TCL / Suma de VA")
    from tcl.sum_of_rvs import Component, SumOfRVs

    comps = [Component(name="X", mean=1.0, variance=0.25, count=30)]
    s = SumOfRVs(comps)
    _check("TCL E(S)=30", _close(s.expected_value_raw(), 30.0))
    _check("TCL V(S)=7.5", _close(s.variance_raw(), 7.5))
    r = s.probability("cdf_left", s=25)
    _check("TCL P(S<=25) finito", r.final_value is not None and 0 < r.final_value < 1, f"P={r.final_value:.4f}")


# ---------------------------------------------------------------------------
# 5. Approximations
# ---------------------------------------------------------------------------
def qa_approximations():
    print("\n[5] Approximations engine")
    from approximations.approximator import try_approximations

    results = try_approximations(
        "Binomial", {"n": 100, "p": 0.6}, "probability", {"r": 60}
    )
    has_normal = any(r.to_model == "Normal" for r in results)
    _check("Bi(100,0.6) → Normal aparece", has_normal)
    if has_normal:
        nr = [r for r in results if r.to_model == "Normal"][0]
        _check("Bi→N condicion OK", nr.condition_met)


# ---------------------------------------------------------------------------
# 6. Compound solver
# ---------------------------------------------------------------------------
def qa_compound():
    print("\n[6] Compound problems")
    from calculation.compound_solver import solve_compound

    cfg = {
        "compound_type": "hiper_binomial",
        "box_N": 10, "box_R": 2, "sample_n": 2,
        "num_boxes": 15, "reject_r": 1,
        "query_type": "cdf_left", "query_r": 2,
    }
    try:
        sol = solve_compound(cfg)
        _check("hiper_binomial resuelve", sol is not None and "final_value" in sol, f"P={sol.get('final_value'):.4f}")
    except Exception as e:
        _check("hiper_binomial resuelve", False, f"EXC {e}")

    cfg2 = {
        "compound_type": "pascal_conditional",
        "r_success": 20, "p": 0.9, "condition_n": 25, "query_n": 30,
    }
    try:
        sol = solve_compound(cfg2)
        _check("pascal_conditional resuelve", sol is not None and "final_value" in sol, f"P={sol.get('final_value'):.4f}")
    except Exception as e:
        _check("pascal_conditional resuelve", False, f"EXC {e}")


# ---------------------------------------------------------------------------
# 7. Continuos
# ---------------------------------------------------------------------------
def qa_continuous():
    print("\n[7] Modelos continuos")
    from models.continuous.normal import Normal
    from models.continuous.gamma import Gamma

    n = Normal(mu=10, sigma=2)
    _check("Normal P(X<12)≈0.8413", _close(n.cdf_left(12).final_value, 0.8413, 1e-3))

    g = Gamma(r=2, lam=1)
    _check("Gamma(2,1) P(X<2)≈0.5940", _close(g.cdf_left(2).final_value, 0.5940, 1e-3))

    # Wilson-Hilferty smoke: Gamma grande → Normal
    from approximations.approximator import try_approximations
    rs = try_approximations("Gamma", {"r": 30, "lam": 2}, "cdf_left", {"x": 15})
    wh = [r for r in rs if r.to_model == "Normal"]
    _check("Gamma(30,2) Wilson-Hilferty existe", bool(wh))


# ---------------------------------------------------------------------------
# 8. Datos Agrupados
# ---------------------------------------------------------------------------
def qa_datos_agrupados():
    print("\n[8] Datos agrupados")
    from data_processing.grouped_data import GroupedData

    intervals = [(10, 20), (20, 30), (30, 40), (40, 50)]
    freqs = [5, 8, 7, 4]
    gd = GroupedData(intervals, freqs)
    try:
        media = gd.mean().final_value
        _check("GD media calcula", media is not None and 15 < media < 40, f"media={media:.3f}")
    except Exception as e:
        _check("GD media calcula", False, f"EXC {e}")
    try:
        mediana = gd.median().final_value
        _check("GD mediana calcula", mediana is not None, f"med={mediana:.3f}")
    except Exception as e:
        _check("GD mediana calcula", False, f"EXC {e}")


# ---------------------------------------------------------------------------
# 9. Probabilidad (Bayes + two-events)
# ---------------------------------------------------------------------------
def qa_probabilidad():
    print("\n[9] Probabilidad (eventos + Bayes)")
    from probability.bayes import BayesCalc
    from probability.basic import solve_two_events

    bc = BayesCalc(
        labels=["H1", "H2", "H3"],
        priors=[0.2, 0.5, 0.3],
        likelihoods=[0.1, 0.3, 0.5],
        evidence_label="E",
    )
    try:
        post = bc.posteriors()
        # posteriors() retorna lista de tuples (label, value)
        if post and isinstance(post[0], tuple):
            total = sum(p[1] for p in post)
        elif post and isinstance(post[0], dict):
            total = sum(p.get("value", p.get("posterior", 0.0)) for p in post)
        else:
            total = sum(float(p) for p in post)
        _check("Bayes posteriors suman 1", _close(total, 1.0, 1e-6), f"sum={total:.6f}")
    except Exception as e:
        _check("Bayes posteriors suman 1", False, f"EXC {e}")

    try:
        sol = solve_two_events(
            {"P(A)": 0.4, "P(B)": 0.5, "P(A∩B)": 0.2},
            name_A="A", name_B="B",
        )
        _check("solve_two_events 3-knowns", sol is not None)
    except Exception as e:
        _check("solve_two_events 3-knowns", False, f"EXC {e}")


# ---------------------------------------------------------------------------
# 10. CustomPMF
# ---------------------------------------------------------------------------
def qa_custom_pmf():
    print("\n[10] CustomPMF")
    from models.discrete.custom_pmf import CustomPMF

    try:
        pmf = CustomPMF(expr="(x+2)/k", domain=[0, 1, 2, 3])
        _check("CustomPMF k=14", _close(pmf._k_value, 14.0, 1e-9), f"k={pmf._k_value}")
        e = pmf.mean().final_value
        _check("CustomPMF E(X)≈1.857", _close(e, 1.857, 5e-3), f"E={e:.4f}")
        p = pmf.probability(2).final_value
        _check("CustomPMF P(X=2)=4/14", _close(p, 4/14, 1e-9), f"P={p:.4f}")
    except Exception as e:
        _check("CustomPMF end-to-end", False, f"EXC {type(e).__name__}: {e}")

    # Conditional probability + parser detection
    try:
        m = CustomPMF(expr="(x**2+1)/k", domain=[1, 2, 3, 4, 5])
        _check("CustomPMF k=60 ((x²+1)/k)", _close(m._k_value, 60.0, 1e-9),
               f"k={m._k_value}")
        _check("CustomPMF E(X)=4.0 exact",
               _close(m.mean().final_value, 4.0, 1e-9),
               f"E={m.mean().final_value:.6f}")
        _check("CustomPMF σ≈1.1106",
               _close(m.std_dev().final_value, 1.1106, 5e-4),
               f"σ={m.std_dev().final_value:.6f}")
        cr = m.conditional("=", 5, ">", 2)
        _check("CustomPMF P(X=5|X>2)=26/53",
               _close(cr.final_value, 26/53, 1e-9),
               f"v={cr.final_value:.6f}")
        cr_imp = m.conditional("=", 5, ">", 5)
        import math as _math
        _check("CustomPMF P(·|X>5)=NaN",
               _math.isnan(cr_imp.final_value),
               f"v={cr_imp.final_value}")
    except Exception as e:
        _check("CustomPMF conditional", False, f"EXC {type(e).__name__}: {e}")

    try:
        from interpreter.nl_parser import NLParser
        r = NLParser().parse(
            "P(X=x) = (x**2+1)/k para x en {1,2,3,4,5}. "
            "Probabilidad de exactamente 5 sabiendo que mas de 2."
        )
        ok = (r.get("status") == "complete"
              and r.get("query_type") == "conditional"
              and r.get("query_params", {}).get("num_op") == "="
              and r.get("query_params", {}).get("num_val") == 5
              and r.get("query_params", {}).get("den_op") == ">"
              and r.get("query_params", {}).get("den_val") == 2)
        _check("Parser detecta conditional NL", ok,
               f"status={r.get('status')} qt={r.get('query_type')} "
               f"qp={r.get('query_params')}")
    except Exception as e:
        _check("Parser detecta conditional NL", False,
               f"EXC {type(e).__name__}: {e}")


# ---------------------------------------------------------------------------
# 11. Imports de UI (catch syntax errors)
# ---------------------------------------------------------------------------
def qa_ui_imports():
    print("\n[11] UI imports (sin ejecutar Streamlit)")
    targets = [
        "ui.components.step_display",
        "ui.components.summary_panel",
        "ui.components.graph_panel",
        "ui.components.table_panel",
        "ui.components.data_processing_ui",
        "ui.components.probability_ui",
        "ui.components.continuous_ui",
        "ui.components.compound_ui",
        "ui.components.approximations_ui",
        "ui.components.multinomial_ui",
        "ui.components.tcl_ui",
        "ui.components.theory_ui",
        "ui.components.custom_pmf_ui",
    ]
    for name in targets:
        try:
            __import__(name)
            _check(f"import {name}", True)
        except Exception as e:
            _check(f"import {name}", False, f"{type(e).__name__}: {e}")


# ---------------------------------------------------------------------------
# 12. HTTP smoke (si Streamlit corre)
# ---------------------------------------------------------------------------
def qa_http_smoke():
    print("\n[12] HTTP smoke (Streamlit)")
    import urllib.request
    any_ok = False
    for port in (8501, 8502):
        try:
            r = urllib.request.urlopen(f"http://localhost:{port}/", timeout=3)
            if r.status == 200:
                any_ok = True
                print(f"  (info) Streamlit {port} sirviendo")
        except Exception:
            pass
    _check("Streamlit >=1 puerto sirviendo", any_ok)


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
def main() -> int:
    print("=" * 70)
    print("QA SMOKE — cada modo y flujo sin UI manual")
    print("=" * 70)
    for fn in [
        qa_ui_imports,
        qa_known_answers,
        qa_continuous,
        qa_multinomial,
        qa_tcl,
        qa_custom_pmf,
        qa_approximations,
        qa_compound,
        qa_datos_agrupados,
        qa_probabilidad,
        qa_parser_and_mode,
        qa_http_smoke,
    ]:
        try:
            fn()
        except Exception as e:
            print(f"  [FAIL] {fn.__name__} EXC: {e}")
            traceback.print_exc()

    print("\n" + "=" * 70)
    total = len(RESULTS)
    passed = sum(1 for _, ok, _ in RESULTS if ok)
    print(f"RESULTADO: {passed}/{total} OK")
    print("=" * 70)
    fails = [(n, d) for n, ok, d in RESULTS if not ok]
    if fails:
        print("\nFALLAS:")
        for n, d in fails:
            print(f"  - {n}: {d}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
