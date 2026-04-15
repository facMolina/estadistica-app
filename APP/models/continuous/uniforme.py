"""Distribucion Uniforme Continua."""

import math
from scipy import stats as _st
from models.continuous._base import ContinuousBase
from calculation.step_engine import StepBuilder
from calculation.statistics_common import format_number


class Uniforme(ContinuousBase):
    """
    Uniforme(a, b): f(x) = 1/(b−a)  para a ≤ x ≤ b.
    scipy: uniform(loc=a, scale=b−a)
    """

    def __init__(self, a: float, b: float):
        if b <= a:
            raise ValueError("b debe ser > a")
        self.a = a
        self.b = b
        self._dist = _st.uniform(loc=a, scale=b - a)

    def name(self):    return "Uniforme"
    def params_dict(self): return {"a": self.a, "b": self.b}
    def domain(self):  return (self.a, self.b)

    def latex_formula(self):
        width = self.b - self.a
        return (rf"f(x) = \frac{{1}}{{b - a}} = \frac{{1}}{{{format_number(width)}}}"
                rf",\quad {self.a} \leq x \leq {self.b}")

    # ------------------------------------------------------------------
    def density_value(self, x: float) -> float:
        return 1.0 / (self.b - self.a) if self.a <= x <= self.b else 0.0

    def density(self, x: float):
        a, b = self.a, self.b
        fval = self.density_value(x)
        width = b - a
        builder = StepBuilder(f"f({x})")
        builder.add_step(
            desc="f(x) = 1/(b−a)  para a ≤ x ≤ b, 0 en otro caso",
            latex=r"f(x) = \frac{1}{b - a}",
            level_min=1,
        )
        if a <= x <= b:
            builder.add_step(
                desc=f"f({x}) = 1/({b}−{a}) = 1/{format_number(width)} = {format_number(fval, 6)}",
                latex=rf"f({x}) = \frac{{1}}{{{b} - {a}}} = \frac{{1}}{{{format_number(width)}}} = {format_number(fval, 6)}",
                result=fval, level_min=2,
            )
        else:
            builder.add_step(desc=f"x = {x} fuera de [{a}, {b}] → f(x) = 0", result=0.0, level_min=1)
        return builder.build(final_value=fval, final_latex=rf"f({x}) = {format_number(fval, 6)}")

    # ------------------------------------------------------------------
    def cdf_left(self, x: float):
        a, b = self.a, self.b
        if x < a:
            fx = 0.0
        elif x > b:
            fx = 1.0
        else:
            fx = (x - a) / (b - a)
        builder = StepBuilder(f"F({x})")
        builder.add_step(
            desc="F(x) = (x−a)/(b−a)  para a ≤ x ≤ b",
            latex=r"F(x) = \frac{x - a}{b - a}",
            level_min=1,
        )
        if a <= x <= b:
            builder.add_step(
                desc=f"F({x}) = ({x}−{a})/({b}−{a}) = {format_number(x-a, 4)}/{format_number(b-a)} = {format_number(fx, 6)}",
                latex=rf"F({x}) = \frac{{{x} - {a}}}{{{b} - {a}}} = \frac{{{format_number(x-a, 4)}}}{{{format_number(b-a)}}} = {format_number(fx, 6)}",
                result=fx, level_min=1,
            )
        elif x < a:
            builder.add_step(desc=f"x < a → F(x) = 0", result=0.0, level_min=1)
        else:
            builder.add_step(desc=f"x > b → F(x) = 1", result=1.0, level_min=1)
        return builder.build(final_value=fx, final_latex=rf"F({x}) = {format_number(fx, 6)}")

    # ------------------------------------------------------------------
    def mean(self):
        mu = (self.a + self.b) / 2
        builder = StepBuilder("Esperanza Matematica")
        builder.add_step(desc="E(X) = (a + b) / 2", latex=r"E(X) = \frac{a + b}{2}", level_min=1)
        builder.add_step(
            desc=f"E(X) = ({self.a} + {self.b}) / 2 = {format_number(mu)}",
            latex=rf"E(X) = \frac{{{self.a} + {self.b}}}{{2}} = {format_number(mu)}",
            result=mu, level_min=2,
        )
        return builder.build(final_value=mu, final_latex=rf"E(X) = {format_number(mu)}")

    def variance(self):
        var = (self.b - self.a) ** 2 / 12
        builder = StepBuilder("Varianza")
        builder.add_step(desc="V(X) = (b−a)²/12", latex=r"V(X) = \frac{(b-a)^2}{12}", level_min=1)
        builder.add_step(
            desc=f"V(X) = ({self.b}−{self.a})²/12 = {format_number((self.b-self.a)**2, 4)}/12 = {format_number(var)}",
            latex=rf"V(X) = \frac{{({self.b} - {self.a})^2}}{{12}} = {format_number(var)}",
            result=var, level_min=2,
        )
        return builder.build(final_value=var, final_latex=rf"V(X) = {format_number(var)}")

    def mode(self):
        builder = StepBuilder("Moda")
        builder.add_step(desc="Uniforme: cualquier valor en [a, b] es igualmente probable — no hay moda única",
                         latex=r"Mo \in [a,\, b]", level_min=1)
        mu = (self.a + self.b) / 2
        builder.add_step(desc=f"Se usa el punto medio: (a+b)/2 = {format_number(mu)}", result=mu, level_min=2)
        return builder.build(final_value=mu, final_latex=r"Mo \in [a, b]")

    def median(self):
        me = (self.a + self.b) / 2
        builder = StepBuilder("Mediana")
        builder.add_step(desc="Me = (a + b) / 2  (simétrica → Me = E(X))",
                         latex=r"Me = \frac{a + b}{2}", level_min=1)
        builder.add_step(
            desc=f"Me = ({self.a} + {self.b}) / 2 = {format_number(me)}",
            latex=rf"Me = {format_number(me)}", result=me, level_min=2,
        )
        return builder.build(final_value=me, final_latex=rf"Me = {format_number(me)}")

    def skewness(self):
        builder = StepBuilder("Coeficiente de Asimetria")
        builder.add_step(desc="Uniforme: As = 0  (distribución simétrica)",
                         latex=r"As = 0", level_min=1)
        return builder.build(final_value=0.0, final_latex=r"As = 0")

    def kurtosis(self):
        builder = StepBuilder("Coeficiente de Kurtosis")
        builder.add_step(desc="Uniforme: Ku = 9/5 = 1.8  (platicúrtica)",
                         latex=r"Ku = \frac{9}{5} = 1.8", level_min=1)
        return builder.build(final_value=1.8, final_latex=r"Ku = 1.8")

    def fractile(self, alpha: float):
        x_alpha = self.a + alpha * (self.b - self.a)
        builder = StepBuilder(f"x({alpha})")
        builder.add_step(desc="x(α) = a + α·(b−a)", latex=r"x(\alpha) = a + \alpha \cdot (b - a)", level_min=1)
        builder.add_step(
            desc=f"x({alpha}) = {self.a} + {alpha}·({self.b}−{self.a}) = {format_number(x_alpha, 4)}",
            latex=rf"x({alpha}) = {self.a} + {alpha} \cdot {format_number(self.b - self.a)} = {format_number(x_alpha, 4)}",
            result=x_alpha, level_min=2,
        )
        return builder.build(final_value=x_alpha, final_latex=rf"x({alpha}) = {format_number(x_alpha, 4)}")

    def display_domain(self):
        margin = (self.b - self.a) * 0.15
        return self.a - margin, self.b + margin
