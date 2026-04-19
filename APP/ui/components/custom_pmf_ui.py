"""UI para el modelo CustomPMF (PMF discreta casera con normalizador k).

Patrón análogo a `multinomial_ui`: sidebar dedicado + main dedicado, porque
CustomPMF no comparte el shape (n, p, m, …) del resto de los modelos discretos.
"""

from __future__ import annotations

import streamlit as st

from models.discrete.custom_pmf import CustomPMF
from calculation.statistics_common import format_number


def _parse_domain(s: str) -> list:
    out: list = []
    for tok in s.split(","):
        tok = tok.strip()
        if not tok:
            continue
        try:
            v = int(tok)
        except ValueError:
            v = float(tok)
        out.append(v)
    return out


def render_custom_pmf_sidebar(sc: dict | None = None) -> dict:
    """Sidebar para CustomPMF.

    Devuelve dict con `model`, `expr`, `domain`, `k_var`, `query_type`,
    `query_params`, `error`. Si la fórmula es inválida `model` viene en None
    y `error` describe el problema (la UI principal lo muestra).
    """
    sc_params = (sc or {}).get("params", {}) if sc else {}
    sc_qp = (sc or {}).get("query_params", {}) if sc else {}
    sc_qt = (sc or {}).get("query_type", "full_analysis") if sc else "full_analysis"

    default_expr = sc_params.get("expr", "(x+2)/k")
    default_domain_list = sc_params.get("domain", [0, 1, 2, 3, 4])
    default_domain_str = ", ".join(
        str(int(d)) if float(d).is_integer() else str(d)
        for d in default_domain_list
    )
    default_k_var = sc_params.get("k_var", "k")

    st.subheader("Parámetros — PMF casera")
    expr = st.text_input(
        "Expresión P(X=x)",
        value=default_expr,
        help=("Usá `x` como variable y `k` (o el símbolo elegido) como "
              "normalizador. Ejemplos: `(x+2)/k`, `x**2/k`, `(2*x+1)/k`."),
    )
    domain_str = st.text_input(
        "Dominio (valores separados por coma)",
        value=default_domain_str,
        help="Ej: 0, 1, 2, 3, 4",
    )
    k_var = st.text_input("Símbolo del normalizador", value=default_k_var, max_chars=4)

    error: str | None = None
    model: CustomPMF | None = None
    domain: list = []
    try:
        domain = _parse_domain(domain_str)
        if len(domain) < 2:
            raise ValueError("El dominio debe tener al menos 2 valores.")
        model = CustomPMF(expr=expr, domain=domain, k_var=k_var)
    except Exception as e:
        error = str(e)

    st.markdown("---")
    st.subheader("Consulta")

    QT_LABELS = [
        "P(X = valor)",
        "F(x) = P(X ≤ valor)",
        "G(x) = P(X ≥ valor)",
        "P(A ≤ X ≤ B)",
        "P(A | B) — condicional",
        "Análisis completo",
    ]
    QT_KEYS = ["probability", "cdf_left", "cdf_right", "range",
               "conditional", "full_analysis"]
    qt_idx = QT_KEYS.index(sc_qt) if sc_qt in QT_KEYS else 5
    qt_label = st.selectbox("Tipo de consulta", QT_LABELS, index=qt_idx)
    query_type = QT_KEYS[QT_LABELS.index(qt_label)]

    qp: dict = {}
    if domain:
        d_min = int(min(domain))
        d_max = int(max(domain))
        sc_r = sc_qp.get("r")
        sc_a = sc_qp.get("a")
        sc_b = sc_qp.get("b")
        # sc_qp puede traer listas (CustomPMF/Multinomial) — fallbackeamos.
        sc_r_int = int(sc_r) if isinstance(sc_r, (int, float)) else d_min
        sc_a_int = int(sc_a) if isinstance(sc_a, (int, float)) else d_min
        sc_b_int = int(sc_b) if isinstance(sc_b, (int, float)) else d_max

        if query_type in ("probability", "cdf_left", "cdf_right"):
            qp["r"] = st.number_input(
                "Valor de x",
                min_value=d_min, max_value=d_max,
                value=max(d_min, min(sc_r_int, d_max)),
                step=1,
            )
        elif query_type == "range":
            c1, c2 = st.columns(2)
            with c1:
                qp["a"] = st.number_input(
                    "A (desde)", min_value=d_min, max_value=d_max,
                    value=max(d_min, min(sc_a_int, d_max)), step=1,
                )
            with c2:
                qp["b"] = st.number_input(
                    "B (hasta)", min_value=d_min, max_value=d_max,
                    value=max(d_min, min(sc_b_int, d_max)), step=1,
                )

        elif query_type == "conditional":
            OP_LABELS = ["=", "≤", "<", "≥", ">", "A ≤ X ≤ B"]
            OP_KEYS = ["=", "<=", "<", ">=", ">", "between"]

            def _op_idx(op: str | None, default: int = 0) -> int:
                return OP_KEYS.index(op) if op in OP_KEYS else default

            def _as_int_safe(v, default: int) -> int:
                if isinstance(v, (int, float)):
                    return int(v)
                return default

            def _as_pair(v, default_a: int, default_b: int) -> tuple[int, int]:
                if isinstance(v, (list, tuple)) and len(v) == 2:
                    try:
                        return int(v[0]), int(v[1])
                    except (TypeError, ValueError):
                        pass
                return default_a, default_b

            sc_num_op = sc_qp.get("num_op")
            sc_num_val = sc_qp.get("num_val")
            sc_den_op = sc_qp.get("den_op")
            sc_den_val = sc_qp.get("den_val")

            st.markdown("**Numerador (evento A)**")
            c_no, c_nv = st.columns([1, 2])
            with c_no:
                num_op_label = st.selectbox(
                    "Operador A", OP_LABELS,
                    index=_op_idx(sc_num_op, 0),
                    key="custom_pmf_num_op",
                )
            num_op = OP_KEYS[OP_LABELS.index(num_op_label)]
            with c_nv:
                if num_op == "between":
                    a0, b0 = _as_pair(sc_num_val, d_min, d_max)
                    na, nb = st.columns(2)
                    with na:
                        a_val = st.number_input(
                            "A", min_value=d_min, max_value=d_max,
                            value=max(d_min, min(a0, d_max)), step=1,
                            key="custom_pmf_num_a",
                        )
                    with nb:
                        b_val = st.number_input(
                            "B", min_value=d_min, max_value=d_max,
                            value=max(d_min, min(b0, d_max)), step=1,
                            key="custom_pmf_num_b",
                        )
                    qp["num_val"] = (int(a_val), int(b_val))
                else:
                    default_nv = _as_int_safe(sc_num_val, d_min)
                    qp["num_val"] = st.number_input(
                        "Valor A", min_value=d_min, max_value=d_max,
                        value=max(d_min, min(default_nv, d_max)), step=1,
                        key="custom_pmf_num_val",
                    )
            qp["num_op"] = num_op

            st.markdown("**Denominador (evento B)**")
            c_do, c_dv = st.columns([1, 2])
            with c_do:
                den_op_label = st.selectbox(
                    "Operador B", OP_LABELS,
                    index=_op_idx(sc_den_op, 4),
                    key="custom_pmf_den_op",
                )
            den_op = OP_KEYS[OP_LABELS.index(den_op_label)]
            with c_dv:
                if den_op == "between":
                    a0, b0 = _as_pair(sc_den_val, d_min, d_max)
                    da, db = st.columns(2)
                    with da:
                        a_val = st.number_input(
                            "A ", min_value=d_min, max_value=d_max,
                            value=max(d_min, min(a0, d_max)), step=1,
                            key="custom_pmf_den_a",
                        )
                    with db:
                        b_val = st.number_input(
                            "B ", min_value=d_min, max_value=d_max,
                            value=max(d_min, min(b0, d_max)), step=1,
                            key="custom_pmf_den_b",
                        )
                    qp["den_val"] = (int(a_val), int(b_val))
                else:
                    default_dv = _as_int_safe(sc_den_val, d_min)
                    qp["den_val"] = st.number_input(
                        "Valor B", min_value=d_min, max_value=d_max,
                        value=max(d_min, min(default_dv, d_max)), step=1,
                        key="custom_pmf_den_val",
                    )
            qp["den_op"] = den_op

    return {
        "model": model,
        "expr": expr,
        "domain": domain,
        "k_var": k_var,
        "query_type": query_type,
        "query_params": qp,
        "error": error,
    }


def render_custom_pmf_main(cfg: dict, detail_level: int) -> None:
    """Renderiza el contenido principal para CustomPMF.

    Mantiene paridad visual con los demás modelos discretos: tabs
    Cálculo / Características / Tabla / Gráficos.
    """
    if cfg.get("error") or cfg.get("model") is None:
        st.error(f"PMF inválida: {cfg.get('error') or 'parámetros vacíos.'}")
        return

    model: CustomPMF = cfg["model"]
    qt: str = cfg["query_type"]
    qp: dict = cfg["query_params"]

    st.subheader("PMF casera")
    st.latex(model.latex_formula())
    if model._k_value is not None:
        st.success(
            f"Normalización: {model.k_var} = "
            f"{format_number(model._k_value)}"
        )

    # Imports diferidos para evitar ciclos.
    from ui.components.step_display import render_calc_result
    from ui.components.summary_panel import render_summary
    from ui.components.table_panel import render_table
    from ui.components.graph_panel import render_graphs

    tab_calc, tab_chars, tab_table, tab_graphs = st.tabs(
        ["Cálculo Paso a Paso", "Características", "Tabla de Distribución", "Gráficos"]
    )

    highlight = None

    with tab_calc:
        if qt == "probability":
            r = int(qp.get("r", model.domain[0]))
            highlight = r
            st.subheader(f"P(X = {r})")
            render_calc_result(model.probability(r), detail_level)

        elif qt == "cdf_left":
            r = int(qp.get("r", model.domain[-1]))
            highlight = r
            st.subheader(f"F({r}) = P(X ≤ {r})")
            render_calc_result(model.cdf_left(r), detail_level)

        elif qt == "cdf_right":
            r = int(qp.get("r", model.domain[0]))
            highlight = r
            st.subheader(f"G({r}) = P(X ≥ {r})")
            render_calc_result(model.cdf_right(r), detail_level)

        elif qt == "range":
            a = int(qp.get("a", model.domain[0]))
            b = int(qp.get("b", model.domain[-1]))
            st.subheader(f"P({a} ≤ X ≤ {b})")
            terms = [(x, model.probability_value(x))
                     for x in model.domain if a <= x <= b]
            total = sum(p for _, p in terms)
            sum_terms = " + ".join(f"P(X={x})" for x, _ in terms) or "0"
            sum_vals = " + ".join(format_number(p) for _, p in terms) or "0"
            st.latex(
                rf"P({a} \le X \le {b}) = {sum_terms} = "
                rf"{sum_vals} = {format_number(total)}"
            )
            st.success(f"P({a} ≤ X ≤ {b}) = {format_number(total)}")

        elif qt == "conditional":
            OP_SYMBOL = {"=": "=", "<=": "≤", "<": "<",
                         ">=": "≥", ">": ">", "between": "between"}
            num_op = qp.get("num_op", "=")
            den_op = qp.get("den_op", ">=")
            num_val = qp.get("num_val", model.domain[0])
            den_val = qp.get("den_val", model.domain[0])

            def _fmt(op: str, val) -> str:
                if op == "between" and isinstance(val, (list, tuple)):
                    return f"{int(val[0])} ≤ X ≤ {int(val[1])}"
                return f"X {OP_SYMBOL.get(op, op)} {int(val)}"

            st.subheader(f"P({_fmt(num_op, num_val)} | {_fmt(den_op, den_val)})")
            render_calc_result(
                model.conditional(num_op, num_val, den_op, den_val),
                detail_level,
            )

        else:  # full_analysis
            st.subheader("Probabilidades puntuales")
            for x in model.domain:
                p = model.probability_value(x)
                with st.expander(f"P(X={x}) = {format_number(p)}"):
                    render_calc_result(model.probability(x), detail_level)

    with tab_chars:
        st.subheader("Características")
        chars = model.all_characteristics()
        render_summary(chars, detail_level)

        st.markdown("---")
        st.subheader("Expectativa Parcial Izquierda H(·)")
        d_min, d_max = int(min(model.domain)), int(max(model.domain))
        default_h = max(d_min, min(int(round(model.mean().final_value)), d_max))
        r_h = st.number_input(
            "Valor de x para H(x)",
            min_value=d_min, max_value=d_max,
            value=default_h, step=1, key="custom_pmf_h_val",
        )
        render_calc_result(model.partial_expectation_left(int(r_h)), detail_level)

    with tab_table:
        st.subheader("Tabla de Distribución")
        render_table(model.full_table())

    with tab_graphs:
        st.subheader("Gráficos")
        render_graphs(
            model.full_table(),
            f"CustomPMF({cfg.get('expr', model.expr)})",
            highlight_r=highlight,
        )
