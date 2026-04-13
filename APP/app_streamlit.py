"""Calculadora de Estadistica - Interfaz Web (Streamlit)."""

import sys
import os
import json
import streamlit as st

# Agregar APP al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.discrete.binomial import Binomial
from ui.components.detail_selector import render_detail_selector
from ui.components.step_display import render_calc_result
from ui.components.graph_panel import render_graphs
from ui.components.table_panel import render_table
from ui.components.summary_panel import render_summary
from calculation.statistics_common import format_number
from config.settings import SESSION_CONFIG_PATH

# --- Config ---
st.set_page_config(
    page_title="Calculadora de Estadistica",
    page_icon="📊",
    layout="wide",
)

st.title("Calculadora de Estadistica General")
st.caption("Ing. Sergio Anibal Dopazo - UADE")

# --- Leer session_config escrito por la CLI (una sola vez por sesion) ---
if "session_config_loaded" not in st.session_state:
    if os.path.exists(SESSION_CONFIG_PATH):
        with open(SESSION_CONFIG_PATH, encoding="utf-8") as _f:
            st.session_state["sc"] = json.load(_f)
        os.remove(SESSION_CONFIG_PATH)
        st.session_state["sc_is_new"] = True
    else:
        st.session_state["sc"] = None
        st.session_state["sc_is_new"] = False
    st.session_state["session_config_loaded"] = True

sc = st.session_state.get("sc")
sc_is_new = st.session_state.get("sc_is_new", False)

if sc_is_new:
    st.info(f"Problema cargado desde CLI: {sc.get('interpretation', '')}")
    st.session_state["sc_is_new"] = False

# Etiquetas de consulta (mismo orden que el selectbox de abajo)
_QUERY_LABELS = [
    "P(r = valor)", "F(r) = P(VA <= valor)", "G(r) = P(VA >= valor)",
    "P(A <= r <= B)", "Analisis completo",
]
_QUERY_TYPE_TO_LABEL = {
    "probability":   "P(r = valor)",
    "cdf_left":      "F(r) = P(VA <= valor)",
    "cdf_right":     "G(r) = P(VA >= valor)",
    "range":         "P(A <= r <= B)",
    "full_analysis": "Analisis completo",
}

# Defaults: provienen del session_config si existe, sino valores neutros
_sc_n = int(sc["params"].get("n", 10)) if sc else 10
_sc_p = float(sc["params"].get("p", 0.30)) if sc else 0.30
_sc_qt_label = _QUERY_TYPE_TO_LABEL.get(
    sc.get("query_type", "full_analysis"), "Analisis completo"
) if sc else "P(r = valor)"
_sc_qt_index = _QUERY_LABELS.index(_sc_qt_label) if _sc_qt_label in _QUERY_LABELS else 0
_sc_r = int(sc["query_params"].get("r", 3)) if sc and sc.get("query_params") else 3
_sc_a = int(sc["query_params"].get("a", 2)) if sc and sc.get("query_params") else 2
_sc_b = int(sc["query_params"].get("b", 5)) if sc and sc.get("query_params") else 5
# Clampar valores de r al dominio [0, n]
_sc_r = max(0, min(_sc_r, _sc_n))
_sc_a = max(0, min(_sc_a, _sc_n))
_sc_b = max(0, min(_sc_b, _sc_n))

# --- Sidebar: Seleccion de modelo y parametros ---
with st.sidebar:
    st.header("Configuracion")

    # Selector de modelo
    modelo = st.selectbox("Modelo", ["Binomial"])  # Se agregan mas despues

    # Parametros segun modelo
    if modelo == "Binomial":
        st.subheader("Parametros")
        n = st.number_input("n (cantidad de pruebas)", min_value=1, max_value=1000, value=_sc_n, step=1)
        p = st.number_input("p (probabilidad de exito)", min_value=0.0, max_value=1.0, value=_sc_p, step=0.01, format="%.4f")
        st.markdown("---")
        st.subheader("Consulta")
        query_type = st.selectbox("Tipo de consulta", _QUERY_LABELS, index=_sc_qt_index)

        if query_type in ["P(r = valor)", "F(r) = P(VA <= valor)", "G(r) = P(VA >= valor)"]:
            r_val = st.number_input("Valor de r", min_value=0, max_value=int(n), value=min(_sc_r, int(n)), step=1)
        elif query_type == "P(A <= r <= B)":
            col1, col2 = st.columns(2)
            with col1:
                r_a = st.number_input("A (desde)", min_value=0, max_value=int(n), value=min(_sc_a, int(n)), step=1)
            with col2:
                r_b = st.number_input("B (hasta)", min_value=0, max_value=int(n), value=min(_sc_b, int(n)), step=1)

    st.markdown("---")
    detail_level = render_detail_selector()

    st.markdown("---")
    st.subheader("Formula del modelo")
    if modelo == "Binomial":
        st.latex(r"P(r) = \binom{n}{r} \cdot p^r \cdot (1-p)^{n-r}")


# --- Main content ---
if modelo == "Binomial":
    model = Binomial(n=int(n), p=p)

    # Tabs
    tab_calc, tab_chars, tab_table, tab_graphs = st.tabs([
        "Calculo Paso a Paso", "Caracteristicas", "Tabla de Distribucion", "Graficos",
    ])

    # Tab 1: Calculo paso a paso
    with tab_calc:
        if query_type == "P(r = valor)":
            st.subheader(f"P(r = {r_val}) para Binomial(n={int(n)}, p={p})")
            result = model.probability(int(r_val))
            render_calc_result(result, detail_level)

        elif query_type == "F(r) = P(VA <= valor)":
            st.subheader(f"F({r_val}) = P(VA <= {r_val}) para Binomial(n={int(n)}, p={p})")
            result = model.cdf_left(int(r_val))
            render_calc_result(result, detail_level)

        elif query_type == "G(r) = P(VA >= valor)":
            st.subheader(f"G({r_val}) = P(VA >= {r_val}) para Binomial(n={int(n)}, p={p})")
            result = model.cdf_right(int(r_val))
            render_calc_result(result, detail_level)

        elif query_type == "P(A <= r <= B)":
            st.subheader(f"P({r_a} <= r <= {r_b}) para Binomial(n={int(n)}, p={p})")
            f_b = model.cdf_left(int(r_b))
            f_a_minus_1 = model.cdf_left(int(r_a) - 1) if r_a > 0 else None
            prob_range = f_b.final_value - (f_a_minus_1.final_value if f_a_minus_1 else 0)

            st.markdown(f"**P({r_a} <= r <= {r_b}) = F({r_b}) - F({int(r_a)-1})**")
            st.latex(rf"P({r_a} \leq r \leq {r_b}) = F({r_b}) - F({int(r_a)-1}) = {format_number(f_b.final_value)} - {format_number(f_a_minus_1.final_value if f_a_minus_1 else 0)} = {format_number(prob_range)}")

            with st.expander("Detalle F(B)"):
                render_calc_result(f_b, detail_level)
            if f_a_minus_1:
                with st.expander("Detalle F(A-1)"):
                    render_calc_result(f_a_minus_1, detail_level)

            st.success(f"**Resultado:** P({r_a} <= r <= {r_b}) = {format_number(prob_range)}")

        elif query_type == "Analisis completo":
            st.subheader(f"Analisis completo - Binomial(n={int(n)}, p={p})")
            st.markdown("Todas las probabilidades puntuales:")
            d_min, d_max = model.domain()
            for r in range(d_min, d_max + 1):
                pv = model.probability_value(r)
                if pv > 1e-10:
                    with st.expander(f"P(r={r}) = {format_number(pv, 6)}"):
                        result = model.probability(r)
                        render_calc_result(result, detail_level)

    # Tab 2: Caracteristicas
    with tab_chars:
        st.subheader(f"Caracteristicas - Binomial(n={int(n)}, p={p})")
        chars = model.all_characteristics()
        render_summary(chars, detail_level)

        # Expectativa parcial
        st.markdown("---")
        st.subheader("Expectativa Parcial Izquierda")
        r_h = st.number_input("Valor de r para H(r)", min_value=0, max_value=int(n), value=int(n*p), step=1, key="h_r")
        h_result = model.partial_expectation_left(int(r_h))
        render_calc_result(h_result, detail_level)

    # Tab 3: Tabla
    with tab_table:
        st.subheader(f"Tabla de Distribucion - Binomial(n={int(n)}, p={p})")
        table_data = model.full_table()
        render_table(table_data)

    # Tab 4: Graficos
    with tab_graphs:
        st.subheader(f"Graficos - Binomial(n={int(n)}, p={p})")
        table_data = model.full_table()
        highlight = int(r_val) if query_type in ["P(r = valor)", "F(r) = P(VA <= valor)", "G(r) = P(VA >= valor)"] else None
        render_graphs(table_data, f"Binomial(n={int(n)}, p={p})", highlight_r=highlight)
