"""UI components for continuous probability distribution models."""

import math
import streamlit as st

from models.continuous.normal import Normal
from models.continuous.lognormal import LogNormal
from models.continuous.exponencial import Exponencial
from models.continuous.gamma import Gamma
from models.continuous.weibull import Weibull
from models.continuous.gumbel import GumbelMax, GumbelMin
from models.continuous.pareto import Pareto
from models.continuous.uniforme import Uniforme
from ui.components.step_display import render_calc_result
from ui.components.summary_panel import render_summary
from ui.components.extras import render_extras_tab
from display.graph_builder import build_density_plot
from calculation.statistics_common import format_number

CONTINUOUS_MODELS = [
    "Normal", "Log-Normal", "Exponencial", "Gamma",
    "Weibull", "Gumbel Max", "Gumbel Min", "Pareto", "Uniforme",
]

_QUERY_LABELS = [
    "f(x) — Densidad puntual",
    "F(x) = P(X ≤ x)",
    "G(x) = P(X ≥ x)",
    "P(a ≤ X ≤ b)",
    "x(α) — Fractil",
]
_QUERY_KEYS = ["density", "cdf_left", "cdf_right", "range", "fractile"]
_QT_TO_IDX  = {k: i for i, k in enumerate(_QUERY_KEYS)}


# ---------------------------------------------------------------------------
# Model factory
# ---------------------------------------------------------------------------

def _instantiate(modelo: str, params: dict):
    if modelo == "Normal":
        return Normal(mu=params["mu"], sigma=params["sigma"])
    if modelo == "Log-Normal":
        return LogNormal(m=params["m"], D=params["D"])
    if modelo == "Exponencial":
        return Exponencial(lam=params["lam"])
    if modelo == "Gamma":
        return Gamma(r=params["r"], lam=params["lam"])
    if modelo == "Weibull":
        return Weibull(beta=params["beta"], omega=params["omega"])
    if modelo == "Gumbel Max":
        return GumbelMax(beta=params["beta"], theta=params["theta"])
    if modelo == "Gumbel Min":
        return GumbelMin(beta=params["beta"], theta=params["theta"])
    if modelo == "Pareto":
        return Pareto(theta=params["theta"], b=params["b"])
    if modelo == "Uniforme":
        return Uniforme(a=params["a"], b=params["b"])
    raise ValueError(f"Modelo continuo desconocido: {modelo}")


def _fallback_range(modelo: str, params: dict):
    """Display range estimate when model can't be built yet."""
    if modelo == "Uniforme":
        a, b = params.get("a", 0.0), params.get("b", 1.0)
        return (a - 0.1*(b-a), b + 0.1*(b-a))
    if modelo == "Exponencial":
        lam = params.get("lam", 1.0)
        return (0.0, 5.0 / max(lam, 1e-6))
    if modelo in ("Normal", "Log-Normal"):
        return (-5.0, 5.0)
    if modelo == "Pareto":
        theta = params.get("theta", 1.0)
        return (theta * 0.9, theta * 10)
    return (0.0, 10.0)


# ---------------------------------------------------------------------------
# Sidebar renderer
# ---------------------------------------------------------------------------

def render_continuous_sidebar(sc=None):
    """
    Renders sidebar controls for a continuous model.

    Returns dict:
      model        — instantiated model object (or None on param error)
      model_name   — string name
      title_params — display string
      query_type   — one of _QUERY_KEYS
      query_params — dict of query inputs (x, a, b, or alpha)
      model_error  — error string if model couldn't be built, else None
    """
    sc_params = sc.get("params", {}) if sc else {}
    sc_qtype  = sc.get("query_type",  "cdf_left") if sc else "cdf_left"
    sc_qp     = sc.get("query_params", {})         if sc else {}
    sc_model  = sc.get("model", "Normal")           if sc else "Normal"
    if sc_model not in CONTINUOUS_MODELS:
        sc_model = "Normal"

    modelo = st.selectbox(
        "Modelo",
        CONTINUOUS_MODELS,
        index=CONTINUOUS_MODELS.index(sc_model),
        key="cont_modelo",
    )

    st.subheader("Parámetros")
    params = {}

    if modelo == "Normal":
        params["mu"]    = st.number_input("μ (media)",
                                           value=float(sc_params.get("mu", 0.0)),
                                           step=1.0, format="%.4f", key="cont_mu")
        params["sigma"] = st.number_input("σ (desvío > 0)", min_value=0.0001,
                                           value=max(0.0001, float(sc_params.get("sigma", 1.0))),
                                           step=0.5, format="%.4f", key="cont_sigma")
        title_params = f"μ={format_number(params['mu'])}, σ={format_number(params['sigma'])}"

    elif modelo == "Log-Normal":
        params["m"] = st.number_input("m (log-media)",
                                       value=float(sc_params.get("m", 0.0)),
                                       step=0.5, format="%.4f", key="cont_m")
        params["D"] = st.number_input("D (log-desvío > 0)", min_value=0.0001,
                                       value=max(0.0001, float(sc_params.get("D", 1.0))),
                                       step=0.1, format="%.4f", key="cont_D")
        title_params = f"m={format_number(params['m'])}, D={format_number(params['D'])}"

    elif modelo == "Exponencial":
        params["lam"] = st.number_input("λ (tasa > 0)", min_value=0.0001,
                                         value=max(0.0001, float(sc_params.get("lam", 1.0))),
                                         step=0.1, format="%.4f", key="cont_lam")
        title_params = f"λ={format_number(params['lam'])}"

    elif modelo == "Gamma":
        params["r"]   = st.number_input("r (forma > 0)", min_value=0.0001,
                                         value=max(0.0001, float(sc_params.get("r", 2.0))),
                                         step=0.5, format="%.4f", key="cont_r")
        params["lam"] = st.number_input("λ (tasa > 0)", min_value=0.0001,
                                         value=max(0.0001, float(sc_params.get("lam", 1.0))),
                                         step=0.1, format="%.4f", key="cont_lam_g")
        title_params = f"r={format_number(params['r'])}, λ={format_number(params['lam'])}"

    elif modelo == "Weibull":
        params["beta"]  = st.number_input("β (escala > 0)", min_value=0.0001,
                                           value=max(0.0001, float(sc_params.get("beta", 1.0))),
                                           step=0.5, format="%.4f", key="cont_beta_w")
        params["omega"] = st.number_input("ω (forma > 0)", min_value=0.0001,
                                           value=max(0.0001, float(sc_params.get("omega", 2.0))),
                                           step=0.5, format="%.4f", key="cont_omega")
        title_params = f"β={format_number(params['beta'])}, ω={format_number(params['omega'])}"

    elif modelo in ("Gumbel Max", "Gumbel Min"):
        params["beta"]  = st.number_input("β (escala > 0)", min_value=0.0001,
                                           value=max(0.0001, float(sc_params.get("beta", 1.0))),
                                           step=0.5, format="%.4f", key="cont_beta_g")
        params["theta"] = st.number_input("θ (ubicación / moda)",
                                           value=float(sc_params.get("theta", 0.0)),
                                           step=1.0, format="%.4f", key="cont_theta_g")
        title_params = f"β={format_number(params['beta'])}, θ={format_number(params['theta'])}"

    elif modelo == "Pareto":
        params["theta"] = st.number_input("θ (mínimo > 0)", min_value=0.0001,
                                           value=max(0.0001, float(sc_params.get("theta", 1.0))),
                                           step=0.5, format="%.4f", key="cont_theta_p")
        params["b"]     = st.number_input("b (forma > 0)", min_value=0.0001,
                                           value=max(0.0001, float(sc_params.get("b", 2.0))),
                                           step=0.5, format="%.4f", key="cont_b")
        title_params = f"θ={format_number(params['theta'])}, b={format_number(params['b'])}"

    elif modelo == "Uniforme":
        params["a"] = st.number_input("a (límite inferior)",
                                       value=float(sc_params.get("a", 0.0)),
                                       step=1.0, format="%.4f", key="cont_a")
        params["b"] = st.number_input("b (límite superior > a)",
                                       value=float(sc_params.get("b", 1.0)),
                                       step=1.0, format="%.4f", key="cont_b_u")
        title_params = f"a={format_number(params['a'])}, b={format_number(params['b'])}"

    # Build model (may fail for invalid params)
    model, model_error = None, None
    try:
        model = _instantiate(modelo, params)
        lo, hi = model.display_domain()
    except Exception as exc:
        model_error = str(exc)
        lo, hi = _fallback_range(modelo, params)

    # ------------------------------------------------------------------
    # Query type
    # ------------------------------------------------------------------
    st.markdown("---")
    st.subheader("Consulta")

    qt_idx = _QT_TO_IDX.get(sc_qtype, 1)
    qt_label = st.selectbox("Tipo de consulta", _QUERY_LABELS,
                             index=qt_idx, key="cont_qt")
    query_type = _QUERY_KEYS[_QUERY_LABELS.index(qt_label)]

    finite = not (math.isinf(lo) or math.isinf(hi))
    step   = max(0.001, (hi - lo) / 50) if finite else 0.5
    mid    = (lo + hi) / 2              if finite else 0.0

    qparams: dict = {}
    if query_type in ("density", "cdf_left", "cdf_right"):
        default_x = float(sc_qp.get("x", mid))
        qparams["x"] = st.number_input("x", value=default_x,
                                        step=step, format="%.4f", key="cont_x")
    elif query_type == "range":
        qa = float(sc_qp.get("a", lo + (hi - lo) * 0.25 if finite else -1.0))
        qb = float(sc_qp.get("b", lo + (hi - lo) * 0.75 if finite else  1.0))
        col1, col2 = st.columns(2)
        with col1:
            qparams["a"] = st.number_input("a", value=qa,
                                            step=step, format="%.4f", key="cont_qa")
        with col2:
            qparams["b"] = st.number_input("b", value=qb,
                                            step=step, format="%.4f", key="cont_qb")
    elif query_type == "fractile":
        qparams["alpha"] = st.number_input(
            "α (0 < α < 1)", min_value=0.001, max_value=0.999,
            value=float(sc_qp.get("alpha", 0.5)),
            step=0.01, format="%.4f", key="cont_alpha",
        )

    return {
        "model":        model,
        "model_name":   modelo,
        "title_params": title_params,
        "query_type":   query_type,
        "query_params": qparams,
        "model_error":  model_error,
    }


# ---------------------------------------------------------------------------
# Main content renderer
# ---------------------------------------------------------------------------

def render_continuous_main(cfg: dict, detail_level: int):
    """Renders the main content area (tabs) for a continuous model."""
    model       = cfg["model"]
    modelo      = cfg["model_name"]
    title_params = cfg["title_params"]
    query_type  = cfg["query_type"]
    qparams     = cfg["query_params"]
    model_error = cfg.get("model_error")

    if model_error:
        st.error(f"Parámetros inválidos: {model_error}")
        return

    tab_calc, tab_chars, tab_graph, tab_approx, tab_extras = st.tabs([
        "Cálculo Paso a Paso", "Características", "Gráfico",
        "Aproximaciones", "Cálculos extra",
    ])

    with tab_calc:
        _dispatch(model, modelo, title_params, query_type, qparams, detail_level)

    with tab_approx:
        _render_approximations(model, modelo, query_type, qparams, detail_level)

    with tab_extras:
        render_extras_tab(model, f"{modelo}({title_params})", "continuous", detail_level)

    with tab_chars:
        st.subheader(f"Características — {modelo}({title_params})")
        try:
            chars = model.all_characteristics()
            render_summary(chars, detail_level)
        except Exception as exc:
            st.error(f"Error al calcular características: {exc}")

    with tab_graph:
        st.subheader(f"Gráfico — {modelo}({title_params})")
        x_val = qparams.get("x")
        x_a   = qparams.get("a")
        x_b   = qparams.get("b")
        # For fractile: mark the result value as x_val on the density curve
        if query_type == "fractile":
            try:
                x_val = model.fractile(qparams.get("alpha", 0.5)).final_value
            except Exception:
                x_val = None
            graph_qt = "density"
        else:
            graph_qt = query_type
        try:
            fig = build_density_plot(
                model, f"{modelo}({title_params})",
                query_type=graph_qt, x_val=x_val, x_a=x_a, x_b=x_b,
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as exc:
            st.error(f"Error al generar gráfico: {exc}")


# ---------------------------------------------------------------------------
# Calculation dispatcher
# ---------------------------------------------------------------------------

def _dispatch(model, modelo, title_params, query_type, qparams, detail_level):
    try:
        if query_type == "density":
            x = qparams["x"]
            st.subheader(f"f({format_number(x)}) — {modelo}({title_params})")
            render_calc_result(model.density(x), detail_level)

        elif query_type == "cdf_left":
            x = qparams["x"]
            st.subheader(
                f"F({format_number(x)}) = P(X ≤ {format_number(x)}) — {modelo}({title_params})"
            )
            render_calc_result(model.cdf_left(x), detail_level)

        elif query_type == "cdf_right":
            x = qparams["x"]
            st.subheader(
                f"G({format_number(x)}) = P(X ≥ {format_number(x)}) — {modelo}({title_params})"
            )
            render_calc_result(model.cdf_right(x), detail_level)

        elif query_type == "range":
            a, b = qparams["a"], qparams["b"]
            if a >= b:
                st.error("El límite inferior a debe ser estrictamente menor que b.")
                return
            st.subheader(
                f"P({format_number(a)} ≤ X ≤ {format_number(b)}) — {modelo}({title_params})"
            )
            f_b = model.cdf_left(b)
            f_a = model.cdf_left(a)
            prob = f_b.final_value - f_a.final_value
            st.latex(
                rf"P({format_number(a)} \leq X \leq {format_number(b)}) = "
                rf"F({format_number(b)}) - F({format_number(a)}) = "
                rf"{format_number(f_b.final_value)} - {format_number(f_a.final_value)} = "
                rf"{format_number(prob)}"
            )
            with st.expander(f"Detalle F({format_number(b)})"):
                render_calc_result(f_b, detail_level)
            with st.expander(f"Detalle F({format_number(a)})"):
                render_calc_result(f_a, detail_level)
            st.success(
                f"P({format_number(a)} ≤ X ≤ {format_number(b)}) = {format_number(prob)}"
            )

        elif query_type == "fractile":
            alpha = qparams["alpha"]
            st.subheader(f"x({format_number(alpha)}) — {modelo}({title_params})")
            render_calc_result(model.fractile(alpha), detail_level)

    except Exception as exc:
        st.error(f"Error en el cálculo: {exc}")


# ---------------------------------------------------------------------------
# Aproximaciones tab (solo Gamma está implementada)
# ---------------------------------------------------------------------------

def _render_approximations(model, modelo: str, query_type: str, qparams: dict, detail_level: int):
    """Renderiza pestaña de aproximaciones para modelos continuos."""
    from ui.components.approximations_ui import render_approximations_tab

    st.subheader(f"Aproximaciones — {modelo}")

    if modelo != "Gamma":
        st.info(
            "Aproximaciones continuas implementadas: Gamma → Normal (Wilson-Hilferty).\n\n"
            "Las demás distribuciones continuas no tienen aproximación canónica estándar."
        )
        return

    params = {"r": model.r, "lam": model.lam}

    # Normalizar query_params al formato del approximator
    approx_qp: dict = {}
    if query_type in ("cdf_left", "cdf_right"):
        x = qparams.get("x")
        if x is None:
            st.info("Seleccioná un tipo de consulta F(x) o G(x) para ver aproximaciones.")
            return
        approx_qp = {"x": x}
    elif query_type == "range":
        a, b = qparams.get("a"), qparams.get("b")
        if a is None or b is None:
            return
        approx_qp = {"x": b, "a": a, "b": b}
    else:
        st.info("Wilson-Hilferty está disponible para F(x), G(x) y rangos P(a ≤ X ≤ b).")
        return

    render_approximations_tab(modelo, params, query_type, approx_qp, detail_level)
