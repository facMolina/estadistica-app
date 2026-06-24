# Machete teórico — Estadística General

## Tema I — Datos agrupados

- Marca de clase: $C_i = \tfrac{L_i + L_s}{2}$.
- Media agrupada: $\bar{x} = \tfrac{\sum C_i f_{a_i}}{n}$.
- Varianza muestral: $S^2 = \tfrac{\sum (C_i - \bar{x})^2 f_{a_i}}{n-1}$.
- Coeficiente de variación: $CV = \tfrac{S}{\bar{x}}$.
- Frecuencia acumulada: $F_{a_i} = \sum_{j \le i} f_{a_j}$.
- Fractil $\alpha$: intervalo donde $F_{a_i}/n \ge \alpha$ con interpolación lineal.

## Tema II — Probabilidad

- $P(A \cup B) = P(A) + P(B) - P(A \cap B)$.
- Condicional: $P(A \mid B) = \tfrac{P(A \cap B)}{P(B)}$ si $P(B) > 0$.
- Probabilidad total: $P(E) = \sum_i P(H_i) P(E \mid H_i)$.
- Bayes: $P(H_k \mid E) = \tfrac{P(H_k) P(E \mid H_k)}{\sum_i P(H_i) P(E \mid H_i)}$.
- Independencia: $A, B$ indep. $\iff P(A \cap B) = P(A) P(B)$.

## Tema III — Modelos discretos

- Binomial: $P(X=r) = \binom{n}{r} p^r (1-p)^{n-r}$, $E(X) = np$, $V(X) = np(1-p)$.
- Poisson: $P(X=r) = \tfrac{e^{-m} m^r}{r!}$, $E = V = m$.
- Pascal: $P(X=n) = \binom{n-1}{r-1} p^r (1-p)^{n-r}$, $E = r/p$, $V = r(1-p)/p^2$.
- Hipergeométrico: $P(X=r) = \tfrac{\binom{R}{r}\binom{N-R}{n-r}}{\binom{N}{n}}$, $E = n R/N$.
- Hiper-Pascal: $P(X=n) = \tfrac{r}{n} P_h(r \mid N, R, n)$.
- Multinomial: $P(r_1,\ldots,r_k) = \tfrac{n!}{r_1! \cdots r_k!} \prod p_i^{r_i}$.

## Tema IV — Modelos continuos (2º parcial: tabla de reconocimiento)

Casi siempre dan **(a) la media** y **(b) un dato extra** (la moda, o "el X% está por
debajo de tal valor"). Con esos dos se sacan los parámetros:

- Normal + un percentil → estandarizar para hallar $\sigma$: $\sigma=(x_0-\mu)/z_p$.
- Pareto: media y moda → $b=\mu/(\mu-\delta)$.
- Gamma: media y varianza → $\lambda=\mu/\sigma^2$, $r=\mu^2/\sigma^2$.

Convenciones de la cátedra: **F(x) = P(X ≤ x)** (acumulada izquierda / riesgo en
fiabilidad). **G(x) = P(X > x)** (acumulada derecha / confiabilidad). Siempre
$F(x)+G(x)=1$. Fractil $x_\alpha$: $F(x_\alpha)=\alpha$. $Cv=\sigma/\mu\cdot100$
(representativa la media si $Cv<10\%$). $C$ = constante de Euler-Mascheroni ≈
**0,5772** (solo Gumbel); $\Gamma$ = función Gamma de Euler (Weibull).

| Distribución | Parámetros | Pistas en la consigna |
|---|---|---|
| Normal | μ, σ | se distribuye normalmente; simétrica; media + desvío; X% por encima/debajo de un valor |
| Log-Normal | m, D (de los ln) | asimetría fuerte; logaritmo normal; admite valores bajo la moda; montos/tiempos sesgados |
| Exponencial | λ | tiempo hasta la primera falla; al azar; sin memoria; tasa constante; fusible/chip |
| Weibull | α (escala), β (forma) | desgaste; fatiga; riesgo de rotura; esfuerzo de materiales; vida útil |
| Gumbel del mínimo | α (escala), μ (moda) | valor mínimo de un conjunto; vida humana; sequía; caudal/precipitación mínima |
| Gumbel del máximo | α (escala), μ (moda) | valor máximo; extremos; inundación; caudal máximo; rotura de correa; elongación máxima |
| Pareto | δ (moda/min), b (forma) | mínimo igual a la moda; salarios; ART/seguro pagan el mínimo; inventario mínimo |
| Uniforme | a, b | entre a y b igualmente probable; freno entre ms; tiempo en app entre minutos |
| Poisson (proceso) | m = λ·t | número de eventos en un continuo fijo; fallas por semana; llegadas por hora |
| Gamma / Erlang | λ (tasa), r (nro eventos) | continuo necesario para r eventos; tiempo hasta la r-ésima falla; Gamma con media y varianza |

### Normal

$z=(x-\mu)/\sigma$ · $P(X<x)=\Phi(z)$ → buscar $\Phi(z)$ en la **tabla Z** (no scipy).

| Media | Var | Moda=Mediana=μ | Asimetría | Fractil |
|---|---|---|---|---|
| μ | σ² | μ | 0 (simétrica) | $x_\alpha=\mu+z_\alpha\sigma$ |

Hallar σ con un percentil: si "el p% está por debajo de x₀" → $z_p$ de tabla,
$\sigma=(x_0-\mu)/z_p$. Si dan dos percentiles simétricos, μ es el punto medio.
Truco simetría: $P(\mu<X<x_{0,8})=0,8-0,5=0,30$. "Por encima de la media" = 0,5.
Expectativa parcial izquierda: $H(a)=\mu\Phi(z)-\sigma\varphi(z)$ ($\varphi$ = densidad
estándar). Media condicional $E[X\mid X<a]=H(a)/\Phi(z)$.
⚠️ Error común: usar σ² donde va σ al estandarizar.

### Log-Normal

m y D son media y desvío de los **ln(X)**. $P(X<x)=\Phi\left(\dfrac{\ln x-m}{D}\right)$.

| De μ, σ de X → parámetros | Media | Varianza | Moda | Mediana | Fractil |
|---|---|---|---|---|---|
| $D=\sqrt{\ln(1+(\sigma/\mu)^2)}$ ; $m=\ln\mu-D^2/2$ | $e^{m+D^2/2}$ | $e^{2m+D^2}(e^{D^2}-1)$ | $e^{m-D^2}$ | $e^m$ | $x_\alpha=e^{m+z_\alpha D}$ |

Si solo dan media y desvío de X, primero pasar a m y D.

### Exponencial

Tiempo hasta la **primera** falla al azar; tasa constante; "sin memoria". Es Gamma con r=1.

$f(x)=\lambda e^{-\lambda x}$ · $G(x)=e^{-\lambda x}$ · $F(x)=1-e^{-\lambda x}$ (x≥0)

| Media | Var | Cv | Moda | Mediana | Fractil |
|---|---|---|---|---|---|
| 1/λ | 1/λ² | 100% | 0 | $\ln2/\lambda$ | $x_\alpha=-\ln(1-\alpha)/\lambda$ |

Sin memoria: $P(X>s+t\mid X>s)=P(X>t)=e^{-\lambda t}$. λ es la **tasa** del proceso de
Poisson asociado: "1 falla cada 36 h" → λ=1/36 por hora. Cuidar las **unidades**.

### Weibull

Duración/rotura con desgaste o fatiga, esfuerzo de materiales, "riesgo de rotura".

$G(x)=e^{-(x/\alpha)^\beta}$ = confiabilidad · $F(x)=1-e^{-(x/\alpha)^\beta}$ = riesgo

| Media | Moda | Mediana | Fractil |
|---|---|---|---|
| $\alpha\Gamma(1+1/\beta)$ | $\alpha(1-1/\beta)^{1/\beta}$ si β>1, si no 0 | $\alpha(\ln2)^{1/\beta}$ | $x_\alpha=\alpha(-\ln(1-\alpha))^{1/\beta}$ |

Carga máx. para riesgo ≤ r: $x=\alpha(-\ln(1-r))^{1/\beta}$. β=1 ⇒ Exponencial.

### Gumbel del mínimo

El **mínimo** de un conjunto: vida humana, sequía, caudal/precipitación mínima.

$G(x)=P(X>x)=e^{-e^{(x-\mu)/\alpha}}$ (dominio $-\infty$ a $+\infty$)

| Media | Var | Moda | Mediana | Fractil |
|---|---|---|---|---|
| $\mu-\alpha C$ | $\pi^2\alpha^2/6$ | μ | $\mu+\alpha\ln(\ln2)$ | $x_\alpha=\mu+\alpha\ln(-\ln(1-\alpha))$ |

### Gumbel del máximo

El **máximo** / extremos: inundación, caudal máximo, rotura de correa, elongación máxima.

$F(x)=P(X\le x)=e^{-e^{-(x-\mu)/\alpha}}$

| Media | Var | Moda | Mediana | Fractil |
|---|---|---|---|---|
| $\mu+\alpha C$ | $\pi^2\alpha^2/6$ | μ | $\mu-\alpha\ln(\ln2)$ | $x_\alpha=\mu-\alpha\ln(-\ln\alpha)$ |

⚠️ Ojo: la rotura por esfuerzo es un fenómeno de **mínimos** (rompe el eslabón más
débil) → usar Gumbel del MÍNIMO o Weibull, no Máximo.

### Pareto

El valor más habitual es el **mínimo**; pagos de seguros/ART (pagan el mínimo),
salarios, inventarios mínimos. No admite valores por debajo de δ.

$f(x)=b\delta^b/x^{b+1}$ · $G(x)=(\delta/x)^b$ · $F(x)=1-(\delta/x)^b$ (x≥δ)

| De media y moda → b | Media | Moda | Mediana | Var | Fractil |
|---|---|---|---|---|---|
| $b=\mu/(\mu-\delta)$ | $b\delta/(b-1)$ | δ | $\delta\cdot2^{1/b}$ | $\delta^2b/((b-1)^2(b-2))$ | $x_\alpha=\delta/(1-\alpha)^{1/b}$ |

Media condicional: $E[X\mid X>k]=bk/(b-1)$ con k el umbral.

### Uniforme

"Entre a y b" con todo igualmente probable.

$f(x)=1/(b-a)$ · $F(x)=(x-a)/(b-a)$ (a≤x≤b)

| Media | Var | Fractil |
|---|---|---|
| $(a+b)/2$ | $(b-a)^2/12$ | $x_\alpha=a+\alpha(b-a)$ |

## Tema V — Proceso de Poisson

Nro de eventos/fallas en un continuo **fijo** t. $P(r)=e^{-m}m^r/r!$ con $m=\lambda\cdot t$
· **Media = Var = m**. P(al menos k) = $1-\sum_{r=0}^{k-1}P(r)$. Escalar m a la ventana
pedida: λ=1 cada 36 h y t=1 semana (168 h) → m=168/36=4,6667.

- Llegadas homogéneas con tasa $\lambda$: en tiempo $t$, $N(t) \sim \text{Poi}(\lambda t)$.
- Tiempos entre llegadas: $T_k \sim \text{Exp}(\lambda)$, independientes.
- Tiempo del $r$-ésimo arribo: $S_r \sim \text{Gamma}(r, \lambda)$.

### Gamma / Erlang

Continuo (tiempo) necesario para que ocurran **r** eventos Poisson; "Gamma con media
y varianza". Suma de r exponenciales con igual λ.

$f(x)=\lambda^r x^{r-1}e^{-\lambda x}/(r-1)!$ (x≥0)

| De media y var → parámetros | Media | Var | Moda |
|---|---|---|---|
| $\lambda=\mu/\sigma^2$ ; $r=\mu^2/\sigma^2$ | r/λ | r/λ² | $(r-1)/\lambda$ si r>1, si no 0 |

**Calcular P con Gamma (método de la cátedra, no la gamma incompleta de scipy):**

- **Vía Poisson** (r entero): $F_\Gamma(x)=P(\text{Poisson}(m=\lambda x)\ge r)=1-\sum_{k=0}^{r-1}e^{-\lambda x}(\lambda x)^k/k!$.
- **Vía Normal (Wilson-Hilferty)**, r grande o no entero: $Z=3\sqrt{r}\left[(\lambda x/r)^{1/3}-1+\dfrac{1}{9r}\right]$, luego $P(X\le x)=\Phi(Z)$.

Ejemplo verificado: $F_\Gamma(20; r=4, \lambda=0,3)=0,8488$.

## Tema VI — Aproximaciones

- Hipergeométrico $\to$ Binomial si $n/N \le 0.01$.
- Binomial $\to$ Poisson si $p \le 0.005$ con $m = np$.
- Binomial $\to$ Normal si $np \ge 10$ y $n(1-p) \ge 10$ (con corrección $\pm 0.5$).
- Poisson $\to$ Normal si $m \ge 15$ (con corrección $\pm 0.5$).
- Gamma $\to$ Normal (Wilson-Hilferty): $Y = (X\lambda/r)^{1/3} \sim N(1 - \tfrac{1}{9r}, \tfrac{1}{9r})$.

## Tema VII — Teorema Central del Límite / Suma de variables

- Si $X_1, \ldots, X_n$ iid con $E = \mu$, $V = \sigma^2$, entonces $S_n = \sum X_i$ satisface $\tfrac{S_n - n\mu}{\sigma\sqrt{n}} \xrightarrow{d} N(0,1)$.
- Regla práctica: $n \ge 30$ y $Cv$ de la suma $< 20\%$ para aproximar a Normal si las variables no son normales.
- Suma de normales (exacto), independientes: $\sum a_i X_i \sim N(\sum a_i \mu_i, \sum a_i^2 \sigma_i^2)$. ⚠️ Se suman las **varianzas**, NO los desvíos.
- n copias iguales: $S=N(n\mu,n\sigma^2)$. Ej. consumo de 17 días → $N(17\mu,17\sigma^2)$.
- Ejemplo combinado: 3 mesas ($N(25,5^2)$) + 12 sillas ($N(9,2^2)$) → $W\sim N(3\cdot25+12\cdot9,\ 3\cdot5^2+12\cdot2^2)=N(183,123)$.

## Tema VIII — Bayes con distribuciones continuas

Patrón recurrente: "la moda pasa a X con media Y; ahora hay z unidades, ¿prob. de
que sea [el escenario raro]?" o "pagó más de k, ¿prob. de accidente grave?".

- **Con densidades (valor puntual):** $P(A\mid x)=\dfrac{f_A(x)P(A)}{f_A(x)P(A)+f_B(x)P(B)}$
- **Con colas ("más de k"):** reemplazar f por $G(k)=P(X>k)$ de cada escenario. Si la evidencia es "menos de k", usar $F(k)$.
- **Caso "fósforos"** (una sola distribución, umbral distinto por hipótesis): verosimilitud$_i$ = $F(\text{umbral}_i)$ o $G(\text{umbral}_i)$ de la MISMA distribución para cada grupo/hipótesis.
- Pasos: (1) armar cada distribución con sus parámetros, (2) evaluar f(x), F(k) o G(k), (3) ponderar por la probabilidad previa, (4) Bayes.

## Errores que cuestan puntos (2º parcial)

- Sumar desvíos en vez de varianzas en una suma/TCL.
- Confundir F (≤) con G (>): el "riesgo" es F, la "confiabilidad" es G.
- No convertir unidades de continuo (horas vs días vs semana) en Poisson/Exponencial/Gamma.
- Olvidar interpretar el resultado (varias consignas dan puntos por la interpretación).
- Usar Gumbel de Máximo para una rotura (es de mínimos) o Pareto para algo que admite valores bajo la moda (es log-normal).
- En Pareto, el dominio empieza en δ: P(X<δ)=0.
- No redondear a 4 decimales hacia arriba (medio hacia arriba, 5º dígito ≥5 sube) como pide la consigna.

## Tabla Normal estándar Φ(z) = P(Z ≤ z)

Para z negativo: Φ(−z) = 1 − Φ(z). Fractiles usuales: z(0,90)=1,2816 · z(0,95)=1,6449
· z(0,975)=1,9600 · z(0,99)=2,3263. Tabla completa (z de 0,00 a 3,09) en
`calculation/normal_table.py` y en el modo "Formulario / Reconocimiento" de la app.
