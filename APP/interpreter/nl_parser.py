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
}

# Valor de p para moneda (cara o seca)
_P_MONEDA = 0.5

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

    def parse(self, text: str) -> dict:
        text_lower = text.lower()

        # Paso 0: notación cátedra — bypass completo si hay match
        cathedra = self._try_cathedra(text)
        if cathedra:
            return cathedra

        # Paso 0.5: problemas compuestos (requieren múltiples distribuciones)
        compound = self._detect_compound(text, text_lower)
        if compound:
            return compound

        # Paso 1: detectar modo (antes de buscar modelo)
        if self._is_datos_agrupados(text_lower, text):
            return self._parse_datos_agrupados(text, text_lower)

        if self._is_probabilidad(text_lower, text):
            return self._parse_probabilidad(text, text_lower)

        # Fase A: modelo discreto/continuo
        model = self._detect_model(text_lower)
        if model is None:
            return {
                "status": "need_more_info",
                "model": None,
                "params": {},
                "question": "No pude identificar el modelo estadístico. ¿Cuál es? (Ej: Binomial, Poisson, etc.)",
            }

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
        # Remover prefijos comunes
        desc = re.sub(r"^(?:producir|fabricar|hacer|tener|que\s+se\s+produz\w+)\s+", "", desc)
        # Tomar primera(s) palabra(s) significativas
        words = desc.split()
        if words:
            name = words[0].capitalize().rstrip(",.:;")
            # Si es un artículo, tomar la siguiente
            if name.lower() in ("solo", "al", "la", "el", "las", "los", "un", "una"):
                name = words[1].capitalize().rstrip(",.:;") if len(words) > 1 else name
            return name
        return None

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

        # Patrón de muestreo: "muestra de X (unidades) de cada caja/lote de Y"
        m_sample = re.search(
            r'muestra\s+de\s+(\w+)\s+(?:unidades?\s+)?de\s+cada\s+(?:caja|lote)\s+de\s+(\d+)',
            text_lower,
        )
        if not m_sample:
            return None

        sample_n_raw = m_sample.group(1)
        sample_n = _WORD_TO_NUM.get(sample_n_raw) or (int(sample_n_raw) if sample_n_raw.isdigit() else None)
        if sample_n is None:
            return None
        box_N = int(m_sample.group(2))

        # Número de cajas: "X cajas/lotes"
        m_boxes = re.search(r'(\d+)\s+(?:cajas?|lotes?)', text_lower)
        if not m_boxes:
            return None
        num_boxes = int(m_boxes.group(1))

        # Defectuosas por caja: "X pieza(s) defectuosa(s) en cada caja"
        m_defect = re.search(
            r'(\w+)\s+(?:piezas?\s+)?defectuosas?\s+(?:en\s+)?(?:cada|por)\s+(?:caja|lote)',
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
