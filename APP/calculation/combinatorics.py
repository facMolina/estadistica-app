"""Funciones combinatorias con paso a paso."""

import math
from functools import lru_cache
from calculation.step_types import CalcResult, Step
from calculation.step_engine import StepBuilder


@lru_cache(maxsize=1024)
def factorial(n: int) -> int:
    """Factorial con cache."""
    return math.factorial(n)


@lru_cache(maxsize=4096)
def comb(n: int, r: int) -> int:
    """Numero combinatorio C(n, r)."""
    if r < 0 or r > n:
        return 0
    return math.comb(n, r)


def comb_with_steps(n: int, r: int) -> CalcResult:
    """Calcula C(n, r) con paso a paso detallado."""
    builder = StepBuilder(f"C({n},{r})")

    if r < 0 or r > n:
        builder.add_step(
            desc=f"C({n},{r}) = 0 (r fuera de rango)",
            latex=rf"\binom{{{n}}}{{{r}}} = 0",
            result=0,
            level_min=1,
        )
        return builder.build(final_value=0, final_latex=rf"\binom{{{n}}}{{{r}}} = 0")

    result = comb(n, r)

    # Nivel 1: solo el resultado
    builder.add_step(
        desc=f"C({n},{r}) = {result}",
        latex=rf"\binom{{{n}}}{{{r}}}",
        latex_res=rf"= {result}",
        result=result,
        level_min=1,
    )

    # Nivel 2: formula con valores
    builder.add_step(
        desc=f"Aplicamos la formula del combinatorio",
        latex=rf"\binom{{{n}}}{{{r}}} = \frac{{{n}!}}{{{r}! \cdot {n - r}!}}",
        level_min=2,
    )

    # Nivel 3: desarrollo de factoriales
    if n <= 20:  # Solo mostrar factoriales explícitos para n razonable
        n_fact = factorial(n)
        r_fact = factorial(r)
        nr_fact = factorial(n - r)

        builder.add_step(
            desc=f"{n}! = {n_fact}",
            latex=rf"{n}! = {n_fact}",
            result=n_fact,
            level_min=3,
        )
        builder.add_step(
            desc=f"{r}! = {r_fact}",
            latex=rf"{r}! = {r_fact}",
            result=r_fact,
            level_min=3,
        )
        if n - r != r:
            builder.add_step(
                desc=f"{n - r}! = {nr_fact}",
                latex=rf"{n - r}! = {nr_fact}",
                result=nr_fact,
                level_min=3,
            )

        builder.add_step(
            desc=f"C({n},{r}) = {n_fact} / ({r_fact} * {nr_fact}) = {result}",
            latex=rf"\binom{{{n}}}{{{r}}} = \frac{{{n_fact}}}{{{r_fact} \cdot {nr_fact}}} = {result}",
            result=result,
            level_min=2,
        )
    else:
        # Para n grande, mostrar la forma simplificada
        terms = " \\cdot ".join(str(n - i) for i in range(min(r, n - r)))
        builder.add_step(
            desc=f"Forma simplificada: {terms} / {min(r, n-r)}! = {result}",
            latex=rf"\binom{{{n}}}{{{r}}} = \frac{{{terms}}}{{{min(r, n-r)}!}} = {result}",
            result=result,
            level_min=2,
        )

    return builder.build(
        final_value=result,
        final_latex=rf"\binom{{{n}}}{{{r}}} = {result}",
    )
