"""Modelo de distribucion de Poisson."""

import math
from typing import Tuple, Dict
from models.base import DiscreteModel
from calculation.step_types import CalcResult
from calculation.step_engine import StepBuilder
from calculation.statistics_common import (
    format_number, find_mode_discrete, find_median_discrete,
    compute_cdf_left_discrete,
)
from config.settings import MAX_SUMMATION_TERMS, EPSILON


class Poisson(DiscreteModel):
    """
    Distribucion de Poisson: P(r) = e^(-m) * m^r / r!

    Parametros:
        m: media (lambda * t). Puede construirse como Poisson(m) o Poisson(lam*t).
    Variable: r = numero de ocurrencias (0, 1, 2, ...).
    Dominio infinito — se trunca donde G(r) < EPSILON.
    """

    def __init__(self, m: float):
        if m <= 0:
            raise ValueError("m debe ser > 0")
        self.m = m
        self._domain_max = self._compute_domain_max()

    def _compute_domain_max(self) -> int:
        cum = 0.0
        for r in range(MAX_SUMMATION_TERMS):
            cum += self._prob_raw(r)
            if 1.0 - cum < EPSILON:
                return r
        return MAX_SUMMATION_TERMS - 1

    def _prob_raw(self, r: int) -> float:
        """P(r) numericamente estable via logaritmos."""
        if r < 0:
            return 0.0
        try:
            log_p = -self.m + r * math.log(self.m) - math.lgamma(r + 1)
            return math.exp(log_p)
        except (ValueError, OverflowError):
            return 0.0

    def name(self) -> str:
        return "Poisson"

    def params_dict(self) -> Dict[str, float]:
        return {"m": self.m}

    def domain(self) -> Tuple[int, int]:
        return (0, self._domain_max)

    def latex_formula(self) -> str:
        return (rf"P(r) = \frac{{e^{{-m}} \cdot m^r}}{{r!}}"
                rf" = \frac{{e^{{-{self.m}}} \cdot {self.m}^r}}{{r!}}")

    def probability_value(self, r: int) -> float:
        if r < 0 or r > self._domain_max:
            return 0.0
        return self._prob_raw(r)

    def probability(self, r: int) -> CalcResult:
        m = self.m
        builder = StepBuilder(f"P(r={r})")

        if r < 0:
            builder.add_step(f"r={r} fuera del dominio [0, inf)", level_min=1)
            return builder.build(final_value=0.0, final_latex=f"P(r={r}) = 0")

        builder.add_step(
            desc="Aplicamos la formula del modelo de Poisson",
            latex=rf"P(r) = \frac{{e^{{-m}} \cdot m^r}}{{r!}}",
            level_min=1,
        )
        builder.add_step(
            desc=f"Reemplazamos m={m}, r={r}",
            latex=rf"P(r={r}) = \frac{{e^{{-{m}}} \cdot {m}^{{{r}}}}}{{{r}!}}",
            level_min=2,
        )

        e_val = math.exp(-m)
        m_power = m ** r
        fact_r = math.factorial(r)
        builder.add_step(
            desc=f"e^(-{m}) = {format_number(e_val)}",
            latex=rf"e^{{-{m}}} = {format_number(e_val)}",
            result=e_val,
            level_min=3,
        )
        builder.add_step(
            desc=f"{m}^{r} = {format_number(m_power)}",
            latex=rf"{m}^{{{r}}} = {format_number(m_power)}",
            result=m_power,
            level_min=3,
        )
        builder.add_step(
            desc=f"{r}! = {fact_r}",
            latex=rf"{r}! = {fact_r}",
            result=float(fact_r),
            level_min=3,
        )

        result = self._prob_raw(r)
        builder.add_step(
            desc=f"Resultado: P(r={r}) = {format_number(e_val)} * {format_number(m_power)} / {fact_r}",
            latex=rf"P(r={r}) = \frac{{{format_number(e_val)} \cdot {format_number(m_power)}}}{{{fact_r}}} = {format_number(result, 6)}",
            result=result,
            level_min=2,
        )

        return builder.build(
            final_value=result,
            final_latex=rf"P_{{po}}(r={r} \,/\, m={m}) = {format_number(result, 6)}",
        )

    def cdf_left(self, r: int) -> CalcResult:
        m = self.m
        builder = StepBuilder(f"F({r})")
        builder.add_step(
            desc=f"F({r}) = P(VA <= {r}) = suma de P(x) para x = 0 hasta {r}",
            latex=rf"F_{{po}}({r}\,/\,{m}) = \sum_{{x=0}}^{{{r}}} \frac{{e^{{-{m}}} \cdot {m}^x}}{{x!}}",
            level_min=1,
        )
        total = 0.0
        for x in range(0, r + 1):
            px = self.probability_value(x)
            total += px
            builder.add_step(
                desc=f"P(r={x}) = {format_number(px, 6)}",
                latex=rf"P(r={x}) = {format_number(px, 6)}",
                result=px,
                level_min=3,
            )
        builder.add_step(
            desc=f"F({r}) = {format_number(total, 6)}",
            latex=rf"F_{{po}}({r}\,/\,{m}) = {format_number(total, 6)}",
            result=total,
            level_min=1,
        )
        return builder.build(
            final_value=total,
            final_latex=rf"F_{{po}}({r}\,/\,{m}) = {format_number(total, 6)}",
        )

    def cdf_right(self, r: int) -> CalcResult:
        m = self.m
        d_max = self._domain_max
        builder = StepBuilder(f"G({r})")
        builder.add_step(
            desc=f"G({r}) = P(VA >= {r}) = suma de P(x) para x = {r} hasta infinito (truncado en {d_max})",
            latex=rf"G_{{po}}({r}\,/\,{m}) = \sum_{{x={r}}}^{{\infty}} \frac{{e^{{-{m}}} \cdot {m}^x}}{{x!}}",
            level_min=1,
        )
        total = 0.0
        for x in range(max(r, 0), d_max + 1):
            px = self.probability_value(x)
            total += px
            builder.add_step(
                desc=f"P(r={x}) = {format_number(px, 6)}",
                latex=rf"P(r={x}) = {format_number(px, 6)}",
                result=px,
                level_min=3,
            )
        builder.add_step(
            desc=f"G({r}) = {format_number(total, 6)}",
            latex=rf"G_{{po}}({r}\,/\,{m}) = {format_number(total, 6)}",
            result=total,
            level_min=1,
        )
        return builder.build(
            final_value=total,
            final_latex=rf"G_{{po}}({r}\,/\,{m}) = {format_number(total, 6)}",
        )

    def mean(self) -> CalcResult:
        m = self.m
        builder = StepBuilder("Esperanza Matematica")
        builder.add_step(
            desc="Para Poisson, la esperanza coincide con el parametro m",
            latex=rf"E(r) = \mu = m",
            level_min=1,
        )
        builder.add_step(
            desc=f"E(r) = m = {m}",
            latex=rf"E(r) = {m}",
            result=m,
            level_min=2,
        )
        return builder.build(final_value=m, final_latex=rf"\mu = {m}")

    def variance(self) -> CalcResult:
        m = self.m
        builder = StepBuilder("Varianza")
        builder.add_step(
            desc="Propiedad de Poisson: la varianza coincide con la media (E = V = m)",
            latex=rf"V(r) = \sigma^2 = m",
            level_min=1,
        )
        builder.add_step(
            desc=f"V(r) = m = {m}",
            latex=rf"V(r) = {m}",
            result=m,
            level_min=2,
        )
        return builder.build(final_value=m, final_latex=rf"\sigma^2 = {m}")

    def std_dev(self) -> CalcResult:
        m = self.m
        sigma = math.sqrt(m)
        builder = StepBuilder("Desvio Estandar")
        builder.add_step(
            desc="D(r) = raiz cuadrada de la varianza = sqrt(m)",
            latex=rf"D(r) = \sigma = \sqrt{{m}}",
            level_min=1,
        )
        builder.add_step(
            desc=f"sigma = sqrt({m}) = {format_number(sigma)}",
            latex=rf"\sigma = \sqrt{{{m}}} = {format_number(sigma)}",
            result=sigma,
            level_min=2,
        )
        return builder.build(final_value=sigma, final_latex=rf"\sigma = {format_number(sigma)}")

    def mode(self) -> CalcResult:
        m = self.m
        builder = StepBuilder("Moda")
        if float(m) == int(m):
            mo_low = int(m) - 1
            mo_high = int(m)
            builder.add_step(
                desc=f"Cuando m es entero hay dos modas: m-1 = {mo_low} y m = {mo_high}",
                latex=rf"Mo = m - 1 = {mo_low} \quad \text{{y}} \quad Mo = m = {mo_high}",
                level_min=2,
            )
            mo = mo_high
        else:
            mo = int(m)  # floor(m)
            builder.add_step(
                desc="La moda de Poisson es la parte entera de m: Mo = floor(m)",
                latex=rf"Mo = \lfloor m \rfloor = \lfloor {m} \rfloor = {mo}",
                level_min=2,
            )
        builder.add_step(
            desc=f"Mo = {mo}",
            latex=rf"Mo = {mo}",
            result=float(mo),
            level_min=1,
        )
        return builder.build(final_value=float(mo), final_latex=rf"Mo = {mo}")

    def median(self) -> CalcResult:
        me = find_median_discrete(
            lambda r: compute_cdf_left_discrete(self.probability_value, r, 0),
            0, self._domain_max,
        )
        builder = StepBuilder("Mediana")
        builder.add_step(
            desc="Menor r tal que F(r) >= 0.5",
            latex=rf"Me: \text{{menor }} r \text{{ tal que }} F(r) \geq 0.5",
            level_min=2,
        )
        f_me_minus_1 = compute_cdf_left_discrete(self.probability_value, me - 1, 0) if me > 0 else 0.0
        f_me = compute_cdf_left_discrete(self.probability_value, me, 0)
        builder.add_step(
            desc=f"F({me-1}) = {format_number(f_me_minus_1)} <= 0.5 y F({me}) = {format_number(f_me)} >= 0.5",
            latex=rf"F({me-1}) = {format_number(f_me_minus_1)} \leq 0.5 \quad y \quad F({me}) = {format_number(f_me)} \geq 0.5",
            level_min=2,
        )
        builder.add_step(
            desc=f"Me = {me}",
            latex=rf"Me = {me}",
            result=float(me),
            level_min=1,
        )
        return builder.build(final_value=float(me), final_latex=rf"Me = {me}")

    def cv(self) -> CalcResult:
        m = self.m
        sigma = math.sqrt(m)
        cv_val = (sigma / m * 100) if m != 0 else float("inf")
        builder = StepBuilder("Coeficiente de Variacion")
        builder.add_step(
            desc="Para Poisson: Cv = sigma/mu * 100 = sqrt(m)/m * 100 = 100/sqrt(m)",
            latex=rf"Cv = \frac{{\sigma}}{{\mu}} \cdot 100 = \frac{{\sqrt{{m}}}}{{m}} \cdot 100 = \frac{{100}}{{\sqrt{{m}}}}",
            level_min=1,
        )
        builder.add_step(
            desc=f"Cv = 100 / sqrt({m}) = {format_number(cv_val)}%",
            latex=rf"Cv = \frac{{100}}{{\sqrt{{{m}}}}} = {format_number(cv_val)}\%",
            result=cv_val,
            level_min=2,
        )
        return builder.build(final_value=cv_val, final_latex=rf"Cv = {format_number(cv_val)}\%")

    def skewness(self) -> CalcResult:
        m = self.m
        a3 = 1.0 / math.sqrt(m)
        builder = StepBuilder("Coeficiente de Asimetria")
        builder.add_step(
            desc="Para Poisson: As = 1 / sqrt(m)",
            latex=rf"As = \alpha_3 = \frac{{1}}{{\sqrt{{m}}}}",
            level_min=1,
        )
        builder.add_step(
            desc=f"As = 1 / sqrt({m}) = {format_number(a3)}",
            latex=rf"As = \frac{{1}}{{\sqrt{{{m}}}}} = {format_number(a3)}",
            result=a3,
            level_min=2,
        )
        builder.add_step(
            desc="Poisson siempre tiene asimetria positiva (cola derecha)",
            level_min=1,
        )
        return builder.build(final_value=a3, final_latex=rf"As = {format_number(a3)}")

    def kurtosis(self) -> CalcResult:
        m = self.m
        ku = 3.0 + 1.0 / m
        builder = StepBuilder("Coeficiente de Kurtosis")
        builder.add_step(
            desc="Para Poisson: Ku = 3 + 1/m",
            latex=rf"Ku = \alpha_4 = 3 + \frac{{1}}{{m}}",
            level_min=1,
        )
        builder.add_step(
            desc=f"Ku = 3 + 1/{m} = {format_number(ku)}",
            latex=rf"Ku = 3 + \frac{{1}}{{{m}}} = {format_number(ku)}",
            result=ku,
            level_min=2,
        )
        builder.add_step(
            desc="Leptocurtica (Ku > 3, mas apuntada que la Normal)",
            level_min=1,
        )
        return builder.build(final_value=ku, final_latex=rf"Ku = {format_number(ku)}")

    def partial_expectation_left(self, r: int) -> CalcResult:
        m = self.m
        builder = StepBuilder(f"H({r})")
        builder.add_step(
            desc=f"Expectativa parcial izquierda H({r}) = suma x*P(x) para x = 0 hasta {r}",
            latex=rf"H_{{po}}({r}\,/\,{m}) = \sum_{{x=0}}^{{{r}}} x \cdot \frac{{e^{{-{m}}} \cdot {m}^x}}{{x!}}",
            level_min=1,
        )
        builder.add_step(
            desc="Formula directa: H(r) = m * F(r-1/m)",
            latex=rf"H_{{po}}({r}\,/\,{m}) = m \cdot F_{{po}}({r-1}\,/\,{m})",
            level_min=2,
        )
        total = sum(x * self.probability_value(x) for x in range(0, r + 1))
        builder.add_step(
            desc=f"H({r}) = {format_number(total)}",
            latex=rf"H_{{po}}({r}\,/\,{m}) = {format_number(total)}",
            result=total,
            level_min=1,
        )
        return builder.build(
            final_value=total,
            final_latex=rf"H_{{po}}({r}\,/\,{m}) = {format_number(total)}",
        )
