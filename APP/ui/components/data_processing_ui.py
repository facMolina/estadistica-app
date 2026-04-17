"""
UI para Procesamiento de Datos Agrupados (Sprint 2 — Tema I).

Dos funciones publicas:
  render_dp_sidebar() -> dict   — controles del sidebar, retorna config
  render_dp_main(...)           — tabs principales (Calculos / Tabla / Graficos)
"""

import io
from typing import Optional, Dict, Any

import pandas as pd
import streamlit as st

from data_processing.grouped_data import GroupedData
from ui.components.step_display import render_calc_result
from display.graph_builder import build_histogram, build_ogiva
from calculation.statistics_common import format_number


# ---------------------------------------------------------------------------
# Dataset de muestra (Guia Tema I — ejemplo generico)
# ---------------------------------------------------------------------------
_SAMPLE_DF = pd.DataFrame({
    "Li": [0.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0],
    "Ls": [2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0],
    "fai": [5,   20,  30,  20,  15,   7,    3   ],
})

_QUERY_OPTIONS = [
    "Resumen estadistico completo",
    "Mediana",
    "Fractil x(α)",
    "P(a < x < b)",
    "P(x < b | x > a)  — condicional",
]


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

def render_dp_sidebar() -> Dict[str, Any]:
    """
    Renderiza la seccion de datos agrupados en el sidebar.
    Retorna dict con claves: gd (GroupedData|None), query (str), qparams (dict).
    """
    st.subheader("Tabla de frecuencias")

    if "dp_df" not in st.session_state:
        st.session_state["dp_df"] = _SAMPLE_DF.copy()

    if st.button("Cargar ejemplo", use_container_width=True, key="dp_load_sample"):
        st.session_state["dp_df"] = _SAMPLE_DF.copy()
        st.rerun()

    df_edited = st.data_editor(
        st.session_state["dp_df"],
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "Li": st.column_config.NumberColumn("Li", format="%.2f", help="Límite inferior"),
            "Ls": st.column_config.NumberColumn("Ls", format="%.2f", help="Límite superior"),
            "fai": st.column_config.NumberColumn("fai", min_value=0, format="%d",
                                                  help="Frecuencia absoluta"),
        },
        key="dp_editor",
    )
    st.session_state["dp_df"] = df_edited

    # Construir GroupedData
    gd: Optional[GroupedData] = None
    error_msg: Optional[str] = None
    try:
        df_clean = df_edited.dropna(subset=["Li", "Ls", "fai"])
        df_clean = df_clean[df_clean["fai"] >= 0]
        if len(df_clean) < 1:
            error_msg = "Ingresá al menos un intervalo con frecuencia."
        else:
            intervals = list(zip(
                df_clean["Li"].astype(float).tolist(),
                df_clean["Ls"].astype(float).tolist(),
            ))
            frequencies = df_clean["fai"].astype(int).tolist()
            for idx, (a, b) in enumerate(intervals):
                if b <= a:
                    error_msg = f"Intervalo {idx+1}: Ls debe ser > Li."
                    break
            if error_msg is None:
                gd = GroupedData(intervals=intervals, frequencies=frequencies)
    except Exception as exc:
        error_msg = str(exc)

    if error_msg:
        st.error(error_msg)
    elif gd is not None:
        st.caption(f"n = {gd.n}  |  k = {gd.k} intervalos")

    st.markdown("---")
    st.subheader("Consulta")
    query = st.selectbox("Calcular", _QUERY_OPTIONS, key="dp_query")

    qparams: Dict[str, float] = {}

    if "Fractil" in query:
        qparams["alpha"] = st.number_input(
            "α (fracción acumulada)",
            min_value=0.001, max_value=0.999,
            value=0.5, step=0.05, format="%.3f",
            key="dp_alpha",
        )

    elif "P(a < x < b)" in query:
        x_min = float(gd.intervals[0][0]) if gd else 0.0
        x_max = float(gd.intervals[-1][1]) if gd else 100.0
        x_mid = (x_min + x_max) / 2
        c1, c2 = st.columns(2)
        with c1:
            qparams["a"] = st.number_input("a", value=x_min, format="%.2f", key="dp_ra")
        with c2:
            qparams["b"] = st.number_input("b", value=x_mid, format="%.2f", key="dp_rb")

    elif "condicional" in query:
        x_min = float(gd.intervals[0][0]) if gd else 0.0
        x_max = float(gd.intervals[-1][1]) if gd else 100.0
        x_mid = (x_min + x_max) / 2
        c1, c2 = st.columns(2)
        with c1:
            qparams["given_above"] = st.number_input(
                "x > a", value=x_min, format="%.2f", key="dp_given"
            )
        with c2:
            qparams["find_below"] = st.number_input(
                "x < b", value=x_max, format="%.2f", key="dp_find"
            )

    return {"gd": gd, "query": query, "qparams": qparams}


# ---------------------------------------------------------------------------
# Contenido principal
# ---------------------------------------------------------------------------

def render_dp_main(
    gd: Optional[GroupedData],
    query: str,
    qparams: Dict[str, float],
    detail_level: int,
) -> None:
    """Renderiza tabs principales para Datos Agrupados."""
    if gd is None:
        st.info("Ingresá los datos en el panel lateral para ver los cálculos.")
        return

    tab_calc, tab_tabla, tab_graficos = st.tabs([
        "Calculos", "Tabla de Frecuencias", "Graficos",
    ])

    with tab_calc:
        _render_calcs(gd, query, qparams, detail_level)

    with tab_tabla:
        _render_freq_table(gd)

    with tab_graficos:
        _render_graphs(gd)


# ---------------------------------------------------------------------------
# Helpers internos
# ---------------------------------------------------------------------------

def _render_calcs(
    gd: GroupedData,
    query: str,
    qparams: Dict[str, float],
    detail_level: int,
) -> None:
    if "Resumen" in query:
        _render_resumen(gd, detail_level)

    elif "Mediana" in query:
        st.subheader("Mediana")
        render_calc_result(gd.median(), detail_level)

    elif "Fractil" in query:
        alpha = float(qparams.get("alpha", 0.5))
        st.subheader(f"Fractil  x(α = {format_number(alpha, 3)})")
        render_calc_result(gd.fractile(alpha), detail_level)

    elif "P(a < x < b)" in query:
        a = float(qparams.get("a", gd.intervals[0][0]))
        b = float(qparams.get("b", gd.intervals[-1][1]))
        st.subheader(f"P({format_number(a)} < x < {format_number(b)})")
        render_calc_result(gd.prob_range(a, b), detail_level)

    elif "condicional" in query:
        ga = float(qparams.get("given_above", gd.intervals[0][0]))
        fb_val = float(qparams.get("find_below", gd.intervals[-1][1]))
        st.subheader(
            f"P(x < {format_number(fb_val)} | x > {format_number(ga)})"
        )
        render_calc_result(gd.prob_conditional(ga, fb_val), detail_level)


def _render_resumen(gd: GroupedData, detail_level: int) -> None:
    """Calcula y muestra todas las caracteristicas estadisticas."""
    mu_res   = gd.mean()
    sn2_res  = gd.variance_n()
    sn12_res = gd.variance_n1()
    sn_res   = gd.std_dev_n()
    sn1_res  = gd.std_dev_n1()
    cvn_res  = gd.cv_n()
    cvn1_res = gd.cv_n1()

    # Fila de metricas rapidas
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Media  x̄", format_number(mu_res.final_value, 4))
    c2.metric("Desvio Sn", format_number(sn_res.final_value, 4))
    c3.metric("Desvio Sn-1", format_number(sn1_res.final_value, 4))
    c4.metric("CV (Sn)", f"{format_number(cvn_res.final_value, 2)} %")

    st.markdown("---")

    with st.expander("Media  x̄", expanded=True):
        render_calc_result(mu_res, detail_level)
    with st.expander("Varianza  Sn²  (poblacional)"):
        render_calc_result(sn2_res, detail_level)
    with st.expander("Varianza  Sn-1²  (muestral corregida)"):
        render_calc_result(sn12_res, detail_level)
    with st.expander("Desvio estandar  Sn"):
        render_calc_result(sn_res, detail_level)
    with st.expander("Desvio estandar  Sn-1"):
        render_calc_result(sn1_res, detail_level)
    with st.expander("Coef. de Variacion  Cvn"):
        render_calc_result(cvn_res, detail_level)
    with st.expander("Coef. de Variacion  Cvn-1"):
        render_calc_result(cvn1_res, detail_level)


def _render_freq_table(gd: GroupedData) -> None:
    rows = gd.build_table()
    df = pd.DataFrame(rows)

    # Formatear columnas flotantes para display
    float_cols = ["Li", "Ls", "Ci", "fi", "Fi", "Gi", "Ci·fai", "(Ci−x̄)²·fai"]
    int_cols = ["fai", "Fai", "Gai"]
    df_display = df.copy()
    for col in float_cols:
        if col in df_display.columns:
            df_display[col] = df_display[col].map(
                lambda v: format_number(v) if isinstance(v, float) else v
            )
    for col in int_cols:
        if col in df_display.columns:
            df_display[col] = df_display[col].astype(int)

    st.dataframe(df_display, use_container_width=True, hide_index=True)

    # Descarga CSV (con valores numericos exactos)
    csv_buf = io.StringIO()
    df.to_csv(csv_buf, index=False)
    st.download_button(
        "Descargar CSV",
        data=csv_buf.getvalue(),
        file_name="tabla_frecuencias.csv",
        mime="text/csv",
    )

    # Paso a paso de cada columna
    st.markdown("---")
    st.subheader("Construcción de la tabla paso a paso")
    _render_table_steps(gd)


def _render_table_steps(gd: GroupedData) -> None:
    """Muestra cómo se calcula cada columna de la tabla de frecuencias."""
    n = gd.n

    # --- Ci ---
    with st.expander("**Ci** — Marca de clase (centro del intervalo)"):
        st.latex(r"C_i = \frac{Li + Ls}{2}")
        for i in range(gd.k):
            a, b = gd.intervals[i]
            ci = gd.ci[i]
            st.latex(
                rf"C_{{{i+1}}} = \frac{{{format_number(a)} + {format_number(b)}}}{{2}} = {format_number(ci)}"
            )

    # --- fai ---
    with st.expander("**fai** — Frecuencia absoluta (dato de entrada)"):
        st.markdown("Las frecuencias absolutas son los datos de entrada: la cantidad de observaciones en cada intervalo.")
        for i in range(gd.k):
            a, b = gd.intervals[i]
            fai = gd.frequencies[i]
            st.latex(rf"f_{{a{i+1}}} \; [{format_number(a)} \text{{–}} {format_number(b)}): \; {fai}")
        st.latex(rf"n = \sum f_{{ai}} = {n}")

    # --- fi ---
    with st.expander("**fi** — Frecuencia relativa"):
        st.latex(rf"f_i = \frac{{f_{{ai}}}}{{n}} \qquad n = {n}")
        for i in range(gd.k):
            fai = gd.frequencies[i]
            fi = fai / n
            st.latex(
                rf"f_{{{i+1}}} = \frac{{{fai}}}{{{n}}} = {format_number(fi)}"
            )

    # --- Fai ---
    with st.expander("**Fai** — Frecuencia acumulada absoluta izquierda"):
        st.latex(r"F_{ai} = \sum_{j=1}^{i} f_{aj}")
        cum_abs = 0
        for i in range(gd.k):
            fai = gd.frequencies[i]
            cum_abs += fai
            if i == 0:
                st.latex(rf"F_{{a1}} = f_{{a1}} = {cum_abs}")
            else:
                st.latex(
                    rf"F_{{a{i+1}}} = F_{{a{i}}} + f_{{a{i+1}}} = "
                    rf"{cum_abs - fai} + {fai} = {cum_abs}"
                )

    # --- Fi ---
    with st.expander("**Fi** — Frecuencia acumulada relativa izquierda"):
        st.latex(r"F_i = \sum_{j=1}^{i} f_j")
        cum = 0.0
        for i in range(gd.k):
            fi = gd.frequencies[i] / n
            cum += fi
            if i == 0:
                st.latex(rf"F_1 = f_1 = {format_number(cum)}")
            else:
                st.latex(
                    rf"F_{{{i+1}}} = F_{{{i}}} + f_{{{i+1}}} = "
                    rf"{format_number(cum - fi)} + {format_number(fi)} = {format_number(cum)}"
                )

    # --- Gai ---
    with st.expander("**Gai** — Frecuencia acumulada absoluta derecha"):
        st.latex(r"G_{ai} = \sum_{j=i}^{k} f_{aj}")
        cum_right = 0
        gai_list = []
        for i in range(gd.k - 1, -1, -1):
            cum_right += gd.frequencies[i]
            gai_list.append(cum_right)
        gai_list.reverse()
        for i in range(gd.k):
            fai = gd.frequencies[i]
            if i == 0:
                st.latex(rf"G_{{a1}} = n = {gai_list[0]}")
            else:
                st.latex(
                    rf"G_{{a{i+1}}} = G_{{a{i}}} - f_{{a{i}}} = "
                    rf"{gai_list[i-1]} - {gd.frequencies[i-1]} = {gai_list[i]}"
                )

    # --- Gi ---
    with st.expander("**Gi** — Frecuencia acumulada relativa derecha"):
        st.latex(r"G_i = \sum_{j=i}^{k} f_j")
        for i in range(gd.k):
            gi = gai_list[i] / n
            if i == 0:
                st.latex(rf"G_1 = 1 = {format_number(gi)}")
            else:
                fi_prev = gd.frequencies[i-1] / n
                gi_prev = gai_list[i-1] / n
                st.latex(
                    rf"G_{{{i+1}}} = G_{{{i}}} - f_{{{i}}} = "
                    rf"{format_number(gi_prev)} - {format_number(fi_prev)} = {format_number(gi)}"
                )

    # --- Ci·fai ---
    with st.expander("**Ci·fai** — Producto para la media"):
        st.latex(r"\bar{x} = \frac{\sum f_{ai} \cdot C_i}{n}")
        total = 0.0
        for i in range(gd.k):
            fai = gd.frequencies[i]
            ci = gd.ci[i]
            fai_ci = fai * ci
            total += fai_ci
            st.latex(
                rf"f_{{a{i+1}}} \cdot C_{{{i+1}}} = {fai} \cdot {format_number(ci)} = {format_number(fai_ci)}"
            )
        st.latex(rf"\sum f_{{ai}} \cdot C_i = {format_number(total)}")

    # --- (Ci−x̄)²·fai ---
    with st.expander("**(Ci−x̄)²·fai** — Producto para la varianza"):
        st.latex(r"S_n^2 = \frac{1}{n} \sum f_{ai} \cdot (C_i - \bar{x})^2")
        mu = sum(gd.ci[i] * gd.frequencies[i] for i in range(gd.k)) / n if n > 0 else 0.0
        st.latex(rf"\bar{{x}} = {format_number(mu)}")
        total = 0.0
        for i in range(gd.k):
            fai = gd.frequencies[i]
            ci = gd.ci[i]
            diff = ci - mu
            val = diff ** 2 * fai
            total += val
            st.latex(
                rf"f_{{a{i+1}}} \cdot (C_{{{i+1}}} - \bar{{x}})^2 = {fai} \cdot ({format_number(ci)} - {format_number(mu)})^2 = "
                rf"{fai} \cdot {format_number(diff**2)} = {format_number(val)}"
            )
        st.latex(rf"\sum f_{{ai}} \cdot (C_i - \bar{{x}})^2 = {format_number(total)}")


def _render_graphs(gd: GroupedData) -> None:
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(
            build_histogram(gd.intervals, gd.frequencies),
            use_container_width=True,
        )
    with col2:
        st.plotly_chart(
            build_ogiva(gd.intervals, gd.frequencies),
            use_container_width=True,
        )
