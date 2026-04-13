"""Tipos de datos para el motor de paso a paso."""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Step:
    """Un paso individual de calculo."""
    description: str           # Texto en espanol: "Calculamos el numero combinatorio C(10,3)"
    latex_formula: str = ""    # LaTeX de la formula general
    latex_substituted: str = "" # LaTeX con valores reemplazados
    latex_result: str = ""     # LaTeX del resultado
    numeric_result: Optional[float] = None
    sub_steps: List["Step"] = field(default_factory=list)
    detail_level_min: int = 1  # Nivel minimo de detalle en el que se muestra
                               # 1=siempre, 2=intermedio+, 3=solo maximo


@dataclass
class CalcResult:
    """Resultado completo de un calculo con paso a paso."""
    name: str                  # "Funcion de Probabilidad P(r)"
    steps: List[Step] = field(default_factory=list)
    final_value: Optional[float] = None
    final_latex: str = ""      # LaTeX completo del resultado final
    fraction_str: str = ""     # Representacion como fraccion (ej: "21/91")

    def get_steps_for_level(self, detail_level: int) -> List[Step]:
        """Filtra steps segun el nivel de detalle solicitado."""
        return _filter_steps(self.steps, detail_level)


def _filter_steps(steps: List[Step], detail_level: int) -> List[Step]:
    """Filtra recursivamente los steps segun nivel de detalle."""
    filtered = []
    for step in steps:
        if step.detail_level_min <= detail_level:
            filtered_step = Step(
                description=step.description,
                latex_formula=step.latex_formula,
                latex_substituted=step.latex_substituted,
                latex_result=step.latex_result,
                numeric_result=step.numeric_result,
                sub_steps=_filter_steps(step.sub_steps, detail_level),
                detail_level_min=step.detail_level_min,
            )
            filtered.append(filtered_step)
    return filtered
