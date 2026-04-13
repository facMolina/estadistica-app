"""Selector de nivel de detalle."""

import streamlit as st
from config.settings import DETAIL_MAX, DETAIL_INTERMEDIATE, DETAIL_BASIC, DETAIL_LABELS


def render_detail_selector() -> int:
    """Renderiza el dropdown de nivel de detalle y retorna el nivel seleccionado."""
    options = [DETAIL_MAX, DETAIL_INTERMEDIATE, DETAIL_BASIC]
    labels = [DETAIL_LABELS[o] for o in options]

    selected_label = st.selectbox(
        "Nivel de detalle",
        labels,
        index=0,  # Maximo detalle por defecto
    )

    return options[labels.index(selected_label)]
