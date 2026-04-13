"""Panel de resumen de caracteristicas."""

import streamlit as st
from calculation.step_types import CalcResult
from ui.components.step_display import render_calc_result
from typing import Dict
from calculation.statistics_common import format_number


def render_summary(characteristics: Dict[str, CalcResult], detail_level: int):
    """Renderiza la tabla resumen de caracteristicas con paso a paso expandible."""
    for name, result in characteristics.items():
        value_str = format_number(result.final_value) if result.final_value is not None else "N/D"
        with st.expander(f"**{name}** = {value_str}", expanded=False):
            render_calc_result(result, detail_level)
