"""Catálogo de modelos: cuáles están implementados en Streamlit y cuáles pendientes."""

# Modelos completamente implementados en app_streamlit.py
IMPLEMENTED_MODELS = {
    "Binomial",
}

# Modelos que la CLI puede identificar pero aún no están en Streamlit
PENDING_MODELS = {
    "Pascal",
    "Hipergeometrico",
    "Hiper-Pascal",
    "Poisson",
    "Multinomial",
    "Normal",
    "Log-Normal",
    "Exponencial",
    "Gamma",
    "Weibull",
    "Gumbel Min",
    "Gumbel Max",
    "Pareto",
    "Uniforme",
}

# Aliases que puede generar Claude → nombre canónico
MODEL_ALIASES = {
    "Binomial Negativa": "Pascal",
    "Binomial negativa": "Pascal",
    "Hipergeométrico": "Hipergeometrico",
    "Hypergeometric": "Hipergeometrico",
    "Hiper Pascal": "Hiper-Pascal",
    "HiperPascal": "Hiper-Pascal",
    "Log Normal": "Log-Normal",
    "Lognormal": "Log-Normal",
    "log-normal": "Log-Normal",
    "Exponential": "Exponencial",
    "exponencial": "Exponencial",
    "Erlang": "Gamma",
    "Gamma/Erlang": "Gamma",
    "gamma": "Gamma",
    "Gumbel": "Gumbel Max",
    "Gumbel Máximo": "Gumbel Max",
    "Gumbel Mínimo": "Gumbel Min",
    "gumbel max": "Gumbel Max",
    "gumbel min": "Gumbel Min",
    "Uniform": "Uniforme",
    "uniforme": "Uniforme",
    "pareto": "Pareto",
    "normal": "Normal",
    "poisson": "Poisson",
    "binomial": "Binomial",
    "pascal": "Pascal",
    "weibull": "Weibull",
}


def normalize_model_name(name: str) -> str:
    """Normaliza el nombre del modelo al nombre canónico del catálogo."""
    if name in MODEL_ALIASES:
        return MODEL_ALIASES[name]
    # Buscar case-insensitive si no hubo match exacto
    for alias, canonical in MODEL_ALIASES.items():
        if alias.lower() == name.lower():
            return canonical
    return name


def is_implemented(model_name: str) -> bool:
    """Retorna True si el modelo está implementado en Streamlit."""
    return normalize_model_name(model_name) in IMPLEMENTED_MODELS
