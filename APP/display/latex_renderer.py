"""Renderizado de formulas LaTeX para Streamlit."""

from calculation.step_types import Step, CalcResult
from typing import List


def render_step_latex(step: Step) -> str:
    """Genera el LaTeX completo de un step."""
    parts = []
    if step.latex_formula:
        parts.append(step.latex_formula)
    if step.latex_substituted:
        parts.append(step.latex_substituted)
    if step.latex_result:
        parts.append(step.latex_result)
    return " ".join(parts) if parts else ""
