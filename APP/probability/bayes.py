"""
Teorema de Bayes y Probabilidad Total para n hipotesis.

P(Hi|E) = P(E|Hi)·P(Hi) / P(E)
P(E) = Σ P(E|Hi)·P(Hi)
"""

from typing import List, Tuple
from calculation.step_types import CalcResult
from calculation.step_engine import StepBuilder
from calculation.statistics_common import format_number


class BayesCalc:
    """
    Resuelve el Teorema de Bayes para n hipotesis mutuamente excluyentes
    y exhaustivas H1, H2, ..., Hn dado el evento evidencia E.

    Params:
        labels    : nombres de cada hipotesis, ej. ["H1", "Bueno", "Defect."]
        priors    : P(Hi) — probabilidades a priori (deben sumar 1)
        likelihoods: P(E|Hi) — verosimilitudes
        evidence_label: nombre del evento evidencia (solo para display)
    """

    def __init__(
        self,
        labels: List[str],
        priors: List[float],
        likelihoods: List[float],
        evidence_label: str = "E",
    ):
        if not (len(labels) == len(priors) == len(likelihoods)):
            raise ValueError("labels, priors y likelihoods deben tener el mismo largo")
        if len(labels) < 2:
            raise ValueError("Se requieren al menos 2 hipotesis")
        self.labels = labels
        self.priors = priors
        self.likelihoods = likelihoods
        self.evidence = evidence_label
        self._joints: List[float] = [p * l for p, l in zip(priors, likelihoods)]
        self._pE: float = sum(self._joints)
        self._posteriors: List[float] = (
            [j / self._pE for j in self._joints] if self._pE > 1e-15 else [0.0] * len(labels)
        )

    # ------------------------------------------------------------------
    # Accesores directos (sin paso a paso)
    # ------------------------------------------------------------------

    def prob_evidence(self) -> float:
        """P(E) = Σ P(E|Hi)·P(Hi)"""
        return self._pE

    def posteriors(self) -> List[Tuple[str, float]]:
        """[(label, P(Hi|E))] para cada hipotesis."""
        return list(zip(self.labels, self._posteriors))

    def full_table(self) -> List[dict]:
        """Tabla completa para mostrar en st.dataframe."""
        rows = []
        for i, label in enumerate(self.labels):
            rows.append({
                "Hipotesis": label,
                "P(Hi)": round(self.priors[i], 6),
                f"P({self.evidence}|Hi)": round(self.likelihoods[i], 6),
                f"P({self.evidence}|Hi)·P(Hi)": round(self._joints[i], 6),
                "P(Hi|E)": round(self._posteriors[i], 6),
                "P(Hi|E) %": round(self._posteriors[i] * 100, 4),
            })
        # Fila total
        rows.append({
            "Hipotesis": "TOTAL",
            "P(Hi)": round(sum(self.priors), 6),
            f"P({self.evidence}|Hi)": "—",
            f"P({self.evidence}|Hi)·P(Hi)": round(self._pE, 6),
            "P(Hi|E)": round(sum(self._posteriors), 6),
            "P(Hi|E) %": round(sum(self._posteriors) * 100, 4),
        })
        return rows

    # ------------------------------------------------------------------
    # CalcResult con paso a paso completo
    # ------------------------------------------------------------------

    def solve(self) -> CalcResult:
        """
        Devuelve un CalcResult con el desarrollo completo del Teorema de Bayes.
        final_value = P(E).
        """
        E = self.evidence
        n = len(self.labels)
        builder = StepBuilder(f"Teorema de Bayes — P(Hi|{E})")

        # Paso 0: formula general
        builder.add_step(
            desc="Teorema de Bayes: actualiza probabilidades a priori dado un evento observado.",
            latex=(
                rf"P(H_i|{E}) = \frac{{P({E}|H_i) \cdot P(H_i)}}{{P({E})}}"
                rf"\quad \text{{donde}} \quad "
                rf"P({E}) = \sum_{{j=1}}^{{{n}}} P({E}|H_j) \cdot P(H_j)"
            ),
            level_min=1,
        )

        # Paso 1: productos P(E|Hi)·P(Hi)
        builder.add_step(
            desc=f"Paso 1 — Calcular los productos P({E}|Hi)·P(Hi) para cada hipotesis:",
            latex=rf"P({E}|H_i) \cdot P(H_i)",
            level_min=1,
        )
        for i, (label, prior, lik, joint) in enumerate(
            zip(self.labels, self.priors, self.likelihoods, self._joints)
        ):
            builder.add_step(
                desc=f"  H{i+1} = {label}:  P({E}|{label})·P({label}) = {format_number(lik)} × {format_number(prior)} = {format_number(joint)}",
                latex=(
                    rf"P({E}|{label}) \cdot P({label}) = "
                    rf"{format_number(lik)} \times {format_number(prior)} = {format_number(joint)}"
                ),
                result=joint,
                level_min=2,
            )

        # Paso 2: P(E) = suma de productos
        terms_str = " + ".join(format_number(j) for j in self._joints)
        builder.add_step(
            desc=f"Paso 2 — Probabilidad total P({E}) = {terms_str} = {format_number(self._pE)}",
            latex=(
                rf"P({E}) = \sum_{{j=1}}^{{{n}}} P({E}|H_j) \cdot P(H_j) = "
                rf"{terms_str} = {format_number(self._pE)}"
            ),
            result=self._pE,
            level_min=1,
        )

        # Paso 3: posteriors P(Hi|E)
        builder.add_step(
            desc=f"Paso 3 — Probabilidades a posteriori P(Hi|{E}):",
            latex=rf"P(H_i|{E}) = \frac{{P({E}|H_i) \cdot P(H_i)}}{{{format_number(self._pE)}}}",
            level_min=1,
        )
        for i, (label, joint, post) in enumerate(
            zip(self.labels, self._joints, self._posteriors)
        ):
            builder.add_step(
                desc=(
                    f"  P({label}|{E}) = {format_number(joint)} / {format_number(self._pE)} "
                    f"= {format_number(post)}  ({format_number(post * 100, 2)} %)"
                ),
                latex=(
                    rf"P({label}|{E}) = \frac{{{format_number(joint)}}}{{{format_number(self._pE)}}}"
                    rf" = {format_number(post)}"
                ),
                result=post,
                level_min=1,
            )

        return builder.build(
            final_value=self._pE,
            final_latex=rf"P({E}) = {format_number(self._pE)}",
        )
