"""Modelo de distribucion Hiper-Pascal."""

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


class HiperPascal(DiscreteModel):
    """
    Distribucion Hiper-Pascal (muestreo sin reposicion hasta r exitos):
        P(n) = (r/n) * C(R,r) * C(N-R, n-r) / C(N,n)

    Es la analogia de Pascal para el proceso Hipergeometrico:
    se extrae sin reposicion de un lote de N (con R favorables)
    hasta obtener el r-esimo exito.

    Parametros:
        r: numero de exitos buscados (entero >= 1, r <= R)
        N: total de elementos en el lote
        R: elementos favorables en el lote

    Variable: n = numero de extracciones necesarias para el r-esimo exito.
    Dominio: n = r, r+1, ..., N-R+r  (= N-(R-r))
    """

    def __init__(self, r: int, N: int, R: int):
        if r < 1:
            raise ValueError("r debe ser >= 1")
        if N < 1:
            raise ValueError("N debe ser >= 1")
        if not (r <= R <= N):
            raise ValueError("Debe cumplirse r <= R <= N")
        self.r = r
        self.N = N
        self.R = R
        self._d_min = r
        self._d_max = N - R + r  # N-(R-r)

    def name(self) -> str:
        return "Hiper-Pascal"

    def params_dict(self) -> Dict[str, float]:
        return {"r": self.r, "N": self.N, "R": self.R}

    def domain(self) -> Tuple[int, int]:
        return (self._d_min, self._d_max)

    def latex_formula(self) -> str:
        return (rf"P(n) = \frac{{r}}{{n}} \cdot "
                rf"\frac{{\binom{{R}}{{r}} \cdot \binom{{N-R}}{{n-r}}}}{{\binom{{N}}{{n}}}}"
                rf" = \frac{{{self.r}}}{{n}} \cdot "
                rf"\frac{{\binom{{{self.R}}}{{{self.r}}} \cdot \binom{{{self.N-self.R}}}{{n-{self.r}}}}}{{\binom{{{self.N}}}{{n}}}}")

    def probability_value(self, n: int) -> float:
        if n < self._d_min or n > self._d_max:
            return 0.0
        denom = comb(self.N, n)
        if denom == 0 or n == 0:
            return 0.0
        p_hiper = comb(self.R, self.r) * comb(self.N - self.R, n - self.r) / denom
        return (self.r / n) * p_hiper

    def probability(self, n: int) -> CalcResult:
        r, N, R = self.r, self.N, self.R
        builder = StepBuilder(f"P(n={n})")

        if n < self._d_min or n > self._d_max:
            builder.add_step(
                f"n={n} fuera del dominio [{self._d_min}, {self._d_max}]",
                level_min=1,
            )
            return builder.build(final_value=0.0, final_latex=f"P(n={n}) = 0")

        builder.add_step(
            desc="Formula del modelo Hiper-Pascal",
            latex=rf"P(n) = \frac{{r}}{{n}} \cdot \frac{{\binom{{R}}{{r}} \cdot \binom{{N-R}}{{n-r}}}}{{\binom{{N}}{{n}}}}",
            level_min=1,
        )
        builder.add_step(
            desc=f"Reemplazamos r={r}, N={N}, R={R}, n={n}",
            latex=rf"P(n={n}) = \frac{{{r}}}{{{n}}} \cdot \frac{{\binom{{{R}}}{{{r}}} \cdot \binom{{{N-R}}}{{{n-r}}}}}{{\binom{{{N}}}{{{n}}}}}",
            level_min=2,
        )

        cr_result = comb_with_steps(R, r)
        cr_val = cr_result.final_value
        builder.add_step(
            desc=f"C({R},{r}) = {cr_val}",
            latex=rf"\binom{{{R}}}{{{r}}} = {cr_val}",
            result=cr_val,
            level_min=2,
        )
        builder.merge_result(cr_result, level_min=3)

        cnr_result = comb_with_steps(N - R, n - r)
        cnr_val = cnr_result.final_value
        builder.add_step(
            desc=f"C({N-R},{n-r}) = {cnr_val}",
            latex=rf"\binom{{{N-R}}}{{{n-r}}} = {cnr_val}",
            result=cnr_val,
            level_min=2,
        )
        builder.merge_result(cnr_result, level_min=3)

        cn_result = comb_with_steps(N, n)
        cn_val = cn_result.final_value
        builder.add_step(
            desc=f"C({N},{n}) = {cn_val}",
            latex=rf"\binom{{{N}}}{{{n}}} = {cn_val}",
            result=cn_val,
            level_min=2,
        )
        builder.merge_result(cn_result, level_min=3)

        p_hiper = cr_val * cnr_val / cn_val if cn_val != 0 else 0.0
        result = (r / n) * p_hiper if n != 0 else 0.0
        builder.add_step(
            desc=f"P(n={n}) = ({r}/{n}) * {cr_val}*{cnr_val}/{cn_val}",
            latex=(rf"P(n={n}) = \frac{{{r}}}{{{n}}} \cdot "
                   rf"\frac{{{cr_val} \cdot {cnr_val}}}{{{cn_val}}} = {format_number(result, 6)}"),
            result=result,
            level_min=2,
        )

        return builder.build(
            final_value=result,
            final_latex=rf"P_{{hpa}}(n={n}\,/\,r={r};\,N={N};\,R={R}) = {format_number(result, 6)}",
        )

    def cdf_left(self, n: int) -> CalcResult:
        r, N, R = self.r, self.N, self.R
        n_eff = min(n, self._d_max)
        builder = StepBuilder(f"F({n})")
        builder.add_step(
            desc=f"F({n}) = P(VA <= {n}) = suma P(x) para x = {self._d_min} hasta {n_eff}",
            latex=rf"F_{{hpa}}({n}\,/\,{r};\,{N};\,{R}) = \sum_{{x={self._d_min}}}^{{{n_eff}}} P_{{hpa}}(x)",
            level_min=1,
        )
        total = 0.0
        for x in range(self._d_min, n_eff + 1):
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
            latex=rf"F_{{hpa}}({n}\,/\,{r};\,{N};\,{R}) = {format_number(total, 6)}",
            result=total,
            level_min=1,
        )
        return builder.build(
            final_value=total,
            final_latex=rf"F_{{hpa}}({n}\,/\,{r};\,{N};\,{R}) = {format_number(total, 6)}",
        )

    def cdf_right(self, n: int) -> CalcResult:
        r, N, R = self.r, self.N, self.R
        n_eff = max(n, self._d_min)
        builder = StepBuilder(f"G({n})")
        builder.add_step(
            desc=f"G({n}) = P(VA >= {n}) = suma P(x) para x = {n_eff} hasta {self._d_max}",
            latex=rf"G_{{hpa}}({n}\,/\,{r};\,{N};\,{R}) = \sum_{{x={n_eff}}}^{{{self._d_max}}} P_{{hpa}}(x)",
            level_min=1,
        )
        total = 0.0
        for x in range(n_eff, self._d_max + 1):
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
            latex=rf"G_{{hpa}}({n}\,/\,{r};\,{N};\,{R}) = {format_number(total, 6)}",
            result=total,
            level_min=1,
        )
        return builder.build(
            final_value=total,
            final_latex=rf"G_{{hpa}}({n}\,/\,{r};\,{N};\,{R}) = {format_number(total, 6)}",
        )

    def mean(self) -> CalcResult:
        r, N, R = self.r, self.N, self.R
        mu = r * (N + 1) / (R + 1)
        builder = StepBuilder("Esperanza Matematica")
        builder.add_step(
            desc="Formula de la esperanza del modelo Hiper-Pascal",
            latex=rf"E(n) = \mu = \frac{{r \cdot (N+1)}}{{R+1}}",
            level_min=1,
        )
        builder.add_step(
            desc=f"E(n) = {r}*({N}+1)/({R}+1) = {r}*{N+1}/{R+1} = {format_number(mu)}",
            latex=rf"E(n) = \frac{{{r} \cdot {N+1}}}{{{R+1}}} = {format_number(mu)}",
            result=mu,
            level_min=2,
        )
        return builder.build(final_value=mu, final_latex=rf"\mu = {format_number(mu)}")

    def variance(self) -> CalcResult:
        """Varianza calculada numericamente."""
        mu = self.mean().final_value
        var = sum((n - mu) ** 2 * self.probability_value(n)
                  for n in range(self._d_min, self._d_max + 1))
        builder = StepBuilder("Varianza")
        builder.add_step(
            desc="V(n) = E[(n - mu)^2]  (calculado numericamente)",
            latex=rf"V(n) = \sigma^2 = E\left[(n-\mu)^2\right]",
            level_min=1,
        )
        builder.add_step(
            desc=f"V(n) = {format_number(var)}",
            latex=rf"\sigma^2 = {format_number(var)}",
            result=var,
            level_min=2,
        )
        return builder.build(final_value=var, final_latex=rf"\sigma^2 = {format_number(var)}")

    def std_dev(self) -> CalcResult:
        var = self.variance().final_value
        sigma = math.sqrt(var)
        builder = StepBuilder("Desvio Estandar")
        builder.add_step(
            desc="D(n) = sqrt(V(n))",
            latex=rf"D(n) = \sigma = \sqrt{{V(n)}}",
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
        mo = find_mode_discrete(self.probability_value, self._d_min, self._d_max)
        builder = StepBuilder("Moda")
        builder.add_step(
            desc="La moda es el valor n con maxima probabilidad",
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
            lambda n: compute_cdf_left_discrete(self.probability_value, n, self._d_min),
            self._d_min, self._d_max,
        )
        builder = StepBuilder("Mediana")
        builder.add_step(
            desc="Menor n tal que F(n) >= 0.5",
            latex=rf"Me: \text{{menor }} n \text{{ tal que }} F(n) \geq 0.5",
            level_min=2,
        )
        f_me_minus_1 = (compute_cdf_left_discrete(self.probability_value, me - 1, self._d_min)
                        if me > self._d_min else 0.0)
        f_me = compute_cdf_left_discrete(self.probability_value, me, self._d_min)
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
        mu = self.mean().final_value
        sigma = self.std_dev().final_value
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
        mu = self.mean().final_value
        sigma = self.std_dev().final_value
        a3 = (sum((n - mu) ** 3 * self.probability_value(n)
                  for n in range(self._d_min, self._d_max + 1)) / sigma ** 3
              if sigma > 1e-15 else 0.0)
        builder = StepBuilder("Coeficiente de Asimetria")
        builder.add_step(
            desc="As = E[(n - mu)^3] / sigma^3  (calculado numericamente)",
            latex=rf"As = \alpha_3 = \frac{{E\left[(n-\mu)^3\right]}}{{\sigma^3}}",
            level_min=1,
        )
        builder.add_step(
            desc=f"As = {format_number(a3)}",
            latex=rf"As = {format_number(a3)}",
            result=a3,
            level_min=2,
        )
        interp = ("Asimetria positiva (cola derecha)" if a3 > 1e-6
                  else "Asimetria negativa (cola izquierda)" if a3 < -1e-6
                  else "Distribucion aproximadamente simetrica")
        builder.add_step(desc=interp, level_min=1)
        return builder.build(final_value=a3, final_latex=rf"As = {format_number(a3)}")

    def kurtosis(self) -> CalcResult:
        mu = self.mean().final_value
        sigma = self.std_dev().final_value
        ku = (sum((n - mu) ** 4 * self.probability_value(n)
                  for n in range(self._d_min, self._d_max + 1)) / sigma ** 4
              if sigma > 1e-15 else 3.0)
        builder = StepBuilder("Coeficiente de Kurtosis")
        builder.add_step(
            desc="Ku = E[(n - mu)^4] / sigma^4  (calculado numericamente)",
            latex=rf"Ku = \alpha_4 = \frac{{E\left[(n-\mu)^4\right]}}{{\sigma^4}}",
            level_min=1,
        )
        builder.add_step(
            desc=f"Ku = {format_number(ku)}",
            latex=rf"Ku = {format_number(ku)}",
            result=ku,
            level_min=2,
        )
        interp = ("Leptocurtica (Ku > 3)" if ku > 3
                  else "Mesocurtica (Ku ≈ 3)" if abs(ku - 3) < 0.1
                  else "Platicurtica (Ku < 3)")
        builder.add_step(desc=interp, level_min=1)
        return builder.build(final_value=ku, final_latex=rf"Ku = {format_number(ku)}")

    def partial_expectation_left(self, n: int) -> CalcResult:
        r, N, R = self.r, self.N, self.R
        builder = StepBuilder(f"H({n})")
        builder.add_step(
            desc=f"H({n}) = suma x*P(x) para x = {self._d_min} hasta {n}",
            latex=rf"H_{{hpa}}({n}\,/\,{r};\,{N};\,{R}) = \sum_{{x={self._d_min}}}^{{{n}}} x \cdot P_{{hpa}}(x)",
            level_min=1,
        )
        total = sum(x * self.probability_value(x) for x in range(self._d_min, n + 1))
        builder.add_step(
            desc=f"H({n}) = {format_number(total)}",
            latex=rf"H_{{hpa}}({n}\,/\,{r};\,{N};\,{R}) = {format_number(total)}",
            result=total,
            level_min=1,
        )
        return builder.build(
            final_value=total,
            final_latex=rf"H_{{hpa}}({n}\,/\,{r};\,{N};\,{R}) = {format_number(total)}",
        )
