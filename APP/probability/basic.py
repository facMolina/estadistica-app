"""
Operaciones basicas de probabilidad — dos eventos A y B.

Cada funcion retorna un CalcResult con paso a paso usando el mismo motor
que los modelos de distribucion.
"""

from typing import Tuple
from calculation.step_types import CalcResult
from calculation.step_engine import StepBuilder
from calculation.statistics_common import format_number


# ---------------------------------------------------------------------------
# Helper interno
# ---------------------------------------------------------------------------

def _ln(name: str) -> str:
    """LaTeX name: si tiene mas de un caracter, envuelve en \\text{}."""
    if len(name) <= 2:
        return name
    return rf"\text{{{name}}}"


# ---------------------------------------------------------------------------
# Funciones publicas
# ---------------------------------------------------------------------------

def calc_intersection(
    pA: float, pB: float,
    relationship: str,
    pAB_user: float = 0.0,
    name_A: str = "A", name_B: str = "B",
) -> Tuple[float, CalcResult]:
    """
    Calcula P(A∩B) segun la relacion entre eventos.
    relationship: "mutually_exclusive" | "independent" | "known"
    Retorna (valor, CalcResult).
    """
    lA, lB = _ln(name_A), _ln(name_B)
    builder = StepBuilder(f"P({name_A}∩{name_B})")

    if relationship == "mutually_exclusive":
        pAB = 0.0
        builder.add_step(
            desc=f"{name_A} y {name_B} son mutuamente excluyentes: no pueden ocurrir juntos.",
            latex=rf"{lA} \cap {lB} = \emptyset \implies P({lA} \cap {lB}) = 0",
            result=0.0,
            level_min=1,
        )

    elif relationship == "independent":
        pAB = pA * pB
        builder.add_step(
            desc=f"{name_A} y {name_B} son independientes: P(A∩B) = P(A)·P(B)",
            latex=rf"P({lA} \cap {lB}) = P({lA}) \cdot P({lB})",
            level_min=1,
        )
        builder.add_step(
            desc=f"P({name_A}∩{name_B}) = {format_number(pA)} × {format_number(pB)} = {format_number(pAB)}",
            latex=(rf"P({lA} \cap {lB}) = {format_number(pA)} \times {format_number(pB)}"
                   rf" = {format_number(pAB)}"),
            result=pAB,
            level_min=1,
        )

    else:  # known
        pAB = pAB_user
        builder.add_step(
            desc=f"P({name_A}∩{name_B}) = {format_number(pAB)}  (dato del problema)",
            latex=rf"P({lA} \cap {lB}) = {format_number(pAB)}",
            result=pAB,
            level_min=1,
        )

    return pAB, builder.build(final_value=pAB,
                               final_latex=rf"P({lA} \cap {lB}) = {format_number(pAB)}")


def calc_union(
    pA: float, pB: float, pAB: float,
    relationship: str,
    name_A: str = "A", name_B: str = "B",
) -> CalcResult:
    """P(A∪B) = P(A) + P(B) − P(A∩B)"""
    lA, lB = _ln(name_A), _ln(name_B)
    pUnion = pA + pB - pAB
    builder = StepBuilder(f"P({name_A}∪{name_B})")

    if relationship == "mutually_exclusive":
        builder.add_step(
            desc="Eventos mutuamente excluyentes: se aplica el axioma de aditividad.",
            latex=rf"P({lA} \cup {lB}) = P({lA}) + P({lB})",
            level_min=1,
        )
    else:
        builder.add_step(
            desc="Regla de la suma para eventos compatibles:",
            latex=rf"P({lA} \cup {lB}) = P({lA}) + P({lB}) - P({lA} \cap {lB})",
            level_min=1,
        )

    builder.add_step(
        desc=f"Sustituir valores:",
        latex=(rf"P({lA} \cup {lB}) = {format_number(pA)} + {format_number(pB)}"
               rf" - {format_number(pAB)} = {format_number(pUnion)}"),
        result=pUnion,
        level_min=1,
    )
    return builder.build(
        final_value=pUnion,
        final_latex=rf"P({lA} \cup {lB}) = {format_number(pUnion)}",
    )


def calc_complement(pX: float, name_X: str = "A") -> CalcResult:
    """P(Xc) = 1 − P(X)"""
    lX = _ln(name_X)
    pXc = 1.0 - pX
    builder = StepBuilder(f"P({name_X}ᶜ)")
    builder.add_step(
        desc=f"Complemento de {name_X}:",
        latex=rf"P({lX}^c) = 1 - P({lX})",
        level_min=1,
    )
    builder.add_step(
        desc=f"P({name_X}ᶜ) = 1 − {format_number(pX)} = {format_number(pXc)}",
        latex=rf"P({lX}^c) = 1 - {format_number(pX)} = {format_number(pXc)}",
        result=pXc,
        level_min=1,
    )
    return builder.build(
        final_value=pXc,
        final_latex=rf"P({lX}^c) = {format_number(pXc)}",
    )


def calc_conditional(
    pAB: float, pB: float,
    name_A: str = "A", name_B: str = "B",
) -> CalcResult:
    """P(A|B) = P(A∩B) / P(B)"""
    lA, lB = _ln(name_A), _ln(name_B)
    builder = StepBuilder(f"P({name_A}|{name_B})")
    builder.add_step(
        desc=f"Definicion de probabilidad condicional:",
        latex=rf"P({lA}|{lB}) = \frac{{P({lA} \cap {lB})}}{{P({lB})}}",
        level_min=1,
    )
    if pB < 1e-15:
        builder.add_step(
            desc=f"P({name_B}) = 0: probabilidad condicional indefinida.",
            level_min=1,
        )
        return builder.build(final_value=float("nan"),
                             final_latex=rf"P({lA}|{lB}) = \text{{indefinida}}")

    pCond = pAB / pB
    builder.add_step(
        desc=f"P({name_A}|{name_B}) = {format_number(pAB)} / {format_number(pB)} = {format_number(pCond)}",
        latex=rf"P({lA}|{lB}) = \frac{{{format_number(pAB)}}}{{{format_number(pB)}}} = {format_number(pCond)}",
        result=pCond,
        level_min=1,
    )
    return builder.build(
        final_value=pCond,
        final_latex=rf"P({lA}|{lB}) = {format_number(pCond)}",
    )


def check_independence(
    pA: float, pB: float, pAB: float,
    name_A: str = "A", name_B: str = "B",
) -> CalcResult:
    """Verifica si P(A∩B) == P(A)·P(B)."""
    lA, lB = _ln(name_A), _ln(name_B)
    product = pA * pB
    are_independent = abs(pAB - product) < 1e-9
    builder = StepBuilder(f"Independencia: {name_A} y {name_B}")
    builder.add_step(
        desc="Criterio de independencia: A y B son independientes si P(A∩B) = P(A)·P(B)",
        latex=rf"{lA} \perp {lB} \iff P({lA} \cap {lB}) = P({lA}) \cdot P({lB})",
        level_min=1,
    )
    builder.add_step(
        desc=f"P({name_A})·P({name_B}) = {format_number(pA)} × {format_number(pB)} = {format_number(product)}",
        latex=rf"P({lA}) \cdot P({lB}) = {format_number(pA)} \times {format_number(pB)} = {format_number(product)}",
        result=product,
        level_min=2,
    )
    builder.add_step(
        desc=f"P({name_A}∩{name_B}) = {format_number(pAB)}",
        latex=rf"P({lA} \cap {lB}) = {format_number(pAB)}",
        result=pAB,
        level_min=2,
    )
    if are_independent:
        verdict = f"{name_A} y {name_B} son INDEPENDIENTES: P(A∩B) = {format_number(pAB)} = P(A)·P(B)"
        latex_verdict = rf"P({lA} \cap {lB}) = P({lA}) \cdot P({lB}) \implies \text{{Independientes}}"
    else:
        verdict = (f"{name_A} y {name_B} son DEPENDIENTES: "
                   f"P(A∩B) = {format_number(pAB)} ≠ P(A)·P(B) = {format_number(product)}")
        latex_verdict = rf"P({lA} \cap {lB}) \neq P({lA}) \cdot P({lB}) \implies \text{{Dependientes}}"
    builder.add_step(desc=verdict, latex=latex_verdict, level_min=1)

    # Interpretacion de P(A|B) vs P(A)
    if pB > 1e-15:
        pA_given_B = pAB / pB
        if not are_independent:
            if pA_given_B > pA + 1e-9:
                interp = f"P({name_A}|{name_B}) = {format_number(pA_given_B)} > P({name_A}) = {format_number(pA)}: {name_B} FAVORECE a {name_A}"
            elif pA_given_B < pA - 1e-9:
                interp = f"P({name_A}|{name_B}) = {format_number(pA_given_B)} < P({name_A}) = {format_number(pA)}: {name_B} DESFAVORECE a {name_A}"
            else:
                interp = f"P({name_A}|{name_B}) ≈ P({name_A}): neutros"
            builder.add_step(desc=interp, level_min=2)

    return builder.build(
        final_value=1.0 if are_independent else 0.0,
        final_latex=latex_verdict,
    )
