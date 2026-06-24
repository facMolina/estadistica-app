"""UI para el modo 'Formulario / Reconocimiento'.

Modo estatico, offline, sin IA y sin logica de calculo: porta el contenido del
FORMULARIO del 2do parcial (tabla de reconocimiento, convenciones de la
catedra, formulas por distribucion, plantillas de ejercicio, tabla Z y
errores comunes) para consulta rapida durante el examen.
"""

from __future__ import annotations

import streamlit as st

REGLA_DE_ORO = (
    "Casi siempre te dan **(a) la media** y **(b) un dato extra** (la moda, o "
    "\"el X% esta por debajo de tal valor\"). Con esos dos sacas los parametros:\n\n"
    "- Normal + un percentil -> estandarizar para hallar $\\sigma$: "
    "$\\sigma=(x_0-\\mu)/z_p$.\n"
    "- Pareto: media y moda -> $b=\\mu/(\\mu-\\delta)$.\n"
    "- Gamma: media y varianza -> $\\lambda=\\mu/\\sigma^2$, $r=\\mu^2/\\sigma^2$."
)

CONVENCIONES = (
    "- **F(x) = P(X ≤ x)** = acumulada izquierda. **G(x) = P(X > x)** = "
    "acumulada derecha. Siempre $F(x)+G(x)=1$.\n"
    "- En fiabilidad: **G(x) = confiabilidad** (dura mas de x). "
    "**F(x) = riesgo** (falla antes de x).\n"
    "- Fractil $x_\\alpha$: deja $\\alpha$ de probabilidad a su izquierda -> "
    "$F(x_\\alpha)=\\alpha$.\n"
    "- $Cv=\\sigma/\\mu\\cdot100$. Representativa la media si $Cv<10\\%$.\n"
    "- $C$ = constante de Euler-Mascheroni ≈ **0,5772** (solo Gumbel). "
    "$\\Gamma$ = funcion Gamma de Euler (Weibull)."
)

# Cada entrada: nombre, parametros, pistas (texto de busqueda/reconocimiento),
# contenido markdown completo (formulas, tabla de momentos, casos especiales).
DISTRIBUCIONES = [
    {
        "nombre": "Normal",
        "parametros": "μ, σ",
        "pistas": "se distribuye normalmente; simetrica; media + desvio; X% por encima/debajo de un valor",
        "contenido": (
            "**Cuando:** medicion simetrica (peso, tiempo, consumo, monto) "
            "\"se distribuye normalmente\".\n\n"
            "$z=(x-\\mu)/\\sigma$  ·  $P(X<x)=\\Phi(z)$ → buscar $\\Phi(z)$ en la tabla Z.\n\n"
            "| Media | Var | Moda=Mediana=μ | Asimetria | Fractil |\n"
            "|---|---|---|---|---|\n"
            "| μ | σ² | μ | 0 (simetrica) | $x_\\alpha=\\mu+z_\\alpha\\sigma$ |\n\n"
            "**Hallar σ con un percentil:** si \"el p% esta por debajo de x₀\" → "
            "$z_p$ de tabla, $\\sigma=(x_0-\\mu)/z_p$. Si dan dos percentiles simetricos, "
            "μ es el punto medio.\n\n"
            "**Truco simetria:** $P(\\mu<X<x_{0,8})=0,8-0,5=0,30$. \"Por encima de la media\" = 0,5.\n\n"
            "**Expectativa parcial izquierda:** $H(a)=\\mu\\Phi(z)-\\sigma\\varphi(z)$, con "
            "$\\varphi(z)$ = densidad estandar. Media condicional "
            "$E[X\\mid X<a]=H(a)/\\Phi(z)$.\n\n"
            "⚠️ **Error comun:** usar σ² donde va σ al estandarizar."
        ),
    },
    {
        "nombre": "Log-Normal",
        "parametros": "m, D (de los ln)",
        "pistas": "asimetria fuerte; logaritmo normal; admite valores bajo la moda; montos/tiempos sesgados",
        "contenido": (
            "**Cuando:** tiempos o montos con asimetria fuerte; \"el logaritmo es normal\". "
            "m y D son la media y el desvio de los **ln(X)**.\n\n"
            "$P(X<x)=\\Phi\\left(\\dfrac{\\ln x-m}{D}\\right)$\n\n"
            "| De μ, σ de X → parametros | Media | Varianza | Moda | Mediana | Fractil |\n"
            "|---|---|---|---|---|---|\n"
            "| $D=\\sqrt{\\ln(1+(\\sigma/\\mu)^2)}$ ; $m=\\ln\\mu-D^2/2$ | $e^{m+D^2/2}$ | "
            "$e^{2m+D^2}(e^{D^2}-1)$ | $e^{m-D^2}$ | $e^m$ | $x_\\alpha=e^{m+z_\\alpha D}$ |\n\n"
            "Si solo dan media y desvio de X, primero pasar a m y D."
        ),
    },
    {
        "nombre": "Exponencial",
        "parametros": "λ",
        "pistas": "tiempo hasta la primera falla; al azar; sin memoria; tasa constante; fusible chip",
        "contenido": (
            "**Cuando:** tiempo/continuo hasta la **primera** falla al azar; tasa constante; "
            "\"sin memoria\". Es Gamma con r=1.\n\n"
            "$f(x)=\\lambda e^{-\\lambda x}$ · $G(x)=e^{-\\lambda x}$ · $F(x)=1-e^{-\\lambda x}$ (x≥0)\n\n"
            "| Media | Var | Cv | Moda | Mediana | Fractil |\n"
            "|---|---|---|---|---|---|\n"
            "| 1/λ | 1/λ² | **100%** | 0 | $\\ln2/\\lambda$ | $x_\\alpha=-\\ln(1-\\alpha)/\\lambda$ |\n\n"
            "**Sin memoria:** $P(X>s+t\\mid X>s)=P(X>t)=e^{-\\lambda t}$.\n\n"
            "λ es la **tasa** del proceso de Poisson asociado. \"1 falla cada 36 h\" → "
            "λ=1/36 por hora. Cuidar las **unidades**."
        ),
    },
    {
        "nombre": "Weibull",
        "parametros": "α (escala), β (forma)",
        "pistas": "desgaste; fatiga; riesgo de rotura; esfuerzo de materiales; vida util",
        "contenido": (
            "**Cuando:** duracion/rotura con desgaste o fatiga, esfuerzo de materiales, "
            "\"riesgo de rotura\".\n\n"
            "$G(x)=e^{-(x/\\alpha)^\\beta}$ = confiabilidad · $F(x)=1-e^{-(x/\\alpha)^\\beta}$ = riesgo\n\n"
            "| Media | Moda | Mediana | Fractil |\n"
            "|---|---|---|---|\n"
            "| $\\alpha\\Gamma(1+1/\\beta)$ | $\\alpha(1-1/\\beta)^{1/\\beta}$ si β>1, si no 0 | "
            "$\\alpha(\\ln2)^{1/\\beta}$ | $x_\\alpha=\\alpha(-\\ln(1-\\alpha))^{1/\\beta}$ |\n\n"
            "**Carga max. para riesgo ≤ r:** $x=\\alpha(-\\ln(1-r))^{1/\\beta}$. β=1 ⇒ Exponencial."
        ),
    },
    {
        "nombre": "Gumbel del minimo",
        "parametros": "α (escala), μ (moda)",
        "pistas": "valor minimo de un conjunto; vida humana; sequia; caudal precipitacion minima",
        "contenido": (
            "**Cuando:** el **minimo** de un conjunto: vida humana, sequia, caudal/precipitacion "
            "minima.\n\n"
            "$G(x)=P(X>x)=e^{-e^{(x-\\mu)/\\alpha}}$ (dominio $-\\infty$ a $+\\infty$)\n\n"
            "| Media | Var | Moda | Mediana | Fractil |\n"
            "|---|---|---|---|---|\n"
            "| $\\mu-\\alpha C$ | $\\pi^2\\alpha^2/6$ | μ | $\\mu+\\alpha\\ln(\\ln2)$ | "
            "$x_\\alpha=\\mu+\\alpha\\ln(-\\ln(1-\\alpha))$ |"
        ),
    },
    {
        "nombre": "Gumbel del maximo",
        "parametros": "α (escala), μ (moda)",
        "pistas": "valor maximo; extremos; inundacion; caudal maximo; rotura de correa; elongacion maxima",
        "contenido": (
            "**Cuando:** el **maximo** / extremos: inundacion, caudal maximo, rotura de correa, "
            "elongacion maxima.\n\n"
            "$F(x)=P(X\\le x)=e^{-e^{-(x-\\mu)/\\alpha}}$\n\n"
            "| Media | Var | Moda | Mediana | Fractil |\n"
            "|---|---|---|---|---|\n"
            "| $\\mu+\\alpha C$ | $\\pi^2\\alpha^2/6$ | μ | $\\mu-\\alpha\\ln(\\ln2)$ | "
            "$x_\\alpha=\\mu-\\alpha\\ln(-\\ln\\alpha)$ |\n\n"
            "⚠️ **Ojo:** la rotura por esfuerzo es un fenomeno de **minimos** (rompe el "
            "eslabon mas debil) → usar Gumbel del MINIMO o Weibull, no Maximo."
        ),
    },
    {
        "nombre": "Pareto",
        "parametros": "δ (moda/min), b (forma)",
        "pistas": "minimo igual a la moda; salarios; ART seguro pagan el minimo; inventario minimo",
        "contenido": (
            "**Cuando:** el valor mas habitual es el **minimo**; pagos de seguros/ART (pagan el "
            "minimo), salarios, inventarios minimos. No admite valores por debajo de δ.\n\n"
            "$f(x)=b\\delta^b/x^{b+1}$ · $G(x)=(\\delta/x)^b$ · $F(x)=1-(\\delta/x)^b$ (x≥δ)\n\n"
            "| De media y moda → b | Media | Moda | Mediana | Var | Fractil |\n"
            "|---|---|---|---|---|---|\n"
            "| $b=\\mu/(\\mu-\\delta)$ | $b\\delta/(b-1)$ | δ | $\\delta\\cdot2^{1/b}$ | "
            "$\\delta^2b/((b-1)^2(b-2))$ | $x_\\alpha=\\delta/(1-\\alpha)^{1/b}$ |\n\n"
            "**Media condicional:** $E[X\\mid X>k]=bk/(b-1)$ con k el umbral."
        ),
    },
    {
        "nombre": "Uniforme",
        "parametros": "a, b",
        "pistas": "entre a y b igualmente probable; freno entre ms; tiempo en app entre minutos",
        "contenido": (
            "**Cuando:** \"entre a y b\" con todo igualmente probable.\n\n"
            "$f(x)=1/(b-a)$ · $F(x)=(x-a)/(b-a)$ (a≤x≤b)\n\n"
            "| Media | Var | Fractil |\n"
            "|---|---|---|\n"
            "| $(a+b)/2$ | $(b-a)^2/12$ | $x_\\alpha=a+\\alpha(b-a)$ |"
        ),
    },
    {
        "nombre": "Poisson (proceso)",
        "parametros": "m = λ·t",
        "pistas": "numero de eventos en un continuo fijo; fallas por semana; llegadas por hora",
        "contenido": (
            "**Cuando:** nro de eventos/fallas en un continuo **fijo** t.\n\n"
            "$P(r)=e^{-m}m^r/r!$ con $m=\\lambda\\cdot t$ · **Media = Var = m**\n\n"
            "- P(al menos k) = $1-\\sum_{r=0}^{k-1}P(r)$.\n"
            "- Escalar m a la ventana pedida: λ=1 cada 36 h y t=1 semana (168 h) → "
            "m=168/36=4,6667."
        ),
    },
    {
        "nombre": "Gamma / Erlang",
        "parametros": "λ (tasa), r (nro eventos)",
        "pistas": "continuo necesario para r eventos; tiempo hasta la r-esima falla; gamma media varianza",
        "contenido": (
            "**Cuando:** continuo (tiempo) necesario para que ocurran **r** eventos Poisson; "
            "\"Gamma con media y varianza\". Suma de r exponenciales con igual λ.\n\n"
            "$f(x)=\\lambda^r x^{r-1}e^{-\\lambda x}/(r-1)!$ (x≥0)\n\n"
            "| De media y var → parametros | Media | Var | Moda |\n"
            "|---|---|---|---|\n"
            "| $\\lambda=\\mu/\\sigma^2$ ; $r=\\mu^2/\\sigma^2$ | r/λ | r/λ² | "
            "$(r-1)/\\lambda$ si r>1, si no 0 |\n\n"
            "**Calcular P con Gamma:**\n"
            "- **Via Poisson** (r entero): $F_\\Gamma(x)=P(\\text{Poisson}(m=\\lambda x)\\ge r)"
            "=1-\\sum_{k=0}^{r-1}e^{-\\lambda x}(\\lambda x)^k/k!$.\n"
            "- **Via Normal (Wilson-Hilferty)**, r grande o no entero: "
            "$Z=3\\sqrt{r}\\left[(\\lambda x/r)^{1/3}-1+\\dfrac{1}{9r}\\right]$, "
            "luego $P(X\\le x)=\\Phi(Z)$."
        ),
    },
]

TCL_CONTENIDO = (
    "**Suma de normales (exacto):** si $X_i\\sim N(\\mu_i,\\sigma_i^2)$ independientes → "
    "$S=\\sum X_i\\sim N\\left(\\sum\\mu_i,\\sum\\sigma_i^2\\right)$. "
    "⚠️ **Se suman las varianzas, NO los desvios.**\n\n"
    "**Combinacion lineal:** $Y=\\sum a_iX_i \\to$ media $\\sum a_i\\mu_i$, var $\\sum a_i^2\\sigma_i^2$.\n\n"
    "**n iguales:** S = n copias → $N(n\\mu,n\\sigma^2)$. Ej. consumo de 17 dias → "
    "$N(17\\mu,17\\sigma^2)$.\n\n"
    "**Variables no normales:** hace falta n ≥ 25-30 y Cv de la suma < 20% para aproximar a Normal.\n\n"
    "**Ej. combinado:** 3 mesas ($N(25,5^2)$) + 12 sillas ($N(9,2^2)$) → "
    "$W\\sim N(3\\cdot25+12\\cdot9,\\ 3\\cdot5^2+12\\cdot2^2)=N(183,123)$."
)

BAYES_CONTINUO_CONTENIDO = (
    "Patron recurrente: \"la moda pasa a X con media Y; ahora hay z unidades, ¿prob. de que sea "
    "[el escenario raro]?\" o \"pago mas de k, ¿prob. de accidente grave?\".\n\n"
    "**Con densidades (valor puntual):** "
    "$P(A\\mid x)=\\dfrac{f_A(x)P(A)}{f_A(x)P(A)+f_B(x)P(B)}$\n\n"
    "**Con colas (\"mas de k\"):** reemplazar f por $G(k)=P(X>k)$ de cada escenario. Si la "
    "evidencia es \"menos de k\", usar $F(k)$.\n\n"
    "**Caso \"fosforos\"** (una sola distribucion, umbral distinto por hipotesis): "
    "verosimilitud$_i$ = $F(\\text{umbral}_i)$ o $G(\\text{umbral}_i)$ de la MISMA distribucion "
    "para cada grupo/hipotesis.\n\n"
    "Pasos: (1) armar cada distribucion con sus parametros, (2) evaluar f(x), F(k) o G(k), "
    "(3) ponderar por la probabilidad previa, (4) Bayes."
)

PLANTILLAS = [
    ("1", "Normal: P(X>a) / P(a<X<b)", "z=(x-μ)/σ → tabla Φ. Restar acumuladas."),
    ("2", "Normal: hallar σ con un percentil", "z_p de tabla, σ=(x₀-μ)/z_p."),
    ("3", "Normal: fractil / \"valor superado el 20%\"", "x=μ+z_ασ. (superado 20% ⇒ α=0,80)"),
    ("4", "Normal: media de la cola (parcial)", "H(a)=μΦ(z)-σφ(z); E[X|X<a]=H/Φ."),
    ("5", "Exponencial / \"sin memoria\"", "G(x)=e^(-λx); condicional → solo el tramo nuevo."),
    ("6", "Weibull: riesgo / carga maxima", "F(x)=1-e^(-(x/α)^β); despejar x con F=r."),
    ("7", "Pareto: P(X>k), fractil, b de media+moda", "b=μ/(μ-δ); G(x)=(δ/x)^b."),
    ("8", "Uniforme: tiempo esperado / prob. en rango", "media=(a+b)/2; F lineal."),
    ("9", "Gumbel: extremo max/min, fractil", "elegir max vs min; usar F o G y su fractil."),
    ("10", "Poisson: \"mas de k eventos en t\"", "m=λt; 1-Σ acumulada."),
    ("11", "Gamma: tiempo para r fallas / demanda", "λ=μ/σ², r=μ²/σ²; via Poisson o Wilson-Hilferty."),
    ("12", "Suma/TCL: consumo de n dias, peso total", "N(Σμ,Σσ²); combinacion lineal a·X."),
    ("13", "Bayes continuo: ¿prob. del escenario raro?", "ponderar f(x), F(k) o G(k) por la previa."),
    ("14", "Teorica: ¿que distribucion y por que?", "nombrar modelo, formula, parametros, justificar."),
]

ERRORES_COMUNES = [
    "Sumar desvios en vez de varianzas en una suma/TCL.",
    "Confundir F (≤) con G (>): el \"riesgo\" es F, la \"confiabilidad\" es G.",
    "No convertir unidades de continuo (horas vs dias vs semana) en Poisson/Exponencial/Gamma.",
    "Olvidar interpretar el resultado (varias consignas dan puntos por la interpretacion).",
    "Usar Gumbel de Maximo para una rotura (es de minimos) o Pareto para algo que admite "
    "valores bajo la moda (es log-normal).",
    "En Pareto, el dominio empieza en δ: P(X<δ)=0.",
    "No redondear a 4 decimales hacia arriba como pide la consigna.",
]

# z de 0.00 a 3.09 -> Phi(z), igual a calculation/normal_table.py (tabla cátedra).
_Z_TABLE_ROWS = [
    (0.0, [.5000, .5040, .5080, .5120, .5160, .5199, .5239, .5279, .5319, .5359]),
    (0.1, [.5398, .5438, .5478, .5517, .5557, .5596, .5636, .5675, .5714, .5753]),
    (0.2, [.5793, .5832, .5871, .5910, .5948, .5987, .6026, .6064, .6103, .6141]),
    (0.3, [.6179, .6217, .6255, .6293, .6331, .6368, .6406, .6443, .6480, .6517]),
    (0.4, [.6554, .6591, .6628, .6664, .6700, .6736, .6772, .6808, .6844, .6879]),
    (0.5, [.6915, .6950, .6985, .7019, .7054, .7088, .7123, .7157, .7190, .7224]),
    (0.6, [.7257, .7291, .7324, .7357, .7389, .7422, .7454, .7486, .7517, .7549]),
    (0.7, [.7580, .7611, .7642, .7673, .7704, .7734, .7764, .7794, .7823, .7852]),
    (0.8, [.7881, .7910, .7939, .7967, .7995, .8023, .8051, .8078, .8106, .8133]),
    (0.9, [.8159, .8186, .8212, .8238, .8264, .8289, .8315, .8340, .8365, .8389]),
    (1.0, [.8413, .8438, .8461, .8485, .8508, .8531, .8554, .8577, .8599, .8621]),
    (1.1, [.8643, .8665, .8686, .8708, .8729, .8749, .8770, .8790, .8810, .8830]),
    (1.2, [.8849, .8869, .8888, .8907, .8925, .8944, .8962, .8980, .8997, .9015]),
    (1.3, [.9032, .9049, .9066, .9082, .9099, .9115, .9131, .9147, .9162, .9177]),
    (1.4, [.9192, .9207, .9222, .9236, .9251, .9265, .9279, .9292, .9306, .9319]),
    (1.5, [.9332, .9345, .9357, .9370, .9382, .9394, .9406, .9418, .9429, .9441]),
    (1.6, [.9452, .9463, .9474, .9484, .9495, .9505, .9515, .9525, .9535, .9545]),
    (1.7, [.9554, .9564, .9573, .9582, .9591, .9599, .9608, .9616, .9625, .9633]),
    (1.8, [.9641, .9649, .9656, .9664, .9671, .9678, .9686, .9693, .9699, .9706]),
    (1.9, [.9713, .9719, .9726, .9732, .9738, .9744, .9750, .9756, .9761, .9767]),
    (2.0, [.9772, .9778, .9783, .9788, .9793, .9798, .9803, .9808, .9812, .9817]),
    (2.1, [.9821, .9826, .9830, .9834, .9838, .9842, .9846, .9850, .9854, .9857]),
    (2.2, [.9861, .9864, .9868, .9871, .9875, .9878, .9881, .9884, .9887, .9890]),
    (2.3, [.9893, .9896, .9898, .9901, .9904, .9906, .9909, .9911, .9913, .9916]),
    (2.4, [.9918, .9920, .9922, .9925, .9927, .9929, .9931, .9932, .9934, .9936]),
    (2.5, [.9938, .9940, .9941, .9943, .9945, .9946, .9948, .9949, .9951, .9952]),
    (2.6, [.9953, .9955, .9956, .9957, .9959, .9960, .9961, .9962, .9963, .9964]),
    (2.7, [.9965, .9966, .9967, .9968, .9969, .9970, .9971, .9972, .9973, .9974]),
    (2.8, [.9974, .9975, .9976, .9977, .9977, .9978, .9979, .9979, .9980, .9981]),
    (2.9, [.9981, .9982, .9982, .9983, .9984, .9984, .9985, .9985, .9986, .9986]),
    (3.0, [.9987, .9987, .9987, .9988, .9988, .9989, .9989, .9989, .9990, .9990]),
]


def render_formulario_sidebar() -> str:
    st.header("Formulario / Reconocimiento")
    st.caption(
        "Consulta estatica y offline (sin IA): tabla de reconocimiento, formulas, "
        "plantillas de ejercicio, tabla Z y errores comunes del 2do parcial."
    )
    busqueda = st.text_input(
        "Buscar pistas del enunciado",
        placeholder='ej: "sin memoria", "rotura", "percentil", "media y moda"',
    )
    st.caption("Filtra la tabla de reconocimiento por coincidencia de texto.")
    return busqueda.strip().lower()


def render_formulario_main(busqueda: str = "") -> None:
    st.subheader("Formulario — 2do Parcial: continuas, Proceso de Poisson, TCL y Bayes")

    with st.expander("Como usar este formulario en el examen", expanded=False):
        st.markdown(
            "1. Lee que es la variable aleatoria (tiempo, peso, dinero, nro de fallas, "
            "maximo/minimo...).\n"
            "2. Identifica la distribucion con la tabla de reconocimiento.\n"
            "3. Saca los parametros a partir de los datos (media, moda, un percentil conocido).\n"
            "4. Escribe F(x) o G(x) y calcula la probabilidad / el fractil pedido.\n"
            "5. Interpreta el resultado en palabras."
        )

    st.markdown("### Tabla de reconocimiento — ¿qué distribución uso?")
    filtradas = DISTRIBUCIONES
    if busqueda:
        filtradas = [
            d for d in DISTRIBUCIONES
            if busqueda in d["pistas"].lower() or busqueda in d["nombre"].lower()
        ]
        if not filtradas:
            st.info("Sin coincidencias — mostrando todas las distribuciones.")
            filtradas = DISTRIBUCIONES

    st.table(
        {
            "Distribución": [d["nombre"] for d in filtradas],
            "Parámetros": [d["parametros"] for d in filtradas],
            "Pistas en la consigna": [d["pistas"] for d in filtradas],
        }
    )

    st.markdown("**Regla de oro de parámetros:**")
    st.markdown(REGLA_DE_ORO)

    with st.expander("Convenciones de la cátedra (F/G, fractil, Cv, constantes)"):
        st.markdown(CONVENCIONES)

    st.markdown("### Distribuciones continuas")
    for d in DISTRIBUCIONES[:8]:
        with st.expander(f"{d['nombre']}  ({d['parametros']})"):
            st.markdown(d["contenido"])

    st.markdown("### Proceso de Poisson")
    for d in DISTRIBUCIONES[8:]:
        with st.expander(f"{d['nombre']}  ({d['parametros']})"):
            st.markdown(d["contenido"])

    st.markdown("### Suma de variables / TCL")
    with st.expander("Suma de normales, combinación lineal, TCL", expanded=False):
        st.markdown(TCL_CONTENIDO)

    st.markdown("### Bayes con distribuciones continuas")
    with st.expander("Patrón Bayes continuo", expanded=False):
        st.markdown(BAYES_CONTINUO_CONTENIDO)

    st.markdown("### Las ~14 plantillas de ejercicio que se repiten")
    st.table(
        {
            "#": [p[0] for p in PLANTILLAS],
            "Patrón": [p[1] for p in PLANTILLAS],
            "Receta": [p[2] for p in PLANTILLAS],
        }
    )

    st.markdown("### Tabla Normal estándar Φ(z) = P(Z ≤ z)")
    st.caption(
        "Para z negativo: Φ(−z) = 1 − Φ(z). Fractiles usuales: z(0,90)=1,2816 · "
        "z(0,95)=1,6449 · z(0,975)=1,9600 · z(0,99)=2,3263."
    )
    with st.expander("Ver tabla Z completa (0.00 a 3.09)", expanded=False):
        cols = [".00", ".01", ".02", ".03", ".04", ".05", ".06", ".07", ".08", ".09"]
        st.table(
            {
                "z": [f"{z:.1f}" for z, _ in _Z_TABLE_ROWS],
                **{c: [f"{row[i]:.4f}" for _, row in _Z_TABLE_ROWS] for i, c in enumerate(cols)},
            }
        )

    st.markdown("### Errores que cuestan puntos")
    for err in ERRORES_COMUNES:
        st.markdown(f"- ⚠️ {err}")
