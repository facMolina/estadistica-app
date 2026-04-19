"""Suma de variables aleatorias independientes + Teorema Central del Límite.

Dados k componentes independientes Xi con E(Xi)=μi y V(Xi)=σi², se computa
S = Σ Xi y se aproxima S ~ N(ΣμI·countI, ΣσI²·countI) vía TCL.

El campo `count` permite expresar "k copias de un mismo componente" sin duplicar
filas: un único registro con `count=30` equivale a sumar 30 variables iid.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import List, Optional, Sequence

from scipy import stats as _st

from calculation.step_engine import StepBuilder
from calculation.step_types import CalcResult
from calculation.statistics_common import format_number


@dataclass
class Component:
    """Componente individual de la suma.

    Atributos:
        name:     etiqueta legible (ej. 'X1', 'tiempo_pieza')
        mean:     E(Xi)
        variance: V(Xi)
        count:    cantidad de copias iid de este componente (default 1)
    """
    name: str
    mean: float
    variance: float
    count: int = 1

    def __post_init__(self):
        if self.variance < 0:
            raise ValueError(f"V({self.name}) = {self.variance} no puede ser negativa")
        if self.count < 1:
            raise ValueError(f"count de {self.name} debe ser >= 1")


class SumOfRVs:
    """S = Σ Xi con aproximación Normal vía TCL."""

    def __init__(self, components: Sequence[Component | dict]):
        if not components:
            raise ValueError("SumOfRVs requiere al menos 1 componente")
        norm_comps: List[Component] = []
        for c in components:
            if isinstance(c, dict):
                norm_comps.append(Component(
                    name=str(c.get("name", f"X{len(norm_comps)+1}")),
                    mean=float(c["mean"]),
                    variance=float(c["variance"]),
                    count=int(c.get("count", 1)),
                ))
            elif isinstance(c, Component):
                norm_comps.append(c)
            else:
                raise TypeError(f"Componente inesperado: {type(c)}")
        self.components: List[Component] = norm_comps

    # ------------------------------------------------------------------
    # Parámetros derivados
    # ------------------------------------------------------------------

    @property
    def total_count(self) -> int:
        return sum(c.count for c in self.components)

    def expected_value_raw(self) -> float:
        return sum(c.count * c.mean for c in self.components)

    def variance_raw(self) -> float:
        return sum(c.count * c.variance for c in self.components)

    def std_dev_raw(self) -> float:
        return math.sqrt(self.variance_raw())

    # ------------------------------------------------------------------
    # Paso a paso: momentos
    # ------------------------------------------------------------------

    def expected_value(self) -> CalcResult:
        builder = StepBuilder("E(S)")
        builder.add_step(
            desc="Por linealidad de la esperanza, E(S) = Σ E(Xi)",
            latex=r"E(S) = \sum_{i=1}^{k} E(X_i)",
            level_min=1,
        )
        parts: list[str] = []
        total = 0.0
        for c in self.components:
            term = c.count * c.mean
            total += term
            if c.count == 1:
                parts.append(f"{format_number(c.mean)}")
            else:
                parts.append(f"{c.count} \\cdot {format_number(c.mean)}")
            builder.add_step(
                desc=(f"Componente {c.name}: E({c.name}) = {format_number(c.mean)}"
                      + (f"  (×{c.count} copias)" if c.count > 1 else "")),
                latex=(rf"{c.count} \cdot {format_number(c.mean)} = {format_number(term)}"
                       if c.count > 1
                       else rf"E({c.name}) = {format_number(c.mean)}"),
                result=term,
                level_min=2,
            )
        builder.add_step(
            desc=f"E(S) = {format_number(total)}",
            latex=rf"E(S) = {' + '.join(parts)} = {format_number(total)}",
            result=total,
            level_min=1,
        )
        return builder.build(
            final_value=total,
            final_latex=rf"E(S) = {format_number(total)}",
        )

    def variance(self) -> CalcResult:
        builder = StepBuilder("V(S)")
        builder.add_step(
            desc="Por independencia, V(S) = Σ V(Xi)",
            latex=r"V(S) = \sum_{i=1}^{k} V(X_i)",
            level_min=1,
        )
        parts: list[str] = []
        total = 0.0
        for c in self.components:
            term = c.count * c.variance
            total += term
            if c.count == 1:
                parts.append(f"{format_number(c.variance)}")
            else:
                parts.append(f"{c.count} \\cdot {format_number(c.variance)}")
            builder.add_step(
                desc=(f"Componente {c.name}: V({c.name}) = {format_number(c.variance)}"
                      + (f"  (×{c.count} copias)" if c.count > 1 else "")),
                latex=(rf"{c.count} \cdot {format_number(c.variance)} = {format_number(term)}"
                       if c.count > 1
                       else rf"V({c.name}) = {format_number(c.variance)}"),
                result=term,
                level_min=2,
            )
        builder.add_step(
            desc=f"V(S) = {format_number(total)}",
            latex=rf"V(S) = {' + '.join(parts)} = {format_number(total)}",
            result=total,
            level_min=1,
        )
        return builder.build(
            final_value=total,
            final_latex=rf"V(S) = {format_number(total)}",
        )

    def std_dev(self) -> CalcResult:
        v = self.variance_raw()
        sigma = math.sqrt(v)
        builder = StepBuilder("σ(S)")
        builder.add_step(
            desc="σ(S) = √V(S)",
            latex=r"\sigma(S) = \sqrt{V(S)}",
            level_min=1,
        )
        builder.add_step(
            desc=f"σ(S) = √{format_number(v)} = {format_number(sigma)}",
            latex=rf"\sigma(S) = \sqrt{{{format_number(v)}}} = {format_number(sigma)}",
            result=sigma,
            level_min=2,
        )
        return builder.build(
            final_value=sigma,
            final_latex=rf"\sigma(S) = {format_number(sigma)}",
        )

    # ------------------------------------------------------------------
    # Aproximación TCL: S ~ N(E(S), √V(S))
    # ------------------------------------------------------------------

    def tcl_condition_met(self, threshold: int = 30) -> bool:
        """Heurística: TCL confiable cuando total_count >= 30."""
        return self.total_count >= threshold

    def _standardize_and_phi(self, s: float) -> tuple[float, float, float, float]:
        mu = self.expected_value_raw()
        sigma = self.std_dev_raw()
        if sigma <= 0:
            raise ValueError("σ(S) = 0: no se puede estandarizar (varianza total nula)")
        z = (s - mu) / sigma
        phi = float(_st.norm.cdf(z))
        return mu, sigma, z, phi

    def _header_steps(self, builder: StepBuilder) -> None:
        """Prepend: fórmulas TCL + cálculo de E(S) y V(S) como referencia."""
        builder.add_step(
            desc="Por el Teorema Central del Límite, S = ΣXi ~ Normal aproximada",
            latex=(r"S = \sum_{i=1}^{k} X_i \;\sim\; N\!\left(\mu_S,\sigma_S\right),"
                   r"\; \mu_S = \sum E(X_i),\; \sigma_S^2 = \sum V(X_i)"),
            level_min=1,
        )
        if not self.tcl_condition_met():
            builder.add_step(
                desc=(f"Nota: k total = {self.total_count} < 30. "
                      f"La aproximación Normal puede no ser precisa."),
                latex="",
                level_min=1,
            )

    def probability(self, query_type: str, **query_params) -> CalcResult:
        """Computa probabilidades sobre S ~ N(E(S), σ(S)) vía TCL.

        query_type:
          - 'cdf_left':  P(S ≤ s).          Param: s
          - 'cdf_right': P(S ≥ s).          Param: s
          - 'range':     P(a ≤ S ≤ b).      Params: a, b
          - 'fractile':  s tal que P(S≤s)=α. Param: alpha
        """
        qt = query_type.lower()

        if qt == "cdf_left":
            s = float(query_params["s"])
            return self._cdf_left(s)
        if qt == "cdf_right":
            s = float(query_params["s"])
            return self._cdf_right(s)
        if qt == "range":
            a = float(query_params["a"])
            b = float(query_params["b"])
            return self._range(a, b)
        if qt == "fractile":
            alpha = float(query_params["alpha"])
            return self._fractile(alpha)
        raise ValueError(f"query_type no soportado: {query_type}")

    def _cdf_left(self, s: float) -> CalcResult:
        mu, sigma, z, phi = self._standardize_and_phi(s)
        builder = StepBuilder(f"P(S ≤ {s})")
        self._header_steps(builder)
        builder.add_step(
            desc=f"E(S) = {format_number(mu)}, σ(S) = {format_number(sigma)}",
            latex=(rf"\mu_S = {format_number(mu)},\; "
                   rf"\sigma_S = {format_number(sigma)}"),
            level_min=1,
        )
        builder.add_step(
            desc=f"Z = ({format_number(s)} − {format_number(mu)}) / {format_number(sigma)} = {format_number(z, 4)}",
            latex=rf"Z = \frac{{{format_number(s)} - {format_number(mu)}}}"
                  rf"{{{format_number(sigma)}}} = {format_number(z, 4)}",
            result=z,
            level_min=1,
        )
        builder.add_step(
            desc=f"P(S ≤ {s}) = Φ({format_number(z, 4)}) = {format_number(phi, 6)}",
            latex=rf"P(S \leq {format_number(s)}) = \Phi({format_number(z, 4)}) = {format_number(phi, 6)}",
            result=phi,
            level_min=1,
        )
        return builder.build(
            final_value=phi,
            final_latex=rf"P(S \leq {format_number(s)}) = {format_number(phi, 6)}",
        )

    def _cdf_right(self, s: float) -> CalcResult:
        mu, sigma, z, phi = self._standardize_and_phi(s)
        prob = 1.0 - phi
        builder = StepBuilder(f"P(S ≥ {s})")
        self._header_steps(builder)
        builder.add_step(
            desc=f"E(S) = {format_number(mu)}, σ(S) = {format_number(sigma)}",
            latex=rf"\mu_S = {format_number(mu)},\; \sigma_S = {format_number(sigma)}",
            level_min=1,
        )
        builder.add_step(
            desc=f"Z = ({format_number(s)} − {format_number(mu)}) / {format_number(sigma)} = {format_number(z, 4)}",
            latex=rf"Z = \frac{{{format_number(s)} - {format_number(mu)}}}"
                  rf"{{{format_number(sigma)}}} = {format_number(z, 4)}",
            result=z,
            level_min=1,
        )
        builder.add_step(
            desc=f"P(S ≥ {s}) = 1 − Φ({format_number(z, 4)}) = {format_number(prob, 6)}",
            latex=rf"P(S \geq {format_number(s)}) = 1 - \Phi({format_number(z, 4)}) = {format_number(prob, 6)}",
            result=prob,
            level_min=1,
        )
        return builder.build(
            final_value=prob,
            final_latex=rf"P(S \geq {format_number(s)}) = {format_number(prob, 6)}",
        )

    def _range(self, a: float, b: float) -> CalcResult:
        if a > b:
            a, b = b, a
        mu = self.expected_value_raw()
        sigma = self.std_dev_raw()
        if sigma <= 0:
            raise ValueError("σ(S) = 0: no se puede estandarizar")
        za = (a - mu) / sigma
        zb = (b - mu) / sigma
        phi_a = float(_st.norm.cdf(za))
        phi_b = float(_st.norm.cdf(zb))
        prob = phi_b - phi_a
        builder = StepBuilder(f"P({a} ≤ S ≤ {b})")
        self._header_steps(builder)
        builder.add_step(
            desc=f"E(S) = {format_number(mu)}, σ(S) = {format_number(sigma)}",
            latex=rf"\mu_S = {format_number(mu)},\; \sigma_S = {format_number(sigma)}",
            level_min=1,
        )
        builder.add_step(
            desc=f"Za = ({format_number(a)} − {format_number(mu)}) / {format_number(sigma)} = {format_number(za, 4)}",
            latex=rf"Z_a = \frac{{{format_number(a)} - {format_number(mu)}}}"
                  rf"{{{format_number(sigma)}}} = {format_number(za, 4)}",
            result=za,
            level_min=2,
        )
        builder.add_step(
            desc=f"Zb = ({format_number(b)} − {format_number(mu)}) / {format_number(sigma)} = {format_number(zb, 4)}",
            latex=rf"Z_b = \frac{{{format_number(b)} - {format_number(mu)}}}"
                  rf"{{{format_number(sigma)}}} = {format_number(zb, 4)}",
            result=zb,
            level_min=2,
        )
        builder.add_step(
            desc=(f"P({a} ≤ S ≤ {b}) = Φ({format_number(zb, 4)}) − Φ({format_number(za, 4)}) "
                  f"= {format_number(phi_b, 6)} − {format_number(phi_a, 6)} = {format_number(prob, 6)}"),
            latex=(rf"P({format_number(a)} \leq S \leq {format_number(b)}) = "
                   rf"\Phi({format_number(zb, 4)}) - \Phi({format_number(za, 4)}) = "
                   rf"{format_number(prob, 6)}"),
            result=prob,
            level_min=1,
        )
        return builder.build(
            final_value=prob,
            final_latex=rf"P({format_number(a)} \leq S \leq {format_number(b)}) = {format_number(prob, 6)}",
        )

    def _fractile(self, alpha: float) -> CalcResult:
        if not (0.0 < alpha < 1.0):
            raise ValueError(f"alpha debe estar en (0,1); recibí {alpha}")
        mu = self.expected_value_raw()
        sigma = self.std_dev_raw()
        z_alpha = float(_st.norm.ppf(alpha))
        s_alpha = mu + z_alpha * sigma
        builder = StepBuilder(f"s({alpha})")
        self._header_steps(builder)
        builder.add_step(
            desc=f"E(S) = {format_number(mu)}, σ(S) = {format_number(sigma)}",
            latex=rf"\mu_S = {format_number(mu)},\; \sigma_S = {format_number(sigma)}",
            level_min=1,
        )
        builder.add_step(
            desc=f"Z({alpha}) = {format_number(z_alpha, 4)}  (de tabla Normal estándar)",
            latex=rf"Z({alpha}) = {format_number(z_alpha, 4)}",
            result=z_alpha,
            level_min=2,
        )
        builder.add_step(
            desc=f"s(α) = μS + Z(α)·σS = {format_number(s_alpha, 4)}",
            latex=rf"s({alpha}) = {format_number(mu)} + {format_number(z_alpha, 4)} "
                  rf"\cdot {format_number(sigma)} = {format_number(s_alpha, 4)}",
            result=s_alpha,
            level_min=1,
        )
        return builder.build(
            final_value=s_alpha,
            final_latex=rf"s({alpha}) = {format_number(s_alpha, 4)}",
        )

    # ------------------------------------------------------------------
    # Constructor auxiliar: a partir de instancias de modelos existentes
    # ------------------------------------------------------------------

    @classmethod
    def from_model_instances(cls, models: Sequence, counts: Optional[Sequence[int]] = None,
                             names: Optional[Sequence[str]] = None) -> "SumOfRVs":
        """Crea SumOfRVs extrayendo mean() y variance() de cada modelo."""
        if counts is None:
            counts = [1] * len(models)
        if names is None:
            names = [getattr(m, "name", lambda: f"X{i+1}")()
                     for i, m in enumerate(models)]
        comps: list[Component] = []
        for m, cnt, nm in zip(models, counts, names):
            mu = m.mean().final_value if hasattr(m, "mean") else float(m.mean)
            v = m.variance().final_value if hasattr(m, "variance") else float(m.variance)
            comps.append(Component(name=nm, mean=float(mu), variance=float(v), count=int(cnt)))
        return cls(comps)

    # ------------------------------------------------------------------
    # Resumen
    # ------------------------------------------------------------------

    def summary_dict(self) -> dict:
        return {
            "k_total": self.total_count,
            "E(S)": self.expected_value_raw(),
            "V(S)": self.variance_raw(),
            "σ(S)": self.std_dev_raw(),
            "tcl_ok": self.tcl_condition_met(),
        }
