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

## Tema IV — Modelos continuos

- Normal: $f(x) = \tfrac{1}{\sigma \sqrt{2\pi}} e^{-\tfrac{(x-\mu)^2}{2\sigma^2}}$; estandarización $Z = \tfrac{x-\mu}{\sigma}$.
- Log-Normal: $Y = \ln X \sim N(m, D)$.
- Exponencial: $f(x) = \lambda e^{-\lambda x}$, $E = 1/\lambda$, $V = 1/\lambda^2$.
- Gamma/Erlang: $f(x) \propto x^{r-1} e^{-\lambda x}$, $E = r/\lambda$, $V = r/\lambda^2$.
- Weibull: $F(x) = 1 - e^{-(x/\beta)^\omega}$.
- Gumbel Max/Min: valores extremos, $F = e^{-e^{-z}}$ o dual.
- Pareto: $F(x) = 1 - (\theta/x)^b$, $x \ge \theta$, $E = b\theta/(b-1)$ si $b>1$.
- Uniforme: $f(x) = 1/(b-a)$ en $[a,b]$, $E = (a+b)/2$, $V = (b-a)^2/12$.

## Tema V — Proceso de Poisson

- Llegadas homogéneas con tasa $\lambda$: en tiempo $t$, $N(t) \sim \text{Poi}(\lambda t)$.
- Tiempos entre llegadas: $T_k \sim \text{Exp}(\lambda)$, independientes.
- Tiempo del $r$-ésimo arribo: $S_r \sim \text{Gamma}(r, \lambda)$.

## Tema VI — Aproximaciones

- Hipergeométrico $\to$ Binomial si $n/N \le 0.01$.
- Binomial $\to$ Poisson si $p \le 0.005$ con $m = np$.
- Binomial $\to$ Normal si $np \ge 10$ y $n(1-p) \ge 10$ (con corrección $\pm 0.5$).
- Poisson $\to$ Normal si $m \ge 15$ (con corrección $\pm 0.5$).
- Gamma $\to$ Normal (Wilson-Hilferty): $Y = (X\lambda/r)^{1/3} \sim N(1 - \tfrac{1}{9r}, \tfrac{1}{9r})$.

## Tema VII — Teorema Central del Límite

- Si $X_1, \ldots, X_n$ iid con $E = \mu$, $V = \sigma^2$, entonces $S_n = \sum X_i$ satisface $\tfrac{S_n - n\mu}{\sigma\sqrt{n}} \xrightarrow{d} N(0,1)$.
- Regla práctica: $n \ge 30$ para aproximación aceptable.
- Suma de normales independientes: $\sum a_i X_i \sim N(\sum a_i \mu_i, \sum a_i^2 \sigma_i^2)$.
