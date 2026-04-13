"""Renderizado de pasos de calculo en Streamlit."""

import streamlit as st
from calculation.step_types import Step, CalcResult
from display.latex_renderer import render_step_latex
from typing import List


def render_calc_result(result: CalcResult, detail_level: int):
    """Renderiza un CalcResult completo segun el nivel de detalle."""
    steps = result.get_steps_for_level(detail_level)
    _render_steps(steps, depth=0)

    if result.final_value is not None and result.final_latex:
        st.success(f"**Resultado:** ${result.final_latex}$")


def _render_steps(steps: List[Step], depth: int):
    """Renderiza steps recursivamente con indentacion."""
    for i, step in enumerate(steps):
        prefix = "  " * depth
        latex = render_step_latex(step)

        if step.sub_steps:
            with st.expander(f"{prefix}Paso {i+1}: {step.description}", expanded=(depth == 0)):
                if latex:
                    st.latex(latex)
                _render_steps(step.sub_steps, depth + 1)
        else:
            if latex:
                st.markdown(f"{prefix}**Paso {i+1}:** {step.description}")
                st.latex(latex)
            else:
                st.markdown(f"{prefix}**{step.description}**")
