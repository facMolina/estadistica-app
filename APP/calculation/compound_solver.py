"""Solver para problemas compuestos (múltiples distribuciones encadenadas)."""

from models.discrete.binomial import Binomial
from models.discrete.hypergeometric import Hipergeometrico
from calculation.statistics_common import format_number


def solve_compound(config: dict) -> dict:
    """Despacha al solver compuesto correspondiente."""
    ctype = config["compound_type"]
    if ctype == "hiper_binomial":
        return solve_hiper_binomial(config)
    if ctype == "pascal_conditional":
        return solve_pascal_conditional(config)
    raise ValueError(f"Tipo compuesto desconocido: {ctype}")


def solve_hiper_binomial(config: dict) -> dict:
    """
    Compuesto: Hipergeométrico (por caja) + Binomial (entre cajas).

    Paso 1: P(rechazar una caja) = Gh(reject_r / sample_n ; box_N ; box_R)
    Paso 2: Binomial(n=num_boxes, p=p_rechazo) → consulta sobre cajas rechazadas
    """
    box_N = config["box_N"]
    box_R = config["box_R"]
    sample_n = config["sample_n"]
    num_boxes = config["num_boxes"]
    reject_r = config.get("reject_r", 1)
    query_type = config["query_type"]
    query_r = config["query_r"]

    # Paso 1: P(rechazar una caja)
    hiper = Hipergeometrico(N=box_N, R=box_R, n=sample_n)
    step1_result = hiper.cdf_right(reject_r)
    p_reject = step1_result.final_value

    # Paso 2: Binomial con p = p_rechazo
    binom = Binomial(n=num_boxes, p=round(p_reject, 10))
    if query_type == "cdf_left":
        step2_result = binom.cdf_left(query_r)
        notation2 = f"Fb({query_r}/{num_boxes};{format_number(p_reject, 4)})"
    elif query_type == "cdf_right":
        step2_result = binom.cdf_right(query_r)
        notation2 = f"Gb({query_r}/{num_boxes};{format_number(p_reject, 4)})"
    else:
        step2_result = binom.probability(query_r)
        notation2 = f"Pb({query_r}/{num_boxes};{format_number(p_reject, 4)})"

    return {
        "compound_type": "hiper_binomial",
        "title": "Problema Compuesto: Hipergeométrico + Binomial",
        "steps": [
            {
                "num": 1,
                "title": "Probabilidad de rechazar una caja (Hipergeométrico)",
                "description": (
                    f"Cada caja tiene N={box_N} piezas con R={box_R} defectuosa(s). "
                    f"Se toma una muestra de n={sample_n}. "
                    f"Se rechaza si se encuentra al menos {reject_r} defectuosa."
                ),
                "notation": f"Gh({reject_r}/{sample_n};{box_N};{box_R})",
                "calc_result": step1_result,
                "result_label": "p (rechazar una caja)",
                "result_value": p_reject,
            },
            {
                "num": 2,
                "title": f"Cajas rechazadas de {num_boxes} (Binomial)",
                "description": (
                    f"Con p={format_number(p_reject, 4)} de rechazar cada caja, "
                    f"en n={num_boxes} cajas independientes."
                ),
                "notation": notation2,
                "calc_result": step2_result,
                "result_label": "Resultado final",
                "result_value": step2_result.final_value,
            },
        ],
        "final_value": step2_result.final_value,
    }


def solve_pascal_conditional(config: dict) -> dict:
    """
    Compuesto: Pascal condicional.

    P(N > query_n | N > condition_n) = P(N > query_n) / P(N > condition_n)

    Usando equivalencia Binomial:
        P(N > k) = P(menos de r éxitos en k ensayos) = Fb(r-1 / k ; p)
    """
    r_success = config["r_success"]
    p = config["p"]
    condition_n = config["condition_n"]
    query_n = config["query_n"]

    binom_query = Binomial(n=query_n, p=p)
    binom_cond = Binomial(n=condition_n, p=p)

    step1_result = binom_query.cdf_left(r_success - 1)
    step2_result = binom_cond.cdf_left(r_success - 1)

    p_num = step1_result.final_value
    p_den = step2_result.final_value
    p_final = p_num / p_den if p_den > 0 else 0.0

    return {
        "compound_type": "pascal_conditional",
        "title": "Problema Compuesto: Pascal Condicional",
        "description": (
            f"Se necesitan {r_success} piezas buenas (p={p}). "
            f"Dado que en {condition_n} piezas no se alcanzó, "
            f"¿P(necesitar más de {query_n})?"
        ),
        "steps": [
            {
                "num": 1,
                "title": f"P(N > {query_n})",
                "description": (
                    f"P(necesitar más de {query_n} ensayos para {r_success} éxitos) = "
                    f"P(menos de {r_success} éxitos en {query_n} ensayos)"
                ),
                "notation": f"Fb({r_success - 1}/{query_n};{p})",
                "calc_result": step1_result,
                "result_label": f"P(N > {query_n})",
                "result_value": p_num,
            },
            {
                "num": 2,
                "title": f"P(N > {condition_n})",
                "description": (
                    f"P(necesitar más de {condition_n} ensayos para {r_success} éxitos) = "
                    f"P(menos de {r_success} éxitos en {condition_n} ensayos)"
                ),
                "notation": f"Fb({r_success - 1}/{condition_n};{p})",
                "calc_result": step2_result,
                "result_label": f"P(N > {condition_n})",
                "result_value": p_den,
            },
        ],
        "conditional": {
            "query_n": query_n,
            "condition_n": condition_n,
            "numerator_value": p_num,
            "denominator_value": p_den,
        },
        "final_value": p_final,
    }
