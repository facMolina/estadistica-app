"""Distribucion Pareto."""

import math
from scipy import stats as _st
from models.continuous._base import ContinuousBase
from calculation.step_engine import StepBuilder
from calculation.statistics_common import format_number


class Pareto(ContinuousBase):
    """
    Pareto(θ, b): f(x) = b·θ^b / x^(b+1),  x ≥ θ.
    θ = mínimo (escala), b = forma (shape > 0).
    scipy: pareto(b=b, loc=0, scale=θ)  →  dominio: x ≥ θ
    """

    def __init__(self, theta: float, b: float):
        if theta <= 0:
            raise ValueError("θ (mínimo) debe ser > 0")
        if b <= 0:
            raise ValueError("b (forma) debe ser > 0")
        self.theta = theta
        self.b = b
        self._dist = _st.pareto(b=b, loc=0, scale=theta)

    def name(self):    return "Pareto"
    def params_dict(self): return {"theta": self.theta, "b": self.b}
    def domain(self):  return (self.theta, math.inf)

    def latex_formula(self):
        return (rf"f(x) = \frac{{b \cdot \theta^b}}{{x^{{b+1}}}},\quad x \geq \theta")

    # ------------------------------------------------------------------
    def density_value(self, x: float) -> float:
        return float(self._dist.pdf(x)) if x >= self.theta else 0.0

    def density(self, x: float):
        theta, b = self.theta, self.b
        fval = self.density_value(x)
        builder = StepBuilder(f"f({x})")
        builder.add_step(
            desc="f(x) = b·θ^b / x^(b+1)  para x ≥ θ",
            latex=rf"f(x) = \frac{{b \cdot \theta^b}}{{x^{{b+1}}}}",
            level_min=1,
        )
        if x >= theta:
            builder.add_step(
                desc=f"f({x}) = {b}·{theta}^{b} / {x}^({b}+1) = {format_number(fval, 6)}",
                latex=rf"f({x}) = \frac{{{b} \cdot {theta}^{{{b}}}}}{{{x}^{{{b}+1}}}} = {format_number(fval, 6)}",
                result=fval, level_min=2,
            )
        else:
            builder.add_step(desc=f"x = {x} < θ = {theta}: f(x) = 0", level_min=1)
        return builder.build(final_value=fval, final_latex=rf"f({x}) = {format_number(fval, 6)}")

    # ------------------------------------------------------------------
    def cdf_left(self, x: float):
        theta, b = self.theta, self.b
        if x < theta:
            fx = 0.0
        else:
            fx = 1.0 - (theta / x) ** b
        builder = StepBuilder(f"F({x})")
        builder.add_step(
            desc="F(x) = 1 − (θ/x)^b  para x ≥ θ",
            latex=r"F(x) = 1 - \left(\frac{\theta}{x}\right)^b",
            level_min=1,
        )
        if x >= theta:
            ratio = theta / x
            power = ratio ** b
            builder.add_step(
                desc=f"θ/x = {theta}/{x} = {format_number(ratio, 4)}",
                latex=rf"\frac{{\theta}}{{x}} = \frac{{{theta}}}{{{x}}} = {format_number(ratio, 4)}",
                result=ratio, level_min=2,
            )
            builder.add_step(
                desc=f"(θ/x)^b = {format_number(ratio, 4)}^{b} = {format_number(power, 6)}",
                latex=rf"\left({format_number(ratio, 4)}\right)^{{{b}}} = {format_number(power, 6)}",
                result=power, level_min=2,
            )
            builder.add_step(
                desc=f"F({x}) = 1 − {format_number(power, 6)} = {format_number(fx, 6)}",
                latex=rf"F({x}) = 1 - {format_number(power, 6)} = {format_number(fx, 6)}",
                result=fx, level_min=1,
            )
        else:
            builder.add_step(desc=f"x < θ → F(x) = 0", result=0.0, level_min=1)
        return builder.build(final_value=fx, final_latex=rf"F({x}) = {format_number(fx, 6)}")

    # ------------------------------------------------------------------
    def mean(self):
        theta, b = self.theta, self.b
        if b > 1:
            mu = b * theta / (b - 1)
            builder = StepBuilder("Esperanza Matematica")
            builder.add_step(desc="E(X) = b·θ/(b−1)  (existe para b > 1)",
                             latex=r"E(X) = \frac{b \cdot \theta}{b - 1}", level_min=1)
            builder.add_step(
                desc=f"E(X) = {b}·{theta}/({b}−1) = {format_number(mu)}",
                latex=rf"E(X) = \frac{{{b} \cdot {theta}}}{{{b} - 1}} = {format_number(mu)}",
                result=mu, level_min=2,
            )
        else:
            mu = math.inf
            builder = StepBuilder("Esperanza Matematica")
            builder.add_step(desc="E(X) = ∞  (no existe para b ≤ 1)",
                             latex=r"E(X) = \infty \quad (b \leq 1)", level_min=1)
        return builder.build(final_value=mu, final_latex=rf"E(X) = {format_number(mu) if not math.isinf(mu) else r'\infty'}")

    def variance(self):
        theta, b = self.theta, self.b
        if b > 2:
            var = b * theta ** 2 / ((b - 1) ** 2 * (b - 2))
            builder = StepBuilder("Varianza")
            builder.add_step(desc="V(X) = b·θ²/((b−1)²·(b−2))  (existe para b > 2)",
                             latex=r"V(X) = \frac{b \cdot \theta^2}{(b-1)^2(b-2)}", level_min=1)
            builder.add_step(
                desc=f"V(X) = {b}·{theta}²/(({b}−1)²·({b}−2)) = {format_number(var)}",
                latex=rf"V(X) = \frac{{{b} \cdot {theta}^2}}{{({b}-1)^2 \cdot ({b}-2)}} = {format_number(var)}",
                result=var, level_min=2,
            )
        else:
            var = math.inf
            builder = StepBuilder("Varianza")
            builder.add_step(desc="V(X) = ∞  (no existe para b ≤ 2)",
                             latex=r"V(X) = \infty \quad (b \leq 2)", level_min=1)
        return builder.build(final_value=var, final_latex=rf"V(X) = {format_number(var) if not math.isinf(var) else r'\infty'}")

    def mode(self):
        builder = StepBuilder("Moda")
        builder.add_step(desc="Mo = θ  (mínimo del dominio, función decreciente)",
                         latex=r"Mo = \theta", level_min=1)
        builder.add_step(desc=f"Mo = {format_number(self.theta)}", latex=rf"Mo = {format_number(self.theta)}", result=self.theta, level_min=2)
        return builder.build(final_value=self.theta, final_latex=rf"Mo = {format_number(self.theta)}")

    def median(self):
        me = self.theta * 2 ** (1.0 / self.b)
        builder = StepBuilder("Mediana")
        builder.add_step(desc="Me = θ · 2^(1/b)", latex=r"Me = \theta \cdot 2^{1/b}", level_min=1)
        builder.add_step(
            desc=f"Me = {self.theta} · 2^(1/{self.b}) = {format_number(me)}",
            latex=rf"Me = {self.theta} \cdot 2^{{1/{self.b}}} = {format_number(me)}",
            result=me, level_min=2,
        )
        return builder.build(final_value=me, final_latex=rf"Me = {format_number(me)}")

    def skewness(self):
        b = self.b
        if b > 3:
            a3 = 2 * (1 + b) / (b - 3) * math.sqrt((b - 2) / b)
        else:
            a3 = math.inf
        builder = StepBuilder("Coeficiente de Asimetria")
        if b > 3:
            builder.add_step(desc="As = 2(1+b)/(b−3)·√((b−2)/b)  (existe para b > 3)",
                             latex=r"As = \frac{2(1+b)}{b-3}\sqrt{\frac{b-2}{b}}", level_min=1)
            builder.add_step(desc=f"As = {format_number(a3)}", result=a3, level_min=2)
        else:
            builder.add_step(desc="As = ∞  (no existe para b ≤ 3)", level_min=1)
        return builder.build(final_value=a3 if not math.isinf(a3) else float('inf'),
                             final_latex=rf"As = {format_number(a3) if not math.isinf(a3) else r'\infty'}")

    def kurtosis(self):
        b = self.b
        if b > 4:
            ku = 3 * (b - 2) * (b**2 + b - 6) / (b * (b - 3) * (b - 4)) + 3
        else:
            ku = math.inf
        builder = StepBuilder("Coeficiente de Kurtosis")
        if b > 4:
            builder.add_step(desc="Ku — fórmula en términos de b  (existe para b > 4)", level_min=1)
            builder.add_step(desc=f"Ku = {format_number(ku)}", result=ku, level_min=2)
        else:
            builder.add_step(desc="Ku = ∞  (no existe para b ≤ 4)", level_min=1)
        return builder.build(final_value=ku if not math.isinf(ku) else float('inf'),
                             final_latex=rf"Ku = {format_number(ku) if not math.isinf(ku) else r'\infty'}")

    def display_domain(self):
        me = self.theta * 2 ** (1.0 / self.b)
        sigma = self.std_dev().final_value
        hi = me + 4 * sigma if not math.isinf(sigma) else me * 10
        return self.theta * 0.95, hi
