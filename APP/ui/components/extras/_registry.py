"""Registry of calculators available in the 'Cálculos extra' tab.

Apendeá la calculadora nueva acá y listo — el dispatcher la muestra
automáticamente en cada flujo donde ``applies_to`` matchee.
"""

from __future__ import annotations

from ui.components.extras._base import ExtraCalculator
from ui.components.extras.linear_transform import LinearTransformCalculator

EXTRA_CALCULATORS: list[ExtraCalculator] = [
    LinearTransformCalculator(),
]
