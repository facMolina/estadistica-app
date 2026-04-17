"""Renderiza la pestaña de Aproximaciones (Sprint 7).

Usa `approximations.approximator.try_approximations()` para obtener todas las
aproximaciones aplicables al modelo + consulta actual y muestra, para cada una:

- Título "Origen → Destino"
- Condición evaluada (✓ si se cumple, ✗ si no, con recordatorio igual se renderiza)
- Parámetros del modelo destino
- Resultado aproximado vs valor exacto + error absoluto
- Paso a paso completo del cálculo (respetando detail_level)
"""

from __future__ import annotations

import streamlit as st

from approximations.approximator import try_approximations, ApproximationResult
from calculation.statistics_common import format_number
from ui.components.step_display import render_calc_result


def render_approximations_tab(
    model_name: str,
    params: dict,
    query_type: str,
    query_params: dict,
    detail_level: int,
):
    """Entrada principal — pensar para llamar desde cada tab 'Aproximaciones'."""
    results = try_approximations(model_name, params, query_type, query_params)

    if not results:
        st.info(
            "No hay aproximaciones aplicables para esta distribución + tipo de consulta.\n\n"
            "Aproximaciones disponibles actualmente:\n"
            "- Hipergeométrico → Binomial (n/N ≤ 0.01)\n"
            "- Binomial → Normal (np ≥ 10 y n(1−p) ≥ 10, con corrección ±0.5)\n"
            "- Binomial → Poisson (p ≤ 0.005)\n"
            "- Poisson → Normal (m ≥ 15, con corrección ±0.5)\n"
            "- Gamma → Normal (Wilson-Hilferty)"
        )
        return

    for i, r in enumerate(results):
        _render_single(r, detail_level, key_suffix=str(i))
        st.markdown("---")


def _render_single(r: ApproximationResult, detail_level: int, key_suffix: str = ""):
    # Header
    icon = "✅" if r.condition_met else "⚠️"
    st.subheader(f"{icon}  {r.from_model} → {r.to_model}")

    # Condición
    cond_color = "green" if r.condition_met else "orange"
    cond_txt = "cumple" if r.condition_met else "no cumple (la aproximación puede tener error alto)"
    st.markdown(
        f"**Condición:** :{cond_color}[{r.condition_str}] — {cond_txt}"
    )

    # Parámetros destino
    st.markdown(f"**Parámetros del modelo aproximado:** {r.target_params_str}")

    # Valor aproximado vs exacto (métricas)
    cols = st.columns(3)
    with cols[0]:
        if r.approx_value is not None:
            st.metric("Valor aproximado", format_number(r.approx_value))
    with cols[1]:
        if r.exact_value is not None:
            st.metric("Valor exacto", format_number(r.exact_value))
    with cols[2]:
        if r.abs_error is not None:
            rel = r.rel_error_pct
            rel_str = f"{rel:.3f}%" if rel is not None else "—"
            st.metric("Error absoluto", format_number(r.abs_error), delta=rel_str)

    # Paso a paso
    with st.expander("Paso a paso", expanded=False):
        render_calc_result(r.calc_result, detail_level)
