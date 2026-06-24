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
from models.continuous import derivations as deriv

_DERIVABLE_MODELS = {
    "Normal", "Log-Normal", "Gamma", "Pareto",
    "Exponencial", "Uniforme", "Gumbel Max", "Gumbel Min",
}

# Llaves de parámetro "directo" por modelo — si sc_params no trae ninguna de
# estas pero sí trae datos crudos (ej. media+varianza), el problema vino con
# datos indirectos (típicamente extraídos por el fallback LLM) y conviene
# arrancar en modo "Desde datos" en vez de "Directo".
_DIRECT_KEYS = {
    "Normal": {"mu", "sigma"},
    "Log-Normal": {"m", "D"},
    "Gamma": {"r", "lam"},
    "Pareto": {"theta", "b"},
    "Exponencial": {"lam"},
    "Uniforme": {"a", "b"},
    "Gumbel Max": {"beta", "theta"},
    "Gumbel Min": {"beta", "theta"},
}


def _sc_suggests_indirect(modelo: str, sc_params: dict) -> bool:
    if not sc_params or modelo not in _DERIVABLE_MODELS:
        return False
    direct = _DIRECT_KEYS.get(modelo, set())
    return not (direct & sc_params.keys())

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
    "E(X | X < a) — Esperanza cond. (cola izq.)",
    "E(X | X > k) — Esperanza cond. (cola der.)",
    "P(μ ≤ X ≤ x(α)) — Rango con borde fractil",
]
_QUERY_KEYS = [
    "density", "cdf_left", "cdf_right", "range", "fractile",
    "cond_left", "cond_right", "range_mu_fractile",
]
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


def _title_params(modelo: str, params: dict) -> str:
    """Formato de título consistente, sin importar si los params vinieron
    de inputs directos o de una derivación."""
    if modelo == "Normal":
        return f"μ={format_number(params['mu'])}, σ={format_number(params['sigma'])}"
    if modelo == "Log-Normal":
        return f"m={format_number(params['m'])}, D={format_number(params['D'])}"
    if modelo == "Exponencial":
        return f"λ={format_number(params['lam'])}"
    if modelo == "Gamma":
        return f"r={format_number(params['r'])}, λ={format_number(params['lam'])}"
    if modelo == "Weibull":
        return f"β={format_number(params['beta'])}, ω={format_number(params['omega'])}"
    if modelo in ("Gumbel Max", "Gumbel Min"):
        return f"β={format_number(params['beta'])}, θ={format_number(params['theta'])}"
    if modelo == "Pareto":
        return f"θ={format_number(params['theta'])}, b={format_number(params['b'])}"
    if modelo == "Uniforme":
        return f"a={format_number(params['a'])}, b={format_number(params['b'])}"
    return ""


def _render_derivation_inputs(modelo: str, params: dict, sc_params: dict, nonce: int):
    """Inputs de la sub-sección "Desde datos". Llena `params` con las claves
    que espera `_instantiate()` y guarda el CalcResult de la derivación en
    `params["_derivation_result"]`. Devuelve un string de error o None."""
    try:
        if modelo == "Normal":
            combo = st.selectbox(
                "Datos disponibles",
                ["Un percentil (μ conocida)", "Dos percentiles"],
                key=f"cont_dd_norm_combo_{nonce}",
            )
            if combo == "Un percentil (μ conocida)":
                mu = st.number_input("μ (media)", value=float(sc_params.get("mu", 0.0)),
                                      step=1.0, format="%.4f", key=f"cont_dd_norm_mu_{nonce}")
                x0 = st.number_input("x0", value=float(sc_params.get("x0", mu + 10.0)),
                                      step=1.0, format="%.4f", key=f"cont_dd_norm_x0_{nonce}")
                p = st.number_input("p = P(X ≤ x0)", min_value=0.001, max_value=0.999,
                                     value=float(sc_params.get("p", 0.9)),
                                     step=0.01, format="%.4f", key=f"cont_dd_norm_p_{nonce}")
                model_d, res = deriv.normal_from_one_percentile(mu, x0, p)
            else:
                col1, col2 = st.columns(2)
                with col1:
                    x1 = st.number_input("x1", value=float(sc_params.get("x1", 0.0)),
                                          step=1.0, format="%.4f", key=f"cont_dd_norm_x1_{nonce}")
                    p1 = st.number_input("p1", min_value=0.001, max_value=0.999,
                                          value=float(sc_params.get("p1", 0.1)),
                                          step=0.01, format="%.4f", key=f"cont_dd_norm_p1_{nonce}")
                with col2:
                    x2 = st.number_input("x2", value=float(sc_params.get("x2", 1.0)),
                                          step=1.0, format="%.4f", key=f"cont_dd_norm_x2_{nonce}")
                    p2 = st.number_input("p2", min_value=0.001, max_value=0.999,
                                          value=float(sc_params.get("p2", 0.9)),
                                          step=0.01, format="%.4f", key=f"cont_dd_norm_p2_{nonce}")
                model_d, res = deriv.normal_from_two_percentiles(x1, p1, x2, p2)
            params["mu"], params["sigma"] = model_d.mu, model_d.sigma

        elif modelo == "Log-Normal":
            mu_x = st.number_input("μx (media de X)", min_value=0.0001,
                                    value=max(0.0001, float(sc_params.get("mu_x", 100.0))),
                                    step=1.0, format="%.4f", key=f"cont_dd_ln_mu_{nonce}")
            sigma_x = st.number_input("σx (desvío de X > 0)", min_value=0.0001,
                                       value=max(0.0001, float(sc_params.get("sigma_x", 20.0))),
                                       step=1.0, format="%.4f", key=f"cont_dd_ln_sigma_{nonce}")
            model_d, res = deriv.lognormal_from_mean_std_x(mu_x, sigma_x)
            params["m"], params["D"] = model_d.m, model_d.D

        elif modelo == "Gamma":
            mu = st.number_input("μ (media)", min_value=0.0001,
                                  value=max(0.0001, float(sc_params.get("mu", 16.0))),
                                  step=1.0, format="%.4f", key=f"cont_dd_gamma_mu_{nonce}")
            var = st.number_input("V(X) (varianza > 0)", min_value=0.0001,
                                   value=max(0.0001, float(sc_params.get("var", 4.0))),
                                   step=0.5, format="%.4f", key=f"cont_dd_gamma_var_{nonce}")
            model_d, res = deriv.gamma_from_mean_variance(mu, var)
            params["r"], params["lam"] = model_d.r, model_d.lam

        elif modelo == "Pareto":
            mu = st.number_input("μ (media)", min_value=0.0001,
                                  value=max(0.0001, float(sc_params.get("mu", 25.0))),
                                  step=1.0, format="%.4f", key=f"cont_dd_pareto_mu_{nonce}")
            moda = st.number_input("Mo (moda = θ, mínimo del dominio > 0)", min_value=0.0001,
                                    value=max(0.0001, float(sc_params.get("moda", 20.0))),
                                    step=1.0, format="%.4f", key=f"cont_dd_pareto_moda_{nonce}")
            model_d, res = deriv.pareto_from_mean_mode(mu, moda)
            params["theta"], params["b"] = model_d.theta, model_d.b

        elif modelo == "Exponencial":
            combo = st.selectbox("Datos disponibles", ["Media", "Tasa (cantidad / período)"],
                                  key=f"cont_dd_exp_combo_{nonce}")
            if combo == "Media":
                mu = st.number_input("μ (media)", min_value=0.0001,
                                      value=max(0.0001, float(sc_params.get("mu", 10.0))),
                                      step=1.0, format="%.4f", key=f"cont_dd_exp_mu_{nonce}")
                model_d, res = deriv.exponencial_from_mean(mu)
            else:
                cantidad = st.number_input("Cantidad de eventos", min_value=0.0001,
                                            value=max(0.0001, float(sc_params.get("cantidad", 1.0))),
                                            step=1.0, format="%.4f", key=f"cont_dd_exp_cant_{nonce}")
                periodo = st.number_input("Período (mismas unidades que x)", min_value=0.0001,
                                           value=max(0.0001, float(sc_params.get("periodo", 36.0))),
                                           step=1.0, format="%.4f", key=f"cont_dd_exp_per_{nonce}")
                model_d, res = deriv.exponencial_from_rate(cantidad, periodo)
            params["lam"] = model_d.lam

        elif modelo == "Uniforme":
            mu = st.number_input("μ (media)", value=float(sc_params.get("mu", 10.0)),
                                  step=1.0, format="%.4f", key=f"cont_dd_unif_mu_{nonce}")
            rango = st.number_input("Rango (b − a > 0)", min_value=0.0001,
                                     value=max(0.0001, float(sc_params.get("rango", 6.0))),
                                     step=1.0, format="%.4f", key=f"cont_dd_unif_rango_{nonce}")
            model_d, res = deriv.uniforme_from_mean_range(mu, rango)
            params["a"], params["b"] = model_d.a, model_d.b

        elif modelo in ("Gumbel Max", "Gumbel Min"):
            mu = st.number_input("μ (media)", value=float(sc_params.get("mu", 50.0)),
                                  step=1.0, format="%.4f", key=f"cont_dd_gumbel_mu_{nonce}")
            var = st.number_input("V(X) (varianza > 0)", min_value=0.0001,
                                   value=max(0.0001, float(sc_params.get("var", 100.0))),
                                   step=1.0, format="%.4f", key=f"cont_dd_gumbel_var_{nonce}")
            if modelo == "Gumbel Max":
                model_d, res = deriv.gumbel_max_from_mean_var(mu, var)
            else:
                model_d, res = deriv.gumbel_min_from_mean_var(mu, var)
            params["beta"], params["theta"] = model_d.beta, model_d.theta

        else:
            return f"Derivación desde datos no implementada para {modelo}."

        params["_derivation_result"] = res
        return None
    except Exception as exc:
        return str(exc)


# ---------------------------------------------------------------------------
# Sidebar renderer
# ---------------------------------------------------------------------------

def render_continuous_sidebar(sc=None, sc_is_new=False):
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
    # Todos los widgets de este sidebar usan key="cont_*_{nonce}" explícito.
    # Streamlit solo respeta value=/index= en el primer mount de cada key; en
    # reruns siguientes con la MISMA key ignora el nuevo default aunque el
    # valor en sesión haya cambiado (el navegador no re-sincroniza el texto
    # mostrado). Por eso versionamos la key con un nonce que se incrementa
    # cada vez que llega un problema nuevo por NL: eso fuerza un remount real
    # del widget en el navegador. Bug real encontrado en vivo el 2026-06-23
    # (borrar solo session_state[key] no alcanzaba — el cálculo ya usaba el
    # valor nuevo pero el campo seguía mostrando el del problema anterior).
    if sc and sc_is_new:
        st.session_state["cont_nonce"] = st.session_state.get("cont_nonce", 0) + 1
    nonce = st.session_state.get("cont_nonce", 0)

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
        key=f"cont_modelo_{nonce}",
    )

    if modelo in _DERIVABLE_MODELS:
        input_mode = st.radio(
            "Ingreso de parámetros", ["Directo", "Desde datos"],
            index=1 if _sc_suggests_indirect(modelo, sc_params) else 0,
            horizontal=True, key=f"cont_input_mode_{nonce}",
        )
    else:
        input_mode = "Directo"

    st.subheader("Parámetros")
    params = {}
    derivation_result = None
    deriv_error = None

    title_params = "—"
    if input_mode == "Desde datos":
        deriv_error = _render_derivation_inputs(modelo, params, sc_params, nonce)
        if deriv_error is None:
            derivation_result = params.pop("_derivation_result")
            title_params = _title_params(modelo, params)

    elif modelo == "Normal":
        params["mu"]    = st.number_input("μ (media)",
                                           value=float(sc_params.get("mu", 0.0)),
                                           step=1.0, format="%.4f", key=f"cont_mu_{nonce}")
        params["sigma"] = st.number_input("σ (desvío > 0)", min_value=0.0001,
                                           value=max(0.0001, float(sc_params.get("sigma", 1.0))),
                                           step=0.5, format="%.4f", key=f"cont_sigma_{nonce}")
        title_params = f"μ={format_number(params['mu'])}, σ={format_number(params['sigma'])}"

    elif modelo == "Log-Normal":
        params["m"] = st.number_input("m (log-media)",
                                       value=float(sc_params.get("m", 0.0)),
                                       step=0.5, format="%.4f", key=f"cont_m_{nonce}")
        params["D"] = st.number_input("D (log-desvío > 0)", min_value=0.0001,
                                       value=max(0.0001, float(sc_params.get("D", 1.0))),
                                       step=0.1, format="%.4f", key=f"cont_D_{nonce}")
        title_params = f"m={format_number(params['m'])}, D={format_number(params['D'])}"

    elif modelo == "Exponencial":
        params["lam"] = st.number_input("λ (tasa > 0)", min_value=0.0001,
                                         value=max(0.0001, float(sc_params.get("lam", 1.0))),
                                         step=0.1, format="%.4f", key=f"cont_lam_{nonce}")
        title_params = f"λ={format_number(params['lam'])}"

    elif modelo == "Gamma":
        params["r"]   = st.number_input("r (forma > 0)", min_value=0.0001,
                                         value=max(0.0001, float(sc_params.get("r", 2.0))),
                                         step=0.5, format="%.4f", key=f"cont_r_{nonce}")
        params["lam"] = st.number_input("λ (tasa > 0)", min_value=0.0001,
                                         value=max(0.0001, float(sc_params.get("lam", 1.0))),
                                         step=0.1, format="%.4f", key=f"cont_lam_g_{nonce}")
        title_params = f"r={format_number(params['r'])}, λ={format_number(params['lam'])}"

    elif modelo == "Weibull":
        params["beta"]  = st.number_input("β (escala > 0)", min_value=0.0001,
                                           value=max(0.0001, float(sc_params.get("beta", 1.0))),
                                           step=0.5, format="%.4f", key=f"cont_beta_w_{nonce}")
        params["omega"] = st.number_input("ω (forma > 0)", min_value=0.0001,
                                           value=max(0.0001, float(sc_params.get("omega", 2.0))),
                                           step=0.5, format="%.4f", key=f"cont_omega_{nonce}")
        title_params = f"β={format_number(params['beta'])}, ω={format_number(params['omega'])}"

    elif modelo in ("Gumbel Max", "Gumbel Min"):
        params["beta"]  = st.number_input("β (escala > 0)", min_value=0.0001,
                                           value=max(0.0001, float(sc_params.get("beta", 1.0))),
                                           step=0.5, format="%.4f", key=f"cont_beta_g_{nonce}")
        params["theta"] = st.number_input("θ (ubicación / moda)",
                                           value=float(sc_params.get("theta", 0.0)),
                                           step=1.0, format="%.4f", key=f"cont_theta_g_{nonce}")
        title_params = f"β={format_number(params['beta'])}, θ={format_number(params['theta'])}"

    elif modelo == "Pareto":
        params["theta"] = st.number_input("θ (mínimo > 0)", min_value=0.0001,
                                           value=max(0.0001, float(sc_params.get("theta", 1.0))),
                                           step=0.5, format="%.4f", key=f"cont_theta_p_{nonce}")
        params["b"]     = st.number_input("b (forma > 0)", min_value=0.0001,
                                           value=max(0.0001, float(sc_params.get("b", 2.0))),
                                           step=0.5, format="%.4f", key=f"cont_b_{nonce}")
        title_params = f"θ={format_number(params['theta'])}, b={format_number(params['b'])}"

    elif modelo == "Uniforme":
        params["a"] = st.number_input("a (límite inferior)",
                                       value=float(sc_params.get("a", 0.0)),
                                       step=1.0, format="%.4f", key=f"cont_a_{nonce}")
        params["b"] = st.number_input("b (límite superior > a)",
                                       value=float(sc_params.get("b", 1.0)),
                                       step=1.0, format="%.4f", key=f"cont_b_u_{nonce}")
        title_params = f"a={format_number(params['a'])}, b={format_number(params['b'])}"

    # Build model (may fail for invalid params)
    model, model_error = None, None
    if deriv_error:
        model_error = deriv_error
        lo, hi = _fallback_range(modelo, params)
    else:
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
                             index=qt_idx, key=f"cont_qt_{nonce}")
    query_type = _QUERY_KEYS[_QUERY_LABELS.index(qt_label)]

    finite = not (math.isinf(lo) or math.isinf(hi))
    step   = max(0.001, (hi - lo) / 50) if finite else 0.5
    mid    = (lo + hi) / 2              if finite else 0.0

    qparams: dict = {}
    if query_type in ("density", "cdf_left", "cdf_right"):
        default_x = float(sc_qp.get("x", mid))
        qparams["x"] = st.number_input("x", value=default_x,
                                        step=step, format="%.4f", key=f"cont_x_{nonce}")
    elif query_type == "range":
        qa = float(sc_qp.get("a", lo + (hi - lo) * 0.25 if finite else -1.0))
        qb = float(sc_qp.get("b", lo + (hi - lo) * 0.75 if finite else  1.0))
        col1, col2 = st.columns(2)
        with col1:
            qparams["a"] = st.number_input("a", value=qa,
                                            step=step, format="%.4f", key=f"cont_qa_{nonce}")
        with col2:
            qparams["b"] = st.number_input("b", value=qb,
                                            step=step, format="%.4f", key=f"cont_qb_{nonce}")
    elif query_type == "fractile":
        qparams["alpha"] = st.number_input(
            "α (0 < α < 1)", min_value=0.001, max_value=0.999,
            value=float(sc_qp.get("alpha", 0.5)),
            step=0.01, format="%.4f", key=f"cont_alpha_{nonce}",
        )
    elif query_type in ("cond_left", "cond_right"):
        label = "a (X < a)" if query_type == "cond_left" else "k (X > k)"
        default_x = float(sc_qp.get("x", mid))
        qparams["x"] = st.number_input(label, value=default_x,
                                        step=step, format="%.4f", key=f"cont_x_cond_{nonce}")
    elif query_type == "range_mu_fractile":
        qparams["alpha"] = st.number_input(
            "α (0 < α < 1) — fractil x(α)", min_value=0.001, max_value=0.999,
            value=float(sc_qp.get("alpha", 0.8)),
            step=0.01, format="%.4f", key=f"cont_alpha_rmf_{nonce}",
        )

    return {
        "model":             model,
        "model_name":        modelo,
        "title_params":      title_params,
        "query_type":        query_type,
        "query_params":      qparams,
        "model_error":       model_error,
        "derivation_result": derivation_result,
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
    derivation_result = cfg.get("derivation_result")

    if model_error:
        st.error(f"Parámetros inválidos: {model_error}")
        return

    if derivation_result is not None:
        st.subheader(f"Derivación de parámetros — {modelo}")
        render_calc_result(derivation_result, detail_level)
        st.markdown("---")

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
        elif query_type == "range_mu_fractile":
            try:
                x_a = model.mean().final_value
                x_b = model.fractile(qparams.get("alpha", 0.8)).final_value
            except Exception:
                x_a, x_b = None, None
            graph_qt = "range"
        elif query_type in ("cond_left", "cond_right"):
            x_val = qparams.get("x")
            graph_qt = "cdf_left" if query_type == "cond_left" else "cdf_right"
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

        elif query_type == "cond_left":
            a = qparams["x"]
            st.subheader(f"E(X | X < {format_number(a)}) — {modelo}({title_params})")
            render_calc_result(model.cond_expectation_left(a), detail_level)

        elif query_type == "cond_right":
            k = qparams["x"]
            st.subheader(f"E(X | X > {format_number(k)}) — {modelo}({title_params})")
            render_calc_result(model.cond_expectation_right(k), detail_level)

        elif query_type == "range_mu_fractile":
            alpha = qparams["alpha"]
            mu_res = model.mean()
            mu = mu_res.final_value
            fr_res = model.fractile(alpha)
            b = fr_res.final_value
            lo_b, hi_b = (mu, b) if mu <= b else (b, mu)
            st.subheader(
                f"P(μ ≤ X ≤ x({format_number(alpha)})) — {modelo}({title_params})"
            )
            f_b = model.cdf_left(hi_b)
            f_a = model.cdf_left(lo_b)
            prob = f_b.final_value - f_a.final_value
            st.latex(rf"\mu = {format_number(mu)} \qquad x({format_number(alpha)}) = {format_number(b)}")
            st.latex(
                rf"P(\mu \leq X \leq x({format_number(alpha)})) = "
                rf"F({format_number(hi_b)}) - F({format_number(lo_b)}) = "
                rf"{format_number(f_b.final_value)} - {format_number(f_a.final_value)} = "
                rf"{format_number(prob)}"
            )
            with st.expander("Detalle μ = E(X)"):
                render_calc_result(mu_res, detail_level)
            with st.expander(f"Detalle x({format_number(alpha)})"):
                render_calc_result(fr_res, detail_level)
            with st.expander(f"Detalle F({format_number(hi_b)})"):
                render_calc_result(f_b, detail_level)
            with st.expander(f"Detalle F({format_number(lo_b)})"):
                render_calc_result(f_a, detail_level)
            st.success(
                f"P(μ ≤ X ≤ x({format_number(alpha)})) = {format_number(prob)}"
            )

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
    elif query_type == "range_mu_fractile":
        try:
            a = model.mean().final_value
            b = model.fractile(qparams.get("alpha", 0.8)).final_value
        except Exception:
            return
        approx_qp = {"x": b, "a": a, "b": b}
    else:
        st.info("Wilson-Hilferty está disponible para F(x), G(x) y rangos P(a ≤ X ≤ b).")
        return

    render_approximations_tab(modelo, params, query_type, approx_qp, detail_level)
