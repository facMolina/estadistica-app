"""
Motor de aproximaciones entre distribuciones.

Implementa las 5 aproximaciones canónicas del Tema VI/VII de la guía:
  - Hipergeométrico → Binomial     si n/N ≤ 0.01
  - Binomial       → Normal         si np ≥ 10 y n(1-p) ≥ 10 (corrección ±0.5)
  - Binomial       → Poisson        si p ≤ 0.005
  - Poisson        → Normal         si m ≥ 15 (corrección ±0.5)
  - Gamma          → Normal         Wilson-Hilferty (siempre aplicable, mejor para r grande)

Cada aproximación devuelve un `ApproximationResult` con condición evaluada,
parámetros del modelo destino, valor aproximado, valor exacto (si fue computable),
error absoluto, y un `CalcResult` con el paso a paso completo.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Optional

from calculation.step_types import CalcResult
from calculation.step_engine import StepBuilder
from calculation.statistics_common import format_number


# ---------------------------------------------------------------------------
# Resultado
# ---------------------------------------------------------------------------

@dataclass
class ApproximationResult:
    from_model: str                    # "Binomial"
    to_model: str                      # "Normal"
    condition_met: bool
    condition_str: str                 # "np = 30 ≥ 10 ∧ n(1-p) = 70 ≥ 10  ✓"
    target_params: dict                # {"mu": 30, "sigma": 4.58}
    target_params_str: str             # "μ = np = 30, σ = √(npq) = 4.58"
    approx_value: Optional[float]
    exact_value: Optional[float]
    abs_error: Optional[float]
    calc_result: CalcResult

    @property
    def rel_error_pct(self) -> Optional[float]:
        if self.exact_value is None or self.approx_value is None or self.exact_value == 0:
            return None
        return abs(self.approx_value - self.exact_value) / abs(self.exact_value) * 100


# ---------------------------------------------------------------------------
# Helpers comunes
# ---------------------------------------------------------------------------

def _phi(z: float) -> float:
    """CDF de la Normal estándar Φ(z)."""
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def _query_label(query_type: str, query_params: dict) -> str:
    r = query_params.get("r", query_params.get("x", "?"))
    if query_type == "cdf_left":
        return f"P(X ≤ {r})"
    if query_type == "cdf_right":
        return f"P(X ≥ {r})"
    if query_type == "probability":
        return f"P(X = {r})"
    if query_type == "range":
        a = query_params.get("a", "a")
        b = query_params.get("b", "b")
        return f"P({a} ≤ X ≤ {b})"
    return "consulta"


# ---------------------------------------------------------------------------
# Dispatch
# ---------------------------------------------------------------------------

def try_approximations(
    model_name: str,
    params: dict,
    query_type: str,
    query_params: dict,
) -> list[ApproximationResult]:
    """Retorna todas las aproximaciones aplicables (cumplan o no la condición)."""
    results: list[ApproximationResult] = []

    if model_name == "Hipergeometrico":
        r = _hiper_to_binomial(params, query_type, query_params)
        if r: results.append(r)

    elif model_name == "Binomial":
        r = _binomial_to_normal(params, query_type, query_params)
        if r: results.append(r)
        r = _binomial_to_poisson(params, query_type, query_params)
        if r: results.append(r)

    elif model_name == "Poisson":
        r = _poisson_to_normal(params, query_type, query_params)
        if r: results.append(r)

    elif model_name == "Gamma":
        r = _gamma_to_normal_wh(params, query_type, query_params)
        if r: results.append(r)

    return results


# ---------------------------------------------------------------------------
# Hipergeometrico -> Binomial
# ---------------------------------------------------------------------------

def _hiper_to_binomial(params: dict, query_type: str, query_params: dict) -> Optional[ApproximationResult]:
    N, R, n = params.get("N"), params.get("R"), params.get("n")
    if N is None or R is None or n is None:
        return None
    r_query = query_params.get("r")
    if r_query is None:
        return None

    ratio = n / N
    condition_met = ratio <= 0.01
    condition_str = f"n/N = {n}/{N} = {format_number(ratio)}  {'≤' if condition_met else '>'}  0.01"

    p = R / N
    target_params = {"n": n, "p": p}
    target_params_str = f"n = {n} (mismo), p = R/N = {R}/{N} = {format_number(p)}"

    from models.discrete.hypergeometric import Hipergeometrico
    from models.discrete.binomial import Binomial

    hiper = Hipergeometrico(N=N, R=R, n=n)
    binom = Binomial(n=n, p=p)

    exact = _eval_discrete(hiper, query_type, r_query)
    approx = _eval_discrete(binom, query_type, r_query)

    sb = StepBuilder("Aproximación Hipergeométrico → Binomial")
    sb.add_step(
        "Verificar condición: el tamaño de muestra es pequeño frente al total (n/N ≤ 0.01).",
        latex_sub=f"\\frac{{n}}{{N}} = \\frac{{{n}}}{{{N}}} = {format_number(ratio)}",
        latex_res="\\le 0.01 \\ \\text{{(cumple)}}" if condition_met else "> 0.01 \\ \\text{{(no cumple)}}",
    )
    sb.add_step(
        "Definir parámetros del modelo Binomial aproximado.",
        latex=r"p = \frac{R}{N}, \quad n = n",
        latex_sub=f"p = \\frac{{{R}}}{{{N}}} = {format_number(p)}",
        latex_res=f"\\text{{Binomial}}(n={n},\\ p={format_number(p)})",
    )
    sb.add_step(
        f"Calcular {_query_label(query_type, query_params)} con la Binomial.",
        latex_res=f"{format_number(approx)}",
        result=approx,
        level_min=1,
    )
    if exact is not None:
        sb.add_step(
            f"Valor exacto con Hipergeométrico: {format_number(exact)} | Error absoluto: {format_number(abs(approx - exact))}.",
            level_min=2,
        )

    return ApproximationResult(
        from_model="Hipergeometrico",
        to_model="Binomial",
        condition_met=condition_met,
        condition_str=condition_str,
        target_params=target_params,
        target_params_str=target_params_str,
        approx_value=approx,
        exact_value=exact,
        abs_error=abs(approx - exact) if (approx is not None and exact is not None) else None,
        calc_result=sb.build(final_value=approx, final_latex=f"\\approx {format_number(approx)}"),
    )


# ---------------------------------------------------------------------------
# Binomial -> Normal  (con corrección de continuidad ±0.5)
# ---------------------------------------------------------------------------

def _binomial_to_normal(params: dict, query_type: str, query_params: dict) -> Optional[ApproximationResult]:
    n, p = params.get("n"), params.get("p")
    if n is None or p is None:
        return None
    r = query_params.get("r")
    if r is None:
        return None

    mu = n * p
    var = n * p * (1 - p)
    sigma = math.sqrt(var)

    cond1 = mu >= 10
    cond2 = n * (1 - p) >= 10
    condition_met = cond1 and cond2
    condition_str = (
        f"np = {format_number(mu)} {'≥' if cond1 else '<'} 10  y  "
        f"n(1-p) = {format_number(n*(1-p))} {'≥' if cond2 else '<'} 10"
    )
    target_params = {"mu": mu, "sigma": sigma}
    target_params_str = (
        f"μ = np = {format_number(mu)}, "
        f"σ = √(np(1-p)) = √{format_number(var)} = {format_number(sigma)}"
    )

    approx = _binomial_normal_query(mu, sigma, query_type, r, query_params)
    exact = _eval_discrete_by_name("Binomial", {"n": n, "p": p}, query_type, r)

    sb = StepBuilder("Aproximación Binomial → Normal (con corrección de continuidad)")
    sb.add_step(
        "Verificar condiciones: np ≥ 10 y n(1-p) ≥ 10.",
        latex_sub=(
            f"np = {n}\\cdot{format_number(p)} = {format_number(mu)}\\ "
            f"({'≥' if cond1 else '<'}\\,10),\\quad "
            f"n(1-p) = {n}\\cdot{format_number(1-p)} = {format_number(n*(1-p))}\\ "
            f"({'≥' if cond2 else '<'}\\,10)"
        ),
        latex_res=r"\text{cumple}" if condition_met else r"\text{no cumple}",
    )
    sb.add_step(
        "Definir parámetros de la Normal aproximada.",
        latex=r"\mu = np,\quad \sigma = \sqrt{np(1-p)}",
        latex_sub=f"\\mu = {format_number(mu)},\\ \\sigma = {format_number(sigma)}",
        latex_res=f"\\text{{Normal}}(\\mu={format_number(mu)},\\ \\sigma={format_number(sigma)})",
    )
    _append_normal_query_steps(sb, mu, sigma, query_type, r, query_params, continuity=True)
    if exact is not None:
        sb.add_step(
            f"Valor exacto con Binomial: {format_number(exact)} | "
            f"Error absoluto: {format_number(abs(approx - exact))}.",
            level_min=2,
        )

    return ApproximationResult(
        from_model="Binomial",
        to_model="Normal",
        condition_met=condition_met,
        condition_str=condition_str,
        target_params=target_params,
        target_params_str=target_params_str,
        approx_value=approx,
        exact_value=exact,
        abs_error=abs(approx - exact) if (approx is not None and exact is not None) else None,
        calc_result=sb.build(final_value=approx, final_latex=f"\\approx {format_number(approx)}"),
    )


# ---------------------------------------------------------------------------
# Binomial -> Poisson
# ---------------------------------------------------------------------------

def _binomial_to_poisson(params: dict, query_type: str, query_params: dict) -> Optional[ApproximationResult]:
    n, p = params.get("n"), params.get("p")
    if n is None or p is None:
        return None
    r = query_params.get("r")
    if r is None:
        return None

    m = n * p
    condition_met = p <= 0.005
    condition_str = f"p = {format_number(p)}  {'≤' if condition_met else '>'}  0.005"
    target_params = {"m": m}
    target_params_str = f"m = np = {n}·{format_number(p)} = {format_number(m)}"

    from models.discrete.poisson import Poisson
    poisson = Poisson(m=m)

    approx = _eval_discrete(poisson, query_type, r)
    exact = _eval_discrete_by_name("Binomial", {"n": n, "p": p}, query_type, r)

    sb = StepBuilder("Aproximación Binomial → Poisson")
    sb.add_step(
        "Verificar condición: p muy pequeño (eventos raros).",
        latex_sub=f"p = {format_number(p)}",
        latex_res=(
            f"{'≤' if condition_met else '>'}\\,0.005 \\ "
            f"\\text{{({'cumple' if condition_met else 'no cumple'})}}"
        ),
    )
    sb.add_step(
        "Definir parámetro de la Poisson aproximada.",
        latex=r"m = np",
        latex_sub=f"m = {n}\\cdot{format_number(p)} = {format_number(m)}",
        latex_res=f"\\text{{Poisson}}(m={format_number(m)})",
    )
    sb.add_step(
        f"Calcular {_query_label(query_type, query_params)} con la Poisson.",
        latex_res=f"{format_number(approx)}",
        result=approx,
    )
    if exact is not None:
        sb.add_step(
            f"Valor exacto con Binomial: {format_number(exact)} | "
            f"Error absoluto: {format_number(abs(approx - exact))}.",
            level_min=2,
        )

    return ApproximationResult(
        from_model="Binomial",
        to_model="Poisson",
        condition_met=condition_met,
        condition_str=condition_str,
        target_params=target_params,
        target_params_str=target_params_str,
        approx_value=approx,
        exact_value=exact,
        abs_error=abs(approx - exact) if (approx is not None and exact is not None) else None,
        calc_result=sb.build(final_value=approx, final_latex=f"\\approx {format_number(approx)}"),
    )


# ---------------------------------------------------------------------------
# Poisson -> Normal (corrección ±0.5)
# ---------------------------------------------------------------------------

def _poisson_to_normal(params: dict, query_type: str, query_params: dict) -> Optional[ApproximationResult]:
    m = params.get("m")
    if m is None:
        return None
    r = query_params.get("r")
    if r is None:
        return None

    mu = m
    sigma = math.sqrt(m)
    condition_met = m >= 15
    condition_str = f"m = {format_number(m)}  {'≥' if condition_met else '<'}  15"
    target_params = {"mu": mu, "sigma": sigma}
    target_params_str = f"μ = m = {format_number(mu)},  σ = √m = {format_number(sigma)}"

    approx = _binomial_normal_query(mu, sigma, query_type, r, query_params)
    exact = _eval_discrete_by_name("Poisson", {"m": m}, query_type, r)

    sb = StepBuilder("Aproximación Poisson → Normal (con corrección de continuidad)")
    sb.add_step(
        "Verificar condición: m ≥ 15.",
        latex_sub=f"m = {format_number(m)}",
        latex_res=r"\text{cumple}" if condition_met else r"\text{no cumple}",
    )
    sb.add_step(
        "Definir parámetros de la Normal aproximada.",
        latex=r"\mu = m,\quad \sigma = \sqrt{m}",
        latex_sub=f"\\mu = {format_number(mu)},\\ \\sigma = {format_number(sigma)}",
        latex_res=f"\\text{{Normal}}(\\mu={format_number(mu)},\\ \\sigma={format_number(sigma)})",
    )
    _append_normal_query_steps(sb, mu, sigma, query_type, r, query_params, continuity=True)
    if exact is not None:
        sb.add_step(
            f"Valor exacto con Poisson: {format_number(exact)} | "
            f"Error absoluto: {format_number(abs(approx - exact))}.",
            level_min=2,
        )

    return ApproximationResult(
        from_model="Poisson",
        to_model="Normal",
        condition_met=condition_met,
        condition_str=condition_str,
        target_params=target_params,
        target_params_str=target_params_str,
        approx_value=approx,
        exact_value=exact,
        abs_error=abs(approx - exact) if (approx is not None and exact is not None) else None,
        calc_result=sb.build(final_value=approx, final_latex=f"\\approx {format_number(approx)}"),
    )


# ---------------------------------------------------------------------------
# Gamma -> Normal (Wilson-Hilferty)
# ---------------------------------------------------------------------------
#
#   Si X ~ Gamma(r, lam), entonces  Y = (X*lam/r)^(1/3)  es aproximadamente
#   Normal con  μ_Y = 1 - 1/(9r),  σ_Y² = 1/(9r).
#
#   Por lo tanto:  P(X ≤ x)  ≈  Φ( z )
#       z = [ (x*lam/r)^(1/3) - (1 - 1/(9r)) ] / sqrt(1/(9r))
#         = 3 * sqrt(r) * [ (x*lam/r)^(1/3) - 1 + 1/(9r) ]
#

def _gamma_to_normal_wh(params: dict, query_type: str, query_params: dict) -> Optional[ApproximationResult]:
    r_param = params.get("r")
    lam = params.get("lam") or params.get("lambda")
    if r_param is None or lam is None:
        return None
    x = query_params.get("x", query_params.get("r"))
    if x is None:
        return None

    condition_met = True  # Wilson-Hilferty es universal; mejor a mayor r
    condition_str = f"Wilson-Hilferty aplicable (mejor aproximación a mayor r). r = {format_number(r_param)}"

    def wh_cdf_left(xv):
        inner = (xv * lam / r_param) ** (1.0 / 3.0)
        mu_y = 1.0 - 1.0 / (9.0 * r_param)
        sigma_y = math.sqrt(1.0 / (9.0 * r_param))
        z = (inner - mu_y) / sigma_y
        return _phi(z), z, inner, mu_y, sigma_y

    sb = StepBuilder("Aproximación Gamma → Normal (Wilson-Hilferty)")
    sb.add_step(
        "Transformación Wilson-Hilferty.",
        latex=r"Y = \left(\frac{X\lambda}{r}\right)^{1/3}\ \sim\ \mathcal{N}\!\left(1-\tfrac{1}{9r},\,\tfrac{1}{9r}\right)",
        level_min=1,
    )

    if query_type == "cdf_left":
        approx, z, inner, mu_y, sigma_y = wh_cdf_left(x)
        sb.add_step(
            f"Aplicar la transformación para x = {format_number(x)}.",
            latex=r"y = (x\lambda/r)^{1/3},\quad z = \frac{y - (1 - 1/(9r))}{\sqrt{1/(9r)}}",
            latex_sub=(
                f"y = \\left(\\tfrac{{{format_number(x)}\\cdot{format_number(lam)}}}{{{format_number(r_param)}}}\\right)^{{1/3}} = {format_number(inner)},"
                f"\\quad z = \\frac{{{format_number(inner)} - {format_number(mu_y)}}}{{{format_number(sigma_y)}}} = {format_number(z)}"
            ),
            latex_res=f"z = {format_number(z)}",
        )
        sb.add_step(
            f"P(X ≤ {format_number(x)}) ≈ Φ(z).",
            latex_sub=f"\\Phi({format_number(z)})",
            latex_res=f"{format_number(approx)}",
            result=approx,
        )
    elif query_type == "cdf_right":
        approx_left, z, inner, mu_y, sigma_y = wh_cdf_left(x)
        approx = 1.0 - approx_left
        sb.add_step(
            f"Aplicar la transformación para x = {format_number(x)}.",
            latex_sub=f"z = {format_number(z)}",
            latex_res=f"z = {format_number(z)}",
        )
        sb.add_step(
            f"P(X ≥ {format_number(x)}) ≈ 1 - Φ(z).",
            latex_sub=f"1 - \\Phi({format_number(z)})",
            latex_res=f"{format_number(approx)}",
            result=approx,
        )
    elif query_type == "range":
        a = query_params.get("a", x)
        b = query_params.get("b", x)
        fa, *_ = wh_cdf_left(a)
        fb, *_ = wh_cdf_left(b)
        approx = fb - fa
        sb.add_step(
            f"P({format_number(a)} ≤ X ≤ {format_number(b)}) ≈ Φ(z_b) - Φ(z_a).",
            latex_res=f"{format_number(approx)}",
            result=approx,
        )
    else:
        approx, *_ = wh_cdf_left(x)

    # Exacto con scipy (via modelo Gamma del proyecto)
    exact = _eval_continuous_by_name("Gamma", {"r": r_param, "lam": lam}, query_type, x, query_params)
    if exact is not None:
        sb.add_step(
            f"Valor exacto con Gamma: {format_number(exact)} | "
            f"Error absoluto: {format_number(abs(approx - exact))}.",
            level_min=2,
        )

    target_params = {"mu_y": 1 - 1 / (9 * r_param), "sigma_y_sq": 1 / (9 * r_param)}
    target_params_str = f"μ_Y = 1 - 1/(9r) = {format_number(1-1/(9*r_param))},  σ_Y² = 1/(9r) = {format_number(1/(9*r_param))}"

    return ApproximationResult(
        from_model="Gamma",
        to_model="Normal",
        condition_met=condition_met,
        condition_str=condition_str,
        target_params=target_params,
        target_params_str=target_params_str,
        approx_value=approx,
        exact_value=exact,
        abs_error=abs(approx - exact) if (approx is not None and exact is not None) else None,
        calc_result=sb.build(final_value=approx, final_latex=f"\\approx {format_number(approx)}"),
    )


# ---------------------------------------------------------------------------
# Helpers de cálculo y steps de Normal con corrección
# ---------------------------------------------------------------------------

def _binomial_normal_query(mu, sigma, query_type, r, query_params) -> float:
    """Calcula el valor aproximado usando Normal con corrección de continuidad."""
    if query_type == "cdf_left":            # P(X ≤ r) ≈ Φ((r + 0.5 - μ)/σ)
        z = (r + 0.5 - mu) / sigma
        return _phi(z)
    if query_type == "cdf_right":           # P(X ≥ r) ≈ 1 - Φ((r - 0.5 - μ)/σ)
        z = (r - 0.5 - mu) / sigma
        return 1.0 - _phi(z)
    if query_type == "probability":         # P(X = r) ≈ Φ((r+0.5-μ)/σ) - Φ((r-0.5-μ)/σ)
        z_hi = (r + 0.5 - mu) / sigma
        z_lo = (r - 0.5 - mu) / sigma
        return _phi(z_hi) - _phi(z_lo)
    if query_type == "range":
        a = query_params.get("a", r)
        b = query_params.get("b", r)
        z_hi = (b + 0.5 - mu) / sigma
        z_lo = (a - 0.5 - mu) / sigma
        return _phi(z_hi) - _phi(z_lo)
    return _phi((r - mu) / sigma)


def _append_normal_query_steps(sb: StepBuilder, mu, sigma, query_type, r, query_params, continuity: bool):
    """Agrega al builder los steps del cálculo normal con corrección ±0.5."""
    cc = 0.5 if continuity else 0.0
    if query_type == "cdf_left":
        z = (r + cc - mu) / sigma
        val = _phi(z)
        sb.add_step(
            f"Aplicar corrección de continuidad: P(X ≤ {r}) ≈ P(Y ≤ {r} + 0.5).",
            latex=r"z = \frac{r + 0.5 - \mu}{\sigma}",
            latex_sub=f"z = \\frac{{{r}+0.5 - {format_number(mu)}}}{{{format_number(sigma)}}} = {format_number(z)}",
            latex_res=f"\\Phi({format_number(z)}) = {format_number(val)}",
            result=val,
        )
    elif query_type == "cdf_right":
        z = (r - cc - mu) / sigma
        val = 1.0 - _phi(z)
        sb.add_step(
            f"Aplicar corrección de continuidad: P(X ≥ {r}) ≈ P(Y ≥ {r} - 0.5).",
            latex=r"z = \frac{r - 0.5 - \mu}{\sigma},\quad P = 1 - \Phi(z)",
            latex_sub=f"z = \\frac{{{r}-0.5 - {format_number(mu)}}}{{{format_number(sigma)}}} = {format_number(z)}",
            latex_res=f"1 - \\Phi({format_number(z)}) = {format_number(val)}",
            result=val,
        )
    elif query_type == "probability":
        z_hi = (r + cc - mu) / sigma
        z_lo = (r - cc - mu) / sigma
        val = _phi(z_hi) - _phi(z_lo)
        sb.add_step(
            f"Aplicar corrección de continuidad: P(X = {r}) ≈ P({r}-0.5 ≤ Y ≤ {r}+0.5).",
            latex_sub=f"\\Phi({format_number(z_hi)}) - \\Phi({format_number(z_lo)})",
            latex_res=f"{format_number(val)}",
            result=val,
        )
    elif query_type == "range":
        a = query_params.get("a", r)
        b = query_params.get("b", r)
        z_hi = (b + cc - mu) / sigma
        z_lo = (a - cc - mu) / sigma
        val = _phi(z_hi) - _phi(z_lo)
        sb.add_step(
            f"Corrección de continuidad: P({a} ≤ X ≤ {b}) ≈ P({a}-0.5 ≤ Y ≤ {b}+0.5).",
            latex_sub=f"\\Phi({format_number(z_hi)}) - \\Phi({format_number(z_lo)})",
            latex_res=f"{format_number(val)}",
            result=val,
        )


def _eval_discrete(model, query_type: str, r: int) -> Optional[float]:
    try:
        if query_type == "probability":
            return model.probability(r).final_value
        if query_type == "cdf_left":
            return model.cdf_left(r).final_value
        if query_type == "cdf_right":
            return model.cdf_right(r).final_value
    except Exception:
        return None
    return None


def _eval_discrete_by_name(name: str, params: dict, query_type: str, r: int) -> Optional[float]:
    try:
        if name == "Binomial":
            from models.discrete.binomial import Binomial
            return _eval_discrete(Binomial(n=params["n"], p=params["p"]), query_type, r)
        if name == "Poisson":
            from models.discrete.poisson import Poisson
            return _eval_discrete(Poisson(m=params["m"]), query_type, r)
    except Exception:
        return None
    return None


def _eval_continuous_by_name(name: str, params: dict, query_type: str, x: float, query_params: dict) -> Optional[float]:
    try:
        if name == "Gamma":
            from models.continuous.gamma import Gamma
            g = Gamma(r=params["r"], lam=params["lam"])
            if query_type == "cdf_left":
                return g.cdf_left(x).final_value
            if query_type == "cdf_right":
                return g.cdf_right(x).final_value
            if query_type == "range":
                a, b = query_params["a"], query_params["b"]
                return g.cdf_left(b).final_value - g.cdf_left(a).final_value
    except Exception:
        return None
    return None
