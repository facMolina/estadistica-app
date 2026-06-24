"""
Bayes continuo: combina verosimilitudes obtenidas de modelos de probabilidad
continuos (densidad puntual f(x), F(x) o G(x)) con probabilidades a priori
discretas P(Hi), reusando el motor de Bayes discreto (`probability/bayes.py`).

Tres formas de evidencia observadas en los parciales:
  - "hay un valor puntual x"        -> verosimilitud = f_i(x)      (densidad)
  - "se observó X > x" (cola der.)  -> verosimilitud = G_i(x)
  - "se observó X < x" (cola izq.)  -> verosimilitud = F_i(x)
  - una sola distribución evaluada en un umbral propio de cada hipótesis
    (ej. "fósforos": cada grupo tarda un tiempo distinto en usar el fósforo)
    -> verosimilitud_i = F(umbral_i)  o  G(umbral_i)  de la MISMA distribución.
"""

from typing import List, Sequence, Tuple

from calculation.step_engine import StepBuilder
from calculation.step_types import CalcResult
from calculation.statistics_common import format_number
from probability.bayes import BayesCalc


def _solve_with_detail(
    labels: Sequence[str],
    priors: Sequence[float],
    likelihood_results: Sequence[CalcResult],
    kind_symbol: str,
    evidence_label: str,
) -> Tuple[BayesCalc, CalcResult]:
    likelihoods = [r.final_value for r in likelihood_results]
    bayes = BayesCalc(list(labels), list(priors), likelihoods, evidence_label)
    bayes_res = bayes.solve()

    builder = StepBuilder(f"Bayes continuo — P(Hi|{evidence_label})")
    builder.add_step(
        desc=(f"Paso 1 — Verosimilitud P({evidence_label}|Hi) de cada hipótesis, "
              f"usando {kind_symbol}(x) del modelo continuo correspondiente:"),
        level_min=1,
    )
    for label, res in zip(labels, likelihood_results):
        builder.add_step(
            desc=f"  {label}: {kind_symbol}(...) = {format_number(res.final_value, 6)}",
            result=res.final_value,
            level_min=2,
        )
        builder.merge_result(res, level_min=3)

    builder.add_step(desc="Paso 2 — Teorema de Bayes (probabilidades a posteriori):", level_min=1)
    builder.merge_result(bayes_res, level_min=2)

    for label, post in bayes.posteriors():
        builder.add_step(
            desc=f"P({label}|{evidence_label}) = {format_number(post, 6)}  ({format_number(post * 100, 2)} %)",
            result=post,
            level_min=1,
        )

    result = builder.build(
        final_value=bayes.prob_evidence(),
        final_latex=rf"P({evidence_label}) = {format_number(bayes.prob_evidence(), 6)}",
    )
    return bayes, result


def bayes_continuo_point(labels: Sequence[str], priors: Sequence[float],
                          models: Sequence, x: float,
                          evidence_label: str = None) -> Tuple[BayesCalc, CalcResult]:
    """P(Hi | X=x) usando la densidad puntual f_i(x) de cada modelo como verosimilitud."""
    results = [m.density(x) for m in models]
    label = evidence_label or f"X={format_number(x)}"
    return _solve_with_detail(labels, priors, results, "f", label)


def bayes_continuo_tail_right(labels: Sequence[str], priors: Sequence[float],
                               models: Sequence, x: float,
                               evidence_label: str = None) -> Tuple[BayesCalc, CalcResult]:
    """P(Hi | X>x) usando la supervivencia G_i(x) de cada modelo como verosimilitud."""
    results = [m.cdf_right(x) for m in models]
    label = evidence_label or f"X>{format_number(x)}"
    return _solve_with_detail(labels, priors, results, "G", label)


def bayes_continuo_tail_left(labels: Sequence[str], priors: Sequence[float],
                              models: Sequence, x: float,
                              evidence_label: str = None) -> Tuple[BayesCalc, CalcResult]:
    """P(Hi | X<x) usando F_i(x) de cada modelo como verosimilitud."""
    results = [m.cdf_left(x) for m in models]
    label = evidence_label or f"X<{format_number(x)}"
    return _solve_with_detail(labels, priors, results, "F", label)


def bayes_continuo_same_model_thresholds(
    labels: Sequence[str], priors: Sequence[float], model,
    thresholds: Sequence[float], tail: str = "left",
    evidence_label: str = "E",
) -> Tuple[BayesCalc, CalcResult]:
    """Caso 'fósforos': UNA sola distribución evaluada en un umbral distinto
    por hipótesis (ej. cada grupo de personas tarda un tiempo distinto en usar
    el fósforo encendido). tail='left' -> F(umbral_i); tail='right' -> G(umbral_i)."""
    if tail == "left":
        results = [model.cdf_left(t) for t in thresholds]
        kind = "F"
    elif tail == "right":
        results = [model.cdf_right(t) for t in thresholds]
        kind = "G"
    else:
        raise ValueError("tail debe ser 'left' o 'right'")
    return _solve_with_detail(labels, priors, results, kind, evidence_label)
