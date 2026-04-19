"""
Parser de lenguaje natural para problemas estadísticos.
Sin dependencias de API — usa regex y keywords.

Al agregar un modelo nuevo: ver sección "Parser de lenguaje natural" en CLAUDE.md.
"""

import re


# ---------------------------------------------------------------------------
# Configuración de reglas — acá se agregan patrones al iterar
# ---------------------------------------------------------------------------

# Fase A: keywords para detectar modelo
MODELO_PATTERNS: dict[str, list[str]] = {
    "Binomial": [
        r"binomial",
        r"bernoulli",
        r"\bmoneda\b",
        r"\bdado\b",
        r"\bdados\b",
        r"ensayos?\s+independientes?",
        r"con\s+reposici[oó]n",
        r"[FGPfgp]b\s*\(",          # notación cátedra: Fb(), Gb(), Pb()
        r"\blanz[ao]",               # "lanzo", "lanza", "lanzar", "lanzamiento"
        r"\btir[ao]",                # "tiro", "tira", "tirar"
        r"\bpruebas?\b",
        r"\bensayos?\b",
        r"\bexitos?\b",
        r"\béxitos?\b",
        r"se\s+(?:realizan?|hacen?|repite[en]?)",
        r"\bprobabilidad\s+de\s+(?:éxito|exito|acierto)",
        r"\bdefectuos[oa]s?\b",
        r"\baciertos?\b",
        r"\bfallad[oa]s?\b",         # "fallada", "fallado", "falladas"
        r"\bfall[oó]\b",             # "falló", "fallo"
        r"\baver[ií]as?\b",          # "avería", "averías"
        r"\bpiezas?\s+malas?\b",
        r"\bunidades?\s+defectuosas?\b",
    ],
    "Poisson": [
        r"poisson",
        r"\bllegadas?\b",
        r"\barribo[s]?\b",
        r"tasa\s+de\s+(?:llegada|ocurrencia|arribo|falla)",
        r"ocurrencias?\s+por",
        r"eventos?\s+por",
        r"llamadas?\s+por",
        r"fallas?\s+por",
        r"[FGPfgp]po\s*\(",         # notación cátedra: Fpo(), Gpo(), Ppo()
        r"\blambda\b",
        r"\bm\s*=\s*\d",            # "m = 5"
    ],
    "Pascal": [
        r"pascal",
        r"binomial\s+negativa",
        r"[FGPfgp]pa\s*\(",         # notación cátedra: Fpa(), Gpa(), Ppa()
        r"r[- ]?[eé]simo\s+[eé]xito",
        r"hasta\s+(?:obtener|conseguir|lograr|encontrar)",
        r"hasta\s+(?:el|la)\s+[rk]?-?[eé]simo",
    ],
    "Hipergeometrico": [
        r"hipergeom[eé]tric[oa]",
        r"[FGPfgp]h\s*\(",          # notación cátedra: Fh(), Gh(), Ph()
        r"sin\s+reposici[oó]n",
        r"\blote\b",
        r"\bpartida\b",
        r"N\s*=\s*\d.*R\s*=\s*\d",  # "N=20 R=8"
    ],
    "Hiper-Pascal": [
        r"hiper[-\s]?pascal",
        r"[FGPfgp]hpa\s*\(",        # notación cátedra: Fhpa(), Ghpa(), Phpa()
    ],
    "Multinomial": [
        r"multinomial",
        r"[Pp]m\s*\(",                                   # notación cátedra: Pm(...)
        r"\bk\s+categor[ií]as?\b",
        r"\b(?:tres|cuatro|cinco|seis)\s+categor[ií]as?\b",
        r"(?:probabilidad|distribuci[oó]n)\s+conjunta",
        r"conjunta\s+de\s+(?:r|x|n)_?\d",
        r"\bvarias?\s+categor[ií]as?\b",
    ],
    "CustomPMF": [
        r"p\s*\(\s*x\s*=\s*x\s*\)\s*=",                 # "P(X=x) = ..." (sobre text_lower)
        r"\bpmf\s+casera\b",
        r"\bfunci[oó]n\s+de\s+probabilidad\s+(?:puntual|discreta)\s+dada\s+por",
        r"\bdistribuci[oó]n\s+discreta\s+con\s+pmf\b",
        r"(?:constante|valor)\s+de\s+normalizaci[oó]n",
    ],
}

# Fase B: patrones para extraer parámetros numéricos por nombre
PARAM_PATTERNS: dict[str, list[str]] = {
    "n": [
        r"\bn\s*=\s*(\d+)",
        r"(\d+)\s*(?:veces|ensayos?|pruebas?|lanzamientos?|intentos?|tiros?|repeticiones?|disparos?|unidades?|latas?|piezas?|semillas?)",
        r"se\s+(?:lanzan?|tiran?|realizan?|hacen?|repite[en]?|producen?|fabrican?|toman?)\s+(\d+)",  # "se lanzan 10", "se producen 10"
        r"(?:lanzan?|tiran?)\s+(?:\w+\s+)?(\d+)\s+veces",                 # "tira un dado 10 veces"
        r"(?:muestra|lote|paquete)\s+de\s+(\d+)",                          # "muestra de 20", "paquete de 200"
        r"(?:en|de)\s+(\d+)\s+(?:disparos?|intentos?|unidades?|pruebas?|ensayos?|piezas?)",  # "en 8 disparos"
        r"(?:examina[rn]?|revisa[rn]?|selecciona[rn]?|toman?)\s+(?:una\s+)?(?:muestra\s+de\s+)?(\d+)",
    ],
    "p": [
        r"\bp\s*=\s*([\d.]+)",
        r"probabilidad\s+(?:de\s+)?(?:\w+\s+){0,5}(?:es\s+|de\s+|del?\s+)?(0[.,]\d+)",
        r"\bprob(?:abilidad)?\s*[=:]\s*([\d.]+)",
        r"(\d+(?:[.,]\d+)?)\s*%",   # "30%" o "0.5%" → se convierte a fracción
        r"(?:éxito|exito|acierto|defecto)\s+(?:es\s+|de\s+|del?\s+)?(0[.,]\d+)",
        r"(0[.,]\d+)\s+(?:de\s+)?(?:probabilidad|prob|chance)",  # "0.3 de probabilidad"
        r"(?:aciertos?|defectuos\w*)\s+(?:del?\s+)?(\d+(?:[.,]\d+)?)\s*%",  # "80% de aciertos"
        r"(\d+(?:[.,]\d+)?)\s*%\s*de\s+(?:aciertos?|defectuos\w*|exito|éxito)",
    ],
}

# Notación cátedra: parseo completo en una sola regex.
# Formato tupla: (regex, modelo, query_type, {grupo: (nombre_param, destino)})
#   destino = "query" → va a query_params  |  "params" → va a params del modelo
CATHEDRA_PATTERNS: list[tuple] = [
    # Binomial: Fb(r/n;p), Gb(r/n;p), Pb(r/n;p)
    (r"[Ff]b\(\s*(\d+)\s*/\s*(\d+)\s*;\s*([\d.]+)\s*\)",
     "Binomial", "cdf_left",    {1: ("r", "query"), 2: ("n", "params"), 3: ("p", "params")}),
    (r"[Gg]b\(\s*(\d+)\s*/\s*(\d+)\s*;\s*([\d.]+)\s*\)",
     "Binomial", "cdf_right",   {1: ("r", "query"), 2: ("n", "params"), 3: ("p", "params")}),
    (r"[Pp]b\(\s*(\d+)\s*/\s*(\d+)\s*;\s*([\d.]+)\s*\)",
     "Binomial", "probability", {1: ("r", "query"), 2: ("n", "params"), 3: ("p", "params")}),
    # Poisson: Fpo(r/m), Gpo(r/m), Ppo(r/m)
    (r"[Ff]po\(\s*(\d+)\s*/\s*([\d.]+)\s*\)",
     "Poisson", "cdf_left",    {1: ("r", "query"), 2: ("m", "params")}),
    (r"[Gg]po\(\s*(\d+)\s*/\s*([\d.]+)\s*\)",
     "Poisson", "cdf_right",   {1: ("r", "query"), 2: ("m", "params")}),
    (r"[Pp]po\(\s*(\d+)\s*/\s*([\d.]+)\s*\)",
     "Poisson", "probability", {1: ("r", "query"), 2: ("m", "params")}),
    # Pascal: Fpa(n/r;p), Gpa(n/r;p), Ppa(n/r;p)
    # grupo 1 = n (query, ensayos), grupo 2 = r (param, exitos buscados), grupo 3 = p
    (r"[Ff]pa\(\s*(\d+)\s*/\s*(\d+)\s*;\s*([\d.]+)\s*\)",
     "Pascal", "cdf_left",    {1: ("r", "query"), 2: ("r", "params"), 3: ("p", "params")}),
    (r"[Gg]pa\(\s*(\d+)\s*/\s*(\d+)\s*;\s*([\d.]+)\s*\)",
     "Pascal", "cdf_right",   {1: ("r", "query"), 2: ("r", "params"), 3: ("p", "params")}),
    (r"[Pp]pa\(\s*(\d+)\s*/\s*(\d+)\s*;\s*([\d.]+)\s*\)",
     "Pascal", "probability", {1: ("r", "query"), 2: ("r", "params"), 3: ("p", "params")}),
    # Hipergeometrico: Fh(r/n;N;R), Gh(r/n;N;R), Ph(r/n;N;R)
    (r"[Ff]h\(\s*(\d+)\s*/\s*(\d+)\s*;\s*(\d+)\s*;\s*(\d+)\s*\)",
     "Hipergeometrico", "cdf_left",
     {1: ("r", "query"), 2: ("n", "params"), 3: ("N", "params"), 4: ("R", "params")}),
    (r"[Gg]h\(\s*(\d+)\s*/\s*(\d+)\s*;\s*(\d+)\s*;\s*(\d+)\s*\)",
     "Hipergeometrico", "cdf_right",
     {1: ("r", "query"), 2: ("n", "params"), 3: ("N", "params"), 4: ("R", "params")}),
    (r"[Pp]h\(\s*(\d+)\s*/\s*(\d+)\s*;\s*(\d+)\s*;\s*(\d+)\s*\)",
     "Hipergeometrico", "probability",
     {1: ("r", "query"), 2: ("n", "params"), 3: ("N", "params"), 4: ("R", "params")}),
    # Hiper-Pascal: Fhpa(n/r;N;R), Ghpa, Phpa
    (r"[Ff]hpa\(\s*(\d+)\s*/\s*(\d+)\s*;\s*(\d+)\s*;\s*(\d+)\s*\)",
     "Hiper-Pascal", "cdf_left",
     {1: ("r", "query"), 2: ("r", "params"), 3: ("N", "params"), 4: ("R", "params")}),
    (r"[Gg]hpa\(\s*(\d+)\s*/\s*(\d+)\s*;\s*(\d+)\s*;\s*(\d+)\s*\)",
     "Hiper-Pascal", "cdf_right",
     {1: ("r", "query"), 2: ("r", "params"), 3: ("N", "params"), 4: ("R", "params")}),
    (r"[Pp]hpa\(\s*(\d+)\s*/\s*(\d+)\s*;\s*(\d+)\s*;\s*(\d+)\s*\)",
     "Hiper-Pascal", "probability",
     {1: ("r", "query"), 2: ("r", "params"), 3: ("N", "params"), 4: ("R", "params")}),
]

# Fase C: keywords para detectar tipo de consulta
QUERY_PATTERNS: dict[str, list[str]] = {
    "cdf_left":    [
        r"F\s*\(", r"acumulad", r"P\s*\(.*?<=", r"\bcdf\b",
        r"a\s+lo\s+sumo", r"como\s+m[uá]cho", r"no\s+m[aá]s\s+de",
        r"menos\s+de", r"menor\s+(?:o\s+)?igual",
        r"hasta\s+\d+",               # "hasta 4"
        r"como\s+m[aá]ximo",
        r"\d+\s+o\s+menos",           # "3 o menos"
        r"\d+\s+o\s+inferior",        # "3 o inferior"
        r"\ba\s+lo\s+m[aá]s\b",       # "a lo más"
    ],
    "cdf_right":   [
        r"G\s*\(", r"P\s*\(.*?>=",
        r"al\s+menos", r"m[aá]s\s+de", r"o\s+m[aá]s",
        r"mayor\s+(?:o\s+)?igual", r"como\s+m[ií]nimo",
        r"no\s+menos\s+de", r"supere",
        r"\balguna?\b",              # "alguna defectuosa" = al menos 1
        r"\balguno?\b",
        r"\d+\s+o\s+m[aá]s",         # "3 o más"
        r"\d+\s+o\s+superior",        # "3 o superior"
        r"por\s+lo\s+menos",          # "por lo menos 3"
    ],
    "probability": [
        r"P\s*\(\s*[rRxX]\s*=", r"exactamente", r"\bpuntual\b",
        r"justo\s+\d+", r"exacto",
        r"(?:salgan?|obtenga[ns]?|haya[ns]?|sean?|saqu[eo])\s+(\d+)",  # "salgan 4", "obtenga 3"
        r"(\d+)\s+(?:cara|seca|éxito|exito|acierto|defectuos)",         # "4 caras"
    ],
    "range":       [r"\bentre\b", r"\brango\b", r"P\s*\(\s*\d+\s*<=.*?<=\s*\d+"],
}

# Patrones adicionales de extracción por modelo
# (se usan en _extract_params además de los de PARAM_PATTERNS)
EXTRA_PARAM_PATTERNS: dict[str, dict[str, list[str]]] = {
    "Poisson": {
        "m": [
            r"\bm\s*=\s*([\d.]+)",
            r"media\s+(?:es\s+|de\s+|=\s*)?([\d.]+)",
            r"promedio\s+(?:es\s+|de\s+|=\s*)?([\d.]+)",
            r"tasa\s+(?:es\s+|de\s+|=\s*)?([\d.]+)",
            r"lambda\s*[=:]\s*([\d.]+)",
            r"(\d+(?:[.,]\d+)?)\s+(?:llegadas?|arribs?|llamadas?|fallas?|eventos?)\s+por",
            r"(?:en|cada|por)\s+(?:\w+\s+)?(?:hora|dia|minuto|mes|año|unidad)\b.*?(\d+(?:[.,]\d+)?)",
        ],
    },
    "Pascal": {
        "r": [
            r"\br\s*=\s*(\d+)",
            r"(\d+)[eé]simo\s+[eé]xito",
            r"(\d+)\s+[eé]xitos?\s+(?:buscados?|necesarios?|requeridos?)",
            r"hasta\s+(?:el\s+|la\s+)?(\d+)[eé]r?[ao]?\s+[eé]xito",
            r"hasta\s+(?:obtener|conseguir|lograr)\s+(\d+)",
        ],
        "p": [
            r"\bp\s*=\s*([\d.]+)",
            r"probabilidad\s+(?:de\s+)?(?:\w+\s+){0,5}(?:es\s+|de\s+|del?\s+)?(0[.,]\d+)",
            r"(\d+(?:[.,]\d+)?)\s*%",
            r"(0[.,]\d+)\s+(?:de\s+)?(?:probabilidad|prob)",
        ],
    },
    "Hipergeometrico": {
        "N": [
            r"\bN\s*=\s*(\d+)",
            r"lote\s+(?:de\s+)?(\d+)",
            r"partida\s+(?:de\s+)?(\d+)",
            r"total\s+(?:de\s+)?(\d+)",
            r"caja\s+(?:con\s+)?(\d+)",
            r"(\d+)\s+(?:unidades?|piezas?|elementos?|bolillas?)\s+(?:en\s+el\s+)?(?:lote|caja|partida|total)",
        ],
        "R": [
            r"\bR\s*=\s*(\d+)",
            r"(\d+)\s+(?:defectuos[oa]s?|favorables?|de\s+segunda|malos?|rotos?)\s+(?:en\s+el\s+)?(?:lote|caja|partida)",
            r"(?:hay|contiene?)\s+(\d+)\s+(?:defectuos[oa]s?|favorables?|de\s+segunda)",
        ],
        "n": [
            r"\bn\s*=\s*(\d+)",
            r"muestra\s+de\s+(\d+)",
            r"selecciona[rn]?\s+(\d+)",
            r"revisa[rn]?\s+(\d+)",
            r"(?:toma[rn]?|extraen?|eligen?)\s+(?:una\s+)?(?:muestra\s+de\s+)?(\d+)",
            r"(?:examina[rn]?)\s+(\d+)",
        ],
    },
    "Hiper-Pascal": {
        "r": [r"\br\s*=\s*(\d+)", r"(\d+)\s+[eé]xitos?\s+(?:buscados?|necesarios?)"],
        "N": [r"\bN\s*=\s*(\d+)", r"lote\s+(?:de\s+)?(\d+)", r"total\s+(?:de\s+)?(\d+)"],
        "R": [r"\bR\s*=\s*(\d+)", r"(\d+)\s+(?:favorables?|defectuos[oa]s?)\s+en\s+el\s+lote"],
    },
    "Multinomial": {
        "n": [
            r"\bn\s*=\s*(\d+)",
            r"(\d+)\s+(?:ensayos?|pruebas?|unidades?|observaciones?|repeticiones?)",
            r"(?:muestra|lote)\s+de\s+(\d+)",
        ],
    },
}

# Parámetros requeridos por modelo y preguntas de follow-up
REQUIRED_PARAMS: dict[str, dict[str, str]] = {
    "Binomial": {
        "n": "¿Cuántos ensayos se realizan (valor de n)?",
        "p": "¿Cuál es la probabilidad de éxito (valor de p, entre 0 y 1)?",
    },
    "Poisson": {
        "m": "¿Cuál es la media (m = lambda * t)? Por ejemplo: m=5, o lambda=2 por hora durante 3 horas.",
    },
    "Pascal": {
        "r": "¿Cuántos éxitos se buscan (valor de r)?",
        "p": "¿Cuál es la probabilidad de éxito por ensayo (valor de p, entre 0 y 1)?",
    },
    "Hipergeometrico": {
        "N": "¿Cuál es el total de elementos en el lote (valor de N)?",
        "R": "¿Cuántos elementos favorables hay en el lote (valor de R)?",
        "n": "¿Cuál es el tamaño de la muestra (valor de n)?",
    },
    "Hiper-Pascal": {
        "r": "¿Cuántos éxitos se buscan (valor de r)?",
        "N": "¿Cuál es el total del lote (valor de N)?",
        "R": "¿Cuántos favorables hay en el lote (valor de R)?",
    },
    "Multinomial": {
        "pi": "¿Cuáles son las probabilidades por categoría? (ej: 0.2; 0.3; 0.5)",
        "ri": "¿Cuáles son los conteos observados por categoría? (ej: 2; 3; 5)",
    },
}

# Valor de p para moneda (cara o seca)
_P_MONEDA = 0.5

# Patrón para detectar "tema X ejercicio Y" / "tema III ej 8" / "guia tema 2 problema 1"
GUIA_EXERCISE_PATTERN = re.compile(
    r"(?:gu[ií]a\s+)?tema\s+"
    r"(?P<tema>[IVXivx]+|\d+|uno|dos|tres|cuatro|cinco|seis|siete)"
    r"\s*[,\-\u2013]?\s*"
    r"(?:ejercicio|ej\.?|problema|prob\.?)\s*"
    r"(?P<num>\d+)",
    re.IGNORECASE,
)

# Números en palabra (para problemas compuestos: "muestra de dos", "una defectuosa")
_WORD_TO_NUM = {
    "un": 1, "una": 1, "uno": 1,
    "dos": 2, "tres": 3, "cuatro": 4, "cinco": 5,
    "seis": 6, "siete": 7, "ocho": 8, "nueve": 9, "diez": 10,
}


# ---------------------------------------------------------------------------
# Clase principal
# ---------------------------------------------------------------------------

class NLParser:
    """
    Parsea texto libre de un problema estadístico en un dict estructurado.
    Retorna el mismo formato de status/model/params/query_type/query_params
    que el antiguo ClaudeClient, para que streamlit_interpreter no cambie.
    """

    def __init__(self):
        self._llm = None  # lazy

    def _get_llm(self):
        """Devuelve un OllamaClient si está habilitado, o None."""
        if self._llm is not None:
            return self._llm
        try:
            from config.settings import OLLAMA_ENABLED
            if not OLLAMA_ENABLED:
                return None
            from llm.ollama_client import OllamaClient
            self._llm = OllamaClient()
            return self._llm
        except Exception:
            return None

    def parse(self, text: str) -> dict:
        result = self._parse_regex(text)
        result.setdefault("_source", "regex")
        # Fallback LLM si el regex no fue concluyente.
        # _skip_llm=True señala respuestas determinísticas (ej: multi-parte)
        # donde el fallback solo agregaría ruido.
        needs_fallback = result.get("status") in ("need_more_info", "error", "unknown")
        if needs_fallback and not result.get("_skip_llm"):
            llm_out = self._fallback_with_llm(text, result)
            if llm_out is not None:
                llm_out["_source"] = "llm"
                return llm_out
        return result

    def _parse_regex(self, text: str) -> dict:
        text_lower = text.lower()

        # Paso 0: notación cátedra — bypass completo si hay match
        cathedra = self._try_cathedra(text)
        if cathedra:
            return cathedra

        # Paso 0.3: referencia a ejercicio de la guia ("tema III ejercicio 8")
        guide = self._detect_guide_exercise(text)
        if guide:
            return guide

        # Paso 0.5: problemas compuestos (requieren múltiples distribuciones)
        compound = self._detect_compound(text, text_lower)
        if compound:
            return compound

        # Paso 1: detectar modo (antes de buscar modelo).
        # Datos Agrupados gana aunque el enunciado tenga varias partes:
        # si detectamos una tabla de frecuencias, la pre-llenamos y el
        # usuario va resolviendo cada inciso sobre esa misma tabla.
        if self._is_datos_agrupados(text_lower, text):
            return self._parse_datos_agrupados(text, text_lower)

        if self._is_probabilidad(text_lower, text):
            return self._parse_probabilidad(text, text_lower)

        if self._is_tcl(text_lower, text):
            return self._parse_tcl(text, text_lower)

        # Paso 1.5: problema multi-parte (a) b) c) …) sin modo detectable —
        # pedir una parte por vez. Marcamos _skip_llm para que el fallback
        # no sobreescriba este mensaje determinístico.
        if self._is_multi_part(text):
            return {
                "status": "need_more_info",
                "model": None,
                "params": {},
                "question": (
                    "Detecté que el enunciado tiene varias partes (a, b, c, …) y "
                    "cada una pide algo distinto. Pegá la consigna de UNA parte por vez "
                    "(ej: sólo el inciso a) para que pueda resolverla."
                ),
                "_skip_llm": True,
            }

        # Fase A: modelo discreto/continuo
        model = self._detect_model(text_lower)
        if model is None:
            return {
                "status": "need_more_info",
                "model": None,
                "params": {},
                "question": "No pude identificar el modelo estadístico. ¿Cuál es? (Ej: Binomial, Poisson, etc.)",
            }

        # Multinomial: flujo multivariado (params/query son vectores)
        if model == "Multinomial":
            return self._parse_multinomial(text, text_lower)

        # CustomPMF: PMF casera con normalizador k
        if model == "CustomPMF":
            return self._parse_custom_pmf(text, text_lower)

        # Fase B: parámetros
        params = self._extract_params(text, text_lower, model)

        # Inferencias especiales de p según contexto
        if model == "Binomial" and "p" not in params:
            if re.search(r"\bmoneda\b", text_lower):
                params["p"] = _P_MONEDA
            elif re.search(r"\bdado\b|\bdados\b", text_lower):
                # Dado: depende de qué busca, por defecto 1/6
                params["p"] = round(1/6, 4)

        # Convertir porcentaje a probabilidad si el texto tiene "%" y p >= 1
        if "p" in params and re.search(r"\d+\s*%", text_lower) and params["p"] >= 1:
            params["p"] = round(params["p"] / 100, 4)

        # Verificar params faltantes
        missing_question = self._check_missing(model, params)
        if missing_question:
            return {
                "status": "need_more_info",
                "model": model,
                "params": params,
                "question": missing_question,
            }

        # Fase C: tipo de consulta y query_params
        query_type, query_params = self._detect_query(text, text_lower, model, params)

        return {
            "status": "complete",
            "model": model,
            "params": params,
            "query_type": query_type,
            "query_params": query_params,
            "interpretation": self._build_interpretation(model, params, query_type, query_params),
        }

    # -----------------------------------------------------------------------
    # Fallback LLM (silencioso — invisible al usuario)
    # -----------------------------------------------------------------------

    def _fallback_with_llm(self, text: str, regex_result: dict) -> dict | None:
        """Intenta resolver con Ollama. Devuelve dict normalizado o None."""
        llm = self._get_llm()
        if llm is None:
            return None
        try:
            if not llm.is_available():
                return None
        except Exception:
            return None
        try:
            import os as _os
            prompt_path = _os.path.join(
                _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))),
                "llm", "prompts", "parser_fallback.txt",
            )
            with open(prompt_path, encoding="utf-8") as f:
                system_prompt = f.read()
        except Exception:
            return None

        try:
            resp = llm.chat(
                [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text},
                ],
                json_mode=True,
                temperature=0.0,
                max_tokens=1024,
            )
        except Exception:
            return None

        try:
            import json as _json
            obj = _json.loads(resp)
        except Exception:
            return None

        return self._validate_llm_output(obj)

    def _validate_llm_output(self, obj) -> dict | None:
        """Normaliza shape del LLM al formato interno. None si no pasa validación."""
        if not isinstance(obj, dict):
            return None
        status = obj.get("status")
        if status not in ("complete", "need_more_info"):
            return None
        conf = obj.get("confidence", 0.0)
        try:
            conf = float(conf)
        except (TypeError, ValueError):
            conf = 0.0
        if conf < 0.6 and status == "complete":
            return None

        try:
            from config.model_catalog import IMPLEMENTED_MODELS, normalize_model_name
        except Exception:
            IMPLEMENTED_MODELS = set()
            normalize_model_name = lambda x: x  # noqa: E731

        model = obj.get("model")
        if model:
            model = normalize_model_name(model)
            # Los compound_types no son modelos: si el LLM los puso en 'model',
            # o dijo mode='compound' sin la config correcta, rechazamos el output
            # para que degrade al resultado regex original (sin regresión).
            _COMPOUND_TYPE_NAMES = {"hiper_binomial", "pascal_conditional",
                                     "bayes_then_pascal", "multi_distribution"}
            if model in _COMPOUND_TYPE_NAMES or obj.get("mode") == "compound":
                return None
            if model not in IMPLEMENTED_MODELS and obj.get("mode") not in (
                "tcl", "TCL / Suma de VA", "grouped_data", "probability"
            ):
                return None

        mode_map = {
            "tcl": "TCL / Suma de VA",
            "TCL": "TCL / Suma de VA",
            "compound": "compound",
            "grouped_data": "Datos Agrupados",
            "probability": "Probabilidad",
            "distributions": "Modelos de Probabilidad",
        }
        mode = mode_map.get(obj.get("mode"), obj.get("mode"))

        out: dict = {
            "status": status,
            "model": model,
            "params": obj.get("params") or {},
            "query_type": obj.get("query_type"),
            "query_params": obj.get("query_params") or {},
        }
        if mode:
            out["mode"] = mode
        if status == "need_more_info":
            out["question"] = obj.get("reason") or "Faltan datos para resolver el problema."
        if obj.get("compound_type"):
            out["compound_type"] = obj["compound_type"]
        if status == "complete" and out.get("model"):
            try:
                out["interpretation"] = self._build_interpretation(
                    out["model"], out["params"],
                    out.get("query_type") or "full_analysis",
                    out["query_params"],
                )
            except Exception:
                pass
        return out

    # -----------------------------------------------------------------------
    # Paso 0: notación cátedra
    # -----------------------------------------------------------------------

    def _try_cathedra(self, text: str) -> dict | None:
        # Params que deben ser enteros
        _INT_PARAMS = {"r", "n", "N", "R", "a", "b"}
        for pattern, model, query_type, group_map in CATHEDRA_PATTERNS:
            m = re.search(pattern, text)
            if m:
                params = {}
                query_params = {}
                for group_idx, (param_name, dest) in group_map.items():
                    val = m.group(group_idx)
                    numeric = float(val) if "." in val else int(val)
                    if param_name in _INT_PARAMS:
                        numeric = int(numeric)
                    if dest == "query":
                        query_params[param_name] = numeric
                    else:
                        params[param_name] = numeric
                return {
                    "status": "complete",
                    "model": model,
                    "params": params,
                    "query_type": query_type,
                    "query_params": query_params,
                    "interpretation": self._build_interpretation(model, params, query_type, query_params),
                }
        return None

    # -----------------------------------------------------------------------
    # Fase A: detectar modelo
    # -----------------------------------------------------------------------

    def _detect_model(self, text_lower: str) -> str | None:
        for model, patterns in MODELO_PATTERNS.items():
            for pat in patterns:
                if re.search(pat, text_lower):
                    return model
        return None

    # -----------------------------------------------------------------------
    # Fase B: extraer parámetros
    # -----------------------------------------------------------------------

    def _extract_params(self, text: str, text_lower: str, model: str) -> dict:
        params = {}
        required = REQUIRED_PARAMS.get(model, {})
        # Usar patrones específicos del modelo si existen, sino los genéricos
        extra = EXTRA_PARAM_PATTERNS.get(model, {})
        for param_name in required:
            patterns = extra.get(param_name) or PARAM_PATTERNS.get(param_name, [])
            for pat in patterns:
                m = re.search(pat, text_lower)
                if m:
                    raw = m.group(1).replace(",", ".")
                    val = float(raw) if "." in raw else int(raw)
                    params[param_name] = val
                    break
        return params

    # -----------------------------------------------------------------------
    # Verificar parámetros faltantes
    # -----------------------------------------------------------------------

    def _check_missing(self, model: str, params: dict) -> str | None:
        required = REQUIRED_PARAMS.get(model, {})
        for param_name, question in required.items():
            if param_name not in params:
                return question
        return None

    # -----------------------------------------------------------------------
    # Fase C: detectar tipo de consulta y query_params
    # -----------------------------------------------------------------------

    def _detect_query(self, text: str, text_lower: str, model: str, params: dict) -> tuple[str, dict]:
        query_type = "full_analysis"
        for qt, patterns in QUERY_PATTERNS.items():
            for pat in patterns:
                if re.search(pat, text, re.IGNORECASE):
                    query_type = qt
                    break
            if query_type != "full_analysis":
                break

        query_params = self._extract_query_params(text, text_lower, query_type, params)
        return query_type, query_params

    def _extract_query_params(self, text: str, text_lower: str, query_type: str, params: dict) -> dict:
        if query_type == "full_analysis":
            return {}

        if query_type == "range":
            nums = re.findall(r"\b(\d+)\b", text)
            int_nums = [int(x) for x in nums if int(x) not in params.values()]
            if len(int_nums) >= 2:
                return {"a": int_nums[0], "b": int_nums[1]}
            return {}

        # probability / cdf_left / cdf_right → buscar valor de r
        # Patrones explícitos con prioridad (más específicos primero)
        # Caso especial: "alguna" → r = 1 (al menos una)
        if re.search(r"\balgunas?\b|\balguno?\b", text, re.IGNORECASE):
            return {"r": 1}

        r_patterns = [
            r"[Ff]\s*\(\s*(\d+)\s*\)",                           # F(4)
            r"[Gg]\s*\(\s*(\d+)\s*\)",                           # G(3)
            r"[Pp]\s*\(\s*[rRxX]\s*=\s*(\d+)\)",                 # P(r=4)
            r"(?:exactamente|justo|exacto)\s+(\d+)",              # "exactamente 4"
            r"(\d+)\s+(?:caras?|secas?|éxitos?|exitos?|aciertos?|defectuos\w*|fallad\w*)",  # "4 caras", "2 falladas"
            r"(?:salgan?|obtenga[ns]?|haya[ns]?|sean?|saqu[eo]|resulten?)\s+(\d+)",  # "salgan 4"
            r"(?:al\s+menos|como\s+m[ií]nimo|por\s+lo\s+menos)\s+(\d+)",  # "al menos 8"
            r"(?:a\s+lo\s+sumo|como\s+m[uá]cho|como\s+m[aá]ximo|no\s+m[aá]s\s+de)\s+(\d+)",  # "a lo sumo 5"
            r"(?:m[aá]s\s+de|supere[en]?|mayor\s+(?:o\s+)?igual\s+(?:a\s+)?)\s+(\d+)",
            r"(?:menor\s+(?:o\s+)?igual\s+(?:a\s+)?)\s+(\d+)",
            r"(?:hasta)\s+(\d+)",                                 # "hasta 4"
            r"(\d+)\s+o\s+menos",                                 # "3 o menos"
            r"(\d+)\s+o\s+m[aá]s",                               # "3 o más"
            r"(\d+)\s+o\s+(?:inferior|superior)",                 # "3 o inferior/superior"
        ]
        for pat in r_patterns:
            m = re.search(pat, text, re.IGNORECASE)
            if m:
                return {"r": int(m.group(1))}

        # Fallback: último número entero que NO sea n ni p (entero)
        param_vals = set()
        for v in params.values():
            if isinstance(v, (int, float)) and float(v) == int(float(v)):
                param_vals.add(int(v))
        all_ints = [int(x) for x in re.findall(r"\b(\d+)\b", text)]
        candidates = [x for x in reversed(all_ints) if x not in param_vals]
        if candidates:
            return {"r": candidates[0]}
        return {}

    # -----------------------------------------------------------------------
    # Detección de modo
    # -----------------------------------------------------------------------

    def _is_datos_agrupados(self, text_lower: str, text: str) -> bool:
        strong = [
            r"datos\s+agrupados?",
            r"\bogiva\b", r"\bojiva\b",
            r"\bhistograma\b",
            r"tabla\s+de\s+frecuencias",
            r"amplitud\s+de\s+clase",
            r"marca\s+de\s+clase",
            r"\bfractil\b", r"\bpercentil\b",
            r"\bcuartil[es]?\b", r"\bdecil[es]?\b",
            r"frecuencia\s+(?:relativa|acumulada|absoluta)",
            r"\bmediana\b.*\binterval",
            r"intervalo\s+de\s+clase",
            r"\bcuasi\s*varianza\b",
        ]
        for pat in strong:
            if re.search(pat, text_lower):
                return True
        # Structural: 3+ intervals like "10-20", "10 a 20"
        intervals = re.findall(
            r'\d+(?:[.,]\d+)?\s*(?:[-–—]|\ba\b)\s*\d+(?:[.,]\d+)?', text_lower
        )
        if len(intervals) >= 3:
            return True
        return False

    def _is_probabilidad(self, text_lower: str, text: str) -> bool:
        """Detecta problemas de probabilidad de eventos (Bayes, dos eventos) — NO distribuciones."""
        strong = [
            r"\bbayes\b",
            r"a\s+priori",
            r"a\s+posteriori",
            r"probabilidad\s+total",
            r"teorema\s+de\s+bayes",
            r"prob(?:abilidad)?\s+condicionada?",
            r"\bmutuamente\s+excluyentes?\b",   # inequívoco de prob. de eventos
            r"\bcomplemento\s+de\b",            # "complemento de A"
            r"uni[oó]n\s+de\s+(?:los\s+)?eventos?",
            r"intersecci[oó]n\s+de\s+(?:los\s+)?eventos?",
        ]
        for pat in strong:
            if re.search(pat, text_lower):
                return True
        # Estructura clásica de Bayes: 3+ fuentes (línea/máquina/urna/proveedor)
        # con porcentajes + condición defectuoso/fallo
        sources = re.findall(
            r"\b(?:l[ií]nea|m[aá]quina|urna|proveedor|planta|fabrica|taller)\s+\d",
            text_lower,
        )
        has_defect = bool(re.search(
            r"defectuos|fallad|aver|fall[oó]|no\s+cumple|rechaz",
            text_lower,
        ))
        pcts = re.findall(r"\d+(?:[.,]\d+)?\s*%", text_lower)
        if len(set(sources)) >= 2 and has_defect and len(pcts) >= 4:
            return True
        # Patrones que requieren case-sensitive (usan mayúsculas)
        case_sensitive = [
            r"P\s*\(\s*[A-Z][^)]{0,10}[|/]\s*[A-Z]",   # P(A|B) o P(A/B)
            r"P\s*\([A-Z]\s*\)\s*[=:]",                  # P(A) = valor
        ]
        for pat in case_sensitive:
            if re.search(pat, text):
                return True
        # Medium signals — need 2 or more
        medium_count = 0
        medium = [
            r"\bcomplemento\b",
            r"\bindependientes?\b",
            r"\burna\b",
            r"\bbolillas?\b", r"\bbolitas?\b",
            r"\bevento[s]?\b",
            r"\bambas\b",       # "producir ambas" → intersección
            r"\bno\s+(?:se\s+)?produz\w+\s+nada\b",  # "no producir nada"
        ]
        for pat in medium:
            if re.search(pat, text_lower):
                medium_count += 1
        # Multiple "probabilidad de ... es de X%" patterns → probability problem
        prob_pct_hits = re.findall(
            r"probabilidad\s+de\s+.{3,60}?\b(?:es|de[l]?)\s+(?:solo\s+)?(?:de[l]?\s+)?"
            r"(\d+(?:[.,]\d+)?)\s*%",
            text_lower,
        )
        if len(prob_pct_hits) >= 2:
            medium_count += 2
        if medium_count >= 2:
            return True
        return False

    # -----------------------------------------------------------------------
    # Parseo de Datos Agrupados
    # -----------------------------------------------------------------------

    def _parse_datos_agrupados(self, text: str, text_lower: str) -> dict:
        intervals, frequencies = self._extract_intervals_frequencies(text)
        if intervals and frequencies and len(intervals) == len(frequencies):
            return {
                "status": "complete",
                "mode": "Datos Agrupados",
                "dp_intervals": intervals,
                "dp_frequencies": frequencies,
                "interpretation": f"Datos agrupados: {len(intervals)} clases detectadas.",
            }
        if intervals:
            return {
                "status": "need_more_info",
                "mode": "Datos Agrupados",
                "question": (
                    f"Detecté {len(intervals)} intervalos. "
                    "¿Cuáles son las frecuencias absolutas (fi) de cada clase?"
                ),
            }
        return {
            "status": "complete",
            "mode": "Datos Agrupados",
            "dp_intervals": None,
            "dp_frequencies": None,
            "interpretation": "Datos agrupados detectados. Ingresá los intervalos y frecuencias en la tabla.",
        }

    def _extract_intervals_frequencies(self, text: str) -> tuple:
        # Separador de intervalo: guion, en-dash, em-dash, o "a" entre números
        _INT_SEP = r'(?:[-–—]|\ba\b)'

        # Pattern 0: línea a línea — más robusto cuando la tabla viene pegada
        # como CSV (“0 a 9,150”) donde la coma es separador de columna, no decimal.
        line_intervals: list = []
        line_freqs: list = []
        for line in text.splitlines():
            m = re.match(
                rf'^\s*(\d+)\s*{_INT_SEP}\s*(\d+)\s*[,;|/:\t]+\s*(\d+)\s*$',
                line,
            )
            if m:
                li, ls, fi = int(m.group(1)), int(m.group(2)), int(m.group(3))
                line_intervals.append((float(li), float(ls)))
                line_freqs.append(fi)
        if len(line_intervals) >= 2:
            return line_intervals, line_freqs

        # Pattern 1: "Li - Ls   fi" on same row (any separator incl. /)
        row_pat = re.findall(
            rf'(\d+(?:[.,]\d+)?)\s*{_INT_SEP}\s*(\d+(?:[.,]\d+)?)\s*[|\s,;:/]+\s*(\d+(?:[.,]\d+)?)',
            text,
        )
        if row_pat:
            intervals = [(float(a.replace(",", ".")), float(b.replace(",", "."))) for a, b, _ in row_pat]
            freqs = [int(float(c.replace(",", "."))) for _, _, c in row_pat]
            return intervals, freqs

        # Pattern 2: intervals listed first, then frequencies separately
        interval_matches = re.findall(
            rf'(\d+(?:[.,]\d+)?)\s*{_INT_SEP}\s*(\d+(?:[.,]\d+)?)', text
        )
        if interval_matches:
            clean = re.sub(rf'\d+(?:[.,]\d+)?\s*{_INT_SEP}\s*\d+(?:[.,]\d+)?', 'INTERVAL', text)
            freq_nums_raw = re.findall(r'\b(\d+(?:[.,]\d+)?)\b', clean)
            freq_nums = [float(f.replace(",", ".")) for f in freq_nums_raw]
            integer_freqs = [int(f) for f in freq_nums if f == int(f) and f >= 1]
            n = len(interval_matches)
            if len(integer_freqs) >= n:
                intervals = [(float(a.replace(",", ".")), float(b.replace(",", "."))) for a, b in interval_matches]
                return intervals, integer_freqs[:n]
        return [], []

    # -----------------------------------------------------------------------
    # Parseo de Probabilidad (eventos, Bayes)
    # -----------------------------------------------------------------------

    def _parse_probabilidad(self, text: str, text_lower: str) -> dict:
        bayes_signals = [r"\bbayes\b", r"a\s+priori", r"a\s+posteriori", r"probabilidad\s+total"]
        is_bayes = any(re.search(p, text_lower) for p in bayes_signals)
        # Heurística estructural: ≥2 fuentes (línea/máquina/…) + defectos + ≥4 %
        if not is_bayes:
            sources = re.findall(
                r"\b(?:l[ií]nea|m[aá]quina|urna|proveedor|planta|fabrica|taller)\s+\d",
                text_lower,
            )
            has_defect = bool(re.search(
                r"defectuos|fallad|aver|fall[oó]|no\s+cumple|rechaz",
                text_lower,
            ))
            pcts = re.findall(r"\d+(?:[.,]\d+)?\s*%", text_lower)
            if len(set(sources)) >= 2 and has_defect and len(pcts) >= 4:
                is_bayes = True

        if is_bayes:
            bayes_data = self._extract_bayes_data(text, text_lower)
            sc: dict = {
                "status": "complete",
                "mode": "Probabilidad",
                "prob_submode": "Bayes / Probabilidad Total",
                "interpretation": "Problema de Bayes / Probabilidad Total detectado.",
            }
            sc.update(bayes_data)
            return sc

        # Probabilidad de eventos
        sc = {
            "status": "complete",
            "mode": "Probabilidad",
            "prob_submode": "Probabilidad de eventos",
            "interpretation": "Probabilidad de eventos detectada.",
        }
        pA = self._extract_prob_named(text, text_lower, "A")
        pB = self._extract_prob_named(text, text_lower, "B")
        if pA is not None:
            sc["prob_pA"] = pA
        if pB is not None:
            sc["prob_pB"] = pB

        # Intentar extracción de lenguaje natural si no encontramos P(A)/P(B) formales
        if pA is None and pB is None:
            nl_data = self._extract_prob_natural_language(text, text_lower)
            sc.update(nl_data)

        # Relationship detection
        if re.search(r"mutuamente\s+excluyentes?|disjuntos?|se\s+excluyen", text_lower):
            sc["prob_rel"] = "mutually_exclusive"
        elif re.search(r"\bindependientes?\b", text_lower):
            sc["prob_rel"] = "independent"
        return sc

    def _extract_bayes_data(self, text: str, text_lower: str) -> dict:
        """Intenta extraer hipótesis, priors y likelihoods de texto libre."""
        # Buscar todos los porcentajes en orden de aparición
        pct_matches = re.findall(r'(\d+(?:[.,]\d+)?)\s*%', text)
        percentages = [float(p.replace(",", ".")) / 100 for p in pct_matches]

        # Necesitamos pares (prior, likelihood) por hipótesis
        # Heurística: si hay 2N porcentajes (N≥2), primera mitad = priors, segunda = likelihoods
        if len(percentages) >= 4 and len(percentages) % 2 == 0:
            n = len(percentages) // 2
            priors = percentages[:n]
            likelihoods = percentages[n:]
            labels = [f"H{i+1}" for i in range(n)]
            # Intentar extraer nombres (letras mayúsculas aisladas o palabras capitalizadas)
            label_cands = re.findall(r'\b([A-Z][a-záéíóúñ]{2,})\b', text)
            stopwords = {
                "La", "El", "De", "Los", "Las", "En", "Un", "Una", "Se", "Con",
                "Por", "Si", "Del", "Al", "Que", "Es", "Son", "Una",
            }
            label_cands = [l for l in label_cands if l not in stopwords]
            if len(label_cands) >= n:
                labels = label_cands[:n]
            return {
                "bayes_labels": labels,
                "bayes_priors": priors,
                "bayes_likelihoods": likelihoods,
            }

        # Fallback: buscar decimales (e.g. "0.20, 0.35, 0.45 ... 0.10, 0.05, 0.02")
        decimal_matches = re.findall(r'\b(0[.,]\d+)\b', text)
        decimals = [float(d.replace(",", ".")) for d in decimal_matches]
        if len(decimals) >= 4 and len(decimals) % 2 == 0:
            n = len(decimals) // 2
            priors = decimals[:n]
            likelihoods = decimals[n:]
            return {
                "bayes_labels": [f"H{i+1}" for i in range(n)],
                "bayes_priors": priors,
                "bayes_likelihoods": likelihoods,
            }
        return {}

    def _extract_prob_named(self, text: str, text_lower: str, name: str) -> float | None:
        """Extrae P(name) del texto. name es 'A' o 'B'."""
        # P(A) = 0.3  /  P(A) = 30%
        m = re.search(
            rf'P\s*\(\s*{name}\s*\)\s*[=:]\s*([\d.,]+)\s*(%)?',
            text, re.IGNORECASE
        )
        if m:
            raw = re.sub(r'[^\d.]', '', m.group(1).replace(",", "."))
            try:
                val = float(raw)
            except ValueError:
                return None
            if m.group(2) == "%":
                val /= 100
            return val
        return None

    def _extract_prob_natural_language(self, text: str, text_lower: str) -> dict:
        """
        Extrae probabilidades de dos eventos desde lenguaje natural español.

        Busca patrones como:
          - "probabilidad de producir X ... es de Y%"
          - "probabilidad de ambas/ambos ... es de Y%"
          - "probabilidad de no producir nada ... es de Y%"

        Retorna dict con claves prob_pB, prob_pAB, prob_pAB_comp, prob_name_A/B, prob_derive_pA.
        """
        result: dict = {}

        # Extraer todos los items "probabilidad de [algo] es de X%"
        items = re.findall(
            r"probabilidad\s+de\s+(.{3,80}?)\s+(?:es|de[l]?)\s+(?:solo\s+)?(?:de[l]?\s+)?"
            r"(\d+(?:[.,]\d+)?)\s*%",
            text_lower,
        )
        if not items:
            return result

        # Clasificar cada probabilidad extraída
        p_both: float | None = None      # P(A∩B) — ambas
        p_neither: float | None = None   # P(A'∩B') — nada/ninguna
        p_marginals: list = []           # probabilidades marginales

        for desc, val_str in items:
            val = float(val_str.replace(",", ".")) / 100
            desc_clean = desc.strip()

            if re.search(r"\bambas?\b|\bambos?\b|\blas\s+dos\b|\blos\s+dos\b", desc_clean):
                p_both = val
            elif re.search(
                r"\bnada\b|\bninguna?\b|\bno\s+(?:se\s+)?produz\w*|"
                r"\bno\s+ocurr\w*|\bno\s+se\s+fabric\w*",
                desc_clean,
            ):
                p_neither = val
            else:
                p_marginals.append((desc_clean, val))

        # La primera marginal es el evento "principal" → P(B)
        # (el otro se derivará de P(A'∩B'))
        if p_marginals:
            desc_B, val_B = p_marginals[0]
            result["prob_pB"] = val_B
            # Intentar extraer nombre del evento
            name_B = self._extract_event_name(desc_B)
            if name_B:
                result["prob_name_B"] = name_B

        if p_both is not None:
            result["prob_pAB"] = p_both

        if p_neither is not None:
            result["prob_pAB_comp"] = p_neither
            result["prob_derive_pA"] = True

        # Si hay segunda marginal, es P(A)
        if len(p_marginals) >= 2:
            desc_A, val_A = p_marginals[1]
            result["prob_pA"] = val_A
            name_A = self._extract_event_name(desc_A)
            if name_A:
                result["prob_name_A"] = name_A

        if result:
            # Mensaje legible para el usuario
            parts = []
            name_B = result.get("prob_name_B", "B")
            name_A = result.get("prob_name_A", "A")
            if "prob_pB" in result:
                parts.append(f"P({name_B}) = {result['prob_pB']}")
            if "prob_pA" in result:
                parts.append(f"P({name_A}) = {result['prob_pA']}")
            if "prob_pAB" in result:
                parts.append(f"P({name_A}∩{name_B}) = {result['prob_pAB']}")
            if "prob_pAB_comp" in result:
                parts.append(f"P(ninguno) = {result['prob_pAB_comp']}")
            result["interpretation"] = (
                "Probabilidad de dos eventos detectada: " + ", ".join(parts) + "."
            )

        return result

    @staticmethod
    def _extract_event_name(desc: str) -> str | None:
        """Extrae un nombre corto de evento de una descripción como 'producir gaseosas'."""
        # Remover prefijos comunes (incluyendo "que" suelto al inicio)
        desc = re.sub(
            r"^(?:producir|fabricar|hacer|tener|que\s+se\s+produz\w+|que)\s+",
            "",
            desc,
        )
        stopwords = {
            "solo", "al", "la", "el", "las", "los", "un", "una",
            "que", "se", "de", "del", "en", "por", "con", "sin",
            "no", "ni", "le", "lo", "les", "su", "sus", "para",
        }
        for w in desc.split():
            name = w.capitalize().rstrip(",.:;")
            if name.lower() not in stopwords and len(name) >= 3:
                return name
        return None

    @staticmethod
    def _is_multi_part(text: str) -> bool:
        """Detecta enunciados con varias partes etiquetadas (a), b), c), …).

        Heurística: al menos dos marcadores distintos de la forma
        ``<newline>|<separador>`` + letra minúscula + ``)`` + contenido,
        donde <separador> incluye ``.``, ``?``, ``:``, ``)``, y permite
        pegado sin espacios (ej. ``Responda:a)``, ``(1p)b)``).
        """
        pattern = re.compile(
            r'(?:^|\n|[\.\?:)]\s{0,3})\s*([a-f])\s*\)\s*\S',
            re.IGNORECASE,
        )
        matches = pattern.findall(text)
        distinct = {m.lower() for m in matches}
        if len(distinct) < 2:
            return False
        # Evitar falsos positivos: aseguro longitud mínima total y separación
        return len(text.strip()) >= 200

    # -----------------------------------------------------------------------
    # Paso 0.3: referencia a ejercicio de la guia
    # -----------------------------------------------------------------------

    def _detect_guide_exercise(self, text: str) -> dict | None:
        """Detecta 'tema X ejercicio Y' y señala la intención sin resolver."""
        match = GUIA_EXERCISE_PATTERN.search(text)
        if not match:
            return None
        return {
            "status": "guide_exercise",
            "tema": match.group("tema"),
            "numero": int(match.group("num")),
            "raw_query": text.strip(),
        }

    # -----------------------------------------------------------------------
    # Detección de problemas compuestos
    # -----------------------------------------------------------------------

    def _detect_compound(self, text: str, text_lower: str) -> dict | None:
        """Detecta problemas que requieren múltiples distribuciones encadenadas."""
        result = self._try_hiper_binomial(text, text_lower)
        if result:
            return result
        result = self._try_pascal_conditional(text, text_lower)
        if result:
            return result
        return None

    def _try_hiper_binomial(self, text: str, text_lower: str) -> dict | None:
        """
        Detecta: muestreo de cajas/lotes (Hipergeométrico) + conteo de rechazos (Binomial).
        Ej: 'tomar muestra de 2 de cada caja de 10, rechazar si alguna defectuosa, 15 cajas...'
        """
        # Señales requeridas: "rechazar" + "caja/lote"
        if not re.search(r'rechaz', text_lower):
            return None
        if not re.search(r'\bcajas?\b|\blotes?\b', text_lower):
            return None

        # Patrón compacto: "muestra de X (unidades) de cada caja/lote de Y"
        m_sample_compact = re.search(
            r'muestra\s+de\s+(\w+)\s+(?:unidades?\s+)?de\s+cada\s+(?:caja|lote)\s+de\s+(\d+)',
            text_lower,
        )
        if m_sample_compact:
            sample_n_raw = m_sample_compact.group(1)
            sample_n = _WORD_TO_NUM.get(sample_n_raw) or (int(sample_n_raw) if sample_n_raw.isdigit() else None)
            box_N = int(m_sample_compact.group(2))
        else:
            # Patrón desacoplado (orden natural):
            # "15 cajas de 10 piezas" + "muestra de 2" + "con 2 defectuosas"
            m_sample = re.search(r'muestra\s+de\s+(\w+)', text_lower)
            m_box = re.search(r'(?:cajas?|lotes?)\s+de\s+(\d+)\s+(?:piezas?|unidades?|elementos?)', text_lower)
            if not m_sample or not m_box:
                return None
            sample_n_raw = m_sample.group(1)
            sample_n = _WORD_TO_NUM.get(sample_n_raw) or (int(sample_n_raw) if sample_n_raw.isdigit() else None)
            box_N = int(m_box.group(1))
        if sample_n is None:
            return None

        # Número de cajas: "X cajas/lotes"
        m_boxes = re.search(r'(\d+)\s+(?:cajas?|lotes?)', text_lower)
        if not m_boxes:
            return None
        num_boxes = int(m_boxes.group(1))

        # Defectuosas por caja: aceptar "X defectuosas en cada caja",
        # "X defectuosas por caja" o "con X defectuosas" (inline al lado de la caja)
        m_defect = re.search(
            r'(\w+)\s+(?:piezas?\s+)?defectuosas?\s+(?:en\s+)?(?:cada|por)\s+(?:caja|lote)',
            text_lower,
        )
        if not m_defect:
            m_defect = re.search(
                r'con\s+(\w+)\s+(?:piezas?\s+)?defectuosas?',
                text_lower,
            )
        if m_defect:
            box_R_raw = m_defect.group(1)
            box_R = _WORD_TO_NUM.get(box_R_raw) or (int(box_R_raw) if box_R_raw.isdigit() else None)
            if box_R is None:
                box_R = 1
        else:
            box_R = 1

        # Consulta: "rechacen menos/más/exactamente de X cajas"
        query_type, query_r = self._extract_compound_query(text_lower)
        if query_r is None:
            return None

        return {
            "status": "compound",
            "compound_type": "hiper_binomial",
            "box_N": box_N,
            "box_R": box_R,
            "sample_n": sample_n,
            "num_boxes": num_boxes,
            "reject_r": 1,
            "query_type": query_type,
            "query_r": query_r,
            "interpretation": (
                f"Problema compuesto: muestreo de {sample_n} piezas de cada caja de {box_N} "
                f"(Hipergeométrico) + conteo de cajas rechazadas de {num_boxes} (Binomial)."
            ),
        }

    def _try_pascal_conditional(self, text: str, text_lower: str) -> dict | None:
        """
        Detecta: Pascal condicional — fabricar r piezas buenas con % defectuosas,
        dado que en k piezas no se alcanzó, P(necesitar más de m).
        """
        # Señales requeridas
        if not re.search(r'(?:luego|después|despues)\s+de\s+(?:fabricar|producir)', text_lower):
            return None
        if not re.search(r'no\s+(?:se\s+)?(?:hab[ií]a\s+)?alcanz', text_lower):
            return None

        # Consulta: "más de X piezas"
        m_query = re.search(r'm[aá]s\s+de\s+(\d+)\s+piezas?', text_lower)
        if not m_query:
            return None
        query_n = int(m_query.group(1))

        # Éxitos requeridos: "pedido de X piezas buenas" o "X piezas buenas"
        m_pedido = re.search(
            r'(\d+)\s+(?:piezas?\s+)?(?:buenas?|correctas?|no\s+defectuosas?)',
            text_lower,
        )
        if not m_pedido:
            return None
        r_success = int(m_pedido.group(1))

        # Tasa de defectuosas: "X% de defectuosas"
        m_defect = re.search(r'(\d+(?:[.,]\d+)?)\s*%\s*(?:de\s+)?defectuosas?', text_lower)
        if not m_defect:
            return None
        defect_rate = float(m_defect.group(1).replace(",", ".")) / 100
        p = round(1 - defect_rate, 6)

        # Condición: "luego de fabricar X piezas"
        m_cond = re.search(
            r'(?:luego|después|despues)\s+de\s+(?:fabricar|producir)\s+(\d+)\s+piezas?',
            text_lower,
        )
        if not m_cond:
            return None
        condition_n = int(m_cond.group(1))

        return {
            "status": "compound",
            "compound_type": "pascal_conditional",
            "r_success": r_success,
            "p": p,
            "condition_n": condition_n,
            "query_n": query_n,
            "interpretation": (
                f"Problema compuesto: Pascal condicional. "
                f"Se necesitan {r_success} piezas buenas (p={p}). "
                f"Dado que en {condition_n} piezas no se alcanzó, "
                f"P(necesitar más de {query_n})."
            ),
        }

    def _extract_compound_query(self, text_lower: str) -> tuple[str, int | None]:
        """Extrae tipo de consulta y valor para problemas compuestos sobre cajas/lotes."""
        unit = r"(?:cajas?|lotes?)"

        # "menos de X cajas" → estrictamente menor → F(X-1)
        m = re.search(rf'menos\s+de\s+(\d+)\s+{unit}', text_lower)
        if m:
            return "cdf_left", int(m.group(1)) - 1

        # "al menos X cajas"
        m = re.search(rf'(?:al\s+menos|como\s+m[ií]nimo|por\s+lo\s+menos)\s+(\d+)\s+{unit}', text_lower)
        if m:
            return "cdf_right", int(m.group(1))

        # "a lo sumo X cajas"
        m = re.search(rf'(?:a\s+lo\s+sumo|como\s+m[aá]ximo|no\s+m[aá]s\s+de)\s+(\d+)\s+{unit}', text_lower)
        if m:
            return "cdf_left", int(m.group(1))

        # "más de X cajas" → estrictamente mayor → G(X+1)
        m = re.search(rf'm[aá]s\s+de\s+(\d+)\s+{unit}', text_lower)
        if m:
            return "cdf_right", int(m.group(1)) + 1

        # "exactamente X cajas"
        m = re.search(rf'(?:exactamente|justo)\s+(\d+)\s+{unit}', text_lower)
        if m:
            return "probability", int(m.group(1))

        # "X o menos cajas"
        m = re.search(rf'(\d+)\s+o\s+menos\s+{unit}', text_lower)
        if m:
            return "cdf_left", int(m.group(1))

        # "X o más cajas"
        m = re.search(rf'(\d+)\s+o\s+m[aá]s\s+{unit}', text_lower)
        if m:
            return "cdf_right", int(m.group(1))

        # Fallback sin unidad: "rechacen menos de X"
        m = re.search(r'rechacen?\s+menos\s+de\s+(\d+)', text_lower)
        if m:
            return "cdf_left", int(m.group(1)) - 1

        m = re.search(r'rechacen?\s+(?:al\s+menos|como\s+m[ií]nimo)\s+(\d+)', text_lower)
        if m:
            return "cdf_right", int(m.group(1))

        m = re.search(r'rechacen?\s+m[aá]s\s+de\s+(\d+)', text_lower)
        if m:
            return "cdf_right", int(m.group(1)) + 1

        return "cdf_left", None

    # -----------------------------------------------------------------------
    # Multinomial: extracción vectorial + flujo propio
    # -----------------------------------------------------------------------

    def _parse_multinomial(self, text: str, text_lower: str) -> dict:
        params, query_params = self._extract_multinomial_params(text, text_lower)

        # Validar que vinieron al menos las probabilidades
        if not params.get("pi"):
            return {
                "status": "need_more_info",
                "model": "Multinomial",
                "params": params,
                "question": REQUIRED_PARAMS["Multinomial"]["pi"],
            }

        # Derivar n de sum(ri) si no vino explícito
        if "n" not in params and query_params.get("r_vector"):
            params["n"] = sum(query_params["r_vector"])

        # Si hay r_vector completo, la consulta es probabilidad conjunta
        if query_params.get("r_vector"):
            if len(query_params["r_vector"]) != len(params["pi"]):
                return {
                    "status": "need_more_info",
                    "model": "Multinomial",
                    "params": params,
                    "question": (f"Detecté {len(params['pi'])} probabilidades pero "
                                 f"{len(query_params['r_vector'])} conteos. "
                                 "Deben tener la misma cantidad."),
                }
            query_type = "joint_probability"
        else:
            query_type = "full_analysis"

        if "n" not in params:
            return {
                "status": "need_more_info",
                "model": "Multinomial",
                "params": params,
                "question": "¿Cuántos ensayos totales (valor de n)?",
            }

        return {
            "status": "complete",
            "model": "Multinomial",
            "params": params,
            "query_type": query_type,
            "query_params": query_params,
            "interpretation": self._build_multinomial_interpretation(params, query_type, query_params),
        }

    def _extract_multinomial_params(self, text: str, text_lower: str) -> tuple[dict, dict]:
        params: dict = {}
        query_params: dict = {}

        # n explícito
        for pat in EXTRA_PARAM_PATTERNS["Multinomial"]["n"]:
            m = re.search(pat, text_lower)
            if m:
                params["n"] = int(m.group(1))
                break

        # pi: lista de probabilidades
        # Formato mixto: decimales "0.2; 0.3; 0.5" o "0.2, 0.3, 0.5" o porcentajes "20%; 30%; 50%"
        _P_ITEM = r"\d+(?:[.,]\d+)?%?"
        _P_LIST = rf"{_P_ITEM}(?:\s*[,;]\s*{_P_ITEM}){{1,}}"
        pi_patterns = [
            rf"(?:p1|p_1)\s*=\s*([\d.]+)\s*[,;]\s*(?:p2|p_2)\s*=\s*([\d.]+)"
            rf"(?:\s*[,;]\s*(?:p3|p_3)\s*=\s*([\d.]+))?"
            rf"(?:\s*[,;]\s*(?:p4|p_4)\s*=\s*([\d.]+))?",
            rf"probabilidades?\s*(?:son|:|=)?\s*({_P_LIST})",
            rf"con\s+probabilidades?\s+({_P_LIST})",
            rf"\bpi\s*[=:]?\s*({_P_LIST})",
        ]
        pi_list = self._match_vector(text, text_lower, pi_patterns)
        if pi_list:
            # Normalizar porcentajes a fracciones
            pi_list = [p / 100 if p > 1 else p for p in pi_list]
            params["pi"] = pi_list

        # ri: lista de conteos / observaciones
        _R_ITEM = r"\d+"
        _R_LIST = rf"{_R_ITEM}(?:\s*[,;]\s*{_R_ITEM}){{1,}}"
        ri_patterns = [
            rf"(?:r1|r_1)\s*=\s*(\d+)\s*[,;]\s*(?:r2|r_2)\s*=\s*(\d+)"
            rf"(?:\s*[,;]\s*(?:r3|r_3)\s*=\s*(\d+))?"
            rf"(?:\s*[,;]\s*(?:r4|r_4)\s*=\s*(\d+))?",
            rf"(?:conteos?|ocurrencias?|frecuencias?|observaciones?)\s*(?:son|:|=)?\s*({_R_LIST})",
            rf"se\s+observaron?\s+({_R_LIST})",
            rf"\bri\s*[=:]?\s*({_R_LIST})",
        ]
        ri_list = self._match_vector(text, text_lower, ri_patterns, integers=True)
        if ri_list:
            query_params["r_vector"] = [int(x) for x in ri_list]

        return params, query_params

    @staticmethod
    def _match_vector(text: str, text_lower: str, patterns: list[str],
                      integers: bool = False) -> list[float]:
        """Prueba varios patrones. Devuelve la primera lista que encuentre."""
        for pat in patterns:
            m = re.search(pat, text_lower)
            if not m:
                continue
            # Si el regex tiene grupos nombrados de a uno, todos los grupos forman el vector
            groups = [g for g in m.groups() if g is not None]
            if len(groups) > 1:
                try:
                    return [float(g.replace(",", ".")) for g in groups]
                except ValueError:
                    continue
            # Caso único grupo que contiene la lista cruda
            raw = groups[0] if groups else ""
            parts = re.findall(r"\d+(?:[.,]\d+)?%?", raw)
            if len(parts) < 2:
                continue
            try:
                out = []
                for p in parts:
                    clean = p.replace(",", ".").rstrip("%")
                    if integers:
                        out.append(int(float(clean)))
                    else:
                        out.append(float(clean))
                return out
            except ValueError:
                continue
        return []

    def _build_multinomial_interpretation(self, params: dict, query_type: str,
                                          query_params: dict) -> str:
        pi_str = ", ".join(str(p) for p in params.get("pi", []))
        n = params.get("n", "?")
        if query_type == "joint_probability" and query_params.get("r_vector"):
            r_str = ", ".join(str(r) for r in query_params["r_vector"])
            return (f"Multinomial(n={n}, pi=[{pi_str}]). "
                    f"Consulta: P(r=[{r_str}]).")
        return f"Multinomial(n={n}, pi=[{pi_str}]). Consulta: análisis completo."

    # -----------------------------------------------------------------------
    # Construir interpretación legible
    # -----------------------------------------------------------------------

    def _build_interpretation(self, model: str, params: dict, query_type: str, query_params: dict) -> str:
        params_str = ", ".join(f"{k}={v}" for k, v in params.items())
        qt_labels = {
            "probability":   "P(r = {r})",
            "cdf_left":      "F({r}) = P(VA ≤ {r})",
            "cdf_right":     "G({r}) = P(VA ≥ {r})",
            "range":         "P({a} ≤ r ≤ {b})",
            "full_analysis": "análisis completo",
        }
        label_tmpl = qt_labels.get(query_type, query_type)
        try:
            label = label_tmpl.format(**query_params)
        except KeyError:
            label = label_tmpl
        return f"{model}({params_str}). Consulta: {label}."

    # -----------------------------------------------------------------------
    # CustomPMF — PMF discreta casera con normalizador k
    # -----------------------------------------------------------------------

    @staticmethod
    def _normalize_pmf_expr(expr: str) -> str:
        """Convierte fragmentos LaTeX a sintaxis Python evaluable.

        - ``\\frac{A}{B}`` → ``(A)/(B)``
        - ``\\sum_{...}^{...}`` → se descarta (no debería aparecer en la PMF
          base, suele venir de un mal copy/paste de la condición de cierre)
        - ``x_i``, ``x_{i}``, ``X_i`` → ``x``  (subíndice de índice de suma)
        - ``^N`` → ``**N``
        - ``\\cdot`` → ``*``
        - ``$``, ``\\,``, ``\\;``, ``\\!`` → se eliminan
        - Comandos ``\\foo`` sueltos se descartan (whitelisting de Python).
        """
        s = expr or ""
        # \frac{A}{B} → (A)/(B)  (resolución no anidada — suficiente para PMFs simples)
        for _ in range(3):
            new = re.sub(
                r"\\frac\s*\{([^{}]*)\}\s*\{([^{}]*)\}",
                r"(\1)/(\2)",
                s,
            )
            if new == s:
                break
            s = new
        # Descartar \sum_{...}^{...} (su presencia adentro de la PMF es
        # casi siempre un error de redacción del enunciado).
        s = re.sub(r"\\sum\s*(?:_\{[^{}]*\})?\s*(?:\^\{?[^{}\s]*\}?)?", "", s)
        # Subíndice de índice de suma: x_i, x_{i}, X_i, X_{i}
        s = re.sub(r"\b([xX])\s*_\s*\{?\s*[ij]\s*\}?", r"\1", s)
        # ^N → **N  (incluyendo {...})
        s = re.sub(r"\^\s*\{([^{}]+)\}", r"**(\1)", s)
        s = re.sub(r"\^\s*([A-Za-z0-9.]+)", r"**\1", s)
        # \cdot, \times → *
        s = re.sub(r"\\(?:cdot|times)", "*", s)
        # Espaciadores LaTeX: \,  \;  \!  \: \>
        s = re.sub(r"\\[,;:!>]", "", s)
        # $ marker
        s = s.replace("$", "")
        # Llaves residuales que envuelven tokens simples
        s = re.sub(r"\{([^{}]+)\}", r"\1", s)
        # Cualquier comando LaTeX restante (\foo) → eliminar (no podemos eval).
        s = re.sub(r"\\[A-Za-z]+", "", s)
        # Normalizar espacios y resolver `· ` (símbolo unicode multiplicación)
        s = s.replace("·", "*").replace("×", "*")
        s = re.sub(r"\s+", " ", s).strip()
        return s

    def _parse_custom_pmf(self, text: str, text_lower: str) -> dict:
        """Extrae expr, dominio y (opcional) k_var. Devuelve complete si se
        puede armar el modelo o need_more_info preguntando por el dominio."""
        # Trabajar sobre el texto sin marcadores LaTeX inline ($...$).
        text_clean = re.sub(r"\$+", " ", text)

        # Expresión: "P(X=x) = (x+2)/k" o "P(X=x) = k·x" o "P(X=x) = x^2 / k"
        m_expr = re.search(
            r"P\s*\(\s*X\s*=\s*x\s*\)\s*=\s*([^\n,;.]+?)(?:\s+(?:para|con|donde|si|,|;|\.|$))",
            text_clean,
            re.IGNORECASE,
        )
        if not m_expr:
            m_expr = re.search(
                r"P\s*\(\s*X\s*=\s*x\s*\)\s*=\s*([^\n]+)",
                text_clean,
                re.IGNORECASE,
            )
        expr = m_expr.group(1).strip() if m_expr else ""
        # Limpiar caracteres sueltos al final
        expr = re.sub(r"\s+(?:para|con|donde|si|y|;|,|\.)+\s*$", "", expr, flags=re.IGNORECASE).strip()
        # Normalizar LaTeX → sintaxis Python evaluable
        expr = self._normalize_pmf_expr(expr)

        # k_var: detectar qué símbolo hace de normalizador
        k_var = "k"
        for candidate in ("k", "K", "c", "C"):
            if re.search(rf"\b{candidate}\b", expr):
                k_var = candidate
                break

        # Dominio: "x ∈ {0,1,2,3}", "x = 0, 1, 2, 3", "para x = 0, 1, 2, 3",
        # "x ∈ [0,3]" (entero), "x = 0, 1, ..., N"
        domain: list[int] = []

        # Patrón con llaves: "x ∈ {0,1,2,3}" o "x = \{1,2,3,4,5\}" o "x ∈ [0,3]"
        m_dom = re.search(
            r"x\s*(?:∈|\\in|en|=)\s*\\?[{\[]([^}\]\\]+)\\?[}\]]",
            text_clean, re.IGNORECASE,
        )
        if not m_dom:
            m_dom = re.search(r"x\s*[:=]\s*([-\d,\s]+(?:,\s*)?[-\d,\s]+)", text_clean, re.IGNORECASE)
        if m_dom:
            raw = m_dom.group(1)
            nums = re.findall(r"-?\d+", raw)
            if len(nums) >= 2:
                domain = [int(n) for n in nums]

        # Rango "0..N" o "x va de 0 a N"
        if not domain:
            m_range = re.search(r"x\s+(?:va|varia)\s+de\s+(\d+)\s+a\s+(\d+)", text_clean, re.IGNORECASE)
            if m_range:
                a, b = int(m_range.group(1)), int(m_range.group(2))
                if b - a <= 20:
                    domain = list(range(a, b + 1))

        params: dict = {"expr": expr, "k_var": k_var}
        if domain:
            params["domain"] = domain

        # Query type
        query_type, query_params = self._detect_custom_pmf_query(text, text_lower)

        if not expr:
            return {
                "status": "need_more_info",
                "model": "CustomPMF",
                "params": params,
                "question": (
                    "Escribí la fórmula de la PMF y el dominio. "
                    "Ejemplo: P(X=x) = (x+2)/k para x ∈ {0,1,2,3}."
                ),
            }

        if not domain:
            return {
                "status": "need_more_info",
                "model": "CustomPMF",
                "params": params,
                "question": (
                    f"Indicá el dominio de x. Ejemplo: x ∈ {{0,1,2,3}} o x = 1, 2, 3, 4."
                ),
                "query_type": query_type,
                "query_params": query_params,
            }

        return {
            "status": "complete",
            "model": "CustomPMF",
            "params": params,
            "query_type": query_type,
            "query_params": query_params,
            "interpretation": (
                f"CustomPMF(expr='{expr}', dominio={domain}). "
                f"Consulta: {query_type}."
            ),
        }

    # Eventos sobre X para detectar en un fragmento de texto.
    # Orden importa: probar compuestos antes que simples.
    _COND_SPLIT_RE = re.compile(
        r"\b(?:sabiendo\s+que|dado\s+que|dado|si\s+ya|condicional\s+a|condicionad[ao]s?\s+a)\b",
        re.IGNORECASE,
    )

    @staticmethod
    def _strip_latex_artifacts(s: str) -> str:
        """Elimina construcciones LaTeX que meten dígitos espurios en el
        fragmento (por ejemplo `\\sum_{i=1}^{5}` mete "1" y "5" que no
        refieren a la consulta)."""
        # \sum_{...}^{...}  y  \sum_{...}  y  \sum^{...}
        s = re.sub(r"\\sum\s*(?:_\{[^{}]*\})?\s*(?:\^\{[^{}]*\}|\^[^\s{}]*)?", " ", s)
        # \frac{a}{b}
        for _ in range(3):
            new = re.sub(r"\\frac\s*\{[^{}]*\}\s*\{[^{}]*\}", " ", s)
            if new == s:
                break
            s = new
        # Cualquier otro comando LaTeX con llaves opcionales
        s = re.sub(r"\\[a-z]+\s*(?:\{[^{}]*\})?", " ", s)
        # Subíndices / superíndices con llaves
        s = re.sub(r"_\{[^{}]*\}", "", s)
        s = re.sub(r"\^\{[^{}]*\}", "", s)
        # Subíndices / superíndices cortos tipo x_i, ^2
        s = re.sub(r"_[a-z0-9]+", "", s)
        s = re.sub(r"\^[a-z0-9]+", "", s)
        s = s.replace("$", " ")
        return s

    @classmethod
    def _extract_event_on_x(cls, frag: str) -> tuple[str, object] | None:
        """Extrae (op, val) o ('between', (a,b)) de un fragmento de texto.

        Devuelve None si no identifica ningún evento.
        """
        s = cls._strip_latex_artifacts(frag.lower())
        # "entre A y B" → between
        m = re.search(r"\bentre\s+(\d+)\s+y\s+(\d+)", s)
        if m:
            return ("between", (int(m.group(1)), int(m.group(2))))
        # Notación matemática directa
        m = re.search(r"\bx\s*(<=|>=|<|>|=)\s*(\d+)", s)
        if m:
            return (m.group(1), int(m.group(2)))
        # "mayor o igual (que|a) N", "menor o igual (que|a) N"
        m = re.search(r"mayor\s+o\s+igual\s+(?:que|a)\s+(\d+)", s)
        if m:
            return (">=", int(m.group(1)))
        m = re.search(r"menor\s+o\s+igual\s+(?:que|a)\s+(\d+)", s)
        if m:
            return ("<=", int(m.group(1)))
        # "más de N", "mayor que N", "superior a N"
        m = re.search(r"m[aá]s\s+de\s+(\d+)|mayor(?:\s+que|\s+a)\s+(\d+)|superior\s+a\s+(\d+)", s)
        if m:
            v = next(g for g in m.groups() if g is not None)
            return (">", int(v))
        # "menos de N", "menor que N", "inferior a N"
        m = re.search(r"menos\s+de\s+(\d+)|menor(?:\s+que|\s+a)\s+(\d+)|inferior\s+a\s+(\d+)", s)
        if m:
            v = next(g for g in m.groups() if g is not None)
            return ("<", int(v))
        # "al menos N", "N o más", "por lo menos N"
        m = re.search(r"al\s+menos\s+(\d+)|(\d+)\s+o\s+m[aá]s|por\s+lo\s+menos\s+(\d+)", s)
        if m:
            v = next(g for g in m.groups() if g is not None)
            return (">=", int(v))
        # "hasta N", "N o menos", "a lo sumo N"
        m = re.search(r"acumulada\s+hasta\s+(\d+)|\bhasta\s+(\d+)|(\d+)\s+o\s+menos|a\s+lo\s+sumo\s+(\d+)", s)
        if m:
            v = next(g for g in m.groups() if g is not None)
            return ("<=", int(v))
        # "exactamente N", "los N [sustantivo]"
        # (el `= N` suelto quedó descartado: era muy propenso a capturar
        # artefactos como `i=1` dentro de `\sum_{i=1}^{5}`; el caso `X=N`
        # lo cubre la "Notación matemática directa" más arriba.)
        m = re.search(r"exactamente\s+(\d+)|\blos\s+(\d+)\s+[a-záéíóúñ]+", s)
        if m:
            v = next(g for g in m.groups() if g is not None)
            return ("=", int(v))
        return None

    def _detect_custom_pmf_query(self, text: str, text_lower: str) -> tuple[str, dict]:
        # Condicional — tiene precedencia sobre los detectores simples.
        # Patrón 1: notación matemática P(X op a | X op b)
        m_cond_math = re.search(
            r"p\s*\(\s*x\s*(?P<no>=|<=|>=|<|>)\s*(?P<nv>\d+)\s*\|\s*"
            r"x\s*(?P<do>=|<=|>=|<|>)\s*(?P<dv>\d+)\s*\)",
            text_lower,
        )
        if m_cond_math:
            return "conditional", {
                "num_op": m_cond_math.group("no"),
                "num_val": int(m_cond_math.group("nv")),
                "den_op": m_cond_math.group("do"),
                "den_val": int(m_cond_math.group("dv")),
            }
        # Patrón 2: lenguaje natural con separador "sabiendo que", "dado", etc.
        split = self._COND_SPLIT_RE.split(text_lower, maxsplit=1)
        if len(split) == 2:
            num_frag, den_frag = split[0], split[1]
            num_evt = self._extract_event_on_x(num_frag)
            den_evt = self._extract_event_on_x(den_frag)
            if num_evt and den_evt:
                qp: dict = {
                    "num_op": num_evt[0], "num_val": num_evt[1],
                    "den_op": den_evt[0], "den_val": den_evt[1],
                }
                return "conditional", qp

        if re.search(r"\besperanza\b|\bmedia\b|\be\s*\(\s*x\s*\)", text_lower):
            return "mean", {}
        if re.search(r"\bvarianza\b|\bv\s*\(\s*x\s*\)", text_lower):
            return "variance", {}
        if re.search(r"desv[ií]o|desviaci[oó]n|\bsigma\b", text_lower):
            return "std_dev", {}
        m_pp = re.search(r"p\s*\(\s*x\s*=\s*(\d+)\s*\)", text_lower)
        if m_pp:
            return "probability", {"r": int(m_pp.group(1))}
        m_fl = re.search(r"f\s*\(\s*(\d+)\s*\)|p\s*\(\s*x\s*<=?\s*(\d+)\s*\)", text_lower)
        if m_fl:
            v = m_fl.group(1) or m_fl.group(2)
            return "cdf_left", {"r": int(v)}
        m_fr = re.search(r"g\s*\(\s*(\d+)\s*\)|p\s*\(\s*x\s*>=?\s*(\d+)\s*\)", text_lower)
        if m_fr:
            v = m_fr.group(1) or m_fr.group(2)
            return "cdf_right", {"r": int(v)}
        # Lenguaje natural: "exactamente N", "acumulada hasta N", "al menos N",
        # "N o menos", "N o más".
        m_ex = re.search(r"exactamente\s+(\d+)", text_lower)
        if m_ex:
            return "probability", {"r": int(m_ex.group(1))}
        m_hasta = re.search(
            r"acumulada\s+hasta\s+(\d+)|hasta\s+(\d+)|(\d+)\s+o\s+menos|a\s+lo\s+sumo\s+(\d+)",
            text_lower,
        )
        if m_hasta:
            v = next(g for g in m_hasta.groups() if g is not None)
            return "cdf_left", {"r": int(v)}
        m_alm = re.search(
            r"al\s+menos\s+(\d+)|(\d+)\s+o\s+m[aá]s|por\s+lo\s+menos\s+(\d+)",
            text_lower,
        )
        if m_alm:
            v = next(g for g in m_alm.groups() if g is not None)
            return "cdf_right", {"r": int(v)}
        return "full_analysis", {}

    # -----------------------------------------------------------------------
    # TCL / Suma de VA
    # -----------------------------------------------------------------------

    _TCL_KEYWORDS = (
        r"teorema central",
        r"teorema del limite",
        r"teorema del límite",
        r"\btcl\b",
        r"suma\s+de\s+(?:\d+\s+)?variables",
        r"suma\s+de\s+va\b",
        r"suma\s+de\s+v\.a",
        r"s\s*=\s*x_?1",
        r"sigma.*x_?i",
        r"agregad[oa]\s+de\s+(?:\d+\s+)?variables",
    )

    def _is_tcl(self, text_lower: str, text: str) -> bool:
        for kw in self._TCL_KEYWORDS:
            if re.search(kw, text_lower):
                return True
        # Heurística: ≥2 patrones "N sust de M [unidad]" + consulta de suma/peso total
        count_objs = re.findall(
            r"(\d+)\s+[a-záéíóúñ]+s?\s+de\s+\d+(?:[.,]\d+)?\s*(?:kg|kilos?|g|m|cm|unidad)",
            text_lower,
        )
        has_total = bool(re.search(
            r"\bpeso\s+total\b|\bsuma\s+total\b|\btotal\s+sea\b|\btotal\s+supere\b|\btotal\s+exced",
            text_lower,
        ))
        if len(count_objs) >= 2 and has_total:
            return True
        return False

    def _parse_tcl(self, text: str, text_lower: str) -> dict:
        """Extrae componentes (mean, variance) de patrones como
        'media 100 y varianza 25', o 'k copias de media μ varianza σ²'.

        En v1 hacemos una extracción best-effort: si no logramos identificar
        componentes, devolvemos need_more_info para que el usuario las cargue
        en la UI.
        """
        components: list[dict] = []

        # Patrón: "k variables con media μ y varianza σ²"
        _NUM = r"\d+(?:[.,]\d+)?"
        m_k = re.search(
            rf"(\d+)\s*(?:variables?|componentes?|copias?|pieza?s?)\s+"
            rf"(?:con\s+)?media\s*(?:=|de)?\s*({_NUM})\s*"
            rf"(?:y\s+)?varianza\s*(?:=|de)?\s*({_NUM})",
            text_lower,
        )
        if m_k:
            try:
                cnt = int(m_k.group(1))
                mu = float(m_k.group(2).replace(",", "."))
                var = float(m_k.group(3).replace(",", "."))
                components.append({"name": "X", "mean": mu, "variance": var, "count": cnt})
            except ValueError:
                pass

        # Patrón: "N nombre de μ kg c/u con (desvío|varianza) X"
        # Ej: "3 mesas de 50 kg cada una con desvío 2, 12 sillas de 8 kg c/u con varianza 1"
        if not components:
            _NUM_2 = r"\d+(?:[.,]\d+)?"
            multi_pat = re.compile(
                rf"(\d+)\s+([a-záéíóúñ]+?)s?\s+de\s+({_NUM_2})\s*(?:kg|kilos?|g|gramos?|m|cm)?\s*"
                rf"(?:c/u|cada\s+una?|c/una?)?\s*(?:con|y)?\s*"
                rf"(?:desv[ií]o(?:\s+est[aá]ndar)?|sigma|σ|varianza|var|v)\s*"
                rf"(?:=|de)?\s*({_NUM_2})",
                re.IGNORECASE,
            )
            for m in multi_pat.finditer(text):
                try:
                    cnt = int(m.group(1))
                    name = m.group(2).strip().capitalize() or "X"
                    mu = float(m.group(3).replace(",", "."))
                    raw4 = m.group(4).replace(",", ".")
                    stat_kw = m.group(0).lower()
                    val = float(raw4)
                    # Si el indicador fue desvío, elevamos al cuadrado
                    is_std = bool(re.search(r"desv[ií]o|sigma|σ", stat_kw))
                    var = val ** 2 if is_std else val
                    components.append({
                        "name": name,
                        "mean": mu,
                        "variance": var,
                        "count": cnt,
                    })
                except (ValueError, AttributeError):
                    pass

        # Patrón: pares sueltos "E(Xi)=μ, V(Xi)=σ²"
        if not components:
            means = re.findall(r"E\s*\(\s*X?_?\d*\s*\)\s*=\s*([\d.,]+)", text, re.IGNORECASE)
            vars_ = re.findall(r"V\s*\(\s*X?_?\d*\s*\)\s*=\s*([\d.,]+)", text, re.IGNORECASE)
            if means and vars_ and len(means) == len(vars_):
                for i, (m, v) in enumerate(zip(means, vars_)):
                    components.append({
                        "name": f"X{i+1}",
                        "mean": float(m.replace(",", ".")),
                        "variance": float(v.replace(",", ".")),
                        "count": 1,
                    })

        # Detectar consulta
        query_type, query_params = self._detect_tcl_query(text, text_lower)

        if not components:
            return {
                "status": "need_more_info",
                "mode": "TCL / Suma de VA",
                "question": ("Cargá las componentes en la tabla: "
                             "para cada Xi, su E(Xi), V(Xi) y cuántas copias iid. "
                             "Si son k=30 Bernoullis con p=0.5: E=0.5, V=0.25, count=30."),
                "components": [],
                "query_type": query_type,
                "query_params": query_params,
            }

        return {
            "status": "complete",
            "mode": "TCL / Suma de VA",
            "components": components,
            "query_type": query_type,
            "query_params": query_params,
            "interpretation": f"TCL: {len(components)} componente(s), consulta {query_type}.",
        }

    def _detect_tcl_query(self, text: str, text_lower: str) -> tuple[str, dict]:
        # Rango: "entre a y b", "P(a <= S <= b)"
        m_range = re.search(r"entre\s+([\d.,]+)\s+y\s+([\d.,]+)", text_lower)
        if m_range:
            try:
                return "range", {
                    "a": float(m_range.group(1).replace(",", ".")),
                    "b": float(m_range.group(2).replace(",", ".")),
                }
            except ValueError:
                pass

        # Fractil
        m_frac = re.search(r"fract[ií]l\s*(?:=|de)?\s*([\d.,]+)", text_lower)
        if m_frac:
            try:
                alpha = float(m_frac.group(1).replace(",", "."))
                if alpha > 1:
                    alpha /= 100
                return "fractile", {"alpha": alpha}
            except ValueError:
                pass

        # Derecha: ≥, >, al menos, más de, mayor
        if re.search(r"(≥|>=|\bal menos\b|\bmayor\b|\bmas de\b|\bmás de\b|\bsupere\b|\bexced)", text_lower):
            m_val2 = re.search(r"s\s*(?:>=|>|≥)\s*([\d.,]+)", text_lower)
            if m_val2:
                return "cdf_right", {"s": float(m_val2.group(1).replace(",", "."))}
            # "peso total ≥ 180", "total supere 180", "al menos 180"
            m_tot = re.search(
                r"(?:peso\s+total|suma\s+total|total)\s*(?:sea|supere|exced\w*|mayor\s+(?:o\s+igual\s+)?a|≥|>=)?\s*([\d.,]+)",
                text_lower,
            )
            if m_tot:
                return "cdf_right", {"s": float(m_tot.group(1).replace(",", "."))}
            m_am = re.search(r"al\s+menos\s+([\d.,]+)", text_lower)
            if m_am:
                return "cdf_right", {"s": float(m_am.group(1).replace(",", "."))}

        # Izquierda (default): ≤, <, menos de, a lo sumo, hasta
        m_left = re.search(r"s\s*(?:<=|<|≤)\s*([\d.,]+)", text_lower)
        if m_left:
            return "cdf_left", {"s": float(m_left.group(1).replace(",", "."))}

        m_hasta = re.search(r"(?:menos de|hasta|a lo sumo|no más de|no mas de)\s*([\d.,]+)",
                            text_lower)
        if m_hasta:
            return "cdf_left", {"s": float(m_hasta.group(1).replace(",", "."))}

        return "cdf_left", {"s": 0.0}
