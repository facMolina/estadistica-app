"""Distribucion Exponencial."""

import math
from scipy import stats as _st
from models.continuous._base import ContinuousBase
from calculation.step_engine import StepBuilder
from calculation.statistics_common import format_number


class Exponencial(ContinuousBase):
    """Exponencial(λ): f(x) = λ·e^(−λx), x ≥ 0."""

    def __init__(self, lam: float):
        if lam <= 0:
            raise ValueError("λ (tasa) debe ser > 0")
        self.lam = lam
        self._dist = _st.expon(scale=1.0 / lam)

    def name(self):    return "Exponencial"
    def params_dict(self): return {"lambda": self.lam}
    def domain(self):  return (0.0, math.inf)

    def latex_formula(self):
        return rf"f(x) = {format_number(self.lam)} \cdot e^{{-{format_number(self.lam)} \cdot x}}, \quad x \geq 0"

    # ------------------------------------------------------------------
    def density_value(self, x: float) -> float:
        return float(self._dist.pdf(x)) if x >= 0 else 0.0

    def density(self, x: float):
        lam = self.lam
        fval = self.density_value(x)
        builder = StepBuilder(f"f({x})")
        builder.add_step(desc="f(x) = λ · e^(−λx)", latex=r"f(x) = \lambda \cdot e^{-\lambda x}", level_min=1)
        builder.add_step(
            desc=f"f({x}) = {lam} · e^(−{lam}·{x}) = {format_number(fval, 6)}",
            latex=rf"f({x}) = {format_number(lam)} \cdot e^{{-{format_number(lam)} \cdot {x}}} = {format_number(fval, 6)}",
            result=fval, level_min=2,
        )
        return builder.build(final_value=fval, final_latex=rf"f({x}) = {format_number(fval, 6)}")

    # ------------------------------------------------------------------
    def cdf_left(self, x: float):
        lam = self.lam
        fx = 1.0 - math.exp(-lam * x) if x >= 0 else 0.0
        builder = StepBuilder(f"F({x})")
        builder.add_step(desc="F(x) = 1 − e^(−λx)", latex=r"F(x) = 1 - e^{-\lambda x}", level_min=1)
        builder.add_step(
            desc=f"F({x}) = 1 − e^(−{lam}·{x}) = 1 − {format_number(math.exp(-lam*x), 6)} = {format_number(fx, 6)}",
            latex=rf"F({x}) = 1 - e^{{-{format_number(lam)} \cdot {x}}} = 1 - {format_number(math.exp(-lam*x) if x>=0 else 1, 6)} = {format_number(fx, 6)}",
            result=fx, level_min=1,
        )
        return builder.build(final_value=fx, final_latex=rf"F({x}) = {format_number(fx, 6)}")

    # ------------------------------------------------------------------
    def mean(self):
        mu = 1.0 / self.lam
        builder = StepBuilder("Esperanza Matematica")
        builder.add_step(desc="E(X) = 1/λ", latex=r"E(X) = \frac{1}{\lambda}", level_min=1)
        builder.add_step(
            desc=f"E(X) = 1/{self.lam} = {format_number(mu)}",
            latex=rf"E(X) = \frac{{1}}{{{format_number(self.lam)}}} = {format_number(mu)}",
            result=mu, level_min=2,
        )
        return builder.build(final_value=mu, final_latex=rf"E(X) = {format_number(mu)}")

    def variance(self):
        var = 1.0 / self.lam ** 2
        builder = StepBuilder("Varianza")
        builder.add_step(desc="V(X) = 1/λ²", latex=r"V(X) = \frac{1}{\lambda^2}", level_min=1)
        builder.add_step(
            desc=f"V(X) = 1/{self.lam}² = {format_number(var)}",
            latex=rf"V(X) = \frac{{1}}{{{format_number(self.lam)}^2}} = {format_number(var)}",
            result=var, level_min=2,
        )
        return builder.build(final_value=var, final_latex=rf"V(X) = {format_number(var)}")

    def mode(self):
        builder = StepBuilder("Moda")
        builder.add_step(desc="Exponencial: Mo = 0  (función decreciente, máximo en x=0)",
                         latex=r"Mo = 0", level_min=1)
        return builder.build(final_value=0.0, final_latex=r"Mo = 0")

    def median(self):
        me = math.log(2) / self.lam
        builder = StepBuilder("Mediana")
        builder.add_step(desc="Me = ln(2) / λ", latex=r"Me = \frac{\ln 2}{\lambda}", level_min=1)
        builder.add_step(
            desc=f"Me = ln(2) / {self.lam} = {format_number(me)}",
            latex=rf"Me = \frac{{\ln 2}}{{{format_number(self.lam)}}} = {format_number(me)}",
            result=me, level_min=2,
        )
        return builder.build(final_value=me, final_latex=rf"Me = {format_number(me)}")

    def skewness(self):
        builder = StepBuilder("Coeficiente de Asimetria")
        builder.add_step(desc="Exponencial: As = 2  (asimetría positiva fija)",
                         latex=r"As = 2", level_min=1)
        return builder.build(final_value=2.0, final_latex=r"As = 2")

    def kurtosis(self):
        builder = StepBuilder("Coeficiente de Kurtosis")
        builder.add_step(desc="Exponencial: Ku = 9",
                         latex=r"Ku = 9", level_min=1)
        return builder.build(final_value=9.0, final_latex=r"Ku = 9")

    def fractile(self, alpha: float):
        x_alpha = -math.log(1.0 - alpha) / self.lam
        builder = StepBuilder(f"x({alpha})")
        builder.add_step(
            desc=f"F(x) = α → 1 − e^(−λx) = {alpha} → x = −ln(1−α)/λ",
            latex=rf"x(\alpha) = -\frac{{\ln(1 - \alpha)}}{{\lambda}}",
            level_min=1,
        )
        builder.add_step(
            desc=f"x({alpha}) = −ln(1−{alpha}) / {self.lam} = {format_number(x_alpha, 4)}",
            latex=rf"x({alpha}) = -\frac{{\ln({1-alpha})}}{{{format_number(self.lam)}}} = {format_number(x_alpha, 4)}",
            result=x_alpha, level_min=2,
        )
        return builder.build(final_value=x_alpha, final_latex=rf"x({alpha}) = {format_number(x_alpha, 4)}")

    def display_domain(self):
        return 0.0, 5.0 / self.lam
