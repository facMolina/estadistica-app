"""Distribucion Log-Normal."""

import math
from scipy import stats as _st
from models.continuous._base import ContinuousBase
from calculation.step_engine import StepBuilder
from calculation.statistics_common import format_number


class LogNormal(ContinuousBase):
    """
    Log-Normal(m, D): si X~LogNormal, entonces Y = ln(X) ~ Normal(m, D).
    Parámetros UADE: m = media del logaritmo, D = desvio del logaritmo.
    scipy: lognorm(s=D, scale=exp(m))
    """

    def __init__(self, m: float, D: float):
        if D <= 0:
            raise ValueError("D (desvio del logaritmo) debe ser > 0")
        self.m = m
        self.D = D
        self._dist = _st.lognorm(s=D, scale=math.exp(m))

    def name(self):    return "Log-Normal"
    def params_dict(self): return {"m": self.m, "D": self.D}
    def domain(self):  return (0.0, math.inf)

    def latex_formula(self):
        return (rf"f(x) = \frac{{1}}{{D \cdot x \cdot \sqrt{{2\pi}}}}"
                rf" \cdot e^{{-\frac{{(\ln x - m)^2}}{{2D^2}}}}, \quad x > 0")

    # ------------------------------------------------------------------
    def density_value(self, x: float) -> float:
        return float(self._dist.pdf(x)) if x > 0 else 0.0

    def density(self, x: float):
        m, D = self.m, self.D
        fval = self.density_value(x)
        builder = StepBuilder(f"f({x})")
        builder.add_step(
            desc="Densidad Log-Normal",
            latex=rf"f(x) = \frac{{1}}{{D \cdot x \cdot \sqrt{{2\pi}}}} \cdot e^{{-\frac{{(\ln x - m)^2}}{{2D^2}}}}",
            level_min=1,
        )
        if x > 0:
            ln_x = math.log(x)
            builder.add_step(
                desc=f"ln({x}) = {format_number(ln_x, 4)}",
                latex=rf"\ln({x}) = {format_number(ln_x, 4)}", result=ln_x, level_min=2,
            )
        builder.add_step(
            desc=f"f({x}) = {format_number(fval, 6)}",
            latex=rf"f({x}) = {format_number(fval, 6)}", result=fval, level_min=1,
        )
        return builder.build(final_value=fval, final_latex=rf"f({x}) = {format_number(fval, 6)}")

    # ------------------------------------------------------------------
    def cdf_left(self, x: float):
        m, D = self.m, self.D
        fx = float(self._dist.cdf(x)) if x > 0 else 0.0
        builder = StepBuilder(f"F({x})")
        builder.add_step(
            desc="F(x) = Φ((ln x − m) / D)",
            latex=rf"F(x) = \Phi\!\left(\frac{{\ln x - m}}{{D}}\right)",
            level_min=1,
        )
        if x > 0:
            ln_x = math.log(x)
            z = (ln_x - m) / D
            builder.add_step(
                desc=f"Y = ln({x}) = {format_number(ln_x, 4)}",
                latex=rf"Y = \ln({x}) = {format_number(ln_x, 4)}", result=ln_x, level_min=2,
            )
            builder.add_step(
                desc=f"Z = (Y − m) / D = ({format_number(ln_x, 4)} − {m}) / {D} = {format_number(z, 4)}",
                latex=rf"Z = \frac{{{format_number(ln_x, 4)} - {m}}}{{{D}}} = {format_number(z, 4)}",
                result=z, level_min=1,
            )
            sign_note = "" if z >= 0 else f"  [Z negativo → Φ(Z) = 1 − Φ({format_number(-z, 4)})]"
            builder.add_step(
                desc=f"F({x}) = Φ({format_number(z, 4)}) = {format_number(fx, 6)}{sign_note}",
                latex=rf"F({x}) = \Phi({format_number(z, 4)}) = {format_number(fx, 6)}",
                result=fx, level_min=1,
            )
        else:
            builder.add_step(desc="x ≤ 0: F(x) = 0", latex="F(x) = 0", result=0.0, level_min=1)
        return builder.build(final_value=fx, final_latex=rf"F({x}) = {format_number(fx, 6)}")

    # ------------------------------------------------------------------
    def mean(self):
        m, D = self.m, self.D
        mu = math.exp(m + D ** 2 / 2)
        builder = StepBuilder("Esperanza Matematica")
        builder.add_step(desc="E(X) = e^(m + D²/2)", latex=r"E(X) = e^{m + D^2/2}", level_min=1)
        builder.add_step(
            desc=f"E(X) = e^({m} + {D}²/2) = e^{format_number(m + D**2/2, 4)} = {format_number(mu)}",
            latex=rf"E(X) = e^{{{format_number(m + D**2/2, 4)}}} = {format_number(mu)}",
            result=mu, level_min=2,
        )
        return builder.build(final_value=mu, final_latex=rf"E(X) = {format_number(mu)}")

    def variance(self):
        m, D = self.m, self.D
        mu = math.exp(m + D ** 2 / 2)
        var = mu ** 2 * (math.exp(D ** 2) - 1)
        builder = StepBuilder("Varianza")
        builder.add_step(desc="V(X) = E(X)² · (e^(D²) − 1)", latex=r"V(X) = E(X)^2 \cdot (e^{D^2} - 1)", level_min=1)
        builder.add_step(
            desc=f"V(X) = {format_number(mu)}² · (e^{D}² − 1) = {format_number(var)}",
            latex=rf"V(X) = {format_number(mu)}^2 \cdot ({format_number(math.exp(D**2), 4)} - 1) = {format_number(var)}",
            result=var, level_min=2,
        )
        return builder.build(final_value=var, final_latex=rf"V(X) = {format_number(var)}")

    def mode(self):
        mo = math.exp(self.m - self.D ** 2)
        builder = StepBuilder("Moda")
        builder.add_step(desc="Mo = e^(m − D²)", latex=r"Mo = e^{m - D^2}", level_min=1)
        builder.add_step(
            desc=f"Mo = e^({self.m} − {self.D}²) = e^{format_number(self.m - self.D**2, 4)} = {format_number(mo)}",
            latex=rf"Mo = e^{{{format_number(self.m - self.D**2, 4)}}} = {format_number(mo)}",
            result=mo, level_min=2,
        )
        return builder.build(final_value=mo, final_latex=rf"Mo = {format_number(mo)}")

    def median(self):
        me = math.exp(self.m)
        builder = StepBuilder("Mediana")
        builder.add_step(desc="Me = e^m", latex=r"Me = e^m", level_min=1)
        builder.add_step(
            desc=f"Me = e^{self.m} = {format_number(me)}",
            latex=rf"Me = e^{{{self.m}}} = {format_number(me)}",
            result=me, level_min=2,
        )
        return builder.build(final_value=me, final_latex=rf"Me = {format_number(me)}")

    def skewness(self):
        D = self.D
        eD2 = math.exp(D ** 2)
        a3 = (eD2 + 2) * math.sqrt(eD2 - 1)
        builder = StepBuilder("Coeficiente de Asimetria")
        builder.add_step(desc="As = (e^(D²) + 2) · √(e^(D²) − 1)",
                         latex=r"As = (e^{D^2} + 2)\sqrt{e^{D^2} - 1}", level_min=1)
        builder.add_step(
            desc=f"As = ({format_number(eD2, 4)} + 2) · √({format_number(eD2, 4)} − 1) = {format_number(a3)}",
            latex=rf"As = ({format_number(eD2, 4)} + 2)\sqrt{{{format_number(eD2, 4)} - 1}} = {format_number(a3)}",
            result=a3, level_min=2,
        )
        return builder.build(final_value=a3, final_latex=rf"As = {format_number(a3)}")

    def kurtosis(self):
        D = self.D
        ku = math.exp(4 * D**2) + 2 * math.exp(3 * D**2) + 3 * math.exp(2 * D**2) - 3
        builder = StepBuilder("Coeficiente de Kurtosis")
        builder.add_step(desc="Ku = e^(4D²) + 2e^(3D²) + 3e^(2D²) − 3",
                         latex=r"Ku = e^{4D^2} + 2e^{3D^2} + 3e^{2D^2} - 3", level_min=1)
        builder.add_step(desc=f"Ku = {format_number(ku)}", result=ku, level_min=2)
        return builder.build(final_value=ku, final_latex=rf"Ku = {format_number(ku)}")

    def fractile(self, alpha: float):
        x_alpha = float(self._dist.ppf(alpha))
        ln_x = math.log(x_alpha) if x_alpha > 0 else float("nan")
        z = (ln_x - self.m) / self.D
        builder = StepBuilder(f"x({alpha})")
        builder.add_step(
            desc=f"x(α): F(x(α)) = α = {alpha} → ln(x) = m + Z(α)·D",
            latex=rf"\ln\!\left(x(\alpha)\right) = m + Z(\alpha) \cdot D",
            level_min=1,
        )
        builder.add_step(
            desc=f"Z({alpha}) = {format_number(z, 4)}  (tabla Normal estándar)",
            latex=rf"Z({alpha}) = {format_number(z, 4)}", result=z, level_min=2,
        )
        builder.add_step(
            desc=f"x({alpha}) = e^({self.m} + {format_number(z, 4)}·{self.D}) = {format_number(x_alpha, 4)}",
            latex=rf"x({alpha}) = e^{{{format_number(self.m)} + {format_number(z, 4)} \cdot {format_number(self.D)}}} = {format_number(x_alpha, 4)}",
            result=x_alpha, level_min=1,
        )
        return builder.build(final_value=x_alpha, final_latex=rf"x({alpha}) = {format_number(x_alpha, 4)}")

    def display_domain(self):
        mu = self.mean().final_value
        sigma = self.std_dev().final_value
        return max(0.0, mu - 3 * sigma), mu + 4 * sigma
