"""Derivacion de parametros de distribuciones continuas a partir de datos indirectos.

El parcial casi nunca da los parametros finales (mu, sigma, r, lambda, b...)
directamente: da percentiles, media+varianza, media+moda, etc. Cada funcion
de este modulo recibe esos datos "de enunciado" y devuelve
``(instancia_del_modelo, CalcResult)`` con el paso a paso de la derivacion,
para mostrarse como un bloque previo a la consulta que el usuario pidio.
"""

from __future__ import annotations

import math

from calculation.step_engine import StepBuilder
from calculation.statistics_common import format_number
from models.continuous.normal import Normal
from models.continuous.lognormal import LogNormal
from models.continuous.gamma import Gamma
from models.continuous.pareto import Pareto
from models.continuous.exponencial import Exponencial
from models.continuous.uniforme import Uniforme
from models.continuous.gumbel import GumbelMax, GumbelMin
from config.settings import EULER_MASCHERONI as _C


# ===========================================================================
# Normal
# ===========================================================================

def normal_from_one_percentile(mu: float, x0: float, p: float):
    """sigma a partir de un percentil: P(X <= x0) = p  ->  sigma = (x0-mu)/Z(p)."""
    from calculation.normal_table import z_critico
    z_p = z_critico(p)
    if z_p == 0:
        raise ValueError("El percentil no puede ser 0.5 (Z=0): no se puede despejar sigma")
    sigma = (x0 - mu) / z_p
    builder = StepBuilder("Normal — σ desde un percentil")
    builder.add_step(
        desc=f"P(X ≤ {x0}) = {p}  →  Z({p}) = (x0 − μ)/σ  →  σ = (x0 − μ)/Z({p})",
        latex=rf"\sigma = \frac{{x_0 - \mu}}{{Z({p})}}",
        level_min=1,
    )
    builder.add_step(
        desc=f"De tabla Z: Z({p}) = {format_number(z_p)}",
        latex=rf"Z({p}) = {format_number(z_p)}", result=z_p, level_min=2,
    )
    builder.add_step(
        desc=f"σ = ({x0} − {mu}) / {format_number(z_p)} = {format_number(sigma)}",
        latex=rf"\sigma = \frac{{{x0} - {mu}}}{{{format_number(z_p)}}} = {format_number(sigma)}",
        result=sigma, level_min=1,
    )
    if sigma <= 0:
        raise ValueError(f"σ resultó ≤ 0 ({format_number(sigma)}): revisar que x0 y p sean consistentes con μ")
    result = builder.build(final_value=sigma, final_latex=rf"\sigma = {format_number(sigma)}")
    return Normal(mu, sigma), result


def normal_from_two_percentiles(x1: float, p1: float, x2: float, p2: float):
    """mu, sigma a partir de dos percentiles: x_i = mu + Z(p_i)*sigma."""
    from calculation.normal_table import z_critico
    z1, z2 = z_critico(p1), z_critico(p2)
    if abs(z1 - z2) < 1e-9:
        raise ValueError("Los dos percentiles dan el mismo Z: no se puede resolver el sistema")
    sigma = (x1 - x2) / (z1 - z2)
    mu = x1 - z1 * sigma
    builder = StepBuilder("Normal — μ, σ desde dos percentiles")
    builder.add_step(
        desc="x1 = μ + Z(p1)·σ,  x2 = μ + Z(p2)·σ  →  sistema de 2 ecuaciones con 2 incógnitas",
        latex=r"x_1 = \mu + Z(p_1)\sigma, \quad x_2 = \mu + Z(p_2)\sigma",
        level_min=1,
    )
    builder.add_step(
        desc=f"De tabla Z: Z({p1}) = {format_number(z1)}, Z({p2}) = {format_number(z2)}",
        latex=rf"Z({p1})={format_number(z1)},\; Z({p2})={format_number(z2)}",
        level_min=2,
    )
    builder.add_step(
        desc=f"σ = (x1 − x2)/(Z(p1) − Z(p2)) = ({x1} − {x2})/({format_number(z1)} − {format_number(z2)}) = {format_number(sigma)}",
        latex=rf"\sigma = \frac{{{x1}-{x2}}}{{{format_number(z1)}-{format_number(z2)}}} = {format_number(sigma)}",
        result=sigma, level_min=1,
    )
    builder.add_step(
        desc=f"μ = x1 − Z(p1)·σ = {x1} − {format_number(z1)}·{format_number(sigma)} = {format_number(mu)}",
        latex=rf"\mu = {x1} - {format_number(z1)} \cdot {format_number(sigma)} = {format_number(mu)}",
        result=mu, level_min=1,
    )
    if sigma <= 0:
        raise ValueError(f"σ resultó ≤ 0 ({format_number(sigma)}): revisar que p1≠p2 y que x1,x2 sean consistentes con p1,p2")
    result = builder.build(final_value=(mu, sigma), final_latex=rf"\mu={format_number(mu)},\ \sigma={format_number(sigma)}")
    return Normal(mu, sigma), result


# ===========================================================================
# Log-Normal
# ===========================================================================

def lognormal_from_mean_std_x(mu_x: float, sigma_x: float):
    """m, D del logaritmo a partir de la media y el desvío de X (no de ln X).

    D = sqrt(ln(1 + (sigma_x/mu_x)^2)),  m = ln(mu_x) - D^2/2.
    """
    if mu_x <= 0:
        raise ValueError("La media de X debe ser > 0 para Log-Normal")
    cv2 = (sigma_x / mu_x) ** 2
    D = math.sqrt(math.log(1.0 + cv2))
    m = math.log(mu_x) - D ** 2 / 2.0
    builder = StepBuilder("Log-Normal — m, D desde media y desvío de X")
    builder.add_step(
        desc="D² = ln(1 + (σx/μx)²),   m = ln(μx) − D²/2",
        latex=r"D^2 = \ln\!\left(1 + \frac{\sigma_x^2}{\mu_x^2}\right), \quad m = \ln(\mu_x) - \frac{D^2}{2}",
        level_min=1,
    )
    builder.add_step(
        desc=f"D² = ln(1 + ({sigma_x}/{mu_x})²) = ln({format_number(1 + cv2, 4)}) = {format_number(D**2, 4)}  →  D = {format_number(D)}",
        latex=rf"D^2 = \ln(1 + {format_number(cv2, 4)}) = {format_number(D**2, 4)} \;\Rightarrow\; D = {format_number(D)}",
        result=D, level_min=1,
    )
    builder.add_step(
        desc=f"m = ln({mu_x}) − {format_number(D**2, 4)}/2 = {format_number(math.log(mu_x), 4)} − {format_number(D**2/2, 4)} = {format_number(m)}",
        latex=rf"m = \ln({mu_x}) - \frac{{{format_number(D**2, 4)}}}{{2}} = {format_number(m)}",
        result=m, level_min=1,
    )
    result = builder.build(final_value=(m, D), final_latex=rf"m={format_number(m)},\ D={format_number(D)}")
    return LogNormal(m, D), result


# ===========================================================================
# Gamma
# ===========================================================================

def gamma_from_mean_variance(mu: float, var: float):
    """lambda, r a partir de media y varianza: lambda = mu/var, r = mu^2/var."""
    if var <= 0:
        raise ValueError("La varianza debe ser > 0")
    lam = mu / var
    r = mu ** 2 / var
    builder = StepBuilder("Gamma — λ, r desde media y varianza")
    builder.add_step(
        desc="E(X) = r/λ,  V(X) = r/λ²   →   λ = μ/V(X),   r = μ²/V(X)",
        latex=r"\lambda = \frac{\mu}{V(X)}, \quad r = \frac{\mu^2}{V(X)}",
        level_min=1,
    )
    builder.add_step(
        desc=f"λ = {mu} / {var} = {format_number(lam)}",
        latex=rf"\lambda = \frac{{{mu}}}{{{var}}} = {format_number(lam)}",
        result=lam, level_min=1,
    )
    builder.add_step(
        desc=f"r = {mu}² / {var} = {format_number(r)}",
        latex=rf"r = \frac{{{mu}^2}}{{{var}}} = {format_number(r)}",
        result=r, level_min=1,
    )
    result = builder.build(final_value=(r, lam), final_latex=rf"r={format_number(r)},\ \lambda={format_number(lam)}")
    return Gamma(r, lam), result


# ===========================================================================
# Pareto
# ===========================================================================

def pareto_from_mean_mode(mu: float, moda: float):
    """theta, b a partir de la media y la moda (Mo = theta): b = mu/(mu-theta)."""
    if moda <= 0:
        raise ValueError("La moda (= θ, mínimo del dominio) debe ser > 0")
    if mu <= moda:
        raise ValueError("La media debe ser mayor que la moda para que exista E(X) (b > 1)")
    theta = moda
    b = mu / (mu - theta)
    builder = StepBuilder("Pareto — θ, b desde media y moda")
    builder.add_step(
        desc="Mo = θ  (la Pareto es decreciente: la moda es el mínimo del dominio)",
        latex=r"\theta = Mo", level_min=1,
    )
    builder.add_step(
        desc=f"θ = {format_number(theta)}",
        latex=rf"\theta = {format_number(theta)}", result=theta, level_min=1,
    )
    builder.add_step(
        desc="E(X) = b·θ/(b−1)  →  b = μ/(μ−θ)",
        latex=r"b = \frac{\mu}{\mu - \theta}", level_min=1,
    )
    builder.add_step(
        desc=f"b = {mu} / ({mu} − {format_number(theta)}) = {format_number(b)}",
        latex=rf"b = \frac{{{mu}}}{{{mu} - {format_number(theta)}}} = {format_number(b)}",
        result=b, level_min=1,
    )
    result = builder.build(final_value=(theta, b), final_latex=rf"\theta={format_number(theta)},\ b={format_number(b)}")
    return Pareto(theta, b), result


# ===========================================================================
# Exponencial
# ===========================================================================

def exponencial_from_mean(mu: float):
    """lambda a partir de la media: lambda = 1/mu."""
    if mu <= 0:
        raise ValueError("La media debe ser > 0")
    lam = 1.0 / mu
    builder = StepBuilder("Exponencial — λ desde la media")
    builder.add_step(
        desc="E(X) = 1/λ  →  λ = 1/μ",
        latex=r"\lambda = \frac{1}{\mu}", level_min=1,
    )
    builder.add_step(
        desc=f"λ = 1/{mu} = {format_number(lam)}",
        latex=rf"\lambda = \frac{{1}}{{{mu}}} = {format_number(lam)}",
        result=lam, level_min=1,
    )
    result = builder.build(final_value=lam, final_latex=rf"\lambda = {format_number(lam)}")
    return Exponencial(lam), result


def exponencial_from_rate(cantidad: float, periodo: float):
    """lambda a partir de una tasa "cantidad cada periodo" (mismas unidades que la consulta)."""
    if periodo <= 0:
        raise ValueError("El período debe ser > 0")
    lam = cantidad / periodo
    builder = StepBuilder("Exponencial — λ desde una tasa")
    builder.add_step(
        desc=f"Tasa dada: {cantidad} cada {periodo} (unidades) → λ = cantidad/período",
        latex=r"\lambda = \frac{\text{cantidad}}{\text{período}}", level_min=1,
    )
    builder.add_step(
        desc=f"λ = {cantidad} / {periodo} = {format_number(lam)}",
        latex=rf"\lambda = \frac{{{cantidad}}}{{{periodo}}} = {format_number(lam)}",
        result=lam, level_min=1,
    )
    result = builder.build(final_value=lam, final_latex=rf"\lambda = {format_number(lam)}")
    return Exponencial(lam), result


# ===========================================================================
# Uniforme
# ===========================================================================

def uniforme_from_mean_range(mu: float, rango: float):
    """a, b a partir de la media y el rango (b - a): a = mu - rango/2, b = mu + rango/2."""
    if rango <= 0:
        raise ValueError("El rango (b − a) debe ser > 0")
    a = mu - rango / 2.0
    b = mu + rango / 2.0
    builder = StepBuilder("Uniforme — a, b desde media y rango")
    builder.add_step(
        desc="E(X) = (a+b)/2,  rango = b−a   →   a = μ − rango/2,  b = μ + rango/2",
        latex=r"a = \mu - \frac{b-a}{2}, \quad b = \mu + \frac{b-a}{2}",
        level_min=1,
    )
    builder.add_step(
        desc=f"a = {mu} − {rango}/2 = {format_number(a)}",
        latex=rf"a = {mu} - \frac{{{rango}}}{{2}} = {format_number(a)}",
        result=a, level_min=1,
    )
    builder.add_step(
        desc=f"b = {mu} + {rango}/2 = {format_number(b)}",
        latex=rf"b = {mu} + \frac{{{rango}}}{{2}} = {format_number(b)}",
        result=b, level_min=1,
    )
    result = builder.build(final_value=(a, b), final_latex=rf"a={format_number(a)},\ b={format_number(b)}")
    return Uniforme(a, b), result


# ===========================================================================
# Gumbel Máxima / Mínima
# ===========================================================================

def gumbel_max_from_mean_var(mu: float, var: float):
    """beta, theta (Gumbel Máxima) a partir de media y varianza.

    beta = sqrt(6*V(X))/pi,   theta = mu - beta*C   (C = Euler-Mascheroni ≈ 0.5772).
    """
    if var <= 0:
        raise ValueError("La varianza debe ser > 0")
    beta = math.sqrt(6.0 * var) / math.pi
    theta = mu - beta * _C
    builder = StepBuilder("Gumbel Máxima — β, θ desde media y varianza")
    builder.add_step(
        desc="V(X) = (π²/6)·β²  →  β = √(6·V(X))/π;     E(X) = θ + β·C  →  θ = μ − β·C",
        latex=r"\beta = \frac{\sqrt{6\,V(X)}}{\pi}, \quad \theta = \mu - \beta \cdot C",
        level_min=1,
    )
    builder.add_step(
        desc=f"β = √(6·{var})/π = {format_number(beta)}",
        latex=rf"\beta = \frac{{\sqrt{{6 \cdot {var}}}}}{{\pi}} = {format_number(beta)}",
        result=beta, level_min=1,
    )
    builder.add_step(
        desc=f"θ = {mu} − {format_number(beta)}·{format_number(_C, 4)} = {format_number(theta)}",
        latex=rf"\theta = {mu} - {format_number(beta)} \cdot {format_number(_C, 4)} = {format_number(theta)}",
        result=theta, level_min=1,
    )
    result = builder.build(final_value=(beta, theta), final_latex=rf"\beta={format_number(beta)},\ \theta={format_number(theta)}")
    return GumbelMax(beta, theta), result


def gumbel_min_from_mean_var(mu: float, var: float):
    """beta, theta (Gumbel Mínima) a partir de media y varianza.

    beta = sqrt(6*V(X))/pi,   theta = mu + beta*C   (C = Euler-Mascheroni ≈ 0.5772).
    """
    if var <= 0:
        raise ValueError("La varianza debe ser > 0")
    beta = math.sqrt(6.0 * var) / math.pi
    theta = mu + beta * _C
    builder = StepBuilder("Gumbel Mínima — β, θ desde media y varianza")
    builder.add_step(
        desc="V(X) = (π²/6)·β²  →  β = √(6·V(X))/π;     E(X) = θ − β·C  →  θ = μ + β·C",
        latex=r"\beta = \frac{\sqrt{6\,V(X)}}{\pi}, \quad \theta = \mu + \beta \cdot C",
        level_min=1,
    )
    builder.add_step(
        desc=f"β = √(6·{var})/π = {format_number(beta)}",
        latex=rf"\beta = \frac{{\sqrt{{6 \cdot {var}}}}}{{\pi}} = {format_number(beta)}",
        result=beta, level_min=1,
    )
    builder.add_step(
        desc=f"θ = {mu} + {format_number(beta)}·{format_number(_C, 4)} = {format_number(theta)}",
        latex=rf"\theta = {mu} + {format_number(beta)} \cdot {format_number(_C, 4)} = {format_number(theta)}",
        result=theta, level_min=1,
    )
    result = builder.build(final_value=(beta, theta), final_latex=rf"\beta={format_number(beta)},\ \theta={format_number(theta)}")
    return GumbelMin(beta, theta), result
