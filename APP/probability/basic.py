"""
Operaciones basicas de probabilidad — dos eventos A y B.

Cada funcion retorna un CalcResult con paso a paso usando el mismo motor
que los modelos de distribucion.
"""

from typing import Dict, Optional, Tuple
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


# ---------------------------------------------------------------------------
# Solver genérico: resolver P(A), P(B), P(A∩B) a partir de datos parciales
# ---------------------------------------------------------------------------

def solve_two_events(
    knowns: Dict[str, Optional[float]],
    name_A: str = "A",
    name_B: str = "B",
) -> Tuple[Dict[str, Optional[float]], Optional[CalcResult]]:
    """
    Resuelve el sistema de dos eventos a partir de cualquier combinación
    de datos conocidos.

    knowns puede contener:
        pA, pB, pAB, pAuB, pNone, pAgB, pBgA, pAc, pBc,
        rel ('independent' | 'mutually_exclusive' | None)

    Retorna (solved_dict, CalcResult con derivación paso a paso).
    solved_dict tiene claves: pA, pB, pAB (None si indeterminado).
    """
    pA: Optional[float] = knowns.get("pA")
    pB: Optional[float] = knowns.get("pB")
    pAB: Optional[float] = knowns.get("pAB")
    pAuB: Optional[float] = knowns.get("pAuB")
    pNone: Optional[float] = knowns.get("pNone")
    pAgB: Optional[float] = knowns.get("pAgB")
    pBgA: Optional[float] = knowns.get("pBgA")
    pAc: Optional[float] = knowns.get("pAc")
    pBc: Optional[float] = knowns.get("pBc")
    rel: Optional[str] = knowns.get("rel")

    lA, lB = _ln(name_A), _ln(name_B)
    builder = StepBuilder("Derivación del sistema")
    derived_any = False  # solo crear CalcResult si hubo derivación

    # --- Paso 0: conversiones directas (complementos) ---
    if pA is None and pAc is not None:
        pA = 1 - pAc
        builder.add_step(
            desc=f"P({name_A}) a partir de su complemento",
            latex=rf"P({lA}) = 1 - P({lA}^c) = 1 - {format_number(pAc, 4)} = {format_number(pA, 4)}",
            result=pA, level_min=1,
        )
        derived_any = True

    if pB is None and pBc is not None:
        pB = 1 - pBc
        builder.add_step(
            desc=f"P({name_B}) a partir de su complemento",
            latex=rf"P({lB}) = 1 - P({lB}^c) = 1 - {format_number(pBc, 4)} = {format_number(pB, 4)}",
            result=pB, level_min=1,
        )
        derived_any = True

    if pNone is not None and pAuB is None:
        pAuB = 1 - pNone
        builder.add_step(
            desc=f"P({name_A}∪{name_B}) a partir de P(ninguno)",
            latex=(rf"P({lA} \cup {lB}) = 1 - P({lA}' \cap {lB}') = "
                   rf"1 - {format_number(pNone, 4)} = {format_number(pAuB, 4)}"),
            result=pAuB, level_min=1,
        )
        derived_any = True

    # --- Resolución iterativa ---
    _MAX_ITER = 10
    for _ in range(_MAX_ITER):
        progress = False

        # P(A∩B) por mutuamente excluyentes
        if pAB is None and rel == "mutually_exclusive":
            pAB = 0.0
            builder.add_step(
                desc="Mutuamente excluyentes → P(A∩B) = 0",
                latex=rf"P({lA} \cap {lB}) = 0",
                result=0.0, level_min=1,
            )
            progress = derived_any = True

        # P(A∩B) por independencia
        if pAB is None and rel == "independent" and pA is not None and pB is not None:
            pAB = pA * pB
            builder.add_step(
                desc="Independientes → P(A∩B) = P(A)·P(B)",
                latex=(rf"P({lA} \cap {lB}) = {format_number(pA, 4)} \cdot "
                       rf"{format_number(pB, 4)} = {format_number(pAB, 4)}"),
                result=pAB, level_min=1,
            )
            progress = derived_any = True

        # P(A∩B) desde P(A|B)·P(B)
        if pAB is None and pAgB is not None and pB is not None:
            pAB = pAgB * pB
            builder.add_step(
                desc="P(A∩B) desde condicional P(A|B)",
                latex=(rf"P({lA} \cap {lB}) = P({lA}|{lB}) \cdot P({lB}) = "
                       rf"{format_number(pAgB, 4)} \cdot {format_number(pB, 4)} = {format_number(pAB, 4)}"),
                result=pAB, level_min=1,
            )
            progress = derived_any = True

        # P(A∩B) desde P(B|A)·P(A)
        if pAB is None and pBgA is not None and pA is not None:
            pAB = pBgA * pA
            builder.add_step(
                desc="P(A∩B) desde condicional P(B|A)",
                latex=(rf"P({lA} \cap {lB}) = P({lB}|{lA}) \cdot P({lA}) = "
                       rf"{format_number(pBgA, 4)} \cdot {format_number(pA, 4)} = {format_number(pAB, 4)}"),
                result=pAB, level_min=1,
            )
            progress = derived_any = True

        # P(A∩B) desde unión: P(A∩B) = P(A) + P(B) - P(A∪B)
        if pAB is None and pA is not None and pB is not None and pAuB is not None:
            pAB = pA + pB - pAuB
            builder.add_step(
                desc="P(A∩B) desde fórmula de unión",
                latex=(rf"P({lA} \cap {lB}) = P({lA}) + P({lB}) - P({lA} \cup {lB}) = "
                       rf"{format_number(pA, 4)} + {format_number(pB, 4)} - "
                       rf"{format_number(pAuB, 4)} = {format_number(pAB, 4)}"),
                result=pAB, level_min=1,
            )
            progress = derived_any = True

        # P(A) desde unión: P(A) = P(A∪B) + P(A∩B) - P(B)
        if pA is None and pB is not None and pAB is not None and pAuB is not None:
            pA = pAuB + pAB - pB
            builder.add_step(
                desc=f"P({name_A}) despejando de la fórmula de unión",
                latex=(rf"P({lA}) = P({lA} \cup {lB}) + P({lA} \cap {lB}) - P({lB}) = "
                       rf"{format_number(pAuB, 4)} + {format_number(pAB, 4)} - "
                       rf"{format_number(pB, 4)} = {format_number(pA, 4)}"),
                result=pA, level_min=1,
            )
            progress = derived_any = True

        # P(B) desde unión: P(B) = P(A∪B) + P(A∩B) - P(A)
        if pB is None and pA is not None and pAB is not None and pAuB is not None:
            pB = pAuB + pAB - pA
            builder.add_step(
                desc=f"P({name_B}) despejando de la fórmula de unión",
                latex=(rf"P({lB}) = P({lA} \cup {lB}) + P({lA} \cap {lB}) - P({lA}) = "
                       rf"{format_number(pAuB, 4)} + {format_number(pAB, 4)} - "
                       rf"{format_number(pA, 4)} = {format_number(pB, 4)}"),
                result=pB, level_min=1,
            )
            progress = derived_any = True

        # P(A∪B) desde P(A) + P(B) - P(A∩B)
        if pAuB is None and pA is not None and pB is not None and pAB is not None:
            pAuB = pA + pB - pAB
            progress = True  # no step needed — auxiliary

        # P(A) desde P(B|A): P(A) = P(A∩B) / P(B|A)
        if pA is None and pBgA is not None and pAB is not None and pBgA > 1e-15:
            pA = pAB / pBgA
            builder.add_step(
                desc=f"P({name_A}) desde condicional P({name_B}|{name_A})",
                latex=(rf"P({lA}) = \frac{{P({lA} \cap {lB})}}{{P({lB}|{lA})}} = "
                       rf"\frac{{{format_number(pAB, 4)}}}{{{format_number(pBgA, 4)}}} = "
                       rf"{format_number(pA, 4)}"),
                result=pA, level_min=1,
            )
            progress = derived_any = True

        # P(B) desde P(A|B): P(B) = P(A∩B) / P(A|B)
        if pB is None and pAgB is not None and pAB is not None and pAgB > 1e-15:
            pB = pAB / pAgB
            builder.add_step(
                desc=f"P({name_B}) desde condicional P({name_A}|{name_B})",
                latex=(rf"P({lB}) = \frac{{P({lA} \cap {lB})}}{{P({lA}|{lB})}} = "
                       rf"\frac{{{format_number(pAB, 4)}}}{{{format_number(pAgB, 4)}}} = "
                       rf"{format_number(pB, 4)}"),
                result=pB, level_min=1,
            )
            progress = derived_any = True

        # P(A) por independencia + unión
        if (pA is None and rel == "independent" and pB is not None
                and pAuB is not None and pB < 1.0):
            pA = (pAuB - pB) / (1 - pB)
            builder.add_step(
                desc=f"P({name_A}) por independencia y unión",
                latex=(rf"P({lA}) = \frac{{P({lA} \cup {lB}) - P({lB})}}{{1 - P({lB})}} = "
                       rf"\frac{{{format_number(pAuB, 4)} - {format_number(pB, 4)}}}"
                       rf"{{{format_number(1 - pB, 4)}}} = {format_number(pA, 4)}"),
                result=pA, level_min=1,
            )
            progress = derived_any = True

        # P(B) por independencia + unión
        if (pB is None and rel == "independent" and pA is not None
                and pAuB is not None and pA < 1.0):
            pB = (pAuB - pA) / (1 - pA)
            builder.add_step(
                desc=f"P({name_B}) por independencia y unión",
                latex=(rf"P({lB}) = \frac{{P({lA} \cup {lB}) - P({lA})}}{{1 - P({lA})}} = "
                       rf"\frac{{{format_number(pAuB, 4)} - {format_number(pA, 4)}}}"
                       rf"{{{format_number(1 - pA, 4)}}} = {format_number(pB, 4)}"),
                result=pB, level_min=1,
            )
            progress = derived_any = True

        if not progress:
            break

    solved = {"pA": pA, "pB": pB, "pAB": pAB}

    if not derived_any:
        return solved, None

    # Resumen final
    parts = []
    if pA is not None:
        parts.append(rf"P({lA}) = {format_number(pA, 4)}")
    if pB is not None:
        parts.append(rf"P({lB}) = {format_number(pB, 4)}")
    if pAB is not None:
        parts.append(rf"P({lA} \cap {lB}) = {format_number(pAB, 4)}")
    if parts:
        builder.add_step(
            desc="Sistema resuelto",
            latex=r",\quad ".join(parts),
            level_min=1,
        )

    cr = builder.build(
        final_value=pAB if pAB is not None else 0.0,
        final_latex=r",\quad ".join(parts) if parts else "",
    )
    return solved, cr
