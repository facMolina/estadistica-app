"""Distribuciones Gumbel Maxima y Minima."""

import math
from scipy import stats as _st
from config.settings import EULER_MASCHERONI
from models.continuous._base import ContinuousBase
from calculation.step_engine import StepBuilder
from calculation.statistics_common import format_number

_C = EULER_MASCHERONI   # ≈ 0.5772


class GumbelMax(ContinuousBase):
    """
    Gumbel Máxima (Tipo I para máximos).
    F(x) = exp(−exp(−(x−θ)/β)),  −∞ < x < +∞.
    Parámetros: β (escala > 0), θ (ubicación = moda).
    scipy: gumbel_r(loc=θ, scale=β)
    """

    def __init__(self, beta: float, theta: float):
        if beta <= 0:
            raise ValueError("β (escala) debe ser > 0")
        self.beta = beta
        self.theta = theta
        self._dist = _st.gumbel_r(loc=theta, scale=beta)

    def name(self):    return "Gumbel Max"
    def params_dict(self): return {"beta": self.beta, "theta": self.theta}
    def domain(self):  return (-math.inf, math.inf)

    def latex_formula(self):
        return (rf"F(x) = e^{{-e^{{-(x-\theta)/\beta}}}},\quad"
                rf"f(x) = \frac{{1}}{{\beta}} e^{{-(x-\theta)/\beta}} \cdot e^{{-e^{{-(x-\theta)/\beta}}}}")

    # ------------------------------------------------------------------
    def density_value(self, x: float) -> float:
        return float(self._dist.pdf(x))

    def density(self, x: float):
        beta, theta = self.beta, self.theta
        z = (x - theta) / beta
        fval = self.density_value(x)
        builder = StepBuilder(f"f({x})")
        builder.add_step(
            desc="f(x) = (1/β)·e^(−z)·e^(−e^(−z)),  z = (x−θ)/β",
            latex=rf"f(x) = \frac{{1}}{{\beta}} e^{{-z}} \cdot e^{{-e^{{-z}}}},\quad z = \frac{{x-\theta}}{{\beta}}",
            level_min=1,
        )
        builder.add_step(
            desc=f"z = ({x} − {theta}) / {beta} = {format_number(z, 4)}",
            latex=rf"z = \frac{{{x} - {theta}}}{{{beta}}} = {format_number(z, 4)}",
            result=z, level_min=2,
        )
        builder.add_step(
            desc=f"f({x}) = {format_number(fval, 6)}",
            latex=rf"f({x}) = {format_number(fval, 6)}", result=fval, level_min=1,
        )
        return builder.build(final_value=fval, final_latex=rf"f({x}) = {format_number(fval, 6)}")

    # ------------------------------------------------------------------
    def cdf_left(self, x: float):
        beta, theta = self.beta, self.theta
        z = (x - theta) / beta
        fx = math.exp(-math.exp(-z))
        builder = StepBuilder(f"F({x})")
        builder.add_step(
            desc="F(x) = e^(−e^(−z)),  z = (x−θ)/β",
            latex=r"F(x) = e^{-e^{-z}},\quad z = \frac{x-\theta}{\beta}",
            level_min=1,
        )
        builder.add_step(
            desc=f"z = ({x} − {theta}) / {beta} = {format_number(z, 4)}",
            latex=rf"z = \frac{{{x} - {theta}}}{{{beta}}} = {format_number(z, 4)}",
            result=z, level_min=1,
        )
        builder.add_step(
            desc=f"F({x}) = e^(−e^(−{format_number(z,4)})) = {format_number(fx, 6)}",
            latex=rf"F({x}) = e^{{-e^{{-{format_number(z, 4)}}}}} = {format_number(fx, 6)}",
            result=fx, level_min=1,
        )
        return builder.build(final_value=fx, final_latex=rf"F({x}) = {format_number(fx, 6)}")

    # ------------------------------------------------------------------
    def mean(self):
        mu = self.theta + self.beta * _C
        builder = StepBuilder("Esperanza Matematica")
        builder.add_step(desc="E(X) = θ + β·C  (C = constante de Euler-Mascheroni ≈ 0.5772)",
                         latex=r"E(X) = \theta + \beta \cdot C,\quad C \approx 0.5772", level_min=1)
        builder.add_step(
            desc=f"E(X) = {self.theta} + {self.beta}·{format_number(_C, 4)} = {format_number(mu)}",
            latex=rf"E(X) = {self.theta} + {self.beta} \cdot {format_number(_C, 4)} = {format_number(mu)}",
            result=mu, level_min=2,
        )
        return builder.build(final_value=mu, final_latex=rf"E(X) = {format_number(mu)}")

    def variance(self):
        var = (math.pi ** 2 / 6) * self.beta ** 2
        builder = StepBuilder("Varianza")
        builder.add_step(desc="V(X) = (π²/6)·β²", latex=r"V(X) = \frac{\pi^2}{6}\beta^2", level_min=1)
        builder.add_step(
            desc=f"V(X) = (π²/6)·{self.beta}² = {format_number(var)}",
            latex=rf"V(X) = \frac{{\pi^2}}{{6}} \cdot {self.beta}^2 = {format_number(var)}",
            result=var, level_min=2,
        )
        return builder.build(final_value=var, final_latex=rf"V(X) = {format_number(var)}")

    def mode(self):
        builder = StepBuilder("Moda")
        builder.add_step(desc="Mo = θ  (parámetro de ubicación = moda)",
                         latex=r"Mo = \theta", level_min=1)
        builder.add_step(desc=f"Mo = {format_number(self.theta)}", latex=rf"Mo = {format_number(self.theta)}", result=self.theta, level_min=2)
        return builder.build(final_value=self.theta, final_latex=rf"Mo = {format_number(self.theta)}")

    def median(self):
        me = self.theta - self.beta * math.log(math.log(2))
        builder = StepBuilder("Mediana")
        builder.add_step(desc="Me = θ − β·ln(ln 2)", latex=r"Me = \theta - \beta \cdot \ln(\ln 2)", level_min=1)
        builder.add_step(
            desc=f"Me = {self.theta} − {self.beta}·{format_number(math.log(math.log(2)),4)} = {format_number(me)}",
            latex=rf"Me = {self.theta} - {self.beta} \cdot {format_number(math.log(math.log(2)),4)} = {format_number(me)}",
            result=me, level_min=2,
        )
        return builder.build(final_value=me, final_latex=rf"Me = {format_number(me)}")

    def skewness(self):
        a3 = 12 * math.sqrt(6) * 1.20206 / math.pi ** 3   # 12√6·ζ(3)/π³ ≈ 1.1395
        a3 = float(self._dist.stats(moments='s'))
        builder = StepBuilder("Coeficiente de Asimetria")
        builder.add_step(desc="As = 12√6·ζ(3)/π³ ≈ 1.1395  (asimetría positiva fija)",
                         latex=r"As = \frac{12\sqrt{6}\,\zeta(3)}{\pi^3} \approx 1.1395", level_min=1)
        builder.add_step(desc=f"As = {format_number(a3)}", result=a3, level_min=2)
        return builder.build(final_value=a3, final_latex=rf"As = {format_number(a3)}")

    def kurtosis(self):
        ku = float(self._dist.stats(moments='k')) + 3
        builder = StepBuilder("Coeficiente de Kurtosis")
        builder.add_step(desc="Ku = 12/5 + 3 = 5.4  (fijo para Gumbel)",
                         latex=r"Ku = \frac{12}{5} + 3 = 5.4", level_min=1)
        builder.add_step(desc=f"Ku = {format_number(ku)}", result=ku, level_min=2)
        return builder.build(final_value=ku, final_latex=rf"Ku = {format_number(ku)}")

    def display_domain(self):
        return self.theta - 3 * self.beta, self.theta + 7 * self.beta


# ===========================================================================

class GumbelMin(ContinuousBase):
    """
    Gumbel Mínima (Tipo I para mínimos).
    F(x) = 1 − exp(−exp((x−θ)/β)),  −∞ < x < +∞.
    scipy: gumbel_l(loc=θ, scale=β)
    """

    def __init__(self, beta: float, theta: float):
        if beta <= 0:
            raise ValueError("β (escala) debe ser > 0")
        self.beta = beta
        self.theta = theta
        self._dist = _st.gumbel_l(loc=theta, scale=beta)

    def name(self):    return "Gumbel Min"
    def params_dict(self): return {"beta": self.beta, "theta": self.theta}
    def domain(self):  return (-math.inf, math.inf)

    def latex_formula(self):
        return (rf"F(x) = 1 - e^{{-e^{{(x-\theta)/\beta}}}},\quad"
                rf"f(x) = \frac{{1}}{{\beta}} e^{{(x-\theta)/\beta}} \cdot e^{{-e^{{(x-\theta)/\beta}}}}")

    # ------------------------------------------------------------------
    def density_value(self, x: float) -> float:
        return float(self._dist.pdf(x))

    def density(self, x: float):
        beta, theta = self.beta, self.theta
        z = (x - theta) / beta
        fval = self.density_value(x)
        builder = StepBuilder(f"f({x})")
        builder.add_step(
            desc="f(x) = (1/β)·e^z·e^(−e^z),  z = (x−θ)/β  [Gumbel Mínima]",
            latex=rf"f(x) = \frac{{1}}{{\beta}} e^{{z}} \cdot e^{{-e^{{z}}}},\quad z = \frac{{x-\theta}}{{\beta}}",
            level_min=1,
        )
        builder.add_step(
            desc=f"z = ({x} − {theta}) / {beta} = {format_number(z, 4)}",
            latex=rf"z = {format_number(z, 4)}", result=z, level_min=2,
        )
        builder.add_step(
            desc=f"f({x}) = {format_number(fval, 6)}",
            latex=rf"f({x}) = {format_number(fval, 6)}", result=fval, level_min=1,
        )
        return builder.build(final_value=fval, final_latex=rf"f({x}) = {format_number(fval, 6)}")

    # ------------------------------------------------------------------
    def cdf_left(self, x: float):
        beta, theta = self.beta, self.theta
        z = (x - theta) / beta
        fx = 1.0 - math.exp(-math.exp(z))
        builder = StepBuilder(f"F({x})")
        builder.add_step(
            desc="F(x) = 1 − e^(−e^z),  z = (x−θ)/β  [Gumbel Mínima]",
            latex=r"F(x) = 1 - e^{-e^{z}},\quad z = \frac{x-\theta}{\beta}",
            level_min=1,
        )
        builder.add_step(
            desc=f"z = ({x} − {theta}) / {beta} = {format_number(z, 4)}",
            latex=rf"z = \frac{{{x} - {theta}}}{{{beta}}} = {format_number(z, 4)}",
            result=z, level_min=1,
        )
        builder.add_step(
            desc=f"F({x}) = 1 − e^(−e^{format_number(z,4)}) = {format_number(fx, 6)}",
            latex=rf"F({x}) = 1 - e^{{-e^{{{format_number(z, 4)}}}}} = {format_number(fx, 6)}",
            result=fx, level_min=1,
        )
        return builder.build(final_value=fx, final_latex=rf"F({x}) = {format_number(fx, 6)}")

    # ------------------------------------------------------------------
    def mean(self):
        mu = self.theta - self.beta * _C
        builder = StepBuilder("Esperanza Matematica")
        builder.add_step(desc="E(X) = θ − β·C  (C ≈ 0.5772, Gumbel Mínima)",
                         latex=r"E(X) = \theta - \beta \cdot C", level_min=1)
        builder.add_step(
            desc=f"E(X) = {self.theta} − {self.beta}·{format_number(_C, 4)} = {format_number(mu)}",
            latex=rf"E(X) = {self.theta} - {self.beta} \cdot {format_number(_C, 4)} = {format_number(mu)}",
            result=mu, level_min=2,
        )
        return builder.build(final_value=mu, final_latex=rf"E(X) = {format_number(mu)}")

    def variance(self):
        var = (math.pi ** 2 / 6) * self.beta ** 2
        builder = StepBuilder("Varianza")
        builder.add_step(desc="V(X) = (π²/6)·β²  (igual que Gumbel Máxima)",
                         latex=r"V(X) = \frac{\pi^2}{6}\beta^2", level_min=1)
        builder.add_step(
            desc=f"V(X) = {format_number(var)}",
            latex=rf"V(X) = \frac{{\pi^2}}{{6}} \cdot {self.beta}^2 = {format_number(var)}",
            result=var, level_min=2,
        )
        return builder.build(final_value=var, final_latex=rf"V(X) = {format_number(var)}")

    def mode(self):
        builder = StepBuilder("Moda")
        builder.add_step(desc="Mo = θ  (parámetro de ubicación)", latex=r"Mo = \theta", level_min=1)
        builder.add_step(desc=f"Mo = {format_number(self.theta)}", latex=rf"Mo = {format_number(self.theta)}", result=self.theta, level_min=2)
        return builder.build(final_value=self.theta, final_latex=rf"Mo = {format_number(self.theta)}")

    def median(self):
        me = self.theta + self.beta * math.log(math.log(2))
        builder = StepBuilder("Mediana")
        builder.add_step(desc="Me = θ + β·ln(ln 2)", latex=r"Me = \theta + \beta \cdot \ln(\ln 2)", level_min=1)
        builder.add_step(desc=f"Me = {format_number(me)}", result=me, level_min=2)
        return builder.build(final_value=me, final_latex=rf"Me = {format_number(me)}")

    def skewness(self):
        a3 = float(self._dist.stats(moments='s'))
        builder = StepBuilder("Coeficiente de Asimetria")
        builder.add_step(desc="Gumbel Mínima: As ≈ −1.1395  (asimetría negativa fija)",
                         latex=r"As \approx -1.1395", level_min=1)
        builder.add_step(desc=f"As = {format_number(a3)}", result=a3, level_min=2)
        return builder.build(final_value=a3, final_latex=rf"As = {format_number(a3)}")

    def kurtosis(self):
        ku = float(self._dist.stats(moments='k')) + 3
        builder = StepBuilder("Coeficiente de Kurtosis")
        builder.add_step(desc="Ku = 5.4  (fijo para Gumbel)", latex=r"Ku = 5.4", level_min=1)
        builder.add_step(desc=f"Ku = {format_number(ku)}", result=ku, level_min=2)
        return builder.build(final_value=ku, final_latex=rf"Ku = {format_number(ku)}")

    def display_domain(self):
        return self.theta - 7 * self.beta, self.theta + 3 * self.beta
