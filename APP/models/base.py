"""Clases base abstractas para modelos de probabilidad."""

from abc import ABC, abstractmethod
from typing import Tuple, Optional, List, Dict
from calculation.step_types import CalcResult


class DiscreteModel(ABC):
    """Clase base para distribuciones discretas."""

    @abstractmethod
    def name(self) -> str:
        """Nombre del modelo (ej: 'Binomial')."""
        ...

    @abstractmethod
    def params_dict(self) -> Dict[str, float]:
        """Diccionario de parametros (ej: {'n': 10, 'p': 0.3})."""
        ...

    @abstractmethod
    def domain(self) -> Tuple[int, int]:
        """Retorna (min_r, max_r) del dominio."""
        ...

    @abstractmethod
    def probability(self, r: int) -> CalcResult:
        """P(VA = r) con paso a paso."""
        ...

    @abstractmethod
    def probability_value(self, r: int) -> float:
        """P(VA = r) solo valor numerico (para calculos internos)."""
        ...

    @abstractmethod
    def cdf_left(self, r: int) -> CalcResult:
        """F(r) = P(VA <= r)."""
        ...

    @abstractmethod
    def cdf_right(self, r: int) -> CalcResult:
        """G(r) = P(VA >= r)."""
        ...

    @abstractmethod
    def mean(self) -> CalcResult:
        """Esperanza matematica E(r) = mu."""
        ...

    @abstractmethod
    def variance(self) -> CalcResult:
        """Varianza V(r) = sigma^2."""
        ...

    @abstractmethod
    def std_dev(self) -> CalcResult:
        """Desvio estandar D(r) = sigma."""
        ...

    @abstractmethod
    def mode(self) -> CalcResult:
        """Moda Mo."""
        ...

    @abstractmethod
    def median(self) -> CalcResult:
        """Mediana Me."""
        ...

    @abstractmethod
    def cv(self) -> CalcResult:
        """Coeficiente de variacion Cv."""
        ...

    @abstractmethod
    def skewness(self) -> CalcResult:
        """Coeficiente de asimetria As."""
        ...

    @abstractmethod
    def kurtosis(self) -> CalcResult:
        """Coeficiente de kurtosis Ku."""
        ...

    @abstractmethod
    def partial_expectation_left(self, r: int) -> CalcResult:
        """Expectativa parcial izquierda H(r)."""
        ...

    @abstractmethod
    def latex_formula(self) -> str:
        """Representacion LaTeX de la funcion de probabilidad."""
        ...

    def full_table(self) -> List[Dict]:
        """Tabla completa de la distribucion."""
        from calculation.statistics_common import build_full_table_discrete
        d_min, d_max = self.domain()
        return build_full_table_discrete(self.probability_value, d_min, d_max)

    def all_characteristics(self) -> Dict[str, CalcResult]:
        """Calcula todas las caracteristicas del modelo."""
        return {
            "Esperanza Matematica": self.mean(),
            "Varianza": self.variance(),
            "Desvio Estandar": self.std_dev(),
            "Moda": self.mode(),
            "Mediana": self.median(),
            "Coef. de Variacion": self.cv(),
            "Coef. de Asimetria": self.skewness(),
            "Coef. de Kurtosis": self.kurtosis(),
        }


class ContinuousModel(ABC):
    """Clase base para distribuciones continuas."""

    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    def params_dict(self) -> Dict[str, float]:
        ...

    @abstractmethod
    def domain(self) -> Tuple[float, float]:
        """Retorna (min_x, max_x). Puede ser (-inf, inf)."""
        ...

    @abstractmethod
    def density(self, x: float) -> CalcResult:
        """f(x) con paso a paso."""
        ...

    @abstractmethod
    def density_value(self, x: float) -> float:
        """f(x) solo valor numerico."""
        ...

    @abstractmethod
    def cdf_left(self, x: float) -> CalcResult:
        """F(x) = P(VA <= x)."""
        ...

    @abstractmethod
    def cdf_right(self, x: float) -> CalcResult:
        """G(x) = P(VA >= x)."""
        ...

    @abstractmethod
    def mean(self) -> CalcResult:
        ...

    @abstractmethod
    def variance(self) -> CalcResult:
        ...

    @abstractmethod
    def std_dev(self) -> CalcResult:
        ...

    @abstractmethod
    def mode(self) -> CalcResult:
        ...

    @abstractmethod
    def median(self) -> CalcResult:
        ...

    @abstractmethod
    def cv(self) -> CalcResult:
        ...

    @abstractmethod
    def skewness(self) -> CalcResult:
        ...

    @abstractmethod
    def kurtosis(self) -> CalcResult:
        ...

    @abstractmethod
    def partial_expectation_left(self, x: float) -> CalcResult:
        ...

    @abstractmethod
    def latex_formula(self) -> str:
        ...

    def fractile(self, alpha: float) -> CalcResult:
        """Fractil x(alpha): valor tal que F(x) = alpha."""
        raise NotImplementedError("Fractil no implementado para este modelo")

    def all_characteristics(self) -> Dict[str, CalcResult]:
        return {
            "Esperanza Matematica": self.mean(),
            "Varianza": self.variance(),
            "Desvio Estandar": self.std_dev(),
            "Moda": self.mode(),
            "Mediana": self.median(),
            "Coef. de Variacion": self.cv(),
            "Coef. de Asimetria": self.skewness(),
            "Coef. de Kurtosis": self.kurtosis(),
        }
