"""UI para el modo TCL / Suma de variables aleatorias."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from calculation.statistics_common import format_number
from tcl.sum_of_rvs import SumOfRVs, Component
from ui.components.step_display import render_calc_result


_DEFAULT_DF = pd.DataFrame({
    "Nombre": ["X1", "X2"],
    "E(Xi)": [100.0, 50.0],
    "V(Xi)": [25.0, 16.0],
    "Cantidad": [1, 1],
})


def render_tcl_sidebar(sc: dict | None = None) -> dict:
    """Sidebar para TCL. Devuelve dict con:
       - sum_obj:     SumOfRVs (o None si hay error)
       - components:  lista de Component
       - query_type:  'cdf_left' | 'cdf_right' | 'range' | 'fractile'
       - query_params: dict
       - title:       str
       - error:       str | None
    """
    st.subheader("Componentes independientes")
    st.caption("Cada fila es una variable Xi con E(Xi), V(Xi). "
               "`Cantidad` permite agregar k copias iid sin repetir filas.")

    if sc and sc.get("components"):
        raw = sc["components"]
        default_df = pd.DataFrame({
            "Nombre":   [c.get("name", f"X{i+1}") for i, c in enumerate(raw)],
            "E(Xi)":    [float(c.get("mean", 0.0)) for c in raw],
            "V(Xi)":    [float(c.get("variance", 0.0)) for c in raw],
            "Cantidad": [int(c.get("count", 1)) for c in raw],
        })
    elif "tcl_df" in st.session_state:
        default_df = st.session_state["tcl_df"]
    else:
        default_df = _DEFAULT_DF.copy()

    edited = st.data_editor(
        default_df,
        num_rows="dynamic",
        hide_index=True,
        use_container_width=True,
        column_config={
            "Nombre":   st.column_config.TextColumn("Nombre", required=True),
            "E(Xi)":    st.column_config.NumberColumn("E(Xi)", step=0.1,
                                                      format="%.4f", required=True),
            "V(Xi)":    st.column_config.NumberColumn("V(Xi)", min_value=0.0, step=0.1,
                                                      format="%.4f", required=True),
            "Cantidad": st.column_config.NumberColumn("Cantidad", min_value=1, step=1,
                                                      required=True),
        },
        key="tcl_editor",
    )
    st.session_state["tcl_df"] = edited

    cleaned = edited.dropna(subset=["Nombre", "E(Xi)", "V(Xi)"]).reset_index(drop=True)
    components: list[Component] = []
    error: str | None = None
    try:
        for _, row in cleaned.iterrows():
            components.append(Component(
                name=str(row["Nombre"]),
                mean=float(row["E(Xi)"]),
                variance=float(row["V(Xi)"]),
                count=int(row["Cantidad"]) if pd.notna(row["Cantidad"]) else 1,
            ))
    except Exception as e:
        error = str(e)

    sum_obj: SumOfRVs | None = None
    if components and error is None:
        try:
            sum_obj = SumOfRVs(components)
        except Exception as e:
            error = str(e)

    if sum_obj is not None:
        k_total = sum_obj.total_count
        st.caption(f"k total = {k_total}  "
                   f"({'✓ TCL aplicable' if k_total >= 30 else '⚠️ k < 30, TCL puede no ser precisa'})")
        st.caption(f"E(S) = {format_number(sum_obj.expected_value_raw())},  "
                   f"V(S) = {format_number(sum_obj.variance_raw())},  "
                   f"σ(S) = {format_number(sum_obj.std_dev_raw())}")

    st.markdown("---")
    st.subheader("Consulta")
    query_options = [
        "P(S ≤ s)",
        "P(S ≥ s)",
        "P(a ≤ S ≤ b)",
        "s tal que P(S ≤ s) = α  (fractil)",
    ]
    qt_labels = ["cdf_left", "cdf_right", "range", "fractile"]
    sc_qt = (sc or {}).get("query_type")
    sc_idx = qt_labels.index(sc_qt) if sc_qt in qt_labels else 0
    q_label = st.selectbox("Tipo de consulta", query_options, index=sc_idx)
    query_type = qt_labels[query_options.index(q_label)]

    query_params: dict = {}
    sc_qp = (sc or {}).get("query_params", {})
    if query_type in ("cdf_left", "cdf_right"):
        s_val = st.number_input("s", value=float(sc_qp.get("s", 150.0)), step=1.0, format="%.4f")
        query_params["s"] = float(s_val)
    elif query_type == "range":
        col_a, col_b = st.columns(2)
        with col_a:
            a_val = st.number_input("a (desde)", value=float(sc_qp.get("a", 140.0)),
                                    step=1.0, format="%.4f")
        with col_b:
            b_val = st.number_input("b (hasta)", value=float(sc_qp.get("b", 160.0)),
                                    step=1.0, format="%.4f")
        query_params["a"] = float(a_val)
        query_params["b"] = float(b_val)
    else:  # fractile
        alpha = st.number_input("α (0,1)", min_value=0.0001, max_value=0.9999,
                                value=float(sc_qp.get("alpha", 0.95)),
                                step=0.01, format="%.4f")
        query_params["alpha"] = float(alpha)

    title = (f"S = Σ Xi  (k={sum_obj.total_count})"
             if sum_obj is not None else "S = Σ Xi")

    return {
        "sum_obj": sum_obj,
        "components": components,
        "query_type": query_type,
        "query_params": query_params,
        "title": title,
        "error": error,
    }


def render_tcl_main(cfg: dict, detail_level: int) -> None:
    """Renderiza la pantalla principal del modo TCL."""
    st.subheader("Teorema Central del Límite — Suma de VA independientes")

    if cfg.get("error"):
        st.error(f"Configuración inválida: {cfg['error']}")
        return
    sum_obj: SumOfRVs | None = cfg.get("sum_obj")
    if sum_obj is None:
        st.info("Agregá al menos una componente para empezar.")
        return

    st.caption(cfg.get("title", ""))

    tab_calc, tab_moments, tab_comps = st.tabs(
        ["Cálculo", "E(S) y V(S) paso a paso", "Componentes"]
    )

    with tab_calc:
        qt = cfg["query_type"]
        qp = cfg["query_params"]
        try:
            res = sum_obj.probability(qt, **qp)
            st.success(res.final_latex.replace("\\", ""))
            render_calc_result(res, detail_level)
        except Exception as e:
            st.error(f"Error al calcular: {e}")

    with tab_moments:
        st.markdown("**E(S) = Σ E(Xi)**")
        render_calc_result(sum_obj.expected_value(), detail_level)
        st.markdown("---")
        st.markdown("**V(S) = Σ V(Xi)** (por independencia)")
        render_calc_result(sum_obj.variance(), detail_level)
        st.markdown("---")
        st.markdown("**σ(S) = √V(S)**")
        render_calc_result(sum_obj.std_dev(), detail_level)

    with tab_comps:
        rows = []
        for c in sum_obj.components:
            rows.append({
                "Nombre": c.name,
                "E(Xi)": c.mean,
                "V(Xi)": c.variance,
                "Cantidad": c.count,
                "E·count": c.mean * c.count,
                "V·count": c.variance * c.count,
            })
        st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
        st.caption(f"k total (Σ counts) = **{sum_obj.total_count}**.  "
                   f"TCL {'aplicable' if sum_obj.tcl_condition_met() else 'con precaución (k<30)'}.")
