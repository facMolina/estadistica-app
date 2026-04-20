"""Pestaña 'Cálculos extra' — calculadoras extensibles sobre la distribución actual.

La pestaña se agrega como tab adicional en cada flujo (discreto estándar,
CustomPMF, continuo). ``render_extras_tab`` elige la calculadora aplicable
según la ``family`` del flujo y el modelo instanciado.
"""

from __future__ import annotations

import streamlit as st

from ui.components.extras._registry import EXTRA_CALCULATORS
from ui.components.extras._base import ExtraCalculator

__all__ = ["render_extras_tab", "EXTRA_CALCULATORS", "ExtraCalculator"]


def render_extras_tab(model, model_label: str, family: str, detail_level: int) -> None:
    """Dibuja la pestaña con el selector de calculadora + render."""
    if model is None:
        st.info("Configurá un modelo válido para ver los cálculos extra.")
        return

    apps = [c for c in EXTRA_CALCULATORS if c.applies_to(family, model)]
    if not apps:
        st.info("No hay cálculos extra disponibles para este modelo.")
        return

    if len(apps) == 1:
        apps[0].render(model, model_label, detail_level)
        return

    choice = st.selectbox(
        "Cálculo",
        [c.short_name for c in apps],
        help="Calculadoras adicionales sobre la distribución actual",
        key="extras_calc_choice",
    )
    sel = next(c for c in apps if c.short_name == choice)
    st.caption(sel.description)
    sel.render(model, model_label, detail_level)
