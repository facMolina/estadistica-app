"""Fichas canónicas por tópico para el modo Consultas Teóricas.

Cada ficha es la **fuente de verdad** de las fórmulas/método de un tema. El
answerer detecta el/los tópico(s) de la pregunta y antepone la(s) ficha(s) al
contexto del modelo, marcadas como autoritativas, para que la fórmula correcta
SIEMPRE esté frente al modelo sin depender del retrieval por coseno.

Notación de cátedra (la misma del MACHETE): F(x)=P(X≤x), G(x)=P(X≥x).
Las fórmulas de distribución son consistentes con las clases de modelo testeadas
(`models/**`); `tests/test_theory_accuracy.py` verifica esa coincidencia.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field

# Reutilizamos las señales fuertes de modelo del parser (discretos + Poisson).
try:
    from interpreter.nl_parser import STRONG_MODEL_PATTERNS
except Exception:  # pragma: no cover - import defensivo
    STRONG_MODEL_PATTERNS = {}


@dataclass(frozen=True)
class TopicCard:
    topic: str                       # clave canónica, ej. "GumbelMin"
    title: str                       # título legible, ej. "Gumbel del Mínimo"
    body: str                        # bloque markdown+LaTeX autoritativo
    keywords: list[str] = field(default_factory=list)  # patrones regex de detección


def _norm(text: str) -> str:
    """Minúsculas sin acentos, para matchear keywords con o sin tildes."""
    t = text.lower()
    t = unicodedata.normalize("NFKD", t)
    return "".join(c for c in t if not unicodedata.combining(c))


# ---------------------------------------------------------------------------
# Fichas — discretos
# ---------------------------------------------------------------------------

_CARDS: dict[str, TopicCard] = {}


def _add(card: TopicCard) -> None:
    _CARDS[card.topic] = card


_add(TopicCard(
    topic="Binomial", title="Binomial",
    keywords=[r"\bbinomial\b", r"\bbernoulli\b", r"\bn\s+ensayos\b", r"\bexito\b"],
    body=(
        "**Binomial** — n ensayos independientes, cada uno éxito (prob. p) o fracaso. "
        "Cuenta el nº de éxitos.\n"
        "- $P(X=r)=\\binom{n}{r}p^{r}(1-p)^{n-r}$\n"
        "- $E(X)=np$ · $V(X)=np(1-p)$.\n"
        "- n fijo y conocido; p constante; ensayos independientes."
    ),
))

_add(TopicCard(
    topic="Poisson", title="Poisson",
    keywords=[r"\bpoisson\b", r"a\s+razon\s+de", r"\beventos?\s+por\b", r"\bllegadas?\b",
              r"\btasa\b", r"\bocurrencias?\b"],
    body=(
        "**Poisson** — nº de eventos en un continuo (tiempo/espacio) fijo, con "
        "media $m=\\lambda t$.\n"
        "- $P(X=r)=\\dfrac{e^{-m}m^{r}}{r!}$\n"
        "- $E(X)=V(X)=m$.\n"
        "- Escalar la tasa a la ventana pedida y **cuidar unidades** "
        "(ej. $\\lambda=1$ cada 36 h, $t=$ 1 semana $=168$ h $\\Rightarrow m=168/36$)."
    ),
))

_add(TopicCard(
    topic="Pascal", title="Pascal (Binomial negativa)",
    keywords=[r"\bpascal\b", r"binomial\s+negativa", r"hasta\s+(el|la|lograr)\b.*exito",
              r"\br[-\s]?esimo\b"],
    body=(
        "**Pascal / Binomial negativa** — nº de ensayos hasta lograr el r-ésimo éxito.\n"
        "- $P(X=n)=\\binom{n-1}{r-1}p^{r}(1-p)^{n-r}$ (n = ensayos, n≥r)\n"
        "- $E(X)=r/p$ · $V(X)=r(1-p)/p^{2}$.\n"
        "- Es Tipo I de la familia de espera; con r=1 es Geométrica."
    ),
))

_add(TopicCard(
    topic="Hipergeometrico", title="Hipergeométrico",
    keywords=[r"hipergeometric", r"sin\s+reposicion", r"sin\s+reemplazo",
              r"\bpoblacion\s+finita\b"],
    body=(
        "**Hipergeométrico** — extracción SIN reposición de una población finita N "
        "con R éxitos; n extracciones.\n"
        "- $P(X=r)=\\dfrac{\\binom{R}{r}\\binom{N-R}{n-r}}{\\binom{N}{n}}$\n"
        "- $E(X)=nR/N$.\n"
        "- Sin reposición (si fuera con reposición → Binomial)."
    ),
))

_add(TopicCard(
    topic="Hiper-Pascal", title="Hiper-Pascal",
    keywords=[r"hiper[-\s]?pascal"],
    body=(
        "**Hiper-Pascal** — espera del r-ésimo éxito en muestreo sin reposición.\n"
        "- $P(X=n)=\\dfrac{r}{n}\\cdot\\dfrac{\\binom{R}{r}\\binom{N-R}{n-r}}{\\binom{N}{n}}$."
    ),
))

_add(TopicCard(
    topic="Multinomial", title="Multinomial",
    keywords=[r"\bmultinomial\b", r"\bk\s+categorias\b", r"varias\s+categorias"],
    body=(
        "**Multinomial** — n ensayos independientes, cada uno cae en una de k "
        "categorías con prob. $p_1,\\dots,p_k$ ($\\sum p_i=1$).\n"
        "- $P(r_1,\\dots,r_k)=\\dfrac{n!}{r_1!\\cdots r_k!}\\,p_1^{r_1}\\cdots p_k^{r_k}$, "
        "con $\\sum r_i=n$."
    ),
))

# ---------------------------------------------------------------------------
# Fichas — continuos (notación cátedra: F=P(X≤x), G=P(X≥x))
# ---------------------------------------------------------------------------

_add(TopicCard(
    topic="Normal", title="Normal",
    keywords=[r"\bnormal(es|mente)?\b", r"\bgauss", r"\bcampana\b", r"\bsimetrica\b",
              r"media\s+y\s+(desvio|desviacion)"],
    body=(
        "**Normal** $N(\\mu,\\sigma)$ — simétrica, moda=mediana=media=$\\mu$.\n"
        "- $z=(x-\\mu)/\\sigma$ · $P(X\\le x)=\\Phi(z)$ (buscar $\\Phi$ en la **tabla Z**).\n"
        "- Hallar $\\sigma$ con un percentil: $\\sigma=(x_0-\\mu)/z_p$.\n"
        "- $x_\\alpha=\\mu+z_\\alpha\\sigma$.\n"
        "⚠️ Estandarizar con $\\sigma$, NO con $\\sigma^{2}$."
    ),
))

_add(TopicCard(
    topic="LogNormal", title="Log-Normal",
    keywords=[r"log[-\s]?normal", r"logaritmo\s+normal", r"\bln\s*\(", r"sesgad",
              r"asimetr"],
    body=(
        "**Log-Normal** — $\\ln(X)$ es Normal con media $m$ y desvío $D$ (de los ln).\n"
        "- $P(X\\le x)=\\Phi\\!\\left(\\dfrac{\\ln x-m}{D}\\right)$.\n"
        "- De $\\mu,\\sigma$ de X: $D=\\sqrt{\\ln(1+(\\sigma/\\mu)^2)}$, $m=\\ln\\mu-D^2/2$.\n"
        "- Mediana $e^{m}$ · Moda $e^{m-D^2}$ · Media $e^{m+D^2/2}$ · $x_\\alpha=e^{m+z_\\alpha D}$.\n"
        "- Asimétrica positiva; admite valores bajo la moda (a diferencia de Pareto)."
    ),
))

_add(TopicCard(
    topic="Exponencial", title="Exponencial",
    keywords=[r"exponencial", r"sin\s+memoria", r"primera\s+falla", r"\bfusible\b",
              r"\bchip\b", r"tasa\s+constante"],
    body=(
        "**Exponencial** $(\\lambda)$ — tiempo hasta la **primera** falla al azar; "
        "sin memoria. Es Gamma con r=1.\n"
        "- $f(x)=\\lambda e^{-\\lambda x}$ · $G(x)=e^{-\\lambda x}$ · $F(x)=1-e^{-\\lambda x}$ (x≥0).\n"
        "- Media $1/\\lambda$ · Var $1/\\lambda^{2}$ · $Cv=100\\%$ · $x_\\alpha=-\\ln(1-\\alpha)/\\lambda$.\n"
        "- Sin memoria: $P(X>s+t\\mid X>s)=e^{-\\lambda t}$. λ es la tasa del proceso de "
        "Poisson — **cuidar unidades**."
    ),
))

_add(TopicCard(
    topic="Gamma", title="Gamma / Erlang",
    keywords=[r"\bgamma\b", r"\berlang\b", r"r[-\s]?esima\s+falla", r"para\s+r\s+eventos",
              r"media\s+y\s+varianza"],
    body=(
        "**Gamma / Erlang** $(\\lambda, r)$ — continuo necesario para r eventos Poisson; "
        "suma de r exponenciales.\n"
        "- $f(x)=\\dfrac{\\lambda^{r}x^{r-1}e^{-\\lambda x}}{(r-1)!}$ (x≥0).\n"
        "- De media y var: $\\lambda=\\mu/\\sigma^{2}$, $r=\\mu^{2}/\\sigma^{2}$.\n"
        "- $F$ por método cátedra (NO gamma incompleta de scipy): vía Poisson si r entero "
        "$F_\\Gamma(x)=1-\\sum_{k=0}^{r-1}e^{-\\lambda x}(\\lambda x)^k/k!$; "
        "vía Wilson-Hilferty si r grande/no entero "
        "$Z=3\\sqrt{r}\\big[(\\lambda x/r)^{1/3}-1+\\tfrac{1}{9r}\\big]$, $F=\\Phi(Z)$."
    ),
))

_add(TopicCard(
    topic="Weibull", title="Weibull",
    keywords=[r"weibull", r"\bdesgaste\b", r"\bfatiga\b", r"esfuerzo\s+de\s+materiales",
              r"riesgo\s+de\s+rotura", r"vida\s+util"],
    body=(
        "**Weibull** (escala $\\alpha$, forma $\\beta$) — desgaste/fatiga; resistencia de "
        "materiales; riesgo de rotura (es la EVT de mínimos para resistencia).\n"
        "- $G(x)=e^{-(x/\\alpha)^{\\beta}}$ (confiabilidad) · $F(x)=1-e^{-(x/\\alpha)^{\\beta}}$ (riesgo), x≥0.\n"
        "- Media $\\alpha\\,\\Gamma(1+1/\\beta)$ · $x_\\alpha=\\alpha(-\\ln(1-\\alpha))^{1/\\beta}$.\n"
        "- $\\beta=1\\Rightarrow$ Exponencial."
    ),
))

_add(TopicCard(
    topic="GumbelMin", title="Gumbel del Mínimo",
    keywords=[r"gumbel.*minim", r"minim.*gumbel", r"eslabon\s+mas\s+debil",
              r"resistencia.*(rotura|ruptura)", r"\bcorrea", r"\bcable",
              r"(rotura|ruptura|romp)\w*\s+(de\s+)?(la\s+|las\s+|el\s+|los\s+)?(correa|cable|material|pieza|fibra)",
              r"primer\s+elemento.*fall", r"sequia", r"caudal\s+minimo",
              r"vida\s+humana"],
    body=(
        "**Gumbel del Mínimo** (escala $\\alpha$, moda $\\mu$) — Fisher–Tippett **Tipo I** "
        "para el **mínimo** de un conjunto. Aplica a vida humana, sequía, caudal mínimo, "
        "y a la **resistencia / tiempo a la rotura** (el sistema falla en su **eslabón más "
        "débil**, el primer elemento en ceder → una correa/cable que se rompe por esfuerzo "
        "es un fenómeno de **mínimos**).\n"
        "- $G(x)=P(X\\ge x)=e^{-e^{+(x-\\mu)/\\alpha}}$ · $F(x)=1-G(x)$ (dominio $-\\infty,+\\infty$).\n"
        "- Exponente con signo **+**. Media $\\mu-\\alpha C$ ($C\\approx0{,}5772$) · "
        "$x_\\alpha=\\mu+\\alpha\\ln(-\\ln(1-\\alpha))$."
    ),
))

_add(TopicCard(
    topic="GumbelMax", title="Gumbel del Máximo",
    keywords=[r"gumbel.*maxim", r"maxim.*gumbel", r"inundacion", r"caudal\s+maximo",
              r"elongacion", r"alargamiento", r"viento\s+maximo", r"precipitacion\s+maxima"],
    body=(
        "**Gumbel del Máximo** (escala $\\alpha$, moda $\\mu$) — Fisher–Tippett **Tipo I** "
        "para el **máximo** de un conjunto. Aplica a inundación, caudal/viento máximo, y a "
        "la **elongación/alargamiento porcentual hasta la rotura** (el hilo se estira tanto "
        "como la fibra de **máxima** elongación). NO para la resistencia ni el tiempo a la "
        "rotura (eso es de mínimos).\n"
        "- $F(x)=P(X\\le x)=e^{-e^{-(x-\\mu)/\\alpha}}$ · $G(x)=1-F(x)$.\n"
        "- Exponente con signo **−**. Media $\\mu+\\alpha C$ ($C\\approx0{,}5772$) · "
        "$x_\\alpha=\\mu-\\alpha\\ln(-\\ln\\alpha)$."
    ),
))

_add(TopicCard(
    topic="Pareto", title="Pareto",
    keywords=[r"\bpareto\b", r"minimo\s+igual\s+a\s+la\s+moda", r"\bart\b", r"\bsalarios?\b",
              r"\bsiniestros?\b", r"pagan?\s+el\s+minimo", r"inventario\s+minimo"],
    body=(
        "**Pareto** (mínimo/moda $\\delta$, forma $b$) — el valor más habitual es el "
        "**mínimo**; seguros/ART, salarios, inventarios. NO admite valores por debajo de "
        "$\\delta$: $P(X<\\delta)=0$.\n"
        "- $f(x)=b\\delta^{b}/x^{b+1}$ · $G(x)=(\\delta/x)^{b}$ · $F(x)=1-(\\delta/x)^{b}$ (x≥δ).\n"
        "- De media y moda: $b=\\mu/(\\mu-\\delta)$. Media $b\\delta/(b-1)$ · "
        "$x_\\alpha=\\delta/(1-\\alpha)^{1/b}$ · $E[X\\mid X>k]=bk/(b-1)$."
    ),
))

_add(TopicCard(
    topic="Uniforme", title="Uniforme",
    keywords=[r"uniforme", r"igualmente\s+probable", r"entre\s+a\s+y\s+b"],
    body=(
        "**Uniforme** (a, b) — todo valor en [a,b] igualmente probable.\n"
        "- $f(x)=1/(b-a)$ · $F(x)=(x-a)/(b-a)$ (a≤x≤b).\n"
        "- Media $(a+b)/2$ · Var $(b-a)^{2}/12$ · $x_\\alpha=a+\\alpha(b-a)$."
    ),
))

# ---------------------------------------------------------------------------
# Fichas — temas-método (sin distribución única)
# ---------------------------------------------------------------------------

_add(TopicCard(
    topic="DatosAgrupados", title="Datos Agrupados",
    keywords=[r"datos\s+agrupados", r"tabla\s+de\s+frecuencias", r"marca\s+de\s+clase",
              r"\bhistograma\b", r"\bogiva\b", r"\bfractil\b", r"\bmediana\b"],
    body=(
        "**Datos Agrupados** — tabla de frecuencias con intervalos.\n"
        "- Marca de clase $C_i=(L_i+L_s)/2$ · Media $\\bar x=\\sum C_i f_{a_i}/n$.\n"
        "- Varianza muestral $S^{2}=\\sum (C_i-\\bar x)^{2}f_{a_i}/(n-1)$ · $CV=S/\\bar x$.\n"
        "- Fractil $\\alpha$: intervalo donde $F_{a_i}/n\\ge\\alpha$, con interpolación lineal."
    ),
))

_add(TopicCard(
    topic="ProbabilidadBayes", title="Probabilidad / Bayes",
    keywords=[r"\bbayes\b", r"probabilidad\s+total", r"\bcondicional\b", r"\bteorema\b",
              r"\bindependen", r"\bp\s*\(\s*a\b", r"union|interseccion"],
    body=(
        "**Probabilidad / Bayes** (eventos discretos).\n"
        "- Unión $P(A\\cup B)=P(A)+P(B)-P(A\\cap B)$ · Condicional $P(A\\mid B)=P(A\\cap B)/P(B)$.\n"
        "- Independencia $\\iff P(A\\cap B)=P(A)P(B)$.\n"
        "- Probabilidad total $P(E)=\\sum_i P(H_i)P(E\\mid H_i)$.\n"
        "- Bayes $P(H_k\\mid E)=\\dfrac{P(H_k)P(E\\mid H_k)}{\\sum_i P(H_i)P(E\\mid H_i)}$."
    ),
))

_add(TopicCard(
    topic="ProcesoPoisson", title="Proceso de Poisson",
    keywords=[r"proceso\s+de\s+poisson", r"tiempo\s+entre\s+llegadas",
              r"r[-\s]?esimo\s+arribo", r"interarrib"],
    body=(
        "**Proceso de Poisson** homogéneo con tasa $\\lambda$.\n"
        "- En tiempo t: $N(t)\\sim\\text{Poisson}(\\lambda t)$.\n"
        "- Tiempo entre llegadas: $T_k\\sim\\text{Exponencial}(\\lambda)$, independientes.\n"
        "- Tiempo del r-ésimo arribo: $S_r\\sim\\text{Gamma}(r,\\lambda)$.\n"
        "- **Cuidar unidades** al escalar $m=\\lambda t$."
    ),
))

_add(TopicCard(
    topic="Aproximaciones", title="Aproximaciones",
    keywords=[r"aproxima", r"\bcorreccion\s+por\s+continuidad\b", r"wilson[-\s]?hilferty"],
    body=(
        "**Aproximaciones** (condiciones de la cátedra).\n"
        "- Hipergeométrico → Binomial si $n/N\\le0{,}01$.\n"
        "- Binomial → Poisson si $p\\le0{,}005$, $m=np$.\n"
        "- Binomial → Normal si $np\\ge10$ y $n(1-p)\\ge10$ (corrección $\\pm0{,}5$).\n"
        "- Poisson → Normal si $m\\ge15$ (corrección $\\pm0{,}5$).\n"
        "- Gamma → Normal (Wilson-Hilferty): $Y=(X\\lambda/r)^{1/3}\\sim N(1-\\tfrac{1}{9r},\\tfrac{1}{9r})$."
    ),
))

_add(TopicCard(
    topic="TCL", title="TCL / Suma de variables",
    keywords=[r"\btcl\b", r"teorema\s+central", r"suma\s+de\s+variables",
              r"suma\s+de\s+(va|v\.a)", r"peso\s+total", r"carga\s+total"],
    body=(
        "**TCL / Suma de variables.**\n"
        "- $X_i$ iid con media $\\mu$, var $\\sigma^{2}$: $\\dfrac{S_n-n\\mu}{\\sigma\\sqrt n}\\to N(0,1)$.\n"
        "- Suma de normales independientes (exacto): "
        "$\\sum a_iX_i\\sim N\\!\\big(\\sum a_i\\mu_i,\\ \\sum a_i^{2}\\sigma_i^{2}\\big)$.\n"
        "⚠️ Se suman las **VARIANZAS**, nunca los desvíos. n copias iguales: $S\\sim N(n\\mu,n\\sigma^{2})$."
    ),
))

_add(TopicCard(
    topic="BayesContinuo", title="Bayes continuo",
    keywords=[r"bayes\s+continu", r"prob.*escenario.*densidad", r"posterior",
              r"verosimilitud"],
    body=(
        "**Bayes con distribuciones continuas.**\n"
        "- Con densidades (valor puntual): $P(A\\mid x)=\\dfrac{f_A(x)P(A)}{\\sum_j f_j(x)P(j)}$.\n"
        "- Con colas (\"más de k\"): reemplazar $f$ por $G(k)=P(X>k)$; si es \"menos de k\", por $F(k)$.\n"
        "- Pasos: armar cada distribución, evaluar $f$/$F$/$G$, ponderar por la previa, Bayes."
    ),
))


# ---------------------------------------------------------------------------
# Detección de tópico
# ---------------------------------------------------------------------------

def detect_topics(question: str, max_topics: int = 2) -> list[TopicCard]:
    """Devuelve las fichas más relevantes a la pregunta (0..max_topics).

    Combina las señales fuertes del parser (STRONG_MODEL_PATTERNS, sobre el texto
    en minúsculas) con las keywords propias de cada ficha (sobre texto sin acentos).
    """
    norm = _norm(question)
    scores: dict[str, int] = {}

    # 1) Señales fuertes del parser (discretos + Poisson): peso alto.
    for model, patterns in (STRONG_MODEL_PATTERNS or {}).items():
        if model not in _CARDS:
            continue
        for pat in patterns:
            if re.search(_norm(pat), norm):
                scores[model] = scores.get(model, 0) + 3
                break

    # 2) Keywords de cada ficha.
    for topic, card in _CARDS.items():
        for pat in card.keywords:
            if re.search(pat, norm):
                scores[topic] = scores.get(topic, 0) + 1

    if not scores:
        return []
    ranked = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
    return [_CARDS[t] for t, _ in ranked[:max_topics]]


def render_cards(cards: list[TopicCard]) -> str:
    """Bloque autoritativo para anteponer al contexto del answerer."""
    if not cards:
        return ""
    parts = [f"### {c.title}\n{c.body}" for c in cards]
    return "\n\n".join(parts)


def get_card(topic: str) -> TopicCard | None:
    return _CARDS.get(topic)


def all_cards() -> dict[str, TopicCard]:
    return dict(_CARDS)
