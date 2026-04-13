"""Panel de tabla de distribucion."""

import streamlit as st
from display.table_builder import build_dataframe
from typing import List, Dict


def render_table(table_data: List[Dict]):
    """Renderiza la tabla de distribucion completa."""
    df = build_dataframe(table_data)
    st.dataframe(df, use_container_width=True, height=400)

    csv = df.to_csv(index=False)
    st.download_button(
        label="Descargar tabla como CSV",
        data=csv,
        file_name="distribucion.csv",
        mime="text/csv",
    )
