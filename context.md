# Contexto del Proyecto: Calculadora de Estadistica con Paso a Paso

Ultima actualizacion: 2026-04-15 (Sprint 6 completado)

---

## Que es este proyecto

Una aplicacion en Python/Streamlit para resolver ejercicios de Estadistica General (UADE) mostrando el **desarrollo completo paso a paso** de cada calculo. Tres modos de uso:

1. **Modelos de Probabilidad**: selector Discreto/Continuo. Discretos (Binomial, Poisson, Pascal, Hipergeometrico, Hiper-Pascal): 4 tabs — calculo, caracteristicas, tabla completa, graficos. Continuos (Normal, Log-Normal, Exponencial, Gamma, Weibull, Gumbel Max/Min, Pareto, Uniforme): 3 tabs — calculo, caracteristicas, curva de densidad sombreada.
2. **Datos Agrupados**: ingreso de intervalos y frecuencias, calcula media, varianza, CV, mediana, fractiles, ogiva e histograma.
3. **Probabilidad**: dos sub-modos — operaciones con dos eventos (union, interseccion, complemento, condicional, independencia) y Bayes/Probabilidad Total con tabla completa.

En los tres modos hay un **intérprete de lenguaje natural** en el sidebar: el usuario describe el problema en texto libre, el parser lo identifica y auto-rellena los widgets. **Sin API key, funciona offline.**

---

## Como ejecutar localmente (cualquier persona)

Requiere **Python 3.9 o superior**. Todos los comandos se corren desde la carpeta `APP/`.

### Windows

```bat
cd C:\Users\PC\Desktop\ESTADISTICA\APP

:: Instalar dependencias (una sola vez)
C:\Python314\python -m pip install -r requirements.txt

:: Lanzar app web (sin API key, funciona offline)
C:\Python314\python -m streamlit run app_streamlit.py

:: Modo CLI (requiere APP/.env con ANTHROPIC_API_KEY=sk-ant-...)
C:\Python314\python main.py
C:\Python314\python main.py --streamlit
```

### macOS / Linux

```bash
cd /ruta/a/ESTADISTICA/APP

# Crear y activar entorno virtual (una sola vez)
python3 -m venv .venv
source .venv/bin/activate

# Instalar dependencias (una sola vez)
pip install -r requirements.txt

# Lanzar app web (sin API key, funciona offline)
python -m streamlit run app_streamlit.py

# Modo CLI (requiere APP/.env con ANTHROPIC_API_KEY=sk-ant-...)
python main.py
python main.py --streamlit
```

La app abre automaticamente en `http://localhost:8501`.

> **Nota Windows:** el `.venv` dentro de `APP/` fue creado originalmente en macOS y no funciona en Windows. En Windows instalar los paquetes directamente en el Python del sistema (`C:\Python314\python`) sin usar el venv.

### Dependencias principales
```
streamlit>=1.40.0
plotly>=5.24.0
scipy>=1.14.0
numpy>=2.0.0
pandas
python-dotenv>=1.0.0
anthropic>=0.40.0   # solo para main.py CLI
PyMuPDF>=1.24.0     # pendiente Sprint 9 (leer PDF de la guia)
```

---

## Fuentes de informacion

Todos los archivos estan en `C:\Users\PC\Desktop\ESTADISTICA\`:

### Teoria (carpeta TEORIA/)
| Archivo | Contenido |
|---------|-----------|
| 1 - Procesamiento de Datos.pdf | Tablas de frecuencia, media, varianza, CV, mediana, fractiles |
| 2 - Teoria de la Probabilidad.pdf | P(A), condicional, Bayes, independencia |
| 3 - Distribuciones Discretos.pdf | Binomial, Pascal, Hipergeometrico, Hiper-Pascal, Multinomial |
| 4 - Distribuciones Continuos.pdf | Normal, Log-Normal, Exponencial, Weibull, Gumbel, Pareto, Uniforme |
| 5 - Proceso de Poisson.pdf | Poisson, Gamma/Erlang, Exponencial |
| 6 - Aproximaciones y TCL.pdf | Condiciones y calculos de aproximacion |

### Guia de ejercicios
Archivo: `Guia Problemas Estadística General - Probabilidad y Estadística - UADE (1).pdf`
- 36 paginas, 7 temas, ~170 ejercicios con respuesta
- Tema I (pag 1-3): Procesamiento de Datos — 5 ejercicios
- Tema II (pag 4-8): Teoria de la Probabilidad — 31 ejercicios
- Tema III (pag 9-14): Discretas — 33 ejercicios
- Tema IV (pag 15-19): Continuas especiales — 27 ejercicios
- Tema V (pag 20-24): Normal y Log-Normal — 27 ejercicios
- Tema VI (pag 25-31): Poisson, Exponencial, Gamma — 40 ejercicios
- Tema VII (pag 33-36): Suma de variables / TCL — 9 ejercicios

---

## Arquitectura general

```
Sidebar Streamlit
        |
 [Selector de modo: Modelos de Prob. | Datos Agrupados | Probabilidad]
        |
 [Expander "Interpretar problema"] ← disponible en los 3 modos
        |
 NLParser (interpreter/nl_parser.py) — regex/keywords, sin API key
   Paso 0: notacion catedra (bypass directo) → modelo + params + query
   Paso 1: detectar modo (Datos Agrupados / Probabilidad / Modelo)
   Paso 2: detectar modelo discreto (Binomial/Poisson/Pascal/etc.)
   Paso 3: extraer parametros (n, p, m, N, R...)
   Paso 4: detectar consulta (cdf_left/right/probability/range)
        |
   "complete" → apply_sc_to_session() → cambia modo + pre-rellena widgets → st.rerun()
   "need_more_info" → muestra pregunta de follow-up → usuario responde
        |
 Motor de calculo → CalcResult (arbol de Steps con detail_level_min)
        |
 UI: tabs (Paso a Paso, Caracteristicas, Tabla, Graficos)
```

---

## Estructura del proyecto

Ubicacion: `C:\Users\PC\Desktop\ESTADISTICA\APP\`

```
APP/
|-- app_streamlit.py            # Entry point Streamlit — 3 modos
|-- main.py                     # Entry point CLI con Claude API
|-- requirements.txt
|-- CLAUDE.md                   # Guia detallada para Claude Code
|
|-- interpreter/
|   |-- nl_parser.py            # Parser regex/keywords — 3 modos
|   |-- streamlit_interpreter.py# Adaptador Streamlit: interpret_turn(), apply_sc_to_session()
|   |-- claude_client.py        # Wrapper Anthropic SDK (solo CLI)
|   |-- problem_parser.py       # Loop CLI multi-turno (solo CLI)
|   |-- system_prompt.py        # Prompt para Claude API
|
|-- config/
|   |-- settings.py             # Constantes, rutas, niveles de detalle
|   |-- model_catalog.py        # IMPLEMENTED_MODELS, normalize_model_name()
|
|-- models/
|   |-- base.py                 # DiscreteModel, ContinuousModel (abstractas)
|   |-- discrete/
|   |   |-- binomial.py         # HECHO
|   |   |-- poisson.py          # HECHO (Sprint 5)
|   |   |-- pascal.py           # HECHO (Sprint 5)
|   |   |-- hypergeometric.py   # HECHO (Sprint 5)
|   |   |-- hiper_pascal.py     # HECHO (Sprint 5)
|   |-- continuous/             # HECHO (Sprint 6)
|   |   |-- _base.py            # ContinuousBase: cdf_right, std_dev, cv, H(x), fractile
|   |   |-- normal.py           # Normal(mu, sigma)
|   |   |-- lognormal.py        # LogNormal(m, D)
|   |   |-- exponencial.py      # Exponencial(lam)
|   |   |-- gamma.py            # Gamma(r, lam) — incluye Erlang
|   |   |-- weibull.py          # Weibull(beta, omega)
|   |   |-- gumbel.py           # GumbelMax(beta, theta) + GumbelMin(beta, theta)
|   |   |-- pareto.py           # Pareto(theta, b)
|   |   |-- uniforme.py         # Uniforme(a, b)
|
|-- calculation/
|   |-- step_types.py           # Step, CalcResult
|   |-- step_engine.py          # StepBuilder
|   |-- combinatorics.py        # comb(), comb_with_steps()
|   |-- statistics_common.py    # F, G, H, J genericas; format_number()
|
|-- data_processing/
|   |-- grouped_data.py         # GroupedData: media, varianza, mediana, fractiles, F(x)
|
|-- probability/
|   |-- basic.py                # calc_intersection/union/complement/conditional/independence
|   |-- bayes.py                # BayesCalc: solve(), posteriors(), full_table()
|
|-- display/
|   |-- graph_builder.py        # Plotly: poligono, CDF, histograma, ogiva, densidad continua
|
|-- ui/
|   |-- components/
|   |   |-- detail_selector.py
|   |   |-- step_display.py     # render_calc_result()
|   |   |-- graph_panel.py      # Modelos de Prob: stem + CDF plots
|   |   |-- table_panel.py      # Tabla distribucion + CSV
|   |   |-- summary_panel.py    # Caracteristicas del modelo
|   |   |-- data_processing_ui.py  # Datos Agrupados: editor tabla + calculos + graficos
|   |   |-- probability_ui.py   # Probabilidad: dos eventos + Bayes
|   |   |-- continuous_ui.py    # Modelos continuos: sidebar + main (tabs calc/chars/grafico)
|
|-- approximations/             # PENDIENTE (Sprint 7)
|-- guide_index/                # PENDIENTE (Sprint 9)
```

---

## Estado de sprints

| Sprint | Contenido | Estado |
|--------|-----------|--------|
| **1** | Motor de calculos (Step, CalcResult, StepBuilder, combinatorics) | HECHO (2026-04-08) |
| **4** | Binomial + UI Streamlit base (4 tabs, 3 niveles de detalle) | HECHO (2026-04-08) |
| **8** | Interprete NL + CLI | HECHO (2026-04-14) |
| **5** | Modelos discretos: Poisson, Pascal, Hipergeometrico, Hiper-Pascal | HECHO (2026-04-15) |
| **2** | Datos Agrupados (Tema I): media, varianza, CV, mediana, fractiles, histograma, ogiva | HECHO (2026-04-15) |
| **3** | Probabilidad (Tema II): dos eventos + Bayes/Prob. Total | HECHO (2026-04-15) |
| **6** | Modelos continuos: Normal, Log-Normal, Exponencial, Gamma/Erlang, Weibull, Gumbel, Pareto, Uniforme | **HECHO (2026-04-15)** |
| **7** | Motor de aproximaciones + TCL | pendiente |
| **9** | Modo guia: "tema X ej Y" → leer PDF → NL parser | pendiente |
| **10** | Pulido, Multinomial, test suite completo | pendiente |

---

## Que queda pendiente

### Sprint 7: Aproximaciones

| De | A | Condicion |
|----|---|-----------|
| Hipergeometrico | Binomial | n/N ≤ 0.01 |
| Binomial | Normal | np≥10 y n(1-p)≥10, correccion ±0.5 |
| Binomial | Poisson | p≤0.005, m=np |
| Poisson | Normal | m≥15, correccion ±0.5 |
| Gamma | Normal | Wilson-Hilferty |

Test: Fg(20/4;0.3) = Gpo(4/6) = 0.8488

### Sprints 9, 10
- Sprint 9: El usuario escribe "tema III ejercicio 8" → leer enunciado del PDF con PyMuPDF → NL parser → resolver
- Sprint 10: Multinomial, test suite contra todos los ejercicios de la guia

---

## Mecanismo clave: Motor de paso a paso

Cada calculo retorna un `CalcResult` con arbol de `Step`. Cada `Step` tiene `detail_level_min`:

| detail_level_min | Se muestra en | Ejemplo |
|------------------|---------------|---------|
| 1 | Siempre (basico) | P(r=4) = 0.3044 |
| 2 | Intermedio y maximo | P(r=4) = C(12,4)*0.45^4*0.55^8 |
| 3 | Solo maximo | C(12,4) = 12!/(4!*8!) = 495 |

Flujo: `StepBuilder.add_step(level_min=N)` → `build()` → `CalcResult` → `get_steps_for_level(N)` → UI renderiza con `st.expander`.

---

## Mecanismo clave: Parser NL

El parser opera en pasos ordenados:
1. **Bypass catedra**: si hay `Fb(r/n;p)`, `Gpo(r/m)`, `Fh(r/n;N;R)`, etc. → parsea directo
2. **Detectar modo**: Datos Agrupados (keywords o ≥3 patrones `X-Y`) / Probabilidad (bayes, a priori, P(A|B), mutuamente excluyentes, etc.) / Modelos de Probabilidad
3. **Detectar modelo**: keywords en `MODELO_PATTERNS`
4. **Extraer params**: regex en `PARAM_PATTERNS` + `EXTRA_PARAM_PATTERNS`
5. **Detectar consulta**: cdf_left / cdf_right / probability / range / full_analysis

Multi-turno: si faltan datos, retorna `need_more_info` con pregunta. El turno siguiente combina el contexto previo.

Al recibir "complete": `apply_sc_to_session(sc, st.session_state)` cambia el modo y pre-rellena widgets, luego `st.rerun()`.

---

## Verificacion: respuestas conocidas de la guia

**Binomial**: Gb(3/10;0.25)=0.4744 | Fb(4/12;0.45)=0.3044 | Gb(10/14;0.75)=0.7415
**Pascal**: Fpa(12/5;0.42)=0.6175 | P(n≤8)=0.4967
**Poisson**: P(r=0/m=5)=0.0067 | Gpo(4/6)=0.8488
**Normal**: P(x<24000)=94.52% | P(x>840)=2.28%
**Gamma**: P(x<150)=44.22%

---

## Decisiones de diseno relevantes

1. **Parser regex, sin API key, para la web**: sin costo, sin latencia, offline. CLI sigue usando Claude API.
2. **3 niveles de detalle**: controlados por dropdown en sidebar, filtrado en `CalcResult.get_steps_for_level()`.
3. **CalcResult siempre**: ningun calculo retorna un float pelado.
4. **`apply_sc_to_session()`**: centraliza el switch de modo + pre-relleno de widgets desde el NL interpreter.
5. **Modo "Probabilidad" sin calculadora de parametros**: el interprete NL puede pre-cargar datos (priors/likelihoods), pero el usuario siempre puede editar la tabla directamente.
6. **Sprint 6 continuo**: `ContinuousBase` en `models/continuous/_base.py` provee defaults para `cdf_right`, `std_dev`, `cv`, `partial_expectation_left` (scipy quad), `fractile` (ppf). Cada modelo guarda `self._dist` scipy. La UI tiene 3 tabs (Calculo, Caracteristicas, Grafico). `build_density_plot()` en `graph_builder.py` sombrea el area segun query_type. El sidebar Modelos de Probabilidad tiene toggle Discreto/Continuo.
