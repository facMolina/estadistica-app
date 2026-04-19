"""UI para el modelo Multinomial (discreto multivariado)."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from calculation.statistics_common import format_number
from models.discrete.multinomial import Multinomial
from ui.components.step_display import render_calc_result


_DEFAULT_DF = pd.DataFrame({
    "Categoría": ["C1", "C2", "C3"],
    "pi": [0.2, 0.3, 0.5],
    "ri": [2, 3, 5],
})


def render_multinomial_sidebar(sc: dict | None = None) -> dict:
    """Sidebar para Multinomial. Devuelve dict config con keys:
       - model:       instancia Multinomial (o None si hay error)
       - labels, pi_vector, r_vector
       - query_type:  "joint_probability" | "marginal" | "full_analysis"
       - query_params
       - title_params
       - error:       str | None
    """
    st.subheader("Parámetros")
    st.caption("Probabilidades por categoría (deben sumar 1). Los conteos `ri` son opcionales "
               "salvo que consultes la probabilidad conjunta.")

    # --- Tabla editable con defaults desde sc ---
    if sc and sc.get("params", {}).get("pi"):
        pi_from_sc = sc["params"]["pi"]
        labels_default = sc["params"].get("labels") or [f"C{i+1}" for i in range(len(pi_from_sc))]
        r_vector_sc = (sc.get("query_params") or {}).get("r_vector") or [0] * len(pi_from_sc)
        default_df = pd.DataFrame({
            "Categoría": labels_default,
            "pi": pi_from_sc,
            "ri": r_vector_sc,
        })
    elif "multinomial_df" in st.session_state:
        default_df = st.session_state["multinomial_df"]
    else:
        default_df = _DEFAULT_DF.copy()

    edited = st.data_editor(
        default_df,
        num_rows="dynamic",
        hide_index=True,
        use_container_width=True,
        column_config={
            "Categoría": st.column_config.TextColumn("Categoría", required=True),
            "pi": st.column_config.NumberColumn("pi (probabilidad)",
                                                min_value=0.0, max_value=1.0,
                                                step=0.01, format="%.4f", required=True),
            "ri": st.column_config.NumberColumn("ri (conteo)",
                                                min_value=0, step=1, required=False),
        },
        key="multinomial_editor",
    )
    st.session_state["multinomial_df"] = edited

    # Normalizar NaN
    edited_clean = edited.dropna(subset=["Categoría", "pi"]).reset_index(drop=True)
    labels = edited_clean["Categoría"].astype(str).tolist()
    try:
        pi_vector = [float(x) for x in edited_clean["pi"].tolist()]
    except Exception:
        pi_vector = []
    try:
        ri_raw = edited_clean["ri"].fillna(0).tolist()
        r_vector = [int(x) for x in ri_raw]
    except Exception:
        r_vector = []

    # --- Validaciones visibles ---
    pi_sum = sum(pi_vector) if pi_vector else 0.0
    if pi_vector:
        st.caption(f"Σ pi = {pi_sum:.4f}  "
                   f"({'✓' if abs(pi_sum - 1.0) < 1e-4 else '⚠️ debe sumar 1'})")

    # --- Consulta ---
    st.markdown("---")
    st.subheader("Consulta")
    query_options = [
        "P(r1, r2, ..., rk) — probabilidad conjunta",
        "Marginal P(Xi = ri)",
        "E(Xi), V(Xi), Cov(Xi, Xj) — características",
    ]
    qt_labels = ["joint_probability", "marginal", "full_analysis"]

    sc_qt = (sc or {}).get("query_type")
    sc_idx = qt_labels.index(sc_qt) if sc_qt in qt_labels else 0
    query_label = st.selectbox("Tipo de consulta", query_options, index=sc_idx)
    query_type = qt_labels[query_options.index(query_label)]

    query_params: dict = {}
    if query_type == "joint_probability":
        query_params["r_vector"] = r_vector
        if r_vector and pi_vector and len(r_vector) != len(pi_vector):
            st.warning("ri debe tener la misma cantidad de elementos que pi.")
    elif query_type == "marginal":
        if labels:
            i_sel = st.selectbox("Categoría i", list(range(1, len(labels) + 1)),
                                 format_func=lambda x: f"{x} — {labels[x-1]}")
        else:
            i_sel = 1
        r_val = st.number_input("ri (valor puntual)", min_value=0, value=0, step=1)
        query_params["i"] = int(i_sel)
        query_params["r"] = int(r_val)

    # --- Instanciar modelo ---
    n_total = sum(r_vector) if r_vector and query_type == "joint_probability" else None
    if n_total is None:
        n_total = st.number_input(
            "n (total de ensayos)", min_value=1, value=max(sum(r_vector), 1), step=1)
    else:
        st.caption(f"n derivado de Σ ri = {n_total}")

    model: Multinomial | None = None
    error: str | None = None
    try:
        model = Multinomial(int(n_total), pi_vector, labels=labels)
    except Exception as e:
        error = str(e)

    title_params = (f"n={n_total}, k={len(pi_vector)}") if pi_vector else ""

    return {
        "model": model,
        "labels": labels,
        "pi_vector": pi_vector,
        "r_vector": r_vector,
        "n": int(n_total),
        "query_type": query_type,
        "query_params": query_params,
        "title_params": title_params,
        "error": error,
    }


def render_multinomial_main(cfg: dict, detail_level: int) -> None:
    """Renderiza el contenido principal para Multinomial."""
    st.subheader(f"Multinomial({cfg.get('title_params', '')})")

    if cfg.get("error"):
        st.error(f"Parámetros inválidos: {cfg['error']}")
        return

    model: Multinomial = cfg["model"]
    qt = cfg["query_type"]
    qp = cfg["query_params"]

    tab_calc, tab_chars = st.tabs(["Cálculo", "Características por categoría"])

    with tab_calc:
        if qt == "joint_probability":
            r_vec = qp.get("r_vector") or []
            if not r_vec:
                st.info("Completá los conteos `ri` en la tabla para calcular la probabilidad conjunta.")
            elif sum(r_vec) != model.n:
                st.warning(f"La suma de ri ({sum(r_vec)}) debe ser igual a n ({model.n}).")
            elif len(r_vec) != model.k:
                st.warning(f"ri debe tener {model.k} valores.")
            else:
                try:
                    res = model.probability(r_vec)
                    st.success(f"P({', '.join(str(x) for x in r_vec)}) = "
                               f"{format_number(res.final_value, 6)}")
                    render_calc_result(res, detail_level)
                except Exception as e:
                    st.error(f"Error: {e}")

        elif qt == "marginal":
            i = qp.get("i", 1)
            r = qp.get("r", 0)
            binom = model.marginal_binomial(i)
            st.caption(f"Por propiedad del Multinomial: X_{i} ~ Binomial(n={model.n}, p={model.p[i-1]})")
            res = binom.probability(int(r))
            st.success(f"P(X_{i} = {r}) = {format_number(res.final_value, 6)}")
            render_calc_result(res, detail_level)

        else:  # full_analysis
            st.info("Ver la pestaña «Características por categoría» para E(Xi), V(Xi), y covarianzas.")

    with tab_chars:
        rows = model.characteristics_summary()
        df = pd.DataFrame(rows)
        df = df[["i", "Categoría", "pi", "E(Xi)", "V(Xi)", "σ(Xi)"]]
        st.dataframe(df, hide_index=True, use_container_width=True)

        st.markdown("---")
        st.caption("Desglose paso a paso:")
        with st.expander("E(Xi) = n · pi"):
            render_calc_result(model.mean_vector(), detail_level)
        with st.expander("V(Xi) = n · pi · (1 - pi)"):
            render_calc_result(model.variance_vector(), detail_level)

        if model.k >= 2:
            st.markdown("**Covarianzas entre pares (Cov(Xi, Xj) = -n · pi · pj):**")
            col_i, col_j = st.columns(2)
            with col_i:
                i_sel = st.selectbox("i", list(range(1, model.k + 1)),
                                     format_func=lambda x: f"{x} — {model.labels[x-1]}",
                                     key="cov_i")
            with col_j:
                j_sel = st.selectbox("j", list(range(1, model.k + 1)),
                                     format_func=lambda x: f"{x} — {model.labels[x-1]}",
                                     index=min(1, model.k - 1),
                                     key="cov_j")
            render_calc_result(model.covariance(int(i_sel), int(j_sel)), detail_level)
