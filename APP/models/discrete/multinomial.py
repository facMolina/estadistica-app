"""Modelo Multinomial (discreto multivariado).

P(r1,...,rk) = n! / (r1! * r2! * ... * rk!) * p1^r1 * p2^r2 * ... * pk^rk

No hereda de DiscreteModel: el "resultado" es un vector r = (r1,...,rk) con sum(r)=n,
no un escalar. La interfaz replica el contrato de paso a paso (métodos devuelven
CalcResult) pero con firma adaptada a vectores.
"""

import math
from typing import Dict, List, Optional, Sequence

from calculation.step_types import CalcResult
from calculation.step_engine import StepBuilder
from calculation.statistics_common import format_number
from config.settings import EPSILON
from models.discrete.binomial import Binomial


class Multinomial:
    """Distribución Multinomial con k categorías."""

    def __init__(self, n: int, p_vector: Sequence[float],
                 labels: Optional[Sequence[str]] = None):
        if not isinstance(n, int) or n < 1:
            raise ValueError("n debe ser un entero >= 1")
        if len(p_vector) < 2:
            raise ValueError("Multinomial requiere al menos 2 categorías")
        if any(p < 0 for p in p_vector):
            raise ValueError("Todas las probabilidades deben ser >= 0")
        total = sum(p_vector)
        if abs(total - 1.0) > 1e-6:
            raise ValueError(f"Las probabilidades deben sumar 1 (suma actual = {total})")

        self.n = n
        self.p = [float(x) for x in p_vector]
        self.k = len(self.p)
        self.labels = list(labels) if labels is not None else [f"C{i+1}" for i in range(self.k)]
        if len(self.labels) != self.k:
            raise ValueError("labels debe tener la misma longitud que p_vector")

    def name(self) -> str:
        return "Multinomial"

    def params_dict(self) -> Dict[str, float]:
        d: Dict[str, float] = {"n": self.n, "k": self.k}
        for i, pi in enumerate(self.p, start=1):
            d[f"p{i}"] = pi
        return d

    def latex_formula(self) -> str:
        return (r"P(r_1,\ldots,r_k) = \frac{n!}{r_1!\,r_2!\cdots r_k!}"
                r"\; p_1^{r_1}\, p_2^{r_2}\cdots p_k^{r_k}")

    # ---- núcleo numérico --------------------------------------------------

    def _validate_r(self, r_vector: Sequence[int]) -> None:
        if len(r_vector) != self.k:
            raise ValueError(
                f"r debe tener {self.k} componentes (igual que p); recibí {len(r_vector)}")
        if any((not isinstance(x, int)) or x < 0 for x in r_vector):
            raise ValueError("Cada ri debe ser entero no negativo")
        if sum(r_vector) != self.n:
            raise ValueError(
                f"La suma de r debe ser n={self.n}; recibí sum(r)={sum(r_vector)}")

    def probability_value(self, r_vector: Sequence[int]) -> float:
        """P(r1,...,rk) como float puro, sin steps."""
        if len(r_vector) != self.k or sum(r_vector) != self.n:
            return 0.0
        if any(x < 0 for x in r_vector):
            return 0.0
        coef = math.factorial(self.n)
        for ri in r_vector:
            coef //= math.factorial(ri)
        prod = 1.0
        for pi, ri in zip(self.p, r_vector):
            prod *= pi ** ri
        return coef * prod

    # ---- paso a paso ------------------------------------------------------

    def probability(self, r_vector: Sequence[int]) -> CalcResult:
        self._validate_r(r_vector)
        r = list(r_vector)
        n = self.n
        builder = StepBuilder(f"P({','.join(str(x) for x in r)})")

        r_str = ",".join(str(x) for x in r)
        p_str = ",".join(format_number(pi) for pi in self.p)

        # Nivel 1
        builder.add_step(
            desc="Aplicamos la fórmula del modelo Multinomial",
            latex=(r"P(r_1,\ldots,r_k) = \frac{n!}{r_1!\cdots r_k!}"
                   r"\; p_1^{r_1}\cdots p_k^{r_k}"),
            level_min=1,
        )

        # Nivel 2: sustitución
        fact_denom = " \\cdot ".join(f"{ri}!" for ri in r)
        powers = " \\cdot ".join(f"{format_number(pi)}^{{{ri}}}"
                                 for pi, ri in zip(self.p, r))
        builder.add_step(
            desc=f"Reemplazamos n={n}, r=({r_str}), p=({p_str})",
            latex=(rf"P({r_str}) = \frac{{{n}!}}{{{fact_denom}}}"
                   rf"\; {powers}"),
            level_min=2,
        )

        # Nivel 3: coeficiente multinomial
        n_fact = math.factorial(n)
        denom_val = 1
        denom_parts = []
        for ri in r:
            rf = math.factorial(ri)
            denom_val *= rf
            denom_parts.append(f"{ri}!={rf}")
        coef = n_fact // denom_val
        builder.add_step(
            desc=f"Calculamos el coeficiente multinomial n!/(r1!·...·rk!)",
            latex=(rf"\frac{{{n}!}}{{{fact_denom}}} = "
                   rf"\frac{{{n_fact}}}{{{denom_val}}} = {coef}"),
            result=float(coef),
            level_min=3,
        )

        # Nivel 3: potencias individuales
        power_values = []
        for i, (pi, ri) in enumerate(zip(self.p, r), start=1):
            val = pi ** ri
            power_values.append(val)
            builder.add_step(
                desc=f"Calculamos p{i}^r{i} = {format_number(pi)}^{ri}",
                latex=rf"{format_number(pi)}^{{{ri}}} = {format_number(val, 8)}",
                result=val,
                level_min=3,
            )

        prod = 1.0
        for v in power_values:
            prod *= v

        # Nivel 2: resultado
        result = coef * prod
        prod_str = " \\cdot ".join(format_number(v, 8) for v in power_values)
        builder.add_step(
            desc=f"Resultado: P({r_str}) = {coef} · {format_number(prod, 8)}",
            latex=(rf"P({r_str}) = {coef} \cdot {prod_str} "
                   rf"= {format_number(result, 6)}"),
            result=result,
            level_min=2,
        )

        return builder.build(
            final_value=result,
            final_latex=rf"P({r_str}) = {format_number(result, 6)}",
        )

    # ---- momentos ---------------------------------------------------------

    def mean_vector(self) -> CalcResult:
        """E(Xi) = n · pi para cada categoría."""
        builder = StepBuilder("Esperanza por categoría")
        builder.add_step(
            desc="En la distribución Multinomial, cada marginal Xi es Binomial(n, pi)",
            latex=r"E(X_i) = n \cdot p_i",
            level_min=1,
        )
        means = []
        for i, pi in enumerate(self.p, start=1):
            mu_i = self.n * pi
            means.append(mu_i)
            builder.add_step(
                desc=f"E(X{i}) = {self.n} · {format_number(pi)} = {format_number(mu_i)}",
                latex=rf"E(X_{{{i}}}) = {self.n} \cdot {format_number(pi)} = {format_number(mu_i)}",
                result=mu_i,
                level_min=2,
            )
        latex_final = r",\; ".join(f"E(X_{{{i}}})={format_number(m)}"
                                   for i, m in enumerate(means, start=1))
        return builder.build(final_value=sum(means), final_latex=latex_final)

    def variance_vector(self) -> CalcResult:
        """V(Xi) = n · pi · (1-pi)."""
        builder = StepBuilder("Varianza por categoría")
        builder.add_step(
            desc="Cada marginal Xi ~ Binomial(n, pi), así que V(Xi) = n·pi·(1-pi)",
            latex=r"V(X_i) = n \cdot p_i \cdot (1 - p_i)",
            level_min=1,
        )
        vars_ = []
        for i, pi in enumerate(self.p, start=1):
            v_i = self.n * pi * (1 - pi)
            vars_.append(v_i)
            builder.add_step(
                desc=f"V(X{i}) = {self.n} · {format_number(pi)} · {format_number(1-pi)} = {format_number(v_i)}",
                latex=(rf"V(X_{{{i}}}) = {self.n} \cdot {format_number(pi)} "
                       rf"\cdot {format_number(1-pi)} = {format_number(v_i)}"),
                result=v_i,
                level_min=2,
            )
        latex_final = r",\; ".join(f"V(X_{{{i}}})={format_number(v)}"
                                   for i, v in enumerate(vars_, start=1))
        return builder.build(final_value=sum(vars_), final_latex=latex_final)

    def covariance(self, i: int, j: int) -> CalcResult:
        """Cov(Xi, Xj) = -n·pi·pj para i≠j; V(Xi) para i=j."""
        if not (1 <= i <= self.k and 1 <= j <= self.k):
            raise ValueError(f"i,j deben estar entre 1 y {self.k}")
        builder = StepBuilder(f"Cov(X{i}, X{j})")
        pi = self.p[i - 1]
        pj = self.p[j - 1]
        if i == j:
            val = self.n * pi * (1 - pi)
            builder.add_step(
                desc="Cov(Xi,Xi) es la varianza V(Xi)",
                latex=rf"Cov(X_{{{i}}}, X_{{{i}}}) = V(X_{{{i}}}) = n \cdot p_{{{i}}} \cdot (1 - p_{{{i}}})",
                level_min=1,
            )
            builder.add_step(
                desc=f"= {self.n} · {format_number(pi)} · {format_number(1-pi)} = {format_number(val)}",
                latex=(rf"Cov(X_{{{i}}}, X_{{{i}}}) = {self.n} \cdot {format_number(pi)} "
                       rf"\cdot {format_number(1-pi)} = {format_number(val)}"),
                result=val,
                level_min=2,
            )
        else:
            val = -self.n * pi * pj
            builder.add_step(
                desc="En Multinomial las categorías están negativamente correlacionadas",
                latex=rf"Cov(X_{{{i}}}, X_{{{j}}}) = -n \cdot p_{{{i}}} \cdot p_{{{j}}}",
                level_min=1,
            )
            builder.add_step(
                desc=f"= -{self.n} · {format_number(pi)} · {format_number(pj)} = {format_number(val)}",
                latex=(rf"Cov(X_{{{i}}}, X_{{{j}}}) = -{self.n} \cdot {format_number(pi)} "
                       rf"\cdot {format_number(pj)} = {format_number(val)}"),
                result=val,
                level_min=2,
            )
        return builder.build(
            final_value=val,
            final_latex=rf"Cov(X_{{{i}}}, X_{{{j}}}) = {format_number(val)}",
        )

    def marginal_binomial(self, i: int) -> Binomial:
        """Marginal Xi ~ Binomial(n, pi). i es 1-indexed."""
        if not (1 <= i <= self.k):
            raise ValueError(f"i debe estar entre 1 y {self.k}")
        return Binomial(self.n, self.p[i - 1])

    def characteristics_summary(self) -> List[Dict[str, float]]:
        """Tabla con E(Xi), V(Xi), σ(Xi) por categoría."""
        rows = []
        for i, (label, pi) in enumerate(zip(self.labels, self.p), start=1):
            mu = self.n * pi
            v = self.n * pi * (1 - pi)
            rows.append({
                "i": i,
                "Categoría": label,
                "pi": pi,
                "E(Xi)": mu,
                "V(Xi)": v,
                "σ(Xi)": math.sqrt(v),
            })
        return rows
