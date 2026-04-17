"""
UI para Teoria de la Probabilidad — Tema II (Sprint 3).

Dos sub-modos:
  1. Probabilidad de eventos: P(A∪B), P(A|B), complemento, independencia
  2. Bayes / Probabilidad Total: n hipotesis con tabla completa

Funciones publicas:
  render_probability_sidebar() -> dict
  render_probability_main(config, detail_level)
"""

import io
from typing import Optional, Dict, Any, List

import pandas as pd
import streamlit as st

from probability.basic import (
    calc_intersection,
    calc_union,
    calc_complement,
    calc_conditional,
    check_independence,
    solve_two_events,
)
from probability.bayes import BayesCalc
from ui.components.step_display import render_calc_result
from calculation.statistics_common import format_number


# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

_SUBMODES = [
    "Probabilidad de eventos",
    "Bayes / Probabilidad Total",
]

# Opciones para el multiselect de datos conocidos
_KNOWN_OPTIONS = [
    "P(A)",
    "P(B)",
    "P(A∩B)",
    "P(A∪B)",
    "P(A'∩B') — ninguno",
    "P(A|B)",
    "P(B|A)",
]

_REL_OPTIONS = [
    "Sin restricción",
    "Independientes  [P(A∩B) = P(A)·P(B)]",
    "Mutuamente excluyentes  [P(A∩B) = 0]",
]

_REL_MAP = {
    "Sin restricción": None,
    "Independientes  [P(A∩B) = P(A)·P(B)]": "independent",
    "Mutuamente excluyentes  [P(A∩B) = 0]": "mutually_exclusive",
}

_SAMPLE_BAYES = pd.DataFrame({
    "Hipotesis": ["Proveedor A", "Proveedor B", "Proveedor C"],
    "P(Hi)":     [0.20,          0.35,          0.45        ],
    "P(E|Hi)":   [0.10,          0.05,          0.02        ],
})


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

def render_probability_sidebar() -> Dict[str, Any]:
    """
    Renderiza sidebar para el modo Probabilidad.
    Retorna dict con claves: submode, params.
    """
    submode = st.selectbox("Tipo de calculo", _SUBMODES, key="prob_submode")
    st.markdown("---")

    params: Dict[str, Any] = {"submode": submode}

    if submode == "Probabilidad de eventos":
        params.update(_sidebar_two_events())
    else:
        params.update(_sidebar_bayes())

    return params


def _sidebar_two_events() -> Dict[str, Any]:
    st.subheader("Eventos")
    c1, c2 = st.columns(2)
    with c1:
        name_A = st.text_input("Nombre de A", value="A", key="prob_nameA")
    with c2:
        name_B = st.text_input("Nombre de B", value="B", key="prob_nameB")

    st.subheader("Datos conocidos")

    known_sel = st.multiselect(
        "Seleccioná los datos que conocés",
        _KNOWN_OPTIONS,
        default=["P(A)", "P(B)", "P(A∩B)"],
        key="prob_known_sel",
    )

    # Inputs para cada dato seleccionado
    knowns: Dict[str, float] = {}

    if "P(A)" in known_sel:
        knowns["pA"] = st.number_input(
            f"P({name_A})", min_value=0.0, max_value=1.0,
            value=0.40, step=0.01, format="%.4f", key="prob_pA")
    if "P(B)" in known_sel:
        knowns["pB"] = st.number_input(
            f"P({name_B})", min_value=0.0, max_value=1.0,
            value=0.60, step=0.01, format="%.4f", key="prob_pB")
    if "P(A∩B)" in known_sel:
        knowns["pAB"] = st.number_input(
            f"P({name_A}∩{name_B})", min_value=0.0, max_value=1.0,
            value=0.20, step=0.01, format="%.4f", key="prob_pAB")
    if "P(A∪B)" in known_sel:
        knowns["pAuB"] = st.number_input(
            f"P({name_A}∪{name_B})", min_value=0.0, max_value=1.0,
            value=0.80, step=0.01, format="%.4f", key="prob_pAuB")
    if "P(A'∩B') — ninguno" in known_sel:
        knowns["pNone"] = st.number_input(
            f"P({name_A}'∩{name_B}') — ninguno", min_value=0.0, max_value=1.0,
            value=0.02, step=0.01, format="%.4f", key="prob_pNone")
    if "P(A|B)" in known_sel:
        knowns["pAgB"] = st.number_input(
            f"P({name_A}|{name_B})", min_value=0.0, max_value=1.0,
            value=0.50, step=0.01, format="%.4f", key="prob_pAgB")
    if "P(B|A)" in known_sel:
        knowns["pBgA"] = st.number_input(
            f"P({name_B}|{name_A})", min_value=0.0, max_value=1.0,
            value=0.50, step=0.01, format="%.4f", key="prob_pBgA")

    st.subheader("Relación entre eventos")
    rel_label = st.radio("", _REL_OPTIONS, key="prob_rel")
    rel = _REL_MAP[rel_label]
    if rel is not None:
        knowns["rel"] = rel

    # Resolver sistema
    solved, derivation_cr = solve_two_events(knowns, name_A, name_B)
    pA = solved.get("pA")
    pB = solved.get("pB")
    pAB = solved.get("pAB")

    # Mostrar resultado de la derivación
    if derivation_cr is not None:
        if pA is not None and pB is not None and pAB is not None:
            st.success(
                f"**Sistema resuelto:** P({name_A})={format_number(pA, 4)}, "
                f"P({name_B})={format_number(pB, 4)}, "
                f"P({name_A}∩{name_B})={format_number(pAB, 4)}"
            )
        else:
            missing = []
            if pA is None: missing.append(f"P({name_A})")
            if pB is None: missing.append(f"P({name_B})")
            if pAB is None: missing.append(f"P({name_A}∩{name_B})")
            st.warning(f"Datos insuficientes. Faltan: {', '.join(missing)}")
    elif pA is None or pB is None or pAB is None:
        missing = []
        if pA is None: missing.append(f"P({name_A})")
        if pB is None: missing.append(f"P({name_B})")
        if pAB is None: missing.append(f"P({name_A}∩{name_B})")
        st.warning(f"Datos insuficientes. Faltan: {', '.join(missing)}")

    # Determinar relationship para las funciones existentes
    relationship = "known"
    if rel == "independent":
        relationship = "independent"
    elif rel == "mutually_exclusive":
        relationship = "mutually_exclusive"

    return {
        "name_A": name_A, "name_B": name_B,
        "pA": pA if pA is not None else 0.0,
        "pB": pB if pB is not None else 0.0,
        "relationship": relationship,
        "pAB_user": pAB if pAB is not None else 0.0,
        "derivation_cr": derivation_cr,
    }


def _sidebar_bayes() -> Dict[str, Any]:
    st.subheader("Evidencia y Hipotesis")

    evidence_label = st.text_input("Nombre del evento evidencia", value="E", key="prob_ev")

    if "bayes_df" not in st.session_state:
        st.session_state["bayes_df"] = _SAMPLE_BAYES.copy()

    if st.button("Cargar ejemplo (3 proveedores)", use_container_width=True, key="bayes_load"):
        st.session_state["bayes_df"] = _SAMPLE_BAYES.copy()
        st.rerun()

    df_edited = st.data_editor(
        st.session_state["bayes_df"],
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "Hipotesis": st.column_config.TextColumn("Hipotesis Hi"),
            "P(Hi)":     st.column_config.NumberColumn("P(Hi)",  min_value=0.0, max_value=1.0,
                                                        format="%.4f"),
            "P(E|Hi)":   st.column_config.NumberColumn("P(E|Hi)", min_value=0.0, max_value=1.0,
                                                        format="%.4f"),
        },
        key="bayes_editor",
    )
    st.session_state["bayes_df"] = df_edited

    # Validar y construir BayesCalc
    bc: Optional[BayesCalc] = None
    error_msg: Optional[str] = None

    try:
        df_clean = df_edited.dropna(subset=["Hipotesis", "P(Hi)", "P(E|Hi)"])
        df_clean = df_clean[df_clean["P(Hi)"] >= 0]
        df_clean = df_clean[df_clean["P(E|Hi)"] >= 0]
        if len(df_clean) < 2:
            error_msg = "Ingresá al menos 2 hipotesis."
        else:
            labels = df_clean["Hipotesis"].astype(str).tolist()
            priors = df_clean["P(Hi)"].astype(float).tolist()
            liks   = df_clean["P(E|Hi)"].astype(float).tolist()
            sum_priors = sum(priors)
            if abs(sum_priors - 1.0) > 0.02:
                st.warning(f"Las probabilidades a priori suman {format_number(sum_priors, 4)} (deberian sumar 1).")
            bc = BayesCalc(labels=labels, priors=priors,
                           likelihoods=liks, evidence_label=evidence_label)
    except Exception as exc:
        error_msg = str(exc)

    if error_msg:
        st.error(error_msg)
    elif bc is not None:
        st.caption(f"P({evidence_label}) = {format_number(bc.prob_evidence(), 4)}")

    return {"evidence_label": evidence_label, "bc": bc}


# ---------------------------------------------------------------------------
# Contenido principal
# ---------------------------------------------------------------------------

def render_probability_main(params: Dict[str, Any], detail_level: int) -> None:
    submode = params.get("submode", "")

    if submode == "Probabilidad de eventos":
        _render_two_events(params, detail_level)
    else:
        _render_bayes(params, detail_level)


# ---------------------------------------------------------------------------
# Sub-modo 1: Dos eventos
# ---------------------------------------------------------------------------

def _render_two_events(params: Dict[str, Any], detail_level: int) -> None:
    name_A = params["name_A"]
    name_B = params["name_B"]
    pA = params["pA"]
    pB = params["pB"]
    relationship = params["relationship"]
    pAB_user = params["pAB_user"]
    derivation_cr = params.get("derivation_cr")

    # Calcular P(A∩B) con paso a paso
    pAB, cr_inter = calc_intersection(pA, pB, relationship, pAB_user, name_A, name_B)

    # Metricas rapidas
    pUnion = pA + pB - pAB
    pAc = 1.0 - pA
    pBc = 1.0 - pB
    pA_given_B = pAB / pB if pB > 1e-15 else float("nan")
    pB_given_A = pAB / pA if pA > 1e-15 else float("nan")

    st.subheader(f"Resultados para A = {name_A}, B = {name_B}")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric(f"P({name_A}∪{name_B})", format_number(pUnion, 4))
    c2.metric(f"P({name_A}∩{name_B})", format_number(pAB, 4))
    c3.metric(f"P({name_A}|{name_B})",
              format_number(pA_given_B, 4) if pB > 1e-15 else "indef.")
    c4.metric(f"P({name_B}|{name_A})",
              format_number(pB_given_A, 4) if pA > 1e-15 else "indef.")

    st.markdown("---")

    # Si hubo derivación del solver, mostrar paso a paso
    if derivation_cr is not None:
        with st.expander("Derivacion del sistema — paso a paso", expanded=True):
            render_calc_result(derivation_cr, detail_level)

    # Paso a paso en expandibles
    with st.expander(f"P({name_A}∩{name_B}) — Interseccion", expanded=(derivation_cr is None)):
        render_calc_result(cr_inter, detail_level)

    with st.expander(f"P({name_A}∪{name_B}) — Union"):
        cr_union = calc_union(pA, pB, pAB, relationship, name_A, name_B)
        render_calc_result(cr_union, detail_level)

    with st.expander(f"P({name_A}ᶜ) — Complemento de {name_A}"):
        render_calc_result(calc_complement(pA, name_A), detail_level)

    with st.expander(f"P({name_B}ᶜ) — Complemento de {name_B}"):
        render_calc_result(calc_complement(pB, name_B), detail_level)

    if pB > 1e-15:
        with st.expander(f"P({name_A}|{name_B}) — Condicional"):
            render_calc_result(calc_conditional(pAB, pB, name_A, name_B), detail_level)

    if pA > 1e-15:
        with st.expander(f"P({name_B}|{name_A}) — Condicional"):
            render_calc_result(calc_conditional(pAB, pA, name_B, name_A), detail_level)

    with st.expander(f"Independencia: {name_A} y {name_B}"):
        render_calc_result(check_independence(pA, pB, pAB, name_A, name_B), detail_level)




# ---------------------------------------------------------------------------
# Sub-modo 2: Bayes
# ---------------------------------------------------------------------------

def _render_bayes(params: Dict[str, Any], detail_level: int) -> None:
    bc: Optional[BayesCalc] = params.get("bc")
    if bc is None:
        st.info("Ingresá las hipotesis y probabilidades en el panel lateral.")
        return

    ev = bc.evidence
    tab_calc, tab_tabla = st.tabs(["Calculo Paso a Paso", "Tabla de Bayes"])

    with tab_calc:
        # Metricas rapidas: posteriors
        posts = bc.posteriors()
        n = len(posts)
        cols = st.columns(min(n, 4))
        for i, (label, post) in enumerate(posts):
            cols[i % 4].metric(
                f"P({label}|{ev})",
                f"{format_number(post * 100, 2)} %",
            )
        cols_extra = st.columns(2)
        cols_extra[0].metric(f"P({ev}) — Prob. total", format_number(bc.prob_evidence(), 6))
        cols_extra[1].metric("Suma posteriors", format_number(sum(p for _, p in posts), 6))

        st.markdown("---")
        st.subheader("Desarrollo completo")
        render_calc_result(bc.solve(), detail_level)

    with tab_tabla:
        _render_bayes_table(bc)


def _render_bayes_table(bc: BayesCalc) -> None:
    rows = bc.full_table()
    df = pd.DataFrame(rows)

    # Formatear columnas flotantes
    ev = bc.evidence
    float_cols = ["P(Hi)", f"P({ev}|Hi)", f"P({ev}|Hi)·P(Hi)", "P(Hi|E)", "P(Hi|E) %"]
    df_display = df.copy()
    for col in float_cols:
        if col in df_display.columns:
            df_display[col] = df_display[col].map(
                lambda v: format_number(v) if isinstance(v, (int, float)) else v
            )

    st.dataframe(df_display, use_container_width=True, hide_index=True)

    # Descarga CSV
    csv_buf = io.StringIO()
    pd.DataFrame(rows).to_csv(csv_buf, index=False)
    st.download_button(
        "Descargar CSV",
        data=csv_buf.getvalue(),
        file_name="bayes_tabla.csv",
        mime="text/csv",
    )
