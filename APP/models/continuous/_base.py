"""Clase base compartida para todos los modelos continuos."""

import math
from scipy import integrate as _quad
from models.base import ContinuousModel
from calculation.step_engine import StepBuilder
from calculation.statistics_common import format_number


class ContinuousBase(ContinuousModel):
    """
    Provee implementaciones default para cdf_right, std_dev, cv,
    partial_expectation_left y fractile.
    Los modelos concretos sólo sobreescriben lo que es específico.
    """

    # ------------------------------------------------------------------
    # cdf_right — default: G(x) = 1 - F(x)
    # ------------------------------------------------------------------

    def cdf_right(self, x: float):
        fx_res = self.cdf_left(x)
        gx = max(0.0, 1.0 - fx_res.final_value)
        builder = StepBuilder(f"G({x})")
        builder.add_step(
            desc="G(x) = P(VA ≥ x) = 1 − F(x)",
            latex=r"G(x) = 1 - F(x)",
            level_min=1,
        )
        builder.add_step(
            desc=f"G({x}) = 1 − {format_number(fx_res.final_value, 6)} = {format_number(gx, 6)}",
            latex=(rf"G({x}) = 1 - {format_number(fx_res.final_value, 6)}"
                   rf" = {format_number(gx, 6)}"),
            result=gx,
            level_min=1,
        )
        return builder.build(final_value=gx, final_latex=rf"G({x}) = {format_number(gx, 6)}")

    # ------------------------------------------------------------------
    # std_dev — default: σ = √V(X)
    # ------------------------------------------------------------------

    def std_dev(self):
        var = self.variance().final_value
        sigma = math.sqrt(max(0.0, var))
        builder = StepBuilder("Desvio Estandar")
        builder.add_step(
            desc="D(X) = σ = √V(X)",
            latex=r"D(X) = \sigma = \sqrt{V(X)}",
            level_min=1,
        )
        builder.add_step(
            desc=f"σ = √{format_number(var)} = {format_number(sigma)}",
            latex=rf"\sigma = \sqrt{{{format_number(var)}}} = {format_number(sigma)}",
            result=sigma,
            level_min=2,
        )
        return builder.build(final_value=sigma, final_latex=rf"\sigma = {format_number(sigma)}")

    # ------------------------------------------------------------------
    # cv — default: Cv = (σ / |μ|) × 100
    # ------------------------------------------------------------------

    def cv(self):
        mu = self.mean().final_value
        sigma = self.std_dev().final_value
        cv_val = (sigma / abs(mu) * 100) if abs(mu) > 1e-15 else float("inf")
        builder = StepBuilder("Coeficiente de Variacion")
        builder.add_step(
            desc="Cv = (σ / |μ|) × 100",
            latex=r"Cv = \frac{\sigma}{|\mu|} \cdot 100",
            level_min=1,
        )
        builder.add_step(
            desc=f"Cv = ({format_number(sigma)} / {format_number(abs(mu))}) × 100 = {format_number(cv_val)}%",
            latex=(rf"Cv = \frac{{{format_number(sigma)}}}{{{format_number(abs(mu))}}}"
                   rf" \cdot 100 = {format_number(cv_val)}\%"),
            result=cv_val,
            level_min=2,
        )
        return builder.build(final_value=cv_val, final_latex=rf"Cv = {format_number(cv_val)}\%")

    # ------------------------------------------------------------------
    # partial_expectation_left — default: integración numérica
    # ------------------------------------------------------------------

    def partial_expectation_left(self, x: float):
        d_min, _ = self.domain()
        sigma = self.std_dev().final_value
        lower = d_min if not math.isinf(d_min) else x - 20 * max(sigma, 1.0)
        try:
            hval, _ = _quad.quad(
                lambda t: t * self.density_value(t), lower, x,
                limit=300, epsabs=1e-8, epsrel=1e-8,
            )
        except Exception:
            hval = float("nan")
        builder = StepBuilder(f"H({x})")
        builder.add_step(
            desc=f"H({x}) = ∫ t·f(t) dt  de −∞ a {x}",
            latex=rf"H({x}) = \int_{{-\infty}}^{{{x}}} t \cdot f(t)\, dt",
            level_min=1,
        )
        builder.add_step(
            desc=f"H({x}) ≈ {format_number(hval, 6)}  (integración numérica)",
            latex=rf"H({x}) = {format_number(hval, 6)}",
            result=hval,
            level_min=1,
        )
        return builder.build(final_value=hval, final_latex=rf"H({x}) = {format_number(hval, 6)}")

    # ------------------------------------------------------------------
    # fractile — default via _dist.ppf (scipy rv_continuous)
    # ------------------------------------------------------------------

    def fractile(self, alpha: float):
        if not hasattr(self, "_dist"):
            raise NotImplementedError("fractile requiere atributo _dist (scipy rv)")
        x_alpha = float(self._dist.ppf(alpha))
        builder = StepBuilder(f"x({alpha})")
        builder.add_step(
            desc=f"Fractil x(α) tal que F(x(α)) = α = {alpha}",
            latex=rf"F\!\left(x(\alpha)\right) = \alpha = {alpha}",
            level_min=1,
        )
        builder.add_step(
            desc=f"x({alpha}) = {format_number(x_alpha, 6)}",
            latex=rf"x({alpha}) = {format_number(x_alpha, 6)}",
            result=x_alpha,
            level_min=1,
        )
        return builder.build(final_value=x_alpha, final_latex=rf"x({alpha}) = {format_number(x_alpha, 6)}")

    # ------------------------------------------------------------------
    # display_domain — rango visual sugerido para gráficos
    # ------------------------------------------------------------------

    def display_domain(self):
        """Retorna (x_low, x_high) para graficar — puede sobreescribirse."""
        mu = self.mean().final_value
        sigma = self.std_dev().final_value
        d_min, d_max = self.domain()
        lo = max(d_min, mu - 4 * sigma) if not math.isinf(d_min) else mu - 4 * sigma
        hi = min(d_max, mu + 4 * sigma) if not math.isinf(d_max) else mu + 4 * sigma
        return lo, hi
