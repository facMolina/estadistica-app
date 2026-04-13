"""Panel de graficos."""

import streamlit as st
from display.graph_builder import build_probability_polygon, build_cdf_plot
from typing import List, Dict, Optional


def render_graphs(table_data: List[Dict], model_name: str, highlight_r: Optional[int] = None):
    """Renderiza los graficos de la distribucion."""
    col1, col2 = st.columns(2)

    with col1:
        fig_prob = build_probability_polygon(
            table_data,
            title=f"Poligono de Probabilidad - {model_name}",
            highlight_r=highlight_r,
        )
        st.plotly_chart(fig_prob, use_container_width=True)

    with col2:
        fig_f = build_cdf_plot(table_data, "F(r)", f"F(r) Acumulada Izquierda - {model_name}")
        st.plotly_chart(fig_f, use_container_width=True)

    fig_g = build_cdf_plot(table_data, "G(r)", f"G(r) Acumulada Derecha - {model_name}")
    st.plotly_chart(fig_g, use_container_width=True)
