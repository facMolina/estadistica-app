"""Modelo de distribucion de Pascal (Binomial Negativa)."""

import math
from typing import Tuple, Dict
from models.base import DiscreteModel
from calculation.step_types import CalcResult
from calculation.step_engine import StepBuilder
from calculation.combinatorics import comb, comb_with_steps
from calculation.statistics_common import (
    format_number, find_mode_discrete, find_median_discrete,
    compute_cdf_left_discrete,
)
from config.settings import MAX_SUMMATION_TERMS, EPSILON


class Pascal(DiscreteModel):
    """
    Distribucion de Pascal (Binomial Negativa):
        P(n) = C(n-1, r-1) * p^r * (1-p)^(n-r)

    Parametros:
        r: numero de exitos buscados (entero >= 1)
        p: probabilidad de exito por ensayo

    Variable: n = numero de ensayos necesarios para obtener el r-esimo exito.
    Dominio: n = r, r+1, r+2, ... (infinito, truncado).

    Notacion catedra: Fpa(n/r;p), Gpa(n/r;p), Ppa(n/r;p)
    Relacion con Binomial: P_pa(n) = (r/n) * P_b(r / n; p)
    """

    def __init__(self, r: int, p: float):
        if r < 1:
            raise ValueError("r debe ser >= 1")
        if not (0 < p <= 1):
            raise ValueError("p debe estar entre 0 y 1 (exclusivo en 0)")
        self.r = r
        self.p = p
        self.q = 1 - p
        self._domain_max = self._compute_domain_max()

    def _compute_domain_max(self) -> int:
        cum = 0.0
        for n in range(self.r, MAX_SUMMATION_TERMS + self.r):
            cum += self._prob_raw(n)
            if 1.0 - cum < EPSILON:
                return n
        return MAX_SUMMATION_TERMS + self.r - 1

    def _prob_raw(self, n: int) -> float:
        if n < self.r:
            return 0.0
        return comb(n - 1, self.r - 1) * (self.p ** self.r) * (self.q ** (n - self.r))

    def name(self) -> str:
        return "Pascal"

    def params_dict(self) -> Dict[str, float]:
        return {"r": self.r, "p": self.p}

    def domain(self) -> Tuple[int, int]:
        return (self.r, self._domain_max)

    def latex_formula(self) -> str:
        return (rf"P(n) = \binom{{n-1}}{{r-1}} \cdot p^r \cdot (1-p)^{{n-r}}"
                rf" = \binom{{n-1}}{{{self.r-1}}} \cdot {self.p}^{{{self.r}}} \cdot {self.q}^{{n-{self.r}}}")

    # Para Pascal el argumento de los metodos abstractos representa n (ensayos),
    # aunque en la firma de la clase base se llama 'r'.

    def probability_value(self, n: int) -> float:
        if n < self.r or n > self._domain_max:
            return 0.0
        return self._prob_raw(n)

    def probability(self, n: int) -> CalcResult:
        r, p, q = self.r, self.p, self.q
        builder = StepBuilder(f"P(n={n})")

        if n < r:
            builder.add_step(
                f"n={n} < r={r}: imposible obtener {r} exitos en menos de {r} ensayos",
                level_min=1,
            )
            return builder.build(final_value=0.0, final_latex=f"P(n={n}) = 0")

        builder.add_step(
            desc="Formula del modelo de Pascal",
            latex=rf"P(n) = \binom{{n-1}}{{r-1}} \cdot p^r \cdot (1-p)^{{n-r}}",
            level_min=1,
        )
        builder.add_step(
            desc=f"Reemplazamos n={n}, r={r}, p={p}, q=1-p={q}",
            latex=rf"P(n={n}) = \binom{{{n-1}}}{{{r-1}}} \cdot {p}^{{{r}}} \cdot {q}^{{{n-r}}}",
            level_min=2,
        )

        c_result = comb_with_steps(n - 1, r - 1)
        c_val = c_result.final_value
        builder.add_step(
            desc=f"Calculamos C({n-1},{r-1})",
            latex=rf"\binom{{{n-1}}}{{{r-1}}}",
            latex_res=rf"= {c_val}",
            result=c_val,
            level_min=2,
        )
        builder.merge_result(c_result, level_min=3)

        p_power = p ** r
        q_power = q ** (n - r)
        builder.add_step(
            desc=f"p^r = {p}^{r} = {format_number(p_power)}",
            latex=rf"{p}^{{{r}}} = {format_number(p_power)}",
            result=p_power,
            level_min=3,
        )
        builder.add_step(
            desc=f"q^(n-r) = {q}^{n-r} = {format_number(q_power)}",
            latex=rf"{q}^{{{n-r}}} = {format_number(q_power)}",
            result=q_power,
            level_min=3,
        )

        result = c_val * p_power * q_power
        builder.add_step(
            desc=f"P(n={n}) = {c_val} * {format_number(p_power)} * {format_number(q_power)}",
            latex=rf"P(n={n}) = {c_val} \cdot {format_number(p_power)} \cdot {format_number(q_power)} = {format_number(result, 6)}",
            result=result,
            level_min=2,
        )

        # Verificacion con relacion Binomial: P_pa(n) = (r/n) * P_b(r/n;p)
        binom_check = (r / n) * (
            comb(n, r) * (p ** r) * (q ** (n - r))
        )
        builder.add_step(
            desc=f"Verificacion con Binomial: (r/n)*P_b(r/n;p) = ({r}/{n})*C({n},{r})*{p}^{r}*{q}^{n-r} = {format_number(binom_check, 6)}",
            latex=rf"\text{{Verif: }} \frac{{r}}{{n}} \cdot P_b\!\left(\frac{{r}}{{n}};p\right) = \frac{{{r}}}{{{n}}} \cdot \binom{{{n}}}{{{r}}} \cdot {p}^{{{r}}} \cdot {q}^{{{n-r}}} = {format_number(binom_check, 6)}",
            result=binom_check,
            level_min=3,
        )

        return builder.build(
            final_value=result,
            final_latex=rf"P_{{pa}}(n={n}\,/\,r={r};\,p={p}) = {format_number(result, 6)}",
        )

    def cdf_left(self, n: int) -> CalcResult:
        r, p = self.r, self.p
        builder = StepBuilder(f"F({n})")
        builder.add_step(
            desc=f"F({n}) = P(VA <= {n}) = suma P(x) para x = {r} hasta {n}",
            latex=rf"F_{{pa}}({n}\,/\,{r};\,{p}) = \sum_{{x={r}}}^{{{n}}} \binom{{x-1}}{{{r-1}}} \cdot {p}^{{{r}}} \cdot {self.q}^{{x-{r}}}",
            level_min=1,
        )
        total = 0.0
        for x in range(r, n + 1):
            px = self.probability_value(x)
            total += px
            builder.add_step(
                desc=f"P(n={x}) = {format_number(px, 6)}",
                latex=rf"P(n={x}) = {format_number(px, 6)}",
                result=px,
                level_min=3,
            )
        builder.add_step(
            desc=f"F({n}) = {format_number(total, 6)}",
            latex=rf"F_{{pa}}({n}\,/\,{r};\,{p}) = {format_number(total, 6)}",
            result=total,
            level_min=1,
        )
        return builder.build(
            final_value=total,
            final_latex=rf"F_{{pa}}({n}\,/\,{r};\,{p}) = {format_number(total, 6)}",
        )

    def cdf_right(self, n: int) -> CalcResult:
        r, p = self.r, self.p
        d_max = self._domain_max
        builder = StepBuilder(f"G({n})")
        builder.add_step(
            desc=f"G({n}) = P(VA >= {n}) = suma P(x) para x = {n} hasta infinito (truncado en {d_max})",
            latex=rf"G_{{pa}}({n}\,/\,{r};\,{p}) = \sum_{{x={n}}}^{{\infty}} \binom{{x-1}}{{{r-1}}} \cdot {p}^{{{r}}} \cdot {self.q}^{{x-{r}}}",
            level_min=1,
        )
        total = 0.0
        for x in range(max(n, r), d_max + 1):
            px = self.probability_value(x)
            total += px
            builder.add_step(
                desc=f"P(n={x}) = {format_number(px, 6)}",
                latex=rf"P(n={x}) = {format_number(px, 6)}",
                result=px,
                level_min=3,
            )
        builder.add_step(
            desc=f"G({n}) = {format_number(total, 6)}",
            latex=rf"G_{{pa}}({n}\,/\,{r};\,{p}) = {format_number(total, 6)}",
            result=total,
            level_min=1,
        )
        return builder.build(
            final_value=total,
            final_latex=rf"G_{{pa}}({n}\,/\,{r};\,{p}) = {format_number(total, 6)}",
        )

    def mean(self) -> CalcResult:
        r, p = self.r, self.p
        mu = r / p
        builder = StepBuilder("Esperanza Matematica")
        builder.add_step(
            desc="Formula de la esperanza del modelo de Pascal",
            latex=rf"E(n) = \mu = \frac{{r}}{{p}}",
            level_min=1,
        )
        builder.add_step(
            desc=f"E(n) = {r} / {p} = {format_number(mu)}",
            latex=rf"E(n) = \frac{{{r}}}{{{p}}} = {format_number(mu)}",
            result=mu,
            level_min=2,
        )
        return builder.build(final_value=mu, final_latex=rf"\mu = {format_number(mu)}")

    def variance(self) -> CalcResult:
        r, p, q = self.r, self.p, self.q
        var = r * q / (p ** 2)
        builder = StepBuilder("Varianza")
        builder.add_step(
            desc="Formula de la varianza del modelo de Pascal",
            latex=rf"V(n) = \sigma^2 = \frac{{r \cdot (1-p)}}{{p^2}}",
            level_min=1,
        )
        builder.add_step(
            desc=f"V(n) = {r} * {q} / {p}^2 = {r} * {q} / {format_number(p**2)} = {format_number(var)}",
            latex=rf"V(n) = \frac{{{r} \cdot {q}}}{{{p}^2}} = \frac{{{format_number(r*q)}}}{{{format_number(p**2)}}} = {format_number(var)}",
            result=var,
            level_min=2,
        )
        return builder.build(final_value=var, final_latex=rf"\sigma^2 = {format_number(var)}")

    def std_dev(self) -> CalcResult:
        var = self.r * self.q / (self.p ** 2)
        sigma = math.sqrt(var)
        builder = StepBuilder("Desvio Estandar")
        builder.add_step(
            desc="D(n) = sqrt(V(n)) = sqrt(r*(1-p)/p^2)",
            latex=rf"D(n) = \sigma = \sqrt{{\frac{{r \cdot (1-p)}}{{p^2}}}}",
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
        r, p, q = self.r, self.p, self.q
        # Mo = floor((r-1)/p) + 1  si r > 1, Mo = 1 si r = 1 (con cualquier p)
        if r == 1:
            mo = 1
        else:
            mo_float = (r - 1) / p
            mo = int(mo_float) if float(mo_float) == int(mo_float) else math.floor(mo_float) + 1
            # Verify numerically
            mo = find_mode_discrete(self.probability_value, self.r, min(self.r + 100, self._domain_max))
        builder = StepBuilder("Moda")
        builder.add_step(
            desc="La moda se obtiene numericamente como el valor n con maxima probabilidad",
            latex=rf"Mo = \arg\max_{{n}} P(n)",
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
            lambda n: compute_cdf_left_discrete(self.probability_value, n, self.r),
            self.r, self._domain_max,
        )
        builder = StepBuilder("Mediana")
        builder.add_step(
            desc="Menor n tal que F(n) >= 0.5",
            latex=rf"Me: \text{{menor }} n \text{{ tal que }} F(n) \geq 0.5",
            level_min=2,
        )
        f_me_minus_1 = compute_cdf_left_discrete(self.probability_value, me - 1, self.r) if me > self.r else 0.0
        f_me = compute_cdf_left_discrete(self.probability_value, me, self.r)
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
        r, p, q = self.r, self.p, self.q
        mu = r / p
        sigma = math.sqrt(r * q) / p
        cv_val = (sigma / mu * 100) if mu != 0 else float("inf")
        builder = StepBuilder("Coeficiente de Variacion")
        builder.add_step(
            desc="Cv = (sigma/mu)*100",
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
        r, p, q = self.r, self.p, self.q
        denom = math.sqrt(r * q)
        a3 = (2 - p) / denom if denom > 0 else 0.0
        builder = StepBuilder("Coeficiente de Asimetria")
        builder.add_step(
            desc="Formula del coeficiente de asimetria del modelo de Pascal",
            latex=rf"As = \alpha_3 = \frac{{2 - p}}{{\sqrt{{r \cdot (1-p)}}}}",
            level_min=1,
        )
        builder.add_step(
            desc=f"As = (2 - {p}) / sqrt({r} * {q}) = {format_number(2-p)} / {format_number(denom)} = {format_number(a3)}",
            latex=rf"As = \frac{{2 - {p}}}{{\sqrt{{{r} \cdot {q}}}}} = \frac{{{format_number(2-p)}}}{{{format_number(denom)}}} = {format_number(a3)}",
            result=a3,
            level_min=2,
        )
        builder.add_step(
            desc="Pascal siempre tiene asimetria positiva (As > 0, cola derecha)",
            level_min=1,
        )
        return builder.build(final_value=a3, final_latex=rf"As = {format_number(a3)}")

    def kurtosis(self) -> CalcResult:
        r, p, q = self.r, self.p, self.q
        # Ku = 3 + (6 + p^2/(r*q)) / 1  → formula estandar: 3 + 6/r + p^2/(r*q)
        ku = 3.0 + 6.0 / r + (p ** 2) / (r * q) if r * q > 0 else 3.0
        builder = StepBuilder("Coeficiente de Kurtosis")
        builder.add_step(
            desc="Formula del coeficiente de kurtosis del modelo de Pascal",
            latex=rf"Ku = \alpha_4 = 3 + \frac{{6}}{{r}} + \frac{{p^2}}{{r \cdot (1-p)}}",
            level_min=1,
        )
        builder.add_step(
            desc=f"Ku = 3 + 6/{r} + {p}^2 / ({r}*{q}) = {format_number(ku)}",
            latex=rf"Ku = 3 + \frac{{6}}{{{r}}} + \frac{{{p}^2}}{{{r} \cdot {q}}} = {format_number(ku)}",
            result=ku,
            level_min=2,
        )
        interp = ("Leptocurtica (Ku > 3)" if ku > 3
                  else "Mesocurtica (Ku = 3)" if abs(ku - 3) < 1e-9
                  else "Platicurtica (Ku < 3)")
        builder.add_step(desc=interp, level_min=1)
        return builder.build(final_value=ku, final_latex=rf"Ku = {format_number(ku)}")

    def partial_expectation_left(self, n: int) -> CalcResult:
        r, p = self.r, self.p
        builder = StepBuilder(f"H({n})")
        builder.add_step(
            desc=f"Expectativa parcial izquierda H({n}) = suma x*P(x) para x = {r} hasta {n}",
            latex=rf"H_{{pa}}({n}\,/\,{r};\,{p}) = \sum_{{x={r}}}^{{{n}}} x \cdot P_{{pa}}(x)",
            level_min=1,
        )
        total = sum(x * self.probability_value(x) for x in range(r, n + 1))
        builder.add_step(
            desc=f"H({n}) = {format_number(total)}",
            latex=rf"H_{{pa}}({n}\,/\,{r};\,{p}) = {format_number(total)}",
            result=total,
            level_min=1,
        )
        return builder.build(
            final_value=total,
            final_latex=rf"H_{{pa}}({n}\,/\,{r};\,{p}) = {format_number(total)}",
        )
