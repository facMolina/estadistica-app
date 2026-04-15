"""Distribucion Normal (Gaussiana)."""

import math
from scipy import stats as _st
from models.continuous._base import ContinuousBase
from calculation.step_engine import StepBuilder
from calculation.statistics_common import format_number


class Normal(ContinuousBase):
    """Normal(μ, σ): f(x) = 1/(σ√2π) · exp(−½·((x−μ)/σ)²)"""

    def __init__(self, mu: float, sigma: float):
        if sigma <= 0:
            raise ValueError("σ (desvio estandar) debe ser > 0")
        self.mu = mu
        self.sigma = sigma
        self._dist = _st.norm(loc=mu, scale=sigma)

    def name(self):    return "Normal"
    def params_dict(self): return {"mu": self.mu, "sigma": self.sigma}
    def domain(self):  return (-math.inf, math.inf)

    def latex_formula(self):
        return (rf"f(x) = \frac{{1}}{{{format_number(self.sigma)}\sqrt{{2\pi}}}}"
                rf" \cdot e^{{-\frac{{1}}{{2}}\left(\frac{{x-{format_number(self.mu)}}}"
                rf"{{{format_number(self.sigma)}}}\right)^2}}")

    # ------------------------------------------------------------------
    def density_value(self, x: float) -> float:
        return float(self._dist.pdf(x))

    def density(self, x: float):
        mu, sigma = self.mu, self.sigma
        z = (x - mu) / sigma
        fval = self.density_value(x)
        builder = StepBuilder(f"f({x})")
        builder.add_step(
            desc="Formula de la densidad Normal",
            latex=rf"f(x) = \frac{{1}}{{\sigma\sqrt{{2\pi}}}} \cdot e^{{-\frac{{1}}{{2}}\left(\frac{{x-\mu}}{{\sigma}}\right)^2}}",
            level_min=1,
        )
        builder.add_step(
            desc=f"Z = (x − μ) / σ = ({x} − {mu}) / {sigma} = {format_number(z, 4)}",
            latex=rf"Z = \frac{{{x} - {mu}}}{{{sigma}}} = {format_number(z, 4)}",
            result=z, level_min=2,
        )
        builder.add_step(
            desc=f"f({x}) = {format_number(fval, 6)}",
            latex=(rf"f({x}) = \frac{{1}}{{{format_number(sigma)}\sqrt{{2\pi}}}}"
                   rf" \cdot e^{{-\frac{{{format_number(z, 4)}^2}}{{2}}}} = {format_number(fval, 6)}"),
            result=fval, level_min=1,
        )
        return builder.build(final_value=fval, final_latex=rf"f({x}) = {format_number(fval, 6)}")

    # ------------------------------------------------------------------
    def cdf_left(self, x: float):
        mu, sigma = self.mu, self.sigma
        z = (x - mu) / sigma
        fx = float(self._dist.cdf(x))
        builder = StepBuilder(f"F({x})")
        builder.add_step(
            desc="F(x) = P(VA ≤ x) = Φ(Z),  Z = (x − μ) / σ",
            latex=rf"F(x) = \Phi\!\left(\frac{{x - \mu}}{{\sigma}}\right)",
            level_min=1,
        )
        builder.add_step(
            desc=f"Z = ({x} − {mu}) / {sigma} = {format_number(z, 4)}",
            latex=rf"Z = \frac{{{x} - {mu}}}{{{sigma}}} = {format_number(z, 4)}",
            result=z, level_min=1,
        )
        if z >= 0:
            builder.add_step(
                desc=f"F({x}) = Φ({format_number(z, 4)}) = {format_number(fx, 6)}",
                latex=rf"F({x}) = \Phi({format_number(z, 4)}) = {format_number(fx, 6)}",
                result=fx, level_min=1,
            )
        else:
            builder.add_step(
                desc=f"Z negativo → Φ(Z) = 1 − Φ(−Z) = 1 − Φ({format_number(-z, 4)})",
                latex=(rf"F({x}) = \Phi({format_number(z, 4)}) = 1 - \Phi({format_number(-z, 4)})"
                       rf" = 1 - {format_number(1 - fx, 6)} = {format_number(fx, 6)}"),
                result=fx, level_min=2,
            )
            builder.add_step(
                desc=f"F({x}) = {format_number(fx, 6)}",
                latex=rf"F({x}) = {format_number(fx, 6)}",
                result=fx, level_min=1,
            )
        return builder.build(final_value=fx, final_latex=rf"F({x}) = {format_number(fx, 6)}")

    # ------------------------------------------------------------------
    def mean(self):
        builder = StepBuilder("Esperanza Matematica")
        builder.add_step(desc="Para la Normal, E(X) = μ  (parámetro directo)",
                         latex=r"E(X) = \mu", level_min=1)
        builder.add_step(desc=f"E(X) = {format_number(self.mu)}",
                         latex=rf"E(X) = {format_number(self.mu)}", result=self.mu, level_min=2)
        return builder.build(final_value=self.mu, final_latex=rf"\mu = {format_number(self.mu)}")

    def variance(self):
        var = self.sigma ** 2
        builder = StepBuilder("Varianza")
        builder.add_step(desc="Para la Normal, V(X) = σ²",
                         latex=r"V(X) = \sigma^2", level_min=1)
        builder.add_step(desc=f"V(X) = {self.sigma}² = {format_number(var)}",
                         latex=rf"V(X) = {self.sigma}^2 = {format_number(var)}", result=var, level_min=2)
        return builder.build(final_value=var, final_latex=rf"\sigma^2 = {format_number(var)}")

    def std_dev(self):
        builder = StepBuilder("Desvio Estandar")
        builder.add_step(desc="Para la Normal, D(X) = σ  (parámetro directo)",
                         latex=r"D(X) = \sigma", level_min=1)
        builder.add_step(desc=f"σ = {format_number(self.sigma)}",
                         latex=rf"\sigma = {format_number(self.sigma)}", result=self.sigma, level_min=2)
        return builder.build(final_value=self.sigma, final_latex=rf"\sigma = {format_number(self.sigma)}")

    def mode(self):
        builder = StepBuilder("Moda")
        builder.add_step(desc="Normal simétrica: Mo = Me = μ",
                         latex=r"Mo = \mu", level_min=1)
        builder.add_step(desc=f"Mo = {format_number(self.mu)}", latex=rf"Mo = {format_number(self.mu)}", result=self.mu, level_min=2)
        return builder.build(final_value=self.mu, final_latex=rf"Mo = {format_number(self.mu)}")

    def median(self):
        builder = StepBuilder("Mediana")
        builder.add_step(desc="Normal simétrica: Me = μ",
                         latex=r"Me = \mu", level_min=1)
        builder.add_step(desc=f"Me = {format_number(self.mu)}", latex=rf"Me = {format_number(self.mu)}", result=self.mu, level_min=2)
        return builder.build(final_value=self.mu, final_latex=rf"Me = {format_number(self.mu)}")

    def skewness(self):
        builder = StepBuilder("Coeficiente de Asimetria")
        builder.add_step(desc="La Normal es perfectamente simétrica: As = 0",
                         latex=r"As = \alpha_3 = 0", level_min=1)
        return builder.build(final_value=0.0, final_latex=r"As = 0")

    def kurtosis(self):
        builder = StepBuilder("Coeficiente de Kurtosis")
        builder.add_step(desc="La Normal es mesocúrtica: Ku = 3",
                         latex=r"Ku = \alpha_4 = 3", level_min=1)
        return builder.build(final_value=3.0, final_latex=r"Ku = 3")

    # ------------------------------------------------------------------
    def fractile(self, alpha: float):
        x_alpha = float(self._dist.ppf(alpha))
        z_alpha = (x_alpha - self.mu) / self.sigma
        builder = StepBuilder(f"x({alpha})")
        builder.add_step(
            desc=f"x(α) tal que F(x(α)) = α = {alpha}",
            latex=rf"x(\alpha) = \mu + Z(\alpha) \cdot \sigma",
            level_min=1,
        )
        builder.add_step(
            desc=f"De tabla Normal estándar: Z({alpha}) = {format_number(z_alpha, 4)}",
            latex=rf"Z({alpha}) = {format_number(z_alpha, 4)}",
            result=z_alpha, level_min=2,
        )
        builder.add_step(
            desc=f"x({alpha}) = {self.mu} + {format_number(z_alpha, 4)} × {self.sigma} = {format_number(x_alpha, 4)}",
            latex=rf"x({alpha}) = {format_number(self.mu)} + {format_number(z_alpha, 4)} \cdot {format_number(self.sigma)} = {format_number(x_alpha, 4)}",
            result=x_alpha, level_min=1,
        )
        return builder.build(final_value=x_alpha, final_latex=rf"x({alpha}) = {format_number(x_alpha, 4)}")

    def partial_expectation_left(self, x: float):
        from scipy.stats import norm
        mu, sigma = self.mu, self.sigma
        z = (x - mu) / sigma
        phi_z = float(norm.cdf(z))
        phi_pdf_z = float(norm.pdf(z))
        h = mu * phi_z - sigma * phi_pdf_z
        builder = StepBuilder(f"H({x})")
        builder.add_step(
            desc="H(x) = μ·Φ(Z) − σ·φ(Z),   Z = (x−μ)/σ",
            latex=rf"H(x) = \mu \cdot \Phi(Z) - \sigma \cdot \varphi(Z)",
            level_min=1,
        )
        builder.add_step(
            desc=f"Z = ({x} − {mu}) / {sigma} = {format_number(z, 4)}",
            latex=rf"Z = {format_number(z, 4)}", result=z, level_min=2,
        )
        builder.add_step(
            desc=f"H({x}) = {mu}·{format_number(phi_z, 6)} − {sigma}·{format_number(phi_pdf_z, 6)} = {format_number(h, 6)}",
            latex=(rf"H({x}) = {format_number(mu)} \cdot {format_number(phi_z, 6)}"
                   rf" - {format_number(sigma)} \cdot {format_number(phi_pdf_z, 6)}"
                   rf" = {format_number(h, 6)}"),
            result=h, level_min=2,
        )
        return builder.build(final_value=h, final_latex=rf"H({x}) = {format_number(h, 6)}")

    def display_domain(self):
        return self.mu - 4 * self.sigma, self.mu + 4 * self.sigma
