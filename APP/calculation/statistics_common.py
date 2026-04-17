"""Funciones estadisticas comunes para todas las distribuciones."""

import math
from decimal import Decimal, ROUND_DOWN
from typing import Callable, Tuple, Optional
from calculation.step_types import CalcResult
from calculation.step_engine import StepBuilder


def compute_cdf_left_discrete(prob_func: Callable[[int], float],
                               r: int, domain_min: int) -> float:
    """F(r) = P(VA <= r) = sum P(x) para x de domain_min a r."""
    return sum(prob_func(x) for x in range(domain_min, r + 1))


def compute_cdf_right_discrete(prob_func: Callable[[int], float],
                                r: int, domain_max: int) -> float:
    """G(r) = P(VA >= r) = sum P(x) para x de r a domain_max."""
    return sum(prob_func(x) for x in range(r, domain_max + 1))


def compute_partial_expectation_left(prob_func: Callable[[int], float],
                                      r: int, domain_min: int) -> float:
    """H(r) = sum x*P(x) para x de domain_min a r."""
    return sum(x * prob_func(x) for x in range(domain_min, r + 1))


def compute_partial_expectation_right(prob_func: Callable[[int], float],
                                       r: int, domain_max: int) -> float:
    """J(r) = sum x*P(x) para x de r a domain_max."""
    return sum(x * prob_func(x) for x in range(r, domain_max + 1))


def compute_truncated_mean_left(h_r: float, f_r: float) -> Optional[float]:
    """Promedio truncado izquierdo = H(r) / F(r)."""
    if abs(f_r) < 1e-15:
        return None
    return h_r / f_r


def compute_truncated_mean_right(j_r: float, g_r: float) -> Optional[float]:
    """Promedio truncado derecho = J(r) / G(r)."""
    if abs(g_r) < 1e-15:
        return None
    return j_r / g_r


def compute_truncated_mean_two_sided(h_b: float, h_a_minus_1: float,
                                      f_b: float, f_a_minus_1: float) -> Optional[float]:
    """Promedio truncado a dos colas = [H(B) - H(A-1)] / [F(B) - F(A-1)]."""
    denom = f_b - f_a_minus_1
    if abs(denom) < 1e-15:
        return None
    return (h_b - h_a_minus_1) / denom


def find_mode_discrete(prob_func: Callable[[int], float],
                        domain_min: int, domain_max: int) -> int:
    """Encuentra la moda (valor con mayor probabilidad)."""
    best_r = domain_min
    best_p = prob_func(domain_min)
    for r in range(domain_min + 1, domain_max + 1):
        p = prob_func(r)
        if p > best_p:
            best_p = p
            best_r = r
    return best_r


def find_median_discrete(cdf_left_func: Callable[[int], float],
                          domain_min: int, domain_max: int) -> int:
    """Encuentra la mediana: menor r tal que F(r) >= 0.5."""
    for r in range(domain_min, domain_max + 1):
        if cdf_left_func(r) >= 0.5:
            return r
    return domain_max


def build_full_table_discrete(prob_func: Callable[[int], float],
                               domain_min: int, domain_max: int) -> list:
    """Construye tabla completa: r, P(r), F(r), G(r), H(r), J(r)."""
    table = []
    cum_f = 0.0
    cum_h = 0.0

    # Primero calculamos todo hacia adelante
    rows = []
    for r in range(domain_min, domain_max + 1):
        p_r = prob_func(r)
        cum_f += p_r
        cum_h += r * p_r
        rows.append({"r": r, "P(r)": p_r, "F(r)": cum_f, "H(r)": cum_h})

    # Ahora calculamos G(r) y J(r) hacia atras
    total_mean = cum_h  # E(r) = sum r*P(r)
    cum_g = 0.0
    cum_j = 0.0
    for i in range(len(rows) - 1, -1, -1):
        row = rows[i]
        cum_g += row["P(r)"]
        cum_j += row["r"] * row["P(r)"]
        row["G(r)"] = cum_g
        row["J(r)"] = cum_j

    return rows


def _custom_round(value: float, decimals: int) -> float:
    """Trunca a *decimals* decimales; sube el último dígito solo si el siguiente es >= 6.

    Regla de cátedra:
        5.º dígito >= 6 → el 4.º sube 1
        5.º dígito <= 5 → el 4.º queda igual
    Ejemplo: 0.55648 → 0.5565 | 0.55645 → 0.5564
    """
    if value == 0:
        return 0.0
    d = Decimal(str(value))
    sign = 1 if d >= 0 else -1
    d = abs(d)

    step = Decimal(10) ** -decimals
    truncated = (d / step).to_integral_value(rounding=ROUND_DOWN) * step

    step_extra = Decimal(10) ** -(decimals + 1)
    extended = (d / step_extra).to_integral_value(rounding=ROUND_DOWN)
    next_digit = int(extended % 10)

    if next_digit >= 6:
        truncated += step

    return float(sign * truncated)


def format_number(value: float, decimals: int = 4) -> str:
    """Formatea un número con hasta *decimals* cifras decimales.

    Usa redondeo de cátedra: sube el último dígito solo si el siguiente es >= 6.
    Enteros se muestran sin decimales (ej. 495 → '495').
    Si no se pierde información al truncar, no agrega ceros de relleno
    (ej. 1.5 → '1.5', pero 1.50001 → '1.5000').
    """
    if value == int(value) and abs(value) < 1e12:
        return str(int(value))
    rounded = _custom_round(value, decimals)
    formatted = f"{rounded:.{decimals}f}"
    # Si el valor original ya cabía en menos decimales, quitar ceros sobrantes
    if rounded == value:
        formatted = formatted.rstrip("0").rstrip(".")
    return formatted


def format_fraction(numerator: int, denominator: int) -> str:
    """Formatea como fraccion simplificada."""
    g = math.gcd(abs(numerator), abs(denominator))
    num = numerator // g
    den = denominator // g
    if den == 1:
        return str(num)
    return f"{num}/{den}"
