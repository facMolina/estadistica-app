# Contexto del Proyecto: Calculadora de Estadistica con Paso a Paso

Ultima actualizacion: 2026-04-10

---

## Que es este proyecto

Una aplicacion en Python para resolver ejercicios de Estadistica General (materia de UADE, Ing. Sergio Anibal Dopazo) mostrando el **desarrollo completo paso a paso** de cada calculo. Tiene dos fases:

1. **Fase 1 - CLI** (`main.py`): El usuario describe su problema en texto libre o indica un ejercicio de la guia. La app usa la **API de Claude** para interpretar el enunciado, identificar el modelo de probabilidad correcto y extraer los parametros. Si falta info, hace preguntas guiadas. Al confirmar, lanza la interfaz web.

2. **Fase 2 - Web** (`app_streamlit.py`): Interfaz Streamlit que muestra:
   - Paso a paso del calculo con **3 niveles de detalle** (maximo, intermedio, formula+resultado) controlados por un dropdown
   - Graficos interactivos (Plotly): poligono de probabilidad, acumuladas F(r) y G(r)
   - Tabla completa de la distribucion: r, P(r), F(r), G(r), H(r), J(r) — descargable CSV
   - Caracteristicas del modelo (esperanza, varianza, desvio, moda, mediana, CV, asimetria, kurtosis) con paso a paso expandible

---

## Fuentes de informacion (solo estas, no se deduce nada extra)

Todos los archivos estan en `/Users/facunmolina/Documents/ESTADISTICA/`:

### Teoria (carpeta TEORIA/)
| Archivo | Contenido |
|---------|-----------|
| 0 - Caratula e Indice.pdf | Indice general |
| 1 - Procesamiento de Datos.pdf | Tablas de frecuencia, media, varianza, CV, mediana, fractiles |
| 2 - Teoria de la Probabilidad.pdf | P(A), condicional, Bayes, independencia |
| 3 - Distribuciones Discretos.pdf | Binomial, Pascal, Hipergeometrico, Hiper-Pascal, Multinomial |
| 4 - Distribuciones Continuos.pdf | Normal, Log-Normal, Exponencial, Weibull, Gumbel, Pareto, Uniforme |
| 5 - Proceso de Poisson.pdf | Poisson, Gamma/Erlang, Exponencial (como caso particular) |
| 6 - Aproximaciones y TCL.pdf | Aprox. Hiper→Binom, Binom→Normal, Binom→Poisson, Poisson→Normal, TCL |
| E&G - Diagramas y Conteo.pdf | Material adicional de diagramas y conteo |

### Guia de ejercicios
Archivo: `Guia Problemas Estadística General - Probabilidad y Estadística - UADE (1).pdf`
- 36 paginas, 7 temas, ~170 ejercicios, todos con respuesta
- Tema I (pag 1-3): Procesamiento de Datos — 5 ejercicios
- Tema II (pag 4-8): Teoria de la Probabilidad — 31 ejercicios
- Tema III (pag 9-14): Discretas (Bernoulli/Hipergeometrico) — 33 ejercicios
- Tema IV (pag 15-19): Continuas especiales (Exponencial, Weibull, Gumbel, Pareto, Uniforme) — 27 ejercicios
- Tema V (pag 20-24): Normal y Log-Normal — 27 ejercicios
- Tema VI (pag 25-31): Poisson, Exponencial, Gamma — 40 ejercicios
- Ejemplo combinando modelos (pag 32) — 1 ejercicio
- Tema VII (pag 33-36): Suma de variables / TCL — 9 ejercicios

---

## Arquitectura general

```
Fase 1 (CLI - main.py)              Fase 2 (Web - app_streamlit.py)
        |                                     |
 Usuario describe                    Streamlit muestra:
 problema en texto  ---> Claude API   - Paso a paso (3 niveles de detalle)
        |                interpreta   - Graficos (Plotly)
 Si falta info,          y extrae     - Tabla de distribucion completa
 pregunta guiada         modelo +     - Caracteristicas del modelo
        |                params       - Aproximaciones aplicables
 Confirma modelo ---> config.json --> |
```

### Dos modos de entrada en la CLI

- **Modo A (texto libre)**: El usuario escribe el problema. Claude API lo interpreta, devuelve JSON con modelo, parametros, query. Si falta info pregunta. Se confirma y lanza Streamlit.
- **Modo B (ejercicio de la guia)**: El usuario escribe "tema III ejercicio 8". La app lee el enunciado del PDF, lo envia a Claude API, muestra interpretacion, confirma y resuelve.

---

## Estructura del proyecto

Ubicacion: `/Users/facunmolina/Documents/ESTADISTICA/APP/`

```
APP/
|-- app_streamlit.py            # Entry point Streamlit (Fase 2)
|-- main.py                     # Entry point CLI (Fase 1) [PENDIENTE]
|-- requirements.txt            # Dependencias Python
|-- .env                        # ANTHROPIC_API_KEY [PENDIENTE]
|-- .venv/                      # Virtual environment (ya creado)
|
|-- config/
|   |-- settings.py             # Constantes globales, rutas, niveles de detalle
|   |-- model_catalog.py        # Registro de modelos [PENDIENTE]
|
|-- interpreter/                # [TODO PENDIENTE]
|   |-- claude_client.py        # Wrapper API Anthropic
|   |-- problem_parser.py       # Loop de conversacion CLI
|   |-- system_prompt.py        # Prompt con todos los modelos/temas
|
|-- data_processing/            # Tema I [TODO PENDIENTE]
|   |-- frequency_table.py      # Tablas de frecuencia
|   |-- descriptive_stats.py    # Media, varianza, desvio, CV
|   |-- grouped_data.py         # Datos agrupados en intervalos
|
|-- probability/                # Tema II [TODO PENDIENTE]
|   |-- basic_probability.py    # P(A), P(AuB), P(AnB)
|   |-- conditional.py          # P(A/B), independencia
|   |-- bayes.py                # Bayes, probabilidad total
|
|-- models/
|   |-- base.py                 # Clases abstractas DiscreteModel, ContinuousModel [HECHO]
|   |-- discrete/
|   |   |-- binomial.py         # [HECHO - completo con paso a paso]
|   |   |-- pascal.py           # [PENDIENTE]
|   |   |-- hypergeometric.py   # [PENDIENTE]
|   |   |-- hiper_pascal.py     # [PENDIENTE]
|   |   |-- poisson.py          # [PENDIENTE]
|   |   |-- multinomial.py      # [PENDIENTE]
|   |-- continuous/             # [TODO PENDIENTE]
|   |   |-- normal.py
|   |   |-- normal_standard.py
|   |   |-- log_normal.py
|   |   |-- exponential.py
|   |   |-- gamma_erlang.py
|   |   |-- weibull.py
|   |   |-- uniform.py
|   |   |-- gumbel_min.py
|   |   |-- gumbel_max.py
|   |   |-- pareto.py
|
|-- calculation/
|   |-- step_types.py           # Dataclasses Step, CalcResult [HECHO]
|   |-- step_engine.py          # StepBuilder [HECHO]
|   |-- combinatorics.py        # C(n,r), factorial [HECHO]
|   |-- statistics_common.py    # F, G, H, J, tabla completa, formato [HECHO]
|
|-- approximations/             # [TODO PENDIENTE]
|   |-- approx_engine.py
|   |-- hyper_to_binomial.py
|   |-- binomial_to_normal.py
|   |-- binomial_to_poisson.py
|   |-- poisson_to_normal.py
|   |-- gamma_to_normal.py
|   |-- mermoz.py
|   |-- fisher.py
|   |-- tcl.py
|
|-- display/
|   |-- latex_renderer.py       # LaTeX strings [HECHO]
|   |-- table_builder.py        # DataFrame para tablas [HECHO]
|   |-- graph_builder.py        # Graficos Plotly [HECHO]
|
|-- ui/
|   |-- components/
|   |   |-- detail_selector.py  # Dropdown nivel detalle [HECHO]
|   |   |-- step_display.py     # Renderiza pasos con expandibles [HECHO]
|   |   |-- graph_panel.py      # Panel graficos [HECHO]
|   |   |-- table_panel.py      # Panel tabla + CSV [HECHO]
|   |   |-- summary_panel.py    # Panel caracteristicas [HECHO]
|   |   |-- approx_panel.py     # Panel aproximaciones [PENDIENTE]
|   |   |-- freq_table_panel.py # Panel Tema I [PENDIENTE]
|   |   |-- probability_panel.py# Panel Tema II [PENDIENTE]
|
|-- guide_index/                # [TODO PENDIENTE]
|   |-- exercise_parser.py
|   |-- pdf_reader.py
|   |-- exercise_catalog.py
```

---

## Que esta HECHO (Sprints 1 y 4)

### Sprint 1 - Cimientos (completado 2026-04-08)
Archivos creados y testeados:
- `calculation/step_types.py`: Dataclasses `Step` y `CalcResult`. Cada Step tiene `detail_level_min` (1=siempre, 2=intermedio+, 3=solo maximo). CalcResult tiene metodo `get_steps_for_level(n)` que filtra recursivamente.
- `calculation/step_engine.py`: `StepBuilder` — patron builder para construir arboles de pasos anidados. Metodos: `add_step()`, `add_substep()`, `begin_substeps()/end_substeps()`, `merge_result()`, `build()`.
- `calculation/combinatorics.py`: `comb(n,r)` y `factorial(n)` con `@lru_cache`. `comb_with_steps(n,r)` devuelve CalcResult con desarrollo de factoriales.
- `calculation/statistics_common.py`: Funciones genericas para cualquier distribucion discreta: `compute_cdf_left_discrete`, `compute_cdf_right_discrete`, `compute_partial_expectation_left/right`, `compute_truncated_mean_left/right/two_sided`, `find_mode_discrete`, `find_median_discrete`, `build_full_table_discrete`, `format_number`, `format_fraction`.
- `models/base.py`: Clases abstractas `DiscreteModel` y `ContinuousModel` con interfaz completa (probability, cdf_left, cdf_right, mean, variance, std_dev, mode, median, cv, skewness, kurtosis, partial_expectation_left, latex_formula, full_table, all_characteristics).
- `config/settings.py`: Constantes (EULER_MASCHERONI, PI, niveles de detalle, EPSILON, MAX_SUMMATION_TERMS, rutas a TEORIA/ y guia PDF).

### Sprint 4 - Binomial + UI Streamlit (completado 2026-04-08)

**Modelo Binomial** (`models/discrete/binomial.py`):
- Implementa DiscreteModel completo
- Constructor: `Binomial(n, p)` — valida n>=1 y 0<=p<=1
- Todos los metodos con paso a paso en 3 niveles de detalle:
  - `probability(r)`: P(r) = C(n,r) * p^r * (1-p)^(n-r)
  - `cdf_left(r)`: F(r) = sum P(x) para x=0..r
  - `cdf_right(r)`: G(r) = sum P(x) para x=r..n
  - `mean()`: E(r) = n*p
  - `variance()`: V(r) = n*p*(1-p)
  - `std_dev()`: sigma = sqrt(n*p*(1-p))
  - `mode()`: encuentra Mo en [n*p-(1-p), n*p+p]
  - `median()`: Me = P.E.(n*p), verificado con F(Me-1)<=0.5 y F(Me)>=0.5
  - `cv()`: Cv = sigma/mu * 100
  - `skewness()`: As = (1-2p) / sqrt(n*p*(1-p)) + interpretacion
  - `kurtosis()`: Ku = 3 + (1-6p(1-p)) / (n*p*(1-p)) + interpretacion
  - `partial_expectation_left(r)`: H(r) = sum x*P(x) para x=0..r
  - `full_table()`: tabla completa [r, P(r), F(r), G(r), H(r), J(r)]

**Verificado contra la guia de ejercicios (todos coinciden):**
- Gb(3/10;0.25) = 0.4744
- Fb(4/12;0.45) = 0.3044
- Gb(10/14;0.75) = 0.7415
- Fb(2/7;0.15) = 0.9262
- Fb(8/11;0.90) = 0.0896
- Fb(2/15;0.10) = 0.8159
- Pb(2/15;0.10) = 0.2669

**Interfaz Streamlit** (`app_streamlit.py`):
- Sidebar: selector de modelo, parametros (n, p), tipo de consulta (P(r), F(r), G(r), rango, analisis completo), dropdown de detalle, formula LaTeX
- Tab "Calculo Paso a Paso": renderiza steps segun nivel, con st.expander para sub-pasos
- Tab "Caracteristicas": tabla resumen expandible con paso a paso por fila
- Tab "Tabla de Distribucion": DataFrame completo, descargable CSV
- Tab "Graficos": poligono de probabilidad (stem plot), F(r) y G(r) (step functions), interactivos Plotly

**Componentes UI creados:**
- `ui/components/detail_selector.py`: dropdown con 3 opciones
- `ui/components/step_display.py`: renderiza CalcResult con profundidad recursiva
- `ui/components/graph_panel.py`: 3 graficos Plotly (probabilidad, F, G)
- `ui/components/table_panel.py`: DataFrame + boton CSV
- `ui/components/summary_panel.py`: lista de caracteristicas con expandibles

**Display:**
- `display/latex_renderer.py`: genera string LaTeX de un Step
- `display/table_builder.py`: convierte lista de dicts a DataFrame pandas
- `display/graph_builder.py`: `build_probability_polygon()` (stem plot con linea punteada) y `build_cdf_plot()` (step function)

---

## Como ejecutar lo que ya esta hecho

```bash
cd /Users/facunmolina/Documents/ESTADISTICA/APP

# Activar virtual environment
source .venv/bin/activate

# Lanzar Streamlit
streamlit run app_streamlit.py

# Se abre en http://localhost:8501
```

En la interfaz web:
1. En la sidebar, elegir parametros: n y p
2. Elegir tipo de consulta: P(r=valor), F(r), G(r), rango P(A<=r<=B), o analisis completo
3. Elegir nivel de detalle: "Maximo detalle" (default), "Detalle intermedio", "Formula y resultado"
4. Ver los 4 tabs: Calculo Paso a Paso, Caracteristicas, Tabla, Graficos

---

## Que queda PENDIENTE (orden de sprints)

### Sprint 5: Modelos discretos restantes
- Pascal: P(n) = C(n-1,r-1) * p^r * (1-p)^(n-r) — params: r, p — dominio: r <= n <= inf
- Hipergeometrico: P(r) = C(R,r)*C(N-R,n-r) / C(N,n) — params: N, R, n — dominio: max(0,n-(N-R)) <= r <= min(n,R)
- Hiper-Pascal: P(n) = (r/n)*P_h(r/n;N;R) — params: r, N, R — dominio: r <= n <= (N-R+r)
- Poisson: P(r) = e^(-m)*m^r / r! — params: lambda, t (m=lambda*t) — dominio: 0 <= r <= inf
- Multinomial: Extension de Binomial para multiples categorias
- Integrar todos en el selector de modelo de app_streamlit.py
- Tests: Tema III ej9 Pascal, ej13 Hipergeometrico

### Sprint 6: Modelos continuos (10 modelos)
- Normal, Normal Estandar, Log-Normal, Exponencial, Gamma/Erlang, Weibull, Uniforme, Gumbel Min, Gumbel Max, Pareto
- Usar scipy.stats para CDF numerica, mostrando paso a paso la transformacion (ej: estandarizacion Z para Normal)
- Adaptar app_streamlit.py para soportar modelos continuos (input float en vez de int, densidad en vez de probabilidad)
- Tests: Tema IV (Exponencial, Weibull, Pareto), Tema V (Normal, Log-Normal)

### Sprint 7: Aproximaciones + TCL
- Motor de aproximaciones: verificar condiciones y aplicar
- Hipergeometrico → Binomial (condicion: n/N <= 0.01, p=R/N)
- Binomial → Normal (condicion: np>=10 AND n(1-p)>=10, correccion continuidad +-0.5)
- Binomial → Poisson (condicion: p <= 0.005, m=np)
- Poisson → Normal (condicion: m>=15, correccion +-0.5)
- Gamma → Normal (Wilson-Hilferty)
- Criterio de Mermoz, Fisher, Paulson, Wise
- TCL: suma de variables independientes → Normal
- Tab "Aproximaciones" en Streamlit
- Tests: Tema VI ej15, Tema VII ej4

### Sprint 8: CLI con Claude API
- System prompt con todos los 7 temas, modelos y condiciones
- Wrapper Anthropic SDK
- Loop de conversacion: texto → JSON → validacion → confirmacion → lanzar Streamlit
- main.py como entry point

### Sprint 9: Modo B - Ejercicios de la guia
- Indice de ~170 ejercicios con mapeo a paginas del PDF
- Parser "tema X ej Y" con variantes
- Lector de PDF (PyMuPDF)
- Integracion en main.py: detectar si input es referencia o texto libre

### Sprint 2 (pospuesto): Tema I - Procesamiento de Datos
- Tablas de frecuencia (absoluta, relativa, acumulada)
- Marca de clase, histograma, ojiva
- Media, varianza (Sn y Sn-1), desvio, CV, mediana, moda, fractiles
- Tests: Tema I ej1, ej2, ej4

### Sprint 3 (pospuesto): Tema II - Teoria de la Probabilidad
- P(A), complemento, union, interseccion
- Condicional P(A/B), independencia
- Bayes, probabilidad total
- Tests: Tema II ej2 (Paradoja Bertrand), ej25 (Bayes)

### Sprint 10: Pulido e integracion
- Testing completo contra todos los ejercicios de la guia
- Edge cases (dominios infinitos, overflow factoriales grandes)
- UX: mensajes claros, manejo de errores

---

## Mecanismo clave: Motor de paso a paso

Cada calculo genera un arbol de `Step` con campo `detail_level_min`:

| detail_level_min | Se muestra en          | Ejemplo                                        |
|------------------|------------------------|-------------------------------------------------|
| 1                | Siempre                | P(r=1) = C(R,r)*C(N-R,n-r)/C(N,n) = 0.5385   |
| 2                | Intermedio y Maximo    | P(r=1) = 7*7/91 = 49/91 = 0.5385              |
| 3                | Solo Maximo            | C(7,1) = 7!/(1!*6!) = 5040/(1*720) = 7        |

Los Steps pueden tener `sub_steps` (arbol), y la UI usa `st.expander` para desplegar sub-calculos. El dropdown en la sidebar filtra que pasos se muestran.

Flujo: `StepBuilder` → agrega pasos con `add_step(level_min=N)` → `build()` devuelve `CalcResult` → `CalcResult.get_steps_for_level(N)` filtra → UI renderiza.

---

## Modelos: formulas y caracteristicas (referencia completa)

### Discretos (Temas III y VI)

**Binomial** [HECHO]: P(r) = C(n,r)*p^r*(1-p)^(n-r) | E=n*p | V=n*p*(1-p) | As=(1-2p)/sqrt(npq) | Ku=3+(1-6pq)/(npq) | H=n*p*Fb(r-1/n-1;p)

**Pascal**: P(n) = C(n-1,r-1)*p^r*(1-p)^(n-r) | E=r/p | V=r*(1-p)/p^2 | As=(2-p)/sqrt(r(1-p)) | Relacion: P_pa=(r/n)*P_b

**Hipergeometrico**: P(r) = C(R,r)*C(N-R,n-r)/C(N,n) | E=n*R/N | V=n*(R/N)*(1-R/N)*(N-n)/(N-1) | H=n*(R/N)*Fh(r-1/n-1;N-1;R-1)

**Hiper-Pascal**: P(n) = (r/n)*P_h(r/n;N;R) | E=r*(N+1)/(R+1) | Relacion con Hipergeometrico

**Poisson**: P(r) = e^(-m)*m^r/r! | E=m | V=m | As=1/sqrt(m) | Ku=3+1/m | H=m*F(r-1/m)

**Gamma/Erlang**: f(x) = [lambda^r * x^(r-1) * e^(-lambda*x)] / (r-1)! | E=r/lambda | V=r/lambda^2 | Relacion con Poisson y Chi-cuadrado

### Continuos (Temas IV y V)

**Normal**: f(x) con params mu, sigma | E=mu | V=sigma^2 | As=0 | Ku=3 | Estandarizacion Z=(x-mu)/sigma

**Log-Normal**: params m, D | E=e^(m+D^2/2) | Me=e^m | Mo=e^(m-D^2)

**Exponencial**: f(x)=lambda*e^(-lambda*x) | E=1/lambda | V=1/lambda^2 | As=2 | Ku=9 | Caso particular Gamma r=1

**Weibull**: params beta, omega | E=beta*Gamma(1+1/omega) | Caso omega=1 → Exponencial

**Gumbel Min/Max**: params beta, theta | Euler-Mascheroni C=0.5772 | V=pi^2/6*beta^2

**Pareto**: params theta, b | E=b*theta/(b-1) si b>1 | V solo si b>2

**Uniforme**: params a, b | E=(a+b)/2 | V=(b-a)^2/12 | As=0 | Ku=1.8

### Aproximaciones (Tema de Aproximaciones y TCL)

| De | A | Condicion |
|----|---|-----------|
| Hipergeometrico | Binomial | n/N <= 0.01, p=R/N |
| Binomial | Normal | np>=10 AND n(1-p)>=10, correccion +-0.5 |
| Binomial | Poisson | p<=0.005, m=np |
| Poisson | Normal | m>=15, correccion +-0.5 |
| Gamma | Normal | Wilson-Hilferty |
| Binomial | Mermoz | Cuando ni Normal ni Poisson aplican |

---

## Dependencias

Archivo: `APP/requirements.txt`
```
anthropic>=0.40.0
streamlit>=1.40.0
plotly>=5.24.0
scipy>=1.14.0
numpy>=2.0.0
python-dotenv>=1.0.0
PyMuPDF>=1.24.0
```

Virtual environment creado en `APP/.venv/` con Python 3.13.6.

---

## Verificacion: ejercicios de la guia con respuesta conocida

Estos son los tests clave para validar que cada modelo funciona correctamente:

**Tema I**: Ej1 → media=6.46%, Sn=2.80, CV=43.32% | Ej2 → media=49300lt, mediana=48717.95 | Ej4 → media=11.22min, CV=5.30%

**Tema II**: Ej1 → P(ambas blancas)=0.49 | Ej2 (Bertrand) → 2/3 | Ej25 (Bayes) → 0.7983

**Tema III**: Ej5 → Gb(3/10;0.25)=0.4744, Fb(4/12;0.45)=0.3044 | Ej8 → Fb(2/15;0.10)=0.8159 | Ej9 (Pascal) → Fpa(12/5;0.42)=0.6175 | Ej12 (Pascal) → P(n<=8)=0.4967

**Tema IV**: Ej6 (Exp) → media=100m | Ej7 (Weibull) → 22.29hs | Ej15 (Pareto) → F(0.10)=78228.37 | Ej20 (Pareto) → Me=575.55

**Tema V**: Ej1 (Normal) → P(x<24000)=94.52% | Ej2 (Normal) → P(x>840)=2.28% | Ej7 (LN) → P(x>140)=28.75%

**Tema VI**: Ej1 (Poisson) → P(r=0)=0.0067 | Ej13 (Gamma) → P(x<150)=44.22% | Ej15 → Fg(20/4;0.3)=Gpo(4/6)=0.8488 | Ej19 (Gamma) → P(>60)=5.75%

**Tema VII**: Ej1 (TCL) → P(costo<3)=0.2288 | Ej4 → tanque=10762.64lt | Ej9 → max 145 cajas

---

## Decisiones de diseno tomadas

1. **Texto libre + Claude API**: La entrada principal es texto natural, interpretado por la API de Claude. Si falta info, se hacen preguntas guiadas.
2. **Streamlit como UI**: Framework Python que genera la web automaticamente, buen soporte para LaTeX y Plotly.
3. **3 niveles de detalle**: Maximo (cada sub-calculo), intermedio (formulas con valores), basico (formula + resultado). Por defecto siempre maximo.
4. **Un archivo por modelo**: Cada distribucion en su propio .py para evitar archivos gigantes.
5. **StepBuilder con arbol**: Los pasos se organizan jerarquicamente (Step con sub_steps), permitiendo drill-down.
6. **detail_level_min en cada Step**: El filtrado se hace en el CalcResult, no en la UI.
7. **Modo B (ejercicios de la guia)**: Ademas del texto libre, el usuario puede decir "tema X ej Y" y la app lee el enunciado del PDF.
8. **Sprint 4 antes del 2 y 3**: Se priorizo tener algo visual (Binomial + Streamlit) antes de implementar procesamiento de datos y probabilidad basica. Se retoman despues.
