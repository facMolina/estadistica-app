"""Distribucion Gamma / Erlang."""

import math
from scipy import stats as _st
from scipy.special import gamma as _gamma_fn
from models.continuous._base import ContinuousBase
from calculation.step_engine import StepBuilder
from calculation.statistics_common import format_number


class Gamma(ContinuousBase):
    """
    Gamma(r, λ): f(x) = λ^r · x^(r−1) · e^(−λx) / Γ(r),  x ≥ 0.
    Si r es entero → Erlang.  Parámetros UADE: r (forma), λ (tasa).
    scipy: gamma(a=r, scale=1/λ)
    """

    def __init__(self, r: float, lam: float):
        if r <= 0:
            raise ValueError("r (forma) debe ser > 0")
        if lam <= 0:
            raise ValueError("λ (tasa) debe ser > 0")
        self.r = r
        self.lam = lam
        self._dist = _st.gamma(a=r, scale=1.0 / lam)

    def name(self):    return "Gamma"
    def params_dict(self): return {"r": self.r, "lambda": self.lam}
    def domain(self):  return (0.0, math.inf)

    def latex_formula(self):
        return (rf"f(x) = \frac{{\lambda^r \cdot x^{{r-1}} \cdot e^{{-\lambda x}}}}{{\Gamma(r)}}"
                rf",\quad x \geq 0")

    # ------------------------------------------------------------------
    def density_value(self, x: float) -> float:
        return float(self._dist.pdf(x)) if x >= 0 else 0.0

    def density(self, x: float):
        r, lam = self.r, self.lam
        fval = self.density_value(x)
        gamma_r = _gamma_fn(r)
        builder = StepBuilder(f"f({x})")
        builder.add_step(
            desc="f(x) = λ^r · x^(r−1) · e^(−λx) / Γ(r)",
            latex=rf"f(x) = \frac{{\lambda^r \cdot x^{{r-1}} \cdot e^{{-\lambda x}}}}{{\Gamma(r)}}",
            level_min=1,
        )
        builder.add_step(
            desc=f"Γ({r}) = {format_number(gamma_r, 4)}",
            latex=rf"\Gamma({r}) = {format_number(gamma_r, 4)}",
            result=gamma_r, level_min=3,
        )
        builder.add_step(
            desc=f"f({x}) = {format_number(fval, 6)}",
            latex=(rf"f({x}) = \frac{{{format_number(lam)}^{{{r}}} \cdot {x}^{{{r}-1}}"
                   rf" \cdot e^{{-{format_number(lam)} \cdot {x}}}}}{{{format_number(gamma_r, 4)}}}"
                   rf" = {format_number(fval, 6)}"),
            result=fval, level_min=1,
        )
        return builder.build(final_value=fval, final_latex=rf"f({x}) = {format_number(fval, 6)}")

    # ------------------------------------------------------------------
    def cdf_left(self, x: float):
        r, lam = self.r, self.lam
        fx = float(self._dist.cdf(x)) if x >= 0 else 0.0
        builder = StepBuilder(f"F({x})")
        builder.add_step(
            desc="F(x) = Γ_incompleta_regularizada(r, λx) — calculada con función especial",
            latex=rf"F(x) = I(\lambda x;\, r) = \frac{{\gamma(r,\, \lambda x)}}{{\Gamma(r)}}",
            level_min=1,
        )
        builder.add_step(
            desc=f"λx = {lam} × {x} = {format_number(lam * x, 4)}",
            latex=rf"\lambda x = {format_number(lam)} \cdot {x} = {format_number(lam * x, 4)}",
            result=lam * x, level_min=2,
        )
        builder.add_step(
            desc=f"F({x}) = {format_number(fx, 6)}",
            latex=rf"F({x}) = {format_number(fx, 6)}",
            result=fx, level_min=1,
        )
        return builder.build(final_value=fx, final_latex=rf"F({x}) = {format_number(fx, 6)}")

    # ------------------------------------------------------------------
    def mean(self):
        mu = self.r / self.lam
        builder = StepBuilder("Esperanza Matematica")
        builder.add_step(desc="E(X) = r / λ", latex=r"E(X) = \frac{r}{\lambda}", level_min=1)
        builder.add_step(
            desc=f"E(X) = {self.r} / {self.lam} = {format_number(mu)}",
            latex=rf"E(X) = \frac{{{self.r}}}{{{format_number(self.lam)}}} = {format_number(mu)}",
            result=mu, level_min=2,
        )
        return builder.build(final_value=mu, final_latex=rf"E(X) = {format_number(mu)}")

    def variance(self):
        var = self.r / self.lam ** 2
        builder = StepBuilder("Varianza")
        builder.add_step(desc="V(X) = r / λ²", latex=r"V(X) = \frac{r}{\lambda^2}", level_min=1)
        builder.add_step(
            desc=f"V(X) = {self.r} / {self.lam}² = {format_number(var)}",
            latex=rf"V(X) = \frac{{{self.r}}}{{{format_number(self.lam)}^2}} = {format_number(var)}",
            result=var, level_min=2,
        )
        return builder.build(final_value=var, final_latex=rf"V(X) = {format_number(var)}")

    def mode(self):
        mo = (self.r - 1) / self.lam if self.r >= 1 else 0.0
        builder = StepBuilder("Moda")
        if self.r >= 1:
            builder.add_step(desc="Mo = (r − 1) / λ  (para r ≥ 1)",
                             latex=r"Mo = \frac{r - 1}{\lambda}", level_min=1)
            builder.add_step(
                desc=f"Mo = ({self.r} − 1) / {self.lam} = {format_number(mo)}",
                latex=rf"Mo = \frac{{{self.r} - 1}}{{{format_number(self.lam)}}} = {format_number(mo)}",
                result=mo, level_min=2,
            )
        else:
            builder.add_step(desc="Mo = 0  (para r < 1, densidad decreciente)", level_min=1)
        return builder.build(final_value=mo, final_latex=rf"Mo = {format_number(mo)}")

    def median(self):
        me = float(self._dist.ppf(0.5))
        builder = StepBuilder("Mediana")
        builder.add_step(desc="Me: F(Me) = 0.5 — solución numérica via función incompleta gamma",
                         latex=r"F(Me) = 0.5", level_min=1)
        builder.add_step(desc=f"Me ≈ {format_number(me)}", result=me, level_min=2)
        return builder.build(final_value=me, final_latex=rf"Me \approx {format_number(me)}")

    def skewness(self):
        a3 = 2.0 / math.sqrt(self.r)
        builder = StepBuilder("Coeficiente de Asimetria")
        builder.add_step(desc="As = 2/√r", latex=r"As = \frac{2}{\sqrt{r}}", level_min=1)
        builder.add_step(
            desc=f"As = 2/√{self.r} = {format_number(a3)}",
            latex=rf"As = \frac{{2}}{{\sqrt{{{self.r}}}}} = {format_number(a3)}",
            result=a3, level_min=2,
        )
        return builder.build(final_value=a3, final_latex=rf"As = {format_number(a3)}")

    def kurtosis(self):
        ku = 3.0 + 6.0 / self.r
        builder = StepBuilder("Coeficiente de Kurtosis")
        builder.add_step(desc="Ku = 3 + 6/r", latex=r"Ku = 3 + \frac{6}{r}", level_min=1)
        builder.add_step(
            desc=f"Ku = 3 + 6/{self.r} = {format_number(ku)}",
            latex=rf"Ku = 3 + \frac{{6}}{{{self.r}}} = {format_number(ku)}",
            result=ku, level_min=2,
        )
        return builder.build(final_value=ku, final_latex=rf"Ku = {format_number(ku)}")

    def display_domain(self):
        mu = self.r / self.lam
        sigma = math.sqrt(self.r) / self.lam
        return 0.0, mu + 4 * sigma
