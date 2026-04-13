"""Modelo de distribucion Binomial."""

import math
from typing import Tuple, Dict
from models.base import DiscreteModel
from calculation.step_types import CalcResult
from calculation.step_engine import StepBuilder
from calculation.combinatorics import comb, comb_with_steps
from calculation.statistics_common import (
    format_number, format_fraction, find_mode_discrete,
    find_median_discrete, compute_cdf_left_discrete,
)


class Binomial(DiscreteModel):
    """Distribucion Binomial: P(r) = C(n,r) * p^r * (1-p)^(n-r)."""

    def __init__(self, n: int, p: float):
        if n < 1:
            raise ValueError("n debe ser >= 1")
        if not (0 <= p <= 1):
            raise ValueError("p debe estar entre 0 y 1")
        self.n = n
        self.p = p
        self.q = 1 - p

    def name(self) -> str:
        return "Binomial"

    def params_dict(self) -> Dict[str, float]:
        return {"n": self.n, "p": self.p}

    def domain(self) -> Tuple[int, int]:
        return (0, self.n)

    def latex_formula(self) -> str:
        return (rf"P(r) = \binom{{n}}{{r}} \cdot p^r \cdot (1-p)^{{n-r}}"
                rf" = \binom{{{self.n}}}{{r}} \cdot {self.p}^r \cdot {self.q}^{{{self.n}-r}}")

    # --- Valor numerico puro (sin paso a paso) ---

    def probability_value(self, r: int) -> float:
        if r < 0 or r > self.n:
            return 0.0
        return comb(self.n, r) * (self.p ** r) * (self.q ** (self.n - r))

    # --- Con paso a paso ---

    def probability(self, r: int) -> CalcResult:
        n, p, q = self.n, self.p, self.q
        builder = StepBuilder(f"P(r={r})")

        if r < 0 or r > n:
            builder.add_step(f"r={r} fuera del dominio [0, {n}]", level_min=1)
            return builder.build(final_value=0.0, final_latex=f"P(r={r}) = 0")

        # Nivel 1: formula general
        builder.add_step(
            desc="Aplicamos la formula del modelo Binomial",
            latex=rf"P(r) = \binom{{n}}{{r}} \cdot p^r \cdot (1-p)^{{n-r}}",
            level_min=1,
        )

        # Nivel 2: reemplazo de valores
        builder.add_step(
            desc=f"Reemplazamos n={n}, r={r}, p={p}, q=1-p={q}",
            latex=rf"P(r={r}) = \binom{{{n}}}{{{r}}} \cdot {p}^{{{r}}} \cdot {q}^{{{n - r}}}",
            level_min=2,
        )

        # Nivel 3: calculo del combinatorio
        c_result = comb_with_steps(n, r)
        c_val = c_result.final_value
        builder.add_step(
            desc=f"Calculamos C({n},{r})",
            latex=rf"\binom{{{n}}}{{{r}}}",
            latex_res=rf"= {c_val}",
            result=c_val,
            level_min=2,
        )
        builder.merge_result(c_result, level_min=3)

        # Nivel 3: potencias
        p_power = p ** r
        q_power = q ** (n - r)
        builder.add_step(
            desc=f"Calculamos p^r = {p}^{r} = {format_number(p_power)}",
            latex=rf"{p}^{{{r}}} = {format_number(p_power)}",
            result=p_power,
            level_min=3,
        )
        builder.add_step(
            desc=f"Calculamos q^(n-r) = {q}^{n - r} = {format_number(q_power)}",
            latex=rf"{q}^{{{n - r}}} = {format_number(q_power)}",
            result=q_power,
            level_min=3,
        )

        # Resultado
        result = c_val * p_power * q_power
        builder.add_step(
            desc=f"Resultado: P(r={r}) = {c_val} * {format_number(p_power)} * {format_number(q_power)}",
            latex=rf"P(r={r}) = {c_val} \cdot {format_number(p_power)} \cdot {format_number(q_power)} = {format_number(result, 6)}",
            result=result,
            level_min=2,
        )

        return builder.build(
            final_value=result,
            final_latex=rf"P(r={r}) = {format_number(result, 6)}",
        )

    def cdf_left(self, r: int) -> CalcResult:
        n, p = self.n, self.p
        builder = StepBuilder(f"F({r})")

        builder.add_step(
            desc=f"Funcion de probabilidad acumulada izquierda F({r}) = P(VA <= {r})",
            latex=rf"F_b({r}/{n};{p}) = \sum_{{x=0}}^{{{r}}} \binom{{{n}}}{{x}} \cdot {p}^x \cdot {self.q}^{{{n}-x}}",
            level_min=1,
        )

        total = 0.0
        for x in range(0, min(r, n) + 1):
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
            latex=rf"F_b({r}/{n};{p}) = {format_number(total, 6)}",
            result=total,
            level_min=1,
        )

        return builder.build(
            final_value=total,
            final_latex=rf"F_b({r}/{n};{p}) = {format_number(total, 6)}",
        )

    def cdf_right(self, r: int) -> CalcResult:
        n, p = self.n, self.p
        builder = StepBuilder(f"G({r})")

        builder.add_step(
            desc=f"Funcion de probabilidad acumulada derecha G({r}) = P(VA >= {r})",
            latex=rf"G_b({r}/{n};{p}) = \sum_{{x={r}}}^{{{n}}} \binom{{{n}}}{{x}} \cdot {p}^x \cdot {self.q}^{{{n}-x}}",
            level_min=1,
        )

        total = 0.0
        for x in range(max(r, 0), n + 1):
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
            latex=rf"G_b({r}/{n};{p}) = {format_number(total, 6)}",
            result=total,
            level_min=1,
        )

        return builder.build(
            final_value=total,
            final_latex=rf"G_b({r}/{n};{p}) = {format_number(total, 6)}",
        )

    def mean(self) -> CalcResult:
        n, p = self.n, self.p
        mu = n * p
        builder = StepBuilder("Esperanza Matematica")
        builder.add_step(
            desc="Formula de la esperanza del modelo Binomial",
            latex=rf"E(r) = \mu = n \cdot p",
            level_min=1,
        )
        builder.add_step(
            desc=f"E(r) = {n} * {p} = {format_number(mu)}",
            latex=rf"E(r) = {n} \cdot {p} = {format_number(mu)}",
            result=mu,
            level_min=2,
        )
        return builder.build(final_value=mu, final_latex=rf"\mu = {format_number(mu)}")

    def variance(self) -> CalcResult:
        n, p, q = self.n, self.p, self.q
        var = n * p * q
        builder = StepBuilder("Varianza")
        builder.add_step(
            desc="Formula de la varianza del modelo Binomial",
            latex=rf"V(r) = \sigma^2 = n \cdot p \cdot (1-p)",
            level_min=1,
        )
        builder.add_step(
            desc=f"V(r) = {n} * {p} * {q} = {format_number(var)}",
            latex=rf"V(r) = {n} \cdot {p} \cdot {q} = {format_number(var)}",
            result=var,
            level_min=2,
        )
        return builder.build(final_value=var, final_latex=rf"\sigma^2 = {format_number(var)}")

    def std_dev(self) -> CalcResult:
        var = self.n * self.p * self.q
        sigma = math.sqrt(var)
        builder = StepBuilder("Desvio Estandar")
        builder.add_step(
            desc="Desvio estandar = raiz cuadrada de la varianza",
            latex=rf"D(r) = \sigma = \sqrt{{n \cdot p \cdot (1-p)}}",
            level_min=1,
        )
        builder.add_step(
            desc=f"sigma = sqrt({format_number(var)}) = {format_number(sigma)}",
            latex=rf"\sigma = \sqrt{{{format_number(var)}}} = {format_number(sigma)}",
            result=sigma,
            level_min=2,
        )
        return builder.build(final_value=sigma, final_latex=rf"\sigma = {format_number(sigma)}")

    def mode(self) -> CalcResult:
        n, p, q = self.n, self.p, self.q
        low = n * p - q
        high = n * p + p
        mo = find_mode_discrete(self.probability_value, 0, n)
        builder = StepBuilder("Moda")
        builder.add_step(
            desc="Condicion de la moda del modelo Binomial",
            latex=rf"[n \cdot p - (1-p)] < Mo < (n \cdot p + p)",
            level_min=1,
        )
        builder.add_step(
            desc=f"[{format_number(low)}] < Mo < [{format_number(high)}]",
            latex=rf"[{format_number(low)}] < Mo < [{format_number(high)}]",
            level_min=2,
        )
        builder.add_step(
            desc=f"Mo = {mo}",
            latex=rf"Mo = {mo}",
            result=mo,
            level_min=1,
        )
        return builder.build(final_value=mo, final_latex=rf"Mo = {mo}")

    def median(self) -> CalcResult:
        n, p = self.n, self.p
        me_approx = int(n * p)
        me = find_median_discrete(
            lambda r: compute_cdf_left_discrete(self.probability_value, r, 0),
            0, n
        )
        builder = StepBuilder("Mediana")
        builder.add_step(
            desc="La mediana es la parte entera de n*p (para la mayoria de los casos)",
            latex=rf"Me \approx P.E.(n \cdot p) = P.E.({n} \cdot {p}) = P.E.({format_number(n * p)}) = {me_approx}",
            level_min=2,
        )
        builder.add_step(
            desc=f"Verificamos: F({me}-1) <= 0.5 y F({me}) >= 0.5",
            level_min=2,
        )
        f_me_minus_1 = compute_cdf_left_discrete(self.probability_value, me - 1, 0) if me > 0 else 0
        f_me = compute_cdf_left_discrete(self.probability_value, me, 0)
        builder.add_step(
            desc=f"F({me - 1}) = {format_number(f_me_minus_1)} <= 0.5 y F({me}) = {format_number(f_me)} >= 0.5 ✓",
            latex=rf"F({me - 1}) = {format_number(f_me_minus_1)} \leq 0.5 \quad y \quad F({me}) = {format_number(f_me)} \geq 0.5",
            level_min=2,
        )
        builder.add_step(
            desc=f"Me = {me}",
            latex=rf"Me = {me}",
            result=me,
            level_min=1,
        )
        return builder.build(final_value=me, final_latex=rf"Me = {me}")

    def cv(self) -> CalcResult:
        n, p, q = self.n, self.p, self.q
        mu = n * p
        sigma = math.sqrt(n * p * q)
        cv_val = (sigma / mu * 100) if mu != 0 else float('inf')
        builder = StepBuilder("Coeficiente de Variacion")
        builder.add_step(
            desc="Formula del coeficiente de variacion",
            latex=rf"Cv = \frac{{\sigma}}{{\mu}} \cdot 100",
            level_min=1,
        )
        builder.add_step(
            desc=f"Cv = ({format_number(sigma)} / {format_number(mu)}) * 100 = {format_number(cv_val)}%",
            latex=rf"Cv = \frac{{{format_number(sigma)}}}{{{format_number(mu)}}} \cdot 100 = {format_number(cv_val)}\%",
            result=cv_val,
            level_min=2,
        )
        return builder.build(final_value=cv_val, final_latex=rf"Cv = {format_number(cv_val)}\%")

    def skewness(self) -> CalcResult:
        n, p, q = self.n, self.p, self.q
        denom = math.sqrt(n * p * q)
        a3 = (1 - 2 * p) / denom if denom > 0 else 0
        builder = StepBuilder("Coeficiente de Asimetria")
        builder.add_step(
            desc="Formula del coeficiente de asimetria del modelo Binomial",
            latex=rf"As = \alpha_3 = \frac{{1 - 2 \cdot p}}{{\sqrt{{n \cdot p \cdot (1-p)}}}}",
            level_min=1,
        )
        builder.add_step(
            desc=f"As = (1 - 2*{p}) / sqrt({n}*{p}*{q})",
            latex=rf"As = \frac{{1 - 2 \cdot {p}}}{{\sqrt{{{n} \cdot {p} \cdot {q}}}}} = \frac{{{format_number(1 - 2*p)}}}{{{format_number(denom)}}} = {format_number(a3)}",
            result=a3,
            level_min=2,
        )

        if abs(a3) < 1e-10:
            interp = "La distribucion es simetrica (As = 0)"
        elif a3 > 0:
            interp = "La distribucion tiene asimetria positiva (cola derecha)"
        else:
            interp = "La distribucion tiene asimetria negativa (cola izquierda)"
        builder.add_step(desc=interp, level_min=1)

        return builder.build(final_value=a3, final_latex=rf"As = {format_number(a3)}")

    def kurtosis(self) -> CalcResult:
        n, p, q = self.n, self.p, self.q
        npq = n * p * q
        ku = 3 + (1 - 6 * p * q) / npq if npq > 0 else 3
        builder = StepBuilder("Coeficiente de Kurtosis")
        builder.add_step(
            desc="Formula del coeficiente de kurtosis del modelo Binomial",
            latex=rf"Ku = \alpha_4 = 3 + \frac{{1 - 6 \cdot p \cdot (1-p)}}{{n \cdot p \cdot (1-p)}}",
            level_min=1,
        )
        builder.add_step(
            desc=f"Ku = 3 + (1 - 6*{p}*{q}) / ({n}*{p}*{q})",
            latex=rf"Ku = 3 + \frac{{1 - 6 \cdot {p} \cdot {q}}}{{{n} \cdot {p} \cdot {q}}} = 3 + \frac{{{format_number(1 - 6*p*q)}}}{{{format_number(npq)}}} = {format_number(ku)}",
            result=ku,
            level_min=2,
        )

        if abs(ku - 3) < 1e-10:
            interp = "Mesocurtica (Ku = 3, similar a la Normal)"
        elif ku > 3:
            interp = "Leptocurtica (Ku > 3, mas apuntada que la Normal)"
        else:
            interp = "Platicurtica (Ku < 3, mas achatada que la Normal)"
        builder.add_step(desc=interp, level_min=1)

        return builder.build(final_value=ku, final_latex=rf"Ku = {format_number(ku)}")

    def partial_expectation_left(self, r: int) -> CalcResult:
        n, p = self.n, self.p
        builder = StepBuilder(f"H({r})")

        builder.add_step(
            desc=f"Expectativa parcial izquierda H({r})",
            latex=rf"H_b({r}/{n};{p}) = \sum_{{x=0}}^{{{r}}} x \cdot \binom{{{n}}}{{x}} \cdot {p}^x \cdot {self.q}^{{{n}-x}}",
            level_min=1,
        )

        # Formula directa: H_b(r/n;p) = n*p * F_b(r-1/n-1;p)
        builder.add_step(
            desc="Usando la formula directa",
            latex=rf"H_b({r}/{n};{p}) = n \cdot p \cdot F_b({r-1}/{n-1};{p})",
            level_min=2,
        )

        total = sum(x * self.probability_value(x) for x in range(0, min(r, n) + 1))

        builder.add_step(
            desc=f"H({r}) = {format_number(total)}",
            latex=rf"H_b({r}/{n};{p}) = {format_number(total)}",
            result=total,
            level_min=1,
        )

        return builder.build(final_value=total, final_latex=rf"H_b({r}/{n};{p}) = {format_number(total)}")
