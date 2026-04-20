"""Contrato base para las calculadoras de la pestaña 'Cálculos extra'."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Set


class ExtraCalculator(ABC):
    """Calculadora adicional sobre una distribución ya configurada.

    Las subclases declaran en qué familias aplican (``discrete``, ``custom_pmf``,
    ``continuous``) y exponen ``render`` para dibujar su UI dentro de la pestaña.
    """

    name: str = ""
    short_name: str = ""
    description: str = ""
    families: Set[str] = set()

    def applies_to(self, family: str, model) -> bool:
        return family in self.families

    @abstractmethod
    def render(self, model, model_label: str, detail_level: int) -> None: ...
