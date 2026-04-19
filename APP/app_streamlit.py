"""Calculadora de Estadistica - Interfaz Web (Streamlit)."""

import sys
import os
import json
import streamlit as st

# Agregar APP al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.discrete.binomial import Binomial
from models.discrete.poisson import Poisson
from models.discrete.pascal import Pascal
from models.discrete.hypergeometric import Hipergeometrico
from models.discrete.hiper_pascal import HiperPascal
from ui.components.detail_selector import render_detail_selector
from ui.components.step_display import render_calc_result
from ui.components.graph_panel import render_graphs
from ui.components.table_panel import render_table
from ui.components.summary_panel import render_summary
from ui.components.data_processing_ui import render_dp_sidebar, render_dp_main
from ui.components.probability_ui import render_probability_sidebar, render_probability_main
from ui.components.continuous_ui import (
    CONTINUOUS_MODELS as _CONT_MODELS,
    render_continuous_sidebar,
    render_continuous_main,
)
from ui.components.compound_ui import render_compound_main
from ui.components.approximations_ui import render_approximations_tab
from ui.components.custom_pmf_ui import (
    render_custom_pmf_sidebar,
    render_custom_pmf_main,
)
from ui.components.multinomial_ui import (
    render_multinomial_sidebar,
    render_multinomial_main,
)
from ui.components.tcl_ui import render_tcl_sidebar, render_tcl_main
from ui.components.theory_ui import render_theory_sidebar, render_theory_main
from calculation.statistics_common import format_number
from config.settings import SESSION_CONFIG_PATH
from interpreter.streamlit_interpreter import interpret_turn, apply_sc_to_session

# --- Config ---
st.set_page_config(
    page_title="Calculadora de Estadistica",
    page_icon="📊",
    layout="wide",
)

st.title("Calculadora de Estadistica General")
st.caption("UADE — Probabilidad y Estadística General")

if st.session_state.get("last_guide_enunciado"):
    _g = st.session_state["last_guide_enunciado"]
    with st.expander(f"Tema {_g['tema']} — Ejercicio {_g['numero']} (de la guía)",
                     expanded=True):
        st.markdown(_g["text"])
        if _g.get("resp"):
            st.caption(f"Respuesta esperada: {_g['resp']}")

# --- Leer session_config escrito por la CLI (una sola vez por sesion) ---
if "session_config_loaded" not in st.session_state:
    if os.path.exists(SESSION_CONFIG_PATH):
        with open(SESSION_CONFIG_PATH, encoding="utf-8") as _f:
            st.session_state["sc"] = json.load(_f)
        os.remove(SESSION_CONFIG_PATH)
        st.session_state["sc_is_new"] = True
    else:
        st.session_state["sc"] = None
        st.session_state["sc_is_new"] = False
    st.session_state["session_config_loaded"] = True

sc = st.session_state.get("sc")
sc_is_new = st.session_state.get("sc_is_new", False)

# --- Init session_state del intérprete NL ---
if "nl_state" not in st.session_state:
    st.session_state.update({
        "nl_state": "idle",
        "nl_messages": [],
        "nl_follow_up_question": "",
        "nl_partial": None,
        "nl_error": None,
    })

# --- Aplicar cambio de modo pendiente (antes de crear el radio widget) ---
if "_pending_mode" in st.session_state:
    st.session_state["app_mode"] = st.session_state.pop("_pending_mode")

if sc_is_new:
    st.info(f"Problema cargado: {sc.get('interpretation', '')}")
    st.session_state["sc_is_new"] = False

# --- Modelos disponibles ---
_MODELS = ["Binomial", "Poisson", "Pascal", "Hipergeometrico", "Hiper-Pascal",
           "Multinomial", "CustomPMF"]  # discretos
_DISCRETE_MODELS = _MODELS  # alias
_MULTIVARIATE_DISCRETE = {"Multinomial"}
# Modelos discretos con sidebar/main propios (no comparten el shape n,p,m,…).
_NONSTANDARD_DISCRETE = {"Multinomial", "CustomPMF"}

# Variable de consulta segun modelo (r o n)
_MODEL_VAR = {
    "Binomial": "r", "Poisson": "r",
    "Pascal": "n", "Hipergeometrico": "r", "Hiper-Pascal": "n",
}


def _query_labels(var: str) -> list[str]:
    return [
        f"P({var} = valor)",
        f"F({var}) = P(VA <= valor)",
        f"G({var}) = P(VA >= valor)",
        f"P(A <= {var} <= B)",
        "Analisis completo",
    ]


_QUERY_TYPE_TO_KEY = {
    "probability": 0, "cdf_left": 1, "cdf_right": 2,
    "range": 3, "full_analysis": 4,
}

# --- Defaults desde session_config ---
_sc_model   = sc.get("model", "Binomial") if sc else "Binomial"
_sc_is_cont = _sc_model in _CONT_MODELS
if not _sc_is_cont and _sc_model not in _MODELS:
    _sc_model = "Binomial"
_sc_qt_idx  = _QUERY_TYPE_TO_KEY.get(sc.get("query_type", "full_analysis"), 4) if sc else 0
_sc_qp      = sc.get("query_params", {}) if sc else {}
_sc_params  = sc.get("params", {}) if sc else {}

# Params por modelo
_sc_n       = int(_sc_params.get("n", 10))
_sc_p       = float(_sc_params.get("p", 0.30))
_sc_m       = float(_sc_params.get("m", 5.0))
_sc_r_pa    = int(_sc_params.get("r", 3))     # Pascal / HiperPascal: exitos buscados
_sc_N       = int(_sc_params.get("N", 20))
_sc_R       = int(_sc_params.get("R", 8))
_sc_n_hiper = int(_sc_params.get("n", 5))     # Hipergeometrico: muestra

# Query value — defensivo: si vienen como lista (Multinomial, CustomPMF) o tipo
# inesperado, caemos al default entero en lugar de crashear el módulo.
def _as_int(v, default: int) -> int:
    try:
        if isinstance(v, (list, tuple, dict, set)):
            return default
        return int(v)
    except (TypeError, ValueError):
        return default

_sc_r_val   = _as_int(_sc_qp.get("r"), 3)
_sc_a_val   = _as_int(_sc_qp.get("a"), 2)
_sc_b_val   = _as_int(_sc_qp.get("b"), 5)

# --- Continuous sidebar config (populated inside sidebar block) ---
cont_cfg = None
multi_cfg = None  # Multinomial config (populated inside sidebar)
custom_pmf_cfg = None  # CustomPMF config (populated inside sidebar)
detail_level = 2  # default; overwritten in sidebar

# --- Sidebar ---
with st.sidebar:

    # ---- Selector de modo (tope del sidebar) ----
    app_mode = st.radio(
        "Modo",
        ["Modelos de Probabilidad", "Datos Agrupados", "Probabilidad",
         "TCL / Suma de VA", "Consultas Teóricas"],
        horizontal=True,
        key="app_mode",
    )
    st.divider()

    # --- Intérprete de lenguaje natural (todos los modos) ---
    with st.expander("Interpretar problema",
                     expanded=st.session_state["nl_state"] == "follow_up"):

        if st.session_state["nl_error"]:
            st.error(st.session_state["nl_error"])
            st.session_state["nl_error"] = None

        for _msg in st.session_state.get("nl_messages", []):
            if (_msg.get("role") == "assistant"
                    and not _msg.get("content", "").startswith("__partial__")):
                st.info(_msg["content"])

        if st.session_state["nl_state"] == "follow_up":
            st.warning(st.session_state["nl_follow_up_question"])

        placeholder = (
            "Respondé la pregunta de arriba..."
            if st.session_state["nl_state"] == "follow_up"
            else "Describí el problema: modelo, datos agrupados, Bayes, etc."
        )
        user_input = st.text_area(
            "Descripción del problema",
            placeholder=placeholder,
            key="nl_input",
            label_visibility="collapsed",
            height=80,
        )

        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button("Interpretar", use_container_width=True, type="primary"):
                if user_input.strip():
                    with st.spinner("Interpretando..."):
                        result = interpret_turn(
                            st.session_state["nl_messages"], user_input.strip()
                        )
                    if result["action"] == "complete":
                        apply_sc_to_session(result["sc"], st.session_state)
                        st.session_state["sc"] = result["sc"]
                        st.session_state["sc_is_new"] = True
                        st.session_state["nl_state"] = "idle"
                        if result.get("enunciado_from_guide"):
                            st.session_state["last_guide_enunciado"] = {
                                "tema": result["tema"],
                                "numero": result["numero"],
                                "text": result["enunciado_text"],
                                "resp": result.get("expected_resp", ""),
                            }
                        else:
                            st.session_state.pop("last_guide_enunciado", None)
                        st.session_state["nl_messages"] = []
                        st.rerun()
                    elif result["action"] == "follow_up":
                        st.session_state["nl_state"] = "follow_up"
                        st.session_state["nl_follow_up_question"] = result["question"]
                        st.session_state["nl_partial"] = result["partial"]
                        st.session_state["nl_messages"] = result["messages"]
                        if "nl_input_prefill" in result:
                            st.session_state["nl_input"] = result["nl_input_prefill"]
                        st.rerun()
                    else:
                        st.session_state["nl_error"] = result["message"]
                        st.session_state["nl_messages"] = result["messages"]
                        if "nl_input_prefill" in result:
                            st.session_state["nl_input"] = result["nl_input_prefill"]
                        st.rerun()
        with col2:
            if st.session_state["nl_state"] == "follow_up":
                if st.button("Cancelar", use_container_width=True):
                    st.session_state.update({
                        "nl_state": "idle",
                        "nl_messages": [],
                        "nl_follow_up_question": "",
                        "nl_partial": None,
                    })
                    st.rerun()

    st.divider()

    # ================================================================
    # MODO: Modelos de Probabilidad
    # ================================================================
    if app_mode == "Modelos de Probabilidad":

        st.header("Configuracion")

        model_type = st.radio(
            "Tipo de modelo",
            ["Discreto", "Continuo"],
            horizontal=True,
            index=1 if _sc_is_cont else 0,
        )

        if model_type == "Continuo":
            cont_cfg = render_continuous_sidebar(sc=sc if _sc_is_cont else None)
            modelo = cont_cfg["model_name"]
        else:
            modelo = st.selectbox(
                "Modelo",
                _MODELS,
                index=_MODELS.index(_sc_model) if _sc_model in _MODELS else 0,
            )

        if model_type == "Discreto" and modelo in _MULTIVARIATE_DISCRETE:
            # Flujo multivariado (Multinomial): usa su propio sidebar.
            multi_cfg = render_multinomial_sidebar(
                sc=sc if _sc_model == modelo else None
            )
            st.markdown("---")
            detail_level = render_detail_selector()
            st.markdown("---")
            st.subheader("Fórmula")
            if multi_cfg.get("model") is not None:
                st.latex(multi_cfg["model"].latex_formula())

        elif model_type == "Discreto" and modelo == "CustomPMF":
            # PMF casera: sidebar dedicado con expr + dominio + k_var.
            custom_pmf_cfg = render_custom_pmf_sidebar(
                sc=sc if _sc_model == modelo else None
            )
            st.markdown("---")
            detail_level = render_detail_selector()
            st.markdown("---")
            st.subheader("Fórmula")
            if custom_pmf_cfg.get("model") is not None:
                st.latex(custom_pmf_cfg["model"].latex_formula())

        elif model_type == "Discreto":
            var = _MODEL_VAR[modelo]
            ql = _query_labels(var)

            st.subheader("Parametros")

            # ---- Binomial ----
            if modelo == "Binomial":
                n = st.number_input("n (ensayos)", min_value=1, max_value=1000, value=_sc_n, step=1)
                p = st.number_input("p (prob. exito)", min_value=0.0, max_value=1.0,
                                    value=_sc_p, step=0.01, format="%.4f")

            # ---- Poisson ----
            elif modelo == "Poisson":
                m = st.number_input("m (media = λ·t)", min_value=0.01, max_value=500.0,
                                    value=_sc_m, step=0.5, format="%.4f")

            # ---- Pascal ----
            elif modelo == "Pascal":
                r_pa = st.number_input("r (exitos buscados)", min_value=1, max_value=500,
                                       value=_sc_r_pa, step=1)
                p = st.number_input("p (prob. exito)", min_value=0.001, max_value=1.0,
                                    value=_sc_p, step=0.01, format="%.4f")

            # ---- Hipergeometrico ----
            elif modelo == "Hipergeometrico":
                N_h = st.number_input("N (total del lote)", min_value=1, max_value=10000,
                                      value=_sc_N, step=1)
                R_h = st.number_input("R (favorables en lote)", min_value=0, max_value=int(N_h),
                                      value=min(_sc_R, int(N_h)), step=1)
                n_h = st.number_input("n (tamaño muestra)", min_value=1, max_value=int(N_h),
                                      value=min(_sc_n_hiper, int(N_h)), step=1)

            # ---- Hiper-Pascal ----
            elif modelo == "Hiper-Pascal":
                N_hp = st.number_input("N (total del lote)", min_value=1, max_value=10000,
                                       value=_sc_N, step=1)
                R_hp = st.number_input("R (favorables en lote)", min_value=1, max_value=int(N_hp),
                                       value=min(_sc_R, int(N_hp)), step=1)
                r_hp = st.number_input("r (exitos buscados)", min_value=1, max_value=int(R_hp),
                                       value=min(_sc_r_pa, int(R_hp)), step=1)

            st.markdown("---")
            st.subheader("Consulta")
            query_type_label = st.selectbox("Tipo de consulta", ql, index=min(_sc_qt_idx, len(ql) - 1))
            qt_by_pos = ["probability", "cdf_left", "cdf_right", "range", "full_analysis"]
            query_type = qt_by_pos[ql.index(query_type_label)]

            # Dominio para clampeo
            if modelo == "Binomial":
                _dom_min, _dom_max = 0, int(n)
            elif modelo == "Poisson":
                _dom_min, _dom_max = 0, max(int(m * 4), 20)
            elif modelo == "Pascal":
                _dom_min, _dom_max = int(r_pa), int(r_pa) + 200
            elif modelo == "Hipergeometrico":
                _dom_min = max(0, int(n_h) - (int(N_h) - int(R_h)))
                _dom_max = min(int(n_h), int(R_h))
            elif modelo == "Hiper-Pascal":
                _dom_min, _dom_max = int(r_hp), int(N_hp) - int(R_hp) + int(r_hp)

            if query_type in ("probability", "cdf_left", "cdf_right"):
                r_val = st.number_input(
                    f"Valor de {var}",
                    min_value=_dom_min, max_value=_dom_max,
                    value=max(_dom_min, min(_sc_r_val, _dom_max)),
                    step=1,
                )
            elif query_type == "range":
                col1, col2 = st.columns(2)
                with col1:
                    r_a = st.number_input("A (desde)", min_value=_dom_min, max_value=_dom_max,
                                          value=max(_dom_min, min(_sc_a_val, _dom_max)), step=1)
                with col2:
                    r_b = st.number_input("B (hasta)", min_value=_dom_min, max_value=_dom_max,
                                          value=max(_dom_min, min(_sc_b_val, _dom_max)), step=1)

            st.markdown("---")
            detail_level = render_detail_selector()

            st.markdown("---")
            st.subheader("Formula")
            if modelo == "Binomial":
                st.latex(r"P(r) = \binom{n}{r} \cdot p^r \cdot (1-p)^{n-r}")
            elif modelo == "Poisson":
                st.latex(r"P(r) = \frac{e^{-m} \cdot m^r}{r!}")
            elif modelo == "Pascal":
                st.latex(r"P(n) = \binom{n-1}{r-1} \cdot p^r \cdot (1-p)^{n-r}")
            elif modelo == "Hipergeometrico":
                st.latex(r"P(r) = \frac{\binom{R}{r}\binom{N-R}{n-r}}{\binom{N}{n}}")
            elif modelo == "Hiper-Pascal":
                st.latex(r"P(n) = \frac{r}{n} \cdot \frac{\binom{R}{r}\binom{N-R}{n-r}}{\binom{N}{n}}")

        else:  # Continuo — sidebar already rendered; add detail selector + formula here
            st.markdown("---")
            detail_level = render_detail_selector()
            st.markdown("---")
            st.subheader("Formula")
            if cont_cfg and cont_cfg.get("model"):
                try:
                    st.latex(cont_cfg["model"].latex_formula())
                except Exception:
                    pass

    # ================================================================
    # MODO: Datos Agrupados
    # ================================================================
    elif app_mode == "Datos Agrupados":
        dp_config = render_dp_sidebar()
        st.markdown("---")
        detail_level = render_detail_selector()

    # ================================================================
    # MODO: Probabilidad
    # ================================================================
    elif app_mode == "Probabilidad":
        prob_config = render_probability_sidebar()
        st.markdown("---")
        detail_level = render_detail_selector()

    # ================================================================
    # MODO: TCL / Suma de VA
    # ================================================================
    elif app_mode == "TCL / Suma de VA":
        tcl_config = render_tcl_sidebar(
            sc=sc if (sc and sc.get("mode") == "TCL / Suma de VA") else None
        )
        st.markdown("---")
        detail_level = render_detail_selector()

    # ================================================================
    # MODO: Consultas Teóricas
    # ================================================================
    else:
        render_theory_sidebar()


# ---------------------------------------------------------------------------
# Contenido principal — Problema Compuesto
# ---------------------------------------------------------------------------
if st.session_state.get("compound_solution"):
    render_compound_main(st.session_state["compound_solution"], detail_level)
    if st.button("Cerrar resolución compuesta"):
        st.session_state.pop("compound_solution", None)
        st.rerun()
    st.stop()

# ---------------------------------------------------------------------------
# Contenido principal — Datos Agrupados
# ---------------------------------------------------------------------------
if app_mode == "Datos Agrupados":
    st.subheader("Procesamiento de Datos Agrupados — Tema I")
    render_dp_main(
        dp_config["gd"],
        dp_config["query"],
        dp_config["qparams"],
        detail_level,
    )
    st.stop()

# ---------------------------------------------------------------------------
# Contenido principal — Probabilidad
# ---------------------------------------------------------------------------
if app_mode == "Probabilidad":
    st.subheader("Teoria de la Probabilidad")
    render_probability_main(prob_config, detail_level)
    st.stop()


# ---------------------------------------------------------------------------
# Contenido principal — TCL / Suma de VA
# ---------------------------------------------------------------------------
if app_mode == "TCL / Suma de VA":
    render_tcl_main(tcl_config, detail_level)
    st.stop()


# ---------------------------------------------------------------------------
# Contenido principal — Consultas Teóricas
# ---------------------------------------------------------------------------
if app_mode == "Consultas Teóricas":
    render_theory_main()
    st.stop()


# ---------------------------------------------------------------------------
# Contenido principal — Modelos Continuos
# ---------------------------------------------------------------------------
if app_mode == "Modelos de Probabilidad" and cont_cfg is not None:
    render_continuous_main(cont_cfg, detail_level)
    st.stop()


# ---------------------------------------------------------------------------
# Contenido principal — Multinomial (discreto multivariado)
# ---------------------------------------------------------------------------
if app_mode == "Modelos de Probabilidad" and multi_cfg is not None:
    render_multinomial_main(multi_cfg, detail_level)
    st.stop()


# ---------------------------------------------------------------------------
# Contenido principal — CustomPMF (PMF discreta casera con normalizador k)
# ---------------------------------------------------------------------------
if app_mode == "Modelos de Probabilidad" and custom_pmf_cfg is not None:
    render_custom_pmf_main(custom_pmf_cfg, detail_level)
    st.stop()


# ---------------------------------------------------------------------------
# Instanciar modelo (solo llega aqui en modo Modelos de Probabilidad DISCRETO)
# ---------------------------------------------------------------------------
try:
    if modelo == "Binomial":
        model = Binomial(n=int(n), p=p)
        title_params = f"n={int(n)}, p={p}"
    elif modelo == "Poisson":
        model = Poisson(m=m)
        title_params = f"m={m}"
    elif modelo == "Pascal":
        model = Pascal(r=int(r_pa), p=p)
        title_params = f"r={int(r_pa)}, p={p}"
    elif modelo == "Hipergeometrico":
        model = Hipergeometrico(N=int(N_h), R=int(R_h), n=int(n_h))
        title_params = f"N={int(N_h)}, R={int(R_h)}, n={int(n_h)}"
    elif modelo == "Hiper-Pascal":
        model = HiperPascal(r=int(r_hp), N=int(N_hp), R=int(R_hp))
        title_params = f"r={int(r_hp)}, N={int(N_hp)}, R={int(R_hp)}"
except ValueError as e:
    st.error(f"Parametros invalidos: {e}")
    st.stop()


# ---------------------------------------------------------------------------
# Tabs principales (Modelos de Probabilidad)
# ---------------------------------------------------------------------------
tab_calc, tab_chars, tab_table, tab_graphs, tab_approx = st.tabs([
    "Calculo Paso a Paso", "Caracteristicas", "Tabla de Distribucion", "Graficos", "Aproximaciones",
])


def _dispatch_query(model, query_type, title_params, detail_level):
    """Renderiza el calculo en tab_calc segun query_type."""
    d_min, d_max = model.domain()

    if query_type == "probability":
        st.subheader(f"P({var}={r_val}) — {modelo}({title_params})")
        render_calc_result(model.probability(int(r_val)), detail_level)

    elif query_type == "cdf_left":
        st.subheader(f"F({r_val}) = P(VA ≤ {r_val}) — {modelo}({title_params})")
        render_calc_result(model.cdf_left(int(r_val)), detail_level)

    elif query_type == "cdf_right":
        st.subheader(f"G({r_val}) = P(VA ≥ {r_val}) — {modelo}({title_params})")
        render_calc_result(model.cdf_right(int(r_val)), detail_level)

    elif query_type == "range":
        a, b = int(r_a), int(r_b)
        st.subheader(f"P({a} ≤ {var} ≤ {b}) — {modelo}({title_params})")
        f_b_res = model.cdf_left(b)
        f_a1_res = model.cdf_left(a - 1) if a > d_min else None
        val_a1 = f_a1_res.final_value if f_a1_res else 0.0
        prob_range = f_b_res.final_value - val_a1
        st.latex(rf"P({a} \leq {var} \leq {b}) = F({b}) - F({a-1}) = "
                 rf"{format_number(f_b_res.final_value)} - {format_number(val_a1)} = "
                 rf"{format_number(prob_range)}")
        with st.expander(f"Detalle F({b})"):
            render_calc_result(f_b_res, detail_level)
        if f_a1_res:
            with st.expander(f"Detalle F({a-1})"):
                render_calc_result(f_a1_res, detail_level)
        st.success(f"P({a} ≤ {var} ≤ {b}) = {format_number(prob_range)}")

    elif query_type == "full_analysis":
        st.subheader(f"Probabilidades puntuales — {modelo}({title_params})")
        for rv in range(d_min, d_max + 1):
            pv = model.probability_value(rv)
            if pv > 1e-10:
                with st.expander(f"P({var}={rv}) = {format_number(pv, 6)}"):
                    render_calc_result(model.probability(rv), detail_level)


with tab_calc:
    _dispatch_query(model, query_type, title_params, detail_level)

with tab_chars:
    st.subheader(f"Caracteristicas — {modelo}({title_params})")
    chars = model.all_characteristics()
    render_summary(chars, detail_level)
    st.markdown("---")
    st.subheader("Expectativa Parcial Izquierda H(·)")
    d_min, d_max = model.domain()
    default_h = max(d_min, min(int(model.mean().final_value), d_max))
    r_h = st.number_input(
        f"Valor de {var} para H({var})",
        min_value=d_min, max_value=d_max, value=default_h, step=1, key="h_val",
    )
    render_calc_result(model.partial_expectation_left(int(r_h)), detail_level)

with tab_table:
    st.subheader(f"Tabla de Distribucion — {modelo}({title_params})")
    render_table(model.full_table())

with tab_graphs:
    st.subheader(f"Graficos — {modelo}({title_params})")
    highlight = int(r_val) if query_type in ("probability", "cdf_left", "cdf_right") else None
    render_graphs(model.full_table(), f"{modelo}({title_params})", highlight_r=highlight)


with tab_approx:
    st.subheader(f"Aproximaciones — {modelo}({title_params})")
    # Mapear modelo + inputs actuales a params/query_params para el motor de aproximaciones
    _approx_params: dict = {}
    if modelo == "Binomial":
        _approx_params = {"n": int(n), "p": float(p)}
    elif modelo == "Poisson":
        _approx_params = {"m": float(m)}
    elif modelo == "Hipergeometrico":
        _approx_params = {"N": int(N_h), "R": int(R_h), "n": int(n_h)}
    # Pascal y Hiper-Pascal: sin aproximaciones canónicas implementadas actualmente

    _approx_qp: dict = {}
    if query_type in ("probability", "cdf_left", "cdf_right"):
        _approx_qp = {"r": int(r_val)}
    elif query_type == "range":
        _approx_qp = {"r": int(r_a), "a": int(r_a), "b": int(r_b)}

    if not _approx_params or not _approx_qp:
        st.info(
            "No hay aproximaciones aplicables para esta combinación de modelo y tipo de consulta. "
            "Las aproximaciones requieren una consulta puntual o acumulada (P(r), F(r), G(r), rango)."
        )
    else:
        render_approximations_tab(modelo, _approx_params, query_type, _approx_qp, detail_level)
