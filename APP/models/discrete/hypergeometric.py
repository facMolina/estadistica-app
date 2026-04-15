"""Modelo de distribucion Hipergeometrica."""

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


class Hipergeometrico(DiscreteModel):
    """
    Distribucion Hipergeometrica (muestreo sin reposicion):
        P(r) = C(R, r) * C(N-R, n-r) / C(N, n)

    Parametros:
        N: total de elementos en el lote
        R: elementos favorables en el lote
        n: tamano de la muestra

    Variable: r = elementos favorables en la muestra.
    Dominio: max(0, n-(N-R)) <= r <= min(n, R)

    Notacion catedra: Fh(r/n;N;R), Gh(r/n;N;R), Ph(r/n;N;R)
    """

    def __init__(self, N: int, R: int, n: int):
        if N < 1:
            raise ValueError("N debe ser >= 1")
        if not (0 <= R <= N):
            raise ValueError("R debe estar entre 0 y N")
        if not (1 <= n <= N):
            raise ValueError("n debe estar entre 1 y N")
        self.N = N
        self.R = R
        self.n = n
        self._d_min = max(0, n - (N - R))
        self._d_max = min(n, R)

    def name(self) -> str:
        return "Hipergeometrico"

    def params_dict(self) -> Dict[str, float]:
        return {"N": self.N, "R": self.R, "n": self.n}

    def domain(self) -> Tuple[int, int]:
        return (self._d_min, self._d_max)

    def latex_formula(self) -> str:
        return (rf"P(r) = \frac{{\binom{{R}}{{r}} \cdot \binom{{N-R}}{{n-r}}}}{{\binom{{N}}{{n}}}}"
                rf" = \frac{{\binom{{{self.R}}}{{r}} \cdot \binom{{{self.N-self.R}}}{{{self.n}-r}}}}{{\binom{{{self.N}}}{{{self.n}}}}}")

    def probability_value(self, r: int) -> float:
        if r < self._d_min or r > self._d_max:
            return 0.0
        denom = comb(self.N, self.n)
        if denom == 0:
            return 0.0
        return comb(self.R, r) * comb(self.N - self.R, self.n - r) / denom

    def probability(self, r: int) -> CalcResult:
        N, R, n = self.N, self.R, self.n
        builder = StepBuilder(f"P(r={r})")

        if r < self._d_min or r > self._d_max:
            builder.add_step(
                f"r={r} fuera del dominio [{self._d_min}, {self._d_max}]",
                level_min=1,
            )
            return builder.build(final_value=0.0, final_latex=f"P(r={r}) = 0")

        builder.add_step(
            desc="Formula del modelo Hipergeometrico (muestreo sin reposicion)",
            latex=rf"P(r) = \frac{{\binom{{R}}{{r}} \cdot \binom{{N-R}}{{n-r}}}}{{\binom{{N}}{{n}}}}",
            level_min=1,
        )
        builder.add_step(
            desc=f"Reemplazamos N={N}, R={R}, n={n}, r={r}",
            latex=rf"P(r={r}) = \frac{{\binom{{{R}}}{{{r}}} \cdot \binom{{{N-R}}}{{{n-r}}}}}{{\binom{{{N}}}{{{n}}}}}",
            level_min=2,
        )

        # C(R, r)
        cr_result = comb_with_steps(R, r)
        cr_val = cr_result.final_value
        builder.add_step(
            desc=f"C({R},{r}) = {cr_val}",
            latex=rf"\binom{{{R}}}{{{r}}}",
            latex_res=rf"= {cr_val}",
            result=cr_val,
            level_min=2,
        )
        builder.merge_result(cr_result, level_min=3)

        # C(N-R, n-r)
        cnr_result = comb_with_steps(N - R, n - r)
        cnr_val = cnr_result.final_value
        builder.add_step(
            desc=f"C({N-R},{n-r}) = {cnr_val}",
            latex=rf"\binom{{{N-R}}}{{{n-r}}}",
            latex_res=rf"= {cnr_val}",
            result=cnr_val,
            level_min=2,
        )
        builder.merge_result(cnr_result, level_min=3)

        # C(N, n)
        cn_result = comb_with_steps(N, n)
        cn_val = cn_result.final_value
        builder.add_step(
            desc=f"C({N},{n}) = {cn_val}",
            latex=rf"\binom{{{N}}}{{{n}}}",
            latex_res=rf"= {cn_val}",
            result=cn_val,
            level_min=2,
        )
        builder.merge_result(cn_result, level_min=3)

        result = cr_val * cnr_val / cn_val if cn_val != 0 else 0.0
        builder.add_step(
            desc=f"P(r={r}) = {cr_val} * {cnr_val} / {cn_val}",
            latex=rf"P(r={r}) = \frac{{{cr_val} \cdot {cnr_val}}}{{{cn_val}}} = {format_number(result, 6)}",
            result=result,
            level_min=2,
        )

        return builder.build(
            final_value=result,
            final_latex=rf"P_h(r={r}\,/\,n={n};\,N={N};\,R={R}) = {format_number(result, 6)}",
        )

    def cdf_left(self, r: int) -> CalcResult:
        N, R, n = self.N, self.R, self.n
        r_eff = min(r, self._d_max)
        builder = StepBuilder(f"F({r})")
        builder.add_step(
            desc=f"F({r}) = P(VA <= {r}) = suma P(x) para x = {self._d_min} hasta {r_eff}",
            latex=rf"F_h({r}\,/\,{n};\,{N};\,{R}) = \sum_{{x={self._d_min}}}^{{{r_eff}}} \frac{{\binom{{{R}}}{{x}} \cdot \binom{{{N-R}}}{{{n}-x}}}}{{\binom{{{N}}}{{{n}}}}}",
            level_min=1,
        )
        total = 0.0
        for x in range(self._d_min, r_eff + 1):
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
            latex=rf"F_h({r}\,/\,{n};\,{N};\,{R}) = {format_number(total, 6)}",
            result=total,
            level_min=1,
        )
        return builder.build(
            final_value=total,
            final_latex=rf"F_h({r}\,/\,{n};\,{N};\,{R}) = {format_number(total, 6)}",
        )

    def cdf_right(self, r: int) -> CalcResult:
        N, R, n = self.N, self.R, self.n
        r_eff = max(r, self._d_min)
        builder = StepBuilder(f"G({r})")
        builder.add_step(
            desc=f"G({r}) = P(VA >= {r}) = suma P(x) para x = {r_eff} hasta {self._d_max}",
            latex=rf"G_h({r}\,/\,{n};\,{N};\,{R}) = \sum_{{x={r_eff}}}^{{{self._d_max}}} \frac{{\binom{{{R}}}{{x}} \cdot \binom{{{N-R}}}{{{n}-x}}}}{{\binom{{{N}}}{{{n}}}}}",
            level_min=1,
        )
        total = 0.0
        for x in range(r_eff, self._d_max + 1):
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
            latex=rf"G_h({r}\,/\,{n};\,{N};\,{R}) = {format_number(total, 6)}",
            result=total,
            level_min=1,
        )
        return builder.build(
            final_value=total,
            final_latex=rf"G_h({r}\,/\,{n};\,{N};\,{R}) = {format_number(total, 6)}",
        )

    def mean(self) -> CalcResult:
        N, R, n = self.N, self.R, self.n
        mu = n * R / N
        builder = StepBuilder("Esperanza Matematica")
        builder.add_step(
            desc="Formula de la esperanza del modelo Hipergeometrico",
            latex=rf"E(r) = \mu = n \cdot \frac{{R}}{{N}}",
            level_min=1,
        )
        builder.add_step(
            desc=f"E(r) = {n} * {R}/{N} = {format_number(mu)}",
            latex=rf"E(r) = {n} \cdot \frac{{{R}}}{{{N}}} = {format_number(mu)}",
            result=mu,
            level_min=2,
        )
        return builder.build(final_value=mu, final_latex=rf"\mu = {format_number(mu)}")

    def variance(self) -> CalcResult:
        N, R, n = self.N, self.R, self.n
        p = R / N
        # V = n*(R/N)*(1-R/N)*(N-n)/(N-1)
        var = n * p * (1 - p) * (N - n) / (N - 1) if N > 1 else 0.0
        builder = StepBuilder("Varianza")
        builder.add_step(
            desc="Formula de la varianza del modelo Hipergeometrico (incluye factor de correccion por finitud)",
            latex=rf"V(r) = \sigma^2 = n \cdot \frac{{R}}{{N}} \cdot \left(1 - \frac{{R}}{{N}}\right) \cdot \frac{{N-n}}{{N-1}}",
            level_min=1,
        )
        builder.add_step(
            desc=f"V(r) = {n} * ({R}/{N}) * (1 - {R}/{N}) * ({N}-{n})/({N}-1)",
            latex=(rf"V(r) = {n} \cdot \frac{{{R}}}{{{N}}} \cdot "
                   rf"\frac{{{N-R}}}{{{N}}} \cdot \frac{{{N-n}}}{{{N-1}}} = {format_number(var)}"),
            result=var,
            level_min=2,
        )
        return builder.build(final_value=var, final_latex=rf"\sigma^2 = {format_number(var)}")

    def std_dev(self) -> CalcResult:
        N, R, n = self.N, self.R, self.n
        p = R / N
        var = n * p * (1 - p) * (N - n) / (N - 1) if N > 1 else 0.0
        sigma = math.sqrt(var)
        builder = StepBuilder("Desvio Estandar")
        builder.add_step(
            desc="D(r) = sqrt(V(r))",
            latex=rf"D(r) = \sigma = \sqrt{{V(r)}}",
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
            desc="La moda es el valor r con maxima probabilidad en el dominio",
            latex=rf"Mo = \arg\max_{{r}} P(r)",
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
            lambda r: compute_cdf_left_discrete(self.probability_value, r, self._d_min),
            self._d_min, self._d_max,
        )
        builder = StepBuilder("Mediana")
        builder.add_step(
            desc="Menor r tal que F(r) >= 0.5",
            latex=rf"Me: \text{{menor }} r \text{{ tal que }} F(r) \geq 0.5",
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
        N, R, n = self.N, self.R, self.n
        p = R / N
        var = n * p * (1 - p) * (N - n) / (N - 1) if N > 1 else 0.0
        mu = n * p
        sigma = math.sqrt(var)
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
        """Asimetria calculada numericamente: As = E[(r-mu)^3] / sigma^3."""
        mu = self.mean().final_value
        sigma = self.std_dev().final_value
        a3 = (sum((r - mu) ** 3 * self.probability_value(r)
                  for r in range(self._d_min, self._d_max + 1)) / sigma ** 3
              if sigma > 1e-15 else 0.0)
        builder = StepBuilder("Coeficiente de Asimetria")
        builder.add_step(
            desc="As = E[(r - mu)^3] / sigma^3  (calculado numericamente)",
            latex=rf"As = \alpha_3 = \frac{{E\left[(r-\mu)^3\right]}}{{\sigma^3}}",
            level_min=1,
        )
        builder.add_step(
            desc=f"As = {format_number(a3)}",
            latex=rf"As = {format_number(a3)}",
            result=a3,
            level_min=2,
        )
        if abs(a3) < 1e-6:
            interp = "Distribucion simetrica (As ≈ 0)"
        elif a3 > 0:
            interp = "Asimetria positiva (cola derecha)"
        else:
            interp = "Asimetria negativa (cola izquierda)"
        builder.add_step(desc=interp, level_min=1)
        return builder.build(final_value=a3, final_latex=rf"As = {format_number(a3)}")

    def kurtosis(self) -> CalcResult:
        """Kurtosis calculada numericamente: Ku = E[(r-mu)^4] / sigma^4."""
        mu = self.mean().final_value
        sigma = self.std_dev().final_value
        ku = (sum((r - mu) ** 4 * self.probability_value(r)
                  for r in range(self._d_min, self._d_max + 1)) / sigma ** 4
              if sigma > 1e-15 else 3.0)
        builder = StepBuilder("Coeficiente de Kurtosis")
        builder.add_step(
            desc="Ku = E[(r - mu)^4] / sigma^4  (calculado numericamente)",
            latex=rf"Ku = \alpha_4 = \frac{{E\left[(r-\mu)^4\right]}}{{\sigma^4}}",
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

    def partial_expectation_left(self, r: int) -> CalcResult:
        N, R, n = self.N, self.R, self.n
        builder = StepBuilder(f"H({r})")
        builder.add_step(
            desc=f"H({r}) = suma x*P(x) para x = {self._d_min} hasta {r}",
            latex=rf"H_h({r}\,/\,{n};\,{N};\,{R}) = \sum_{{x={self._d_min}}}^{{{r}}} x \cdot P_h(x)",
            level_min=1,
        )
        builder.add_step(
            desc="Formula directa: H_h(r/n;N;R) = n*(R/N) * F_h(r-1 / n-1; N-1; R-1)",
            latex=rf"H_h = n \cdot \frac{{R}}{{N}} \cdot F_h\!\left({r-1}\,/\,{n-1};\,{N-1};\,{R-1}\right)",
            level_min=2,
        )
        total = sum(x * self.probability_value(x) for x in range(self._d_min, r + 1))
        builder.add_step(
            desc=f"H({r}) = {format_number(total)}",
            latex=rf"H_h({r}\,/\,{n};\,{N};\,{R}) = {format_number(total)}",
            result=total,
            level_min=1,
        )
        return builder.build(
            final_value=total,
            final_latex=rf"H_h({r}\,/\,{n};\,{N};\,{R}) = {format_number(total)}",
        )
