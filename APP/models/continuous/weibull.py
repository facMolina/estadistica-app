"""Distribucion Weibull."""

import math
from scipy import stats as _st
from scipy.special import gamma as _gamma_fn
from models.continuous._base import ContinuousBase
from calculation.step_engine import StepBuilder
from calculation.statistics_common import format_number


class Weibull(ContinuousBase):
    """
    Weibull(β, ω): f(x) = (ω/β)·(x/β)^(ω−1)·exp(−(x/β)^ω),  x ≥ 0.
    β = escala (scale), ω = forma (shape).
    scipy: weibull_min(c=ω, scale=β)
    """

    def __init__(self, beta: float, omega: float):
        if beta <= 0:
            raise ValueError("β (escala) debe ser > 0")
        if omega <= 0:
            raise ValueError("ω (forma) debe ser > 0")
        self.beta = beta
        self.omega = omega
        self._dist = _st.weibull_min(c=omega, scale=beta)

    def name(self):    return "Weibull"
    def params_dict(self): return {"beta": self.beta, "omega": self.omega}
    def domain(self):  return (0.0, math.inf)

    def latex_formula(self):
        return (rf"f(x) = \frac{{\omega}}{{\beta}}\left(\frac{{x}}{{\beta}}\right)^{{\omega-1}}"
                rf"e^{{-\left(\frac{{x}}{{\beta}}\right)^\omega}},\quad x \geq 0")

    # ------------------------------------------------------------------
    def density_value(self, x: float) -> float:
        return float(self._dist.pdf(x)) if x >= 0 else 0.0

    def density(self, x: float):
        beta, omega = self.beta, self.omega
        fval = self.density_value(x)
        builder = StepBuilder(f"f({x})")
        builder.add_step(
            desc="f(x) = (ω/β)·(x/β)^(ω−1)·e^(−(x/β)^ω)",
            latex=rf"f(x) = \frac{{\omega}}{{\beta}}\left(\frac{{x}}{{\beta}}\right)^{{\omega-1}}e^{{-\left(\frac{{x}}{{\beta}}\right)^\omega}}",
            level_min=1,
        )
        if x >= 0:
            ratio = x / beta
            builder.add_step(
                desc=f"x/β = {x}/{beta} = {format_number(ratio, 4)}",
                latex=rf"\frac{{x}}{{\beta}} = \frac{{{x}}}{{{beta}}} = {format_number(ratio, 4)}",
                result=ratio, level_min=2,
            )
        builder.add_step(
            desc=f"f({x}) = {format_number(fval, 6)}",
            latex=rf"f({x}) = {format_number(fval, 6)}", result=fval, level_min=1,
        )
        return builder.build(final_value=fval, final_latex=rf"f({x}) = {format_number(fval, 6)}")

    # ------------------------------------------------------------------
    def cdf_left(self, x: float):
        beta, omega = self.beta, self.omega
        fx = 1.0 - math.exp(-(x / beta) ** omega) if x >= 0 else 0.0
        exp_term = math.exp(-(x / beta) ** omega) if x >= 0 else 1.0
        builder = StepBuilder(f"F({x})")
        builder.add_step(
            desc="F(x) = 1 − e^(−(x/β)^ω)",
            latex=r"F(x) = 1 - e^{-\left(\frac{x}{\beta}\right)^\omega}",
            level_min=1,
        )
        if x >= 0:
            ratio = x / beta
            power = ratio ** omega
            builder.add_step(
                desc=f"(x/β)^ω = ({format_number(ratio, 4)})^{omega} = {format_number(power, 4)}",
                latex=rf"\left(\frac{{{x}}}{{{beta}}}\right)^{{{omega}}} = {format_number(power, 4)}",
                result=power, level_min=2,
            )
            builder.add_step(
                desc=f"F({x}) = 1 − e^(−{format_number(power, 4)}) = 1 − {format_number(exp_term, 6)} = {format_number(fx, 6)}",
                latex=rf"F({x}) = 1 - e^{{-{format_number(power, 4)}}} = {format_number(fx, 6)}",
                result=fx, level_min=1,
            )
        return builder.build(final_value=fx, final_latex=rf"F({x}) = {format_number(fx, 6)}")

    # ------------------------------------------------------------------
    def mean(self):
        beta, omega = self.beta, self.omega
        mu = beta * _gamma_fn(1.0 + 1.0 / omega)
        g_val = _gamma_fn(1.0 + 1.0 / omega)
        builder = StepBuilder("Esperanza Matematica")
        builder.add_step(desc="E(X) = β · Γ(1 + 1/ω)", latex=r"E(X) = \beta \cdot \Gamma\!\left(1 + \frac{1}{\omega}\right)", level_min=1)
        builder.add_step(
            desc=f"Γ(1 + 1/{omega}) = Γ({format_number(1+1/omega, 4)}) = {format_number(g_val, 4)}",
            latex=rf"\Gamma\!\left({format_number(1+1/omega, 4)}\right) = {format_number(g_val, 4)}",
            result=g_val, level_min=2,
        )
        builder.add_step(
            desc=f"E(X) = {beta} · {format_number(g_val, 4)} = {format_number(mu)}",
            latex=rf"E(X) = {format_number(beta)} \cdot {format_number(g_val, 4)} = {format_number(mu)}",
            result=mu, level_min=2,
        )
        return builder.build(final_value=mu, final_latex=rf"E(X) = {format_number(mu)}")

    def variance(self):
        beta, omega = self.beta, self.omega
        g1 = _gamma_fn(1.0 + 1.0 / omega)
        g2 = _gamma_fn(1.0 + 2.0 / omega)
        var = beta ** 2 * (g2 - g1 ** 2)
        builder = StepBuilder("Varianza")
        builder.add_step(
            desc="V(X) = β²·[Γ(1+2/ω) − Γ(1+1/ω)²]",
            latex=r"V(X) = \beta^2\left[\Gamma\!\left(1+\frac{2}{\omega}\right) - \Gamma\!\left(1+\frac{1}{\omega}\right)^2\right]",
            level_min=1,
        )
        builder.add_step(
            desc=f"V(X) = {beta}²·({format_number(g2,4)} − {format_number(g1,4)}²) = {format_number(var)}",
            latex=rf"V(X) = {format_number(beta)}^2 \cdot ({format_number(g2,4)} - {format_number(g1,4)}^2) = {format_number(var)}",
            result=var, level_min=2,
        )
        return builder.build(final_value=var, final_latex=rf"V(X) = {format_number(var)}")

    def mode(self):
        omega = self.omega
        if omega > 1:
            mo = self.beta * ((omega - 1) / omega) ** (1.0 / omega)
        else:
            mo = 0.0
        builder = StepBuilder("Moda")
        if omega > 1:
            builder.add_step(
                desc="Mo = β·((ω−1)/ω)^(1/ω)  (para ω > 1)",
                latex=r"Mo = \beta \cdot \left(\frac{\omega-1}{\omega}\right)^{1/\omega}",
                level_min=1,
            )
            builder.add_step(desc=f"Mo = {format_number(mo)}", result=mo, level_min=2)
        else:
            builder.add_step(desc="ω ≤ 1: Mo = 0  (densidad decreciente)", level_min=1)
        return builder.build(final_value=mo, final_latex=rf"Mo = {format_number(mo)}")

    def median(self):
        me = self.beta * math.log(2) ** (1.0 / self.omega)
        builder = StepBuilder("Mediana")
        builder.add_step(desc="Me = β · (ln 2)^(1/ω)", latex=r"Me = \beta \cdot (\ln 2)^{1/\omega}", level_min=1)
        builder.add_step(
            desc=f"Me = {self.beta} · {format_number(math.log(2), 4)}^(1/{self.omega}) = {format_number(me)}",
            latex=rf"Me = {format_number(self.beta)} \cdot {format_number(math.log(2), 4)}^{{1/{self.omega}}} = {format_number(me)}",
            result=me, level_min=2,
        )
        return builder.build(final_value=me, final_latex=rf"Me = {format_number(me)}")

    def skewness(self):
        omega = self.omega
        g1 = _gamma_fn(1 + 1/omega)
        g2 = _gamma_fn(1 + 2/omega)
        g3 = _gamma_fn(1 + 3/omega)
        sigma = math.sqrt(self.beta**2 * (g2 - g1**2))
        mu = self.beta * g1
        a3 = (self.beta**3 * g3 - 3*mu*sigma**2 - mu**3) / sigma**3 if sigma > 0 else 0
        builder = StepBuilder("Coeficiente de Asimetria")
        builder.add_step(desc="As = (μ₃ − 3μσ² − μ³) / σ³  (usando momentos Gamma)",
                         latex=r"As = \frac{\mu_3' - 3\mu\sigma^2 - \mu^3}{\sigma^3}", level_min=1)
        builder.add_step(desc=f"As ≈ {format_number(a3)}", result=a3, level_min=2)
        return builder.build(final_value=a3, final_latex=rf"As = {format_number(a3)}")

    def kurtosis(self):
        ku = float(self._dist.stats(moments='k')) + 3
        builder = StepBuilder("Coeficiente de Kurtosis")
        builder.add_step(desc="Ku — calculado a partir de los momentos de la distribución Weibull",
                         latex=r"Ku = \alpha_4", level_min=1)
        builder.add_step(desc=f"Ku = {format_number(ku)}", result=ku, level_min=2)
        return builder.build(final_value=ku, final_latex=rf"Ku = {format_number(ku)}")

    def display_domain(self):
        mu = self.mean().final_value
        sigma = self.std_dev().final_value
        return 0.0, mu + 4 * sigma
