"""UI para renderizar resoluciones de problemas compuestos."""

import streamlit as st
from ui.components.step_display import render_calc_result
from calculation.statistics_common import format_number


def render_compound_main(solution: dict, detail_level: int) -> None:
    """Renderiza la resolución de un problema compuesto paso a paso."""

    st.subheader(solution["title"])

    if solution.get("description"):
        st.markdown(solution["description"])

    for step in solution["steps"]:
        st.markdown(f"#### Paso {step['num']}: {step['title']}")
        st.markdown(step["description"])
        st.markdown(f"**Notación:** `{step['notation']}`")

        with st.expander("Ver desarrollo paso a paso", expanded=(step["num"] == 1)):
            render_calc_result(step["calc_result"], detail_level)

        st.info(f"**{step['result_label']}** = {format_number(step['result_value'])}")
        st.divider()

    # Probabilidad condicional (Pascal condicional)
    if solution.get("conditional"):
        cond = solution["conditional"]
        query_n = cond["query_n"]
        cond_n = cond["condition_n"]
        p_num = cond["numerator_value"]
        p_den = cond["denominator_value"]

        st.markdown("#### Probabilidad Condicional")
        st.latex(
            rf"P(N > {query_n} \mid N > {cond_n}) = "
            rf"\frac{{P(N > {query_n})}}{{P(N > {cond_n})}} = "
            rf"\frac{{{format_number(p_num)}}}{{{format_number(p_den)}}} = "
            rf"{format_number(solution['final_value'])}"
        )

    st.success(f"**Resultado final = {format_number(solution['final_value'])}**")
