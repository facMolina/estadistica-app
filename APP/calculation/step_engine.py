"""Motor de construccion de pasos (StepBuilder)."""

from typing import List, Optional
from calculation.step_types import Step, CalcResult


class StepBuilder:
    """Builder para construir CalcResult con pasos anidados."""

    def __init__(self, name: str):
        self.name = name
        self._steps: List[Step] = []
        self._step_stack: List[List[Step]] = [self._steps]

    def add_step(
        self,
        desc: str,
        latex: str = "",
        latex_sub: str = "",
        latex_res: str = "",
        result: Optional[float] = None,
        level_min: int = 1,
    ) -> "StepBuilder":
        """Agrega un paso al nivel actual."""
        step = Step(
            description=desc,
            latex_formula=latex,
            latex_substituted=latex_sub,
            latex_result=latex_res,
            numeric_result=result,
            detail_level_min=level_min,
        )
        self._step_stack[-1].append(step)
        return self

    def begin_substeps(self) -> "StepBuilder":
        """Abre un nivel de sub-steps (se agregan al ultimo step del nivel actual)."""
        parent = self._step_stack[-1][-1]
        self._step_stack.append(parent.sub_steps)
        return self

    def end_substeps(self) -> "StepBuilder":
        """Cierra el nivel actual de sub-steps."""
        if len(self._step_stack) > 1:
            self._step_stack.pop()
        return self

    def add_substep(
        self,
        desc: str,
        latex: str = "",
        latex_sub: str = "",
        latex_res: str = "",
        result: Optional[float] = None,
        level_min: int = 3,
    ) -> "StepBuilder":
        """Agrega un sub-step al ultimo step del nivel actual. Shortcut."""
        if not self._step_stack[-1]:
            return self.add_step(desc, latex, latex_sub, latex_res, result, level_min)
        parent = self._step_stack[-1][-1]
        step = Step(
            description=desc,
            latex_formula=latex,
            latex_substituted=latex_sub,
            latex_result=latex_res,
            numeric_result=result,
            detail_level_min=level_min,
        )
        parent.sub_steps.append(step)
        return self

    def merge_result(self, other: CalcResult, level_min: int = 3) -> "StepBuilder":
        """Incorpora los steps de otro CalcResult como sub-steps del ultimo step."""
        if not self._step_stack[-1]:
            return self
        parent = self._step_stack[-1][-1]
        for step in other.steps:
            step.detail_level_min = max(step.detail_level_min, level_min)
            parent.sub_steps.append(step)
        return self

    def build(self, final_value: Optional[float] = None, final_latex: str = "",
              fraction_str: str = "") -> CalcResult:
        """Construye el CalcResult final."""
        return CalcResult(
            name=self.name,
            steps=self._steps,
            final_value=final_value,
            final_latex=final_latex,
            fraction_str=fraction_str,
        )
