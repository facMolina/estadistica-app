# Contexto del Proyecto: Calculadora de Estadistica con Paso a Paso

Ultima actualizacion: 2026-06-23 (Sprint v3 "Cálculos extra" cerrado, modo examen sin IA eliminado — la app siempre intenta usar IA local; redondeo cátedra, tabla Z, derivación de parámetros, paso a paso cátedra Normal/Gamma, Bayes continuo, Formulario)

---

## Que es este proyecto

Una aplicacion en Python/Streamlit para resolver ejercicios de Estadistica General (UADE) mostrando el **desarrollo completo paso a paso** de cada calculo. Tres modos de uso:

1. **Modelos de Probabilidad**: selector Discreto/Continuo. Discretos (Binomial, Poisson, Pascal, Hipergeometrico, Hiper-Pascal): 5 tabs — calculo, caracteristicas, tabla completa, graficos, aproximaciones. Continuos (Normal, Log-Normal, Exponencial, Gamma, Weibull, Gumbel Max/Min, Pareto, Uniforme): 4 tabs — calculo, caracteristicas, curva de densidad sombreada, aproximaciones.
2. **Datos Agrupados**: ingreso de intervalos y frecuencias, calcula media, varianza, CV, mediana, fractiles, ogiva e histograma.
3. **Probabilidad**: dos sub-modos — operaciones con dos eventos (solver genérico `solve_two_events()` que deriva P(A), P(B), P(A∩B) desde cualquier combinación conocida) y Bayes/Probabilidad Total con tabla completa.
4. **Problemas Compuestos** (render especial, no es un modo del selector): dispara automáticamente cuando el parser NL detecta distribuciones encadenadas — Hipergeométrico→Binomial (cajas) y Pascal condicional. Renderiza cada paso con su propio `CalcResult` paso a paso.

En los tres modos hay un **intérprete de lenguaje natural** en el sidebar: el usuario describe el problema en texto libre, el parser lo identifica y auto-rellena los widgets. **Sin API key, funciona offline.** El parser también detecta y extrae probabilidades en lenguaje natural español ("probabilidad de producir X es de Y%") y datos de Bayes (priors/likelihoods) desde texto libre.

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
   Paso 0:   notacion catedra (bypass directo) → modelo + params + query
   Paso 0.5: problemas compuestos (_detect_compound) → status="compound"
   Paso 1:   detectar modo (Datos Agrupados / Probabilidad / Modelo)
   Paso 2:   detectar modelo discreto o continuo (Binomial/Poisson/Pascal/Normal/etc.)
   Paso 3:   extraer parametros (n, p, m, N, R, mu, sigma, lambda...)
   Paso 4:   detectar consulta (cdf_left/right/probability/range)
        |
   "complete" → apply_sc_to_session() → cambia modo + pre-rellena widgets → st.rerun()
   "compound" → solve_compound(config) → render_compound_main() con steps
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
|   |-- compound_solver.py      # HECHO — solve_hiper_binomial, solve_pascal_conditional
|
|-- data_processing/
|   |-- grouped_data.py         # GroupedData: media, varianza, mediana, fractiles, F(x), tabla cátedra
|
|-- probability/
|   |-- basic.py                # calc_intersection/union/complement/conditional/independence + solve_two_events()
|   |-- bayes.py                # BayesCalc: solve(), posteriors(), prob_evidence(), full_table()
|
|-- display/
|   |-- graph_builder.py        # Plotly: poligono, CDF, histograma, ogiva, densidad continua
|   |-- latex_renderer.py
|   |-- table_builder.py
|
|-- ui/
|   |-- components/
|   |   |-- detail_selector.py
|   |   |-- step_display.py     # render_calc_result()
|   |   |-- graph_panel.py      # Modelos de Prob: stem + CDF plots
|   |   |-- table_panel.py      # Tabla distribucion + CSV
|   |   |-- summary_panel.py    # Caracteristicas del modelo
|   |   |-- data_processing_ui.py  # Datos Agrupados: editor tabla + calculos + graficos
|   |   |-- probability_ui.py   # Probabilidad: dos eventos (solver genérico) + Bayes
|   |   |-- continuous_ui.py    # Modelos continuos: sidebar + main (tabs calc/chars/grafico)
|   |   |-- compound_ui.py      # HECHO — render_compound_main() para problemas compuestos
|   |   |-- approximations_ui.py# HECHO (Sprint 7) — render_approximations_tab()
|
|-- approximations/             # HECHO (Sprint 7)
|   |-- __init__.py             # reexporta ApproximationResult y try_approximations
|   |-- approximator.py         # Motor: Hiper→Bi, Bi→N (cc ±0.5), Bi→Po, Po→N (cc ±0.5), Gamma→N (Wilson-Hilferty)
|
|-- tests/
|   |-- test_approximations.py    # 7 tests standalone (Sprint 7)
|   |-- test_guide_index.py       # 8 tests standalone (Sprint 9)
|   |-- test_sprint10.py          # 8 tests: Multinomial + SumOfRVs (Sprint 10)
|   |-- test_guide_corpus.py      # Coverage contra los 180 ejercicios (Sprint 10)
|   |-- coverage_report.md        # Generado por test_guide_corpus — backlog para mejorar parser
|
|-- guide_index/                  # Sprint 9 — indexer PDF + cache
|
|-- tcl/                          # Sprint 10 — Suma de VA / TCL
|   |-- __init__.py               # reexporta SumOfRVs, Component
|   |-- sum_of_rvs.py             # SumOfRVs: E(S), V(S), P(S≤s/≥s/range/fractil) vía TCL
|
|-- models/discrete/multinomial.py  # Sprint 10 — Multinomial (discreto multivariado)
|-- ui/components/multinomial_ui.py # Sprint 10 — UI dedicada (data_editor pi/ri, 2 tabs)
|-- ui/components/tcl_ui.py         # Sprint 10 — UI modo TCL (data_editor componentes, 3 tabs)
```

> **Nota:** este árbol quedó congelado en Sprint 10 (2026-04-18) y no incluye lo agregado en
> Sprint v2 (`llm/`, `theory/`, `models/discrete/custom_pmf.py`, `ui/components/theory_ui.py`)
> ni en el Sprint 2º parcial (`calculation/normal_table.py`, `models/continuous/derivations.py`,
> `probability/bayes_continuo.py`, `ui/components/formulario_ui.py`,
> `tests/test_examenes_2do_parcial.py`). Para el mapa de módulos vigente, usar `APP/CLAUDE.md`
> (organizado por tema/sprint, no como árbol de archivos).

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
| **6** | Modelos continuos: Normal, Log-Normal, Exponencial, Gamma/Erlang, Weibull, Gumbel, Pareto, Uniforme | HECHO (2026-04-15) |
| **—** | Problemas Compuestos (Hipergeometrico+Binomial, Pascal condicional) | HECHO (2026-04-17) |
| **7** | Motor de aproximaciones (Hiper→Bi, Bi→N, Bi→Po, Po→N, Gamma→N Wilson-Hilferty) + tests + UI | **HECHO (2026-04-17)** |
| **9** | Modo guia: "tema X ej Y" → leer PDF → NL parser | **HECHO (2026-04-17)** |
| **10** | Multinomial (discreto multivariado) + TCL / Suma de VA + test suite contra la guía | **HECHO (2026-04-18)** |
| **v2** | Local reasoning fallback (Ollama) + Consultas Teóricas (RAG sobre TEORIA/) + CustomPMF + gate de invisibilidad | **HECHO (2026-04-18 aprox.)** |
| **2º parcial** | Redondeo cátedra + tabla Z + derivación de parámetros desde datos indirectos + paso a paso cátedra (Normal/Log-Normal vía tabla, Gamma vía Poisson/Wilson-Hilferty) + esperanza condicional + Bayes continuo + modo Formulario/Reconocimiento | **HECHO (2026-06-23)** |
| **v3** | Pestaña "Cálculos extra" (registry extensible): `LinearTransformCalculator` para E(a+bX)/V(a+bX), en discreto estándar + CustomPMF + continuo | **HECHO (2026-06-23)** |

---

## Sprint 2º parcial — detalle (2026-06-23)

Contexto: el usuario rinde el 2º parcial el 24/6, que cubre solo continuas (Normal,
Log-Normal, Exponencial, Weibull, Gumbel Máx/Mín, Pareto, Uniforme), Proceso de Poisson
(Poisson, Gamma/Erlang), Suma de variables/TCL y Bayes continuo. Diagnóstico: la app exigía
parámetros finales (μ,σ,r,λ...) pero los parciales reales dan datos indirectos (percentiles,
media+varianza, media+moda), el paso a paso usaba scipy en vez del método de cátedra (tabla Z,
Poisson/Wilson-Hilferty para Gamma), y el redondeo no coincidía con la convención del examen.

Piezas nuevas:
- `calculation/statistics_common.py::_custom_round` — redondeo medio hacia arriba (≥5 sube),
  no banker's rounding. Único punto de formateo (`format_number`), no requirió tocar callers.
- `calculation/normal_table.py` — `phi(z)`, `phi_pdf(z)`, `z_critico(alpha)`, `fmt_z(z)`. Tabla Z
  estándar embebida (no `scipy.stats.norm.cdf`) para que el número coincida con la clave del
  profesor. Consumida por `normal.py`, `lognormal.py`, `tcl/sum_of_rvs.py`.
- `models/continuous/derivations.py` — deriva instancia de modelo + `CalcResult` paso a paso
  desde datos indirectos: percentil(es) (Normal), media+varianza (Gamma, λ=μ/σ², r=μ²/σ²),
  media+moda (Pareto, b=μ/(μ−moda)), media (Exponencial), tasa+período, media+rango (Uniforme),
  media+varianza (Gumbel Máx/Mín). UI: radio "Directo / Desde datos" en `continuous_ui.py`.
- `models/continuous/gamma.py::cdf_left` — método cátedra: vía Proceso de Poisson asociado si
  `r` es entero y ≤30; vía Wilson-Hilferty si `r` es grande o no entero. Verificado contra la
  guía: `Fg(20/4;0.3)=0.8488`.
- `probability/bayes_continuo.py` — Bayes con verosimilitud continua: punto (`f_i(x)`), cola
  derecha/izquierda (`G_i(k)`/`F_i(k)`), y variante "misma familia con parámetros por grupo".
- `ui/components/formulario_ui.py` — modo nuevo "Formulario / Reconocimiento": estático, offline,
  sin lógica de cálculo, portado del FORMULARIO del 2º parcial (tabla de reconocimiento con
  buscador, regla de oro de parámetros, plantillas, tabla Z, errores comunes). `TEORIA/MACHETE.md`
  se reescribió con el mismo contenido (fuente del RAG de Consultas Teóricas).
  **Bug encontrado y corregido (2026-06-23):** `theory/machete_builder.py` tenía el contenido
  viejo de `MACHETE.md` hardcodeado como string de Python (`_MACHETE_SEED`); cualquier test que
  llamara `build_machete(force=True)` (lo hace `tests/test_theory_flow.py`, encadenado en
  `test_regression_v2.py`) revertía en silencio la reescritura. Fix: el contenido vive ahora en
  `theory/machete_seed.md` (markdown plano, sin escaping) y `build_machete` solo copia ese
  archivo a `TEORIA/MACHETE.md`. Editar siempre `machete_seed.md`, nunca `MACHETE.md` directo.
- `tests/test_examenes_2do_parcial.py` (standalone, 9/9 OK) — resuelve end-to-end ejercicios de
  `EJEMPLOS/` (modelos `.md` + parciales reales 2024 + guía Temas IV–VII), no encadenado en
  `test_regression_v2.py`.

Deliberadamente fuera de alcance (congelado): discreto, Temas I–III, soporte de continuas en el
parser NL (`interpreter/nl_parser.py::MODELO_PATTERNS` solo tiene discretos — la entrada guiada
por widgets en `continuous_ui.py` cubre la necesidad por ahora).

---

## Sprint v3 — "Cálculos extra" (2026-06-23)

Pestaña nueva, pensada para iterar: registry extensible en `ui/components/extras/`
(`ExtraCalculator` ABC + `_registry.py` + dispatcher en `__init__.py::render_extras_tab`).
Primera calculadora: `LinearTransformCalculator` (`linear_transform.py`) — `E(a+b·X)` y
`V(a+b·X)` por linealidad, con paso a paso vía `StepBuilder`. Aparece en discreto estándar,
CustomPMF y continuo (no en Multinomial/TCL — no tienen un `E(X)` escalar canónico). Tests en
`tests/test_qa_smoke.py::qa_extras` (4/4 OK, suite completa 61/61 OK).

Se encontró y corrigió un bug de renderizado: los steps mezclaban fórmula/sustitución/resultado
en fragmentos LaTeX separados que `display/latex_renderer.py::render_step_latex` une con un
espacio literal en un solo `st.latex()` — el resultado se veía pegoteado. Fix: cada step ahora es
una sola ecuación autocontenida (convención ya usada en `models/discrete/binomial.py`).

Cómo agregar la próxima calculadora: crear `ui/components/extras/<nombre>.py` con clase que
herede `ExtraCalculator`, registrarla en `_registry.py`. Ideas pendientes (no implementadas):
`QuadraticTransform` (E(a+bX+cX²) discreto), `MGFEvaluator`, `UtilityCalculator`.

## Decisión: siempre usar IA (2026-06-23)

Se eliminó el checkbox "Modo examen (sin IA, 100% offline)" y el toggle manual
`OLLAMA_ENABLED`/`ollama_enabled()`/`set_ollama_enabled()` en `config/settings.py`. La app
siempre intenta usar el servicio local de IA; si no está corriendo, `OllamaClient.is_available()`
sigue devolviendo `False` por el ping real al servicio y las dos features (Consultas Teóricas,
fallback LLM del parser) degradan en silencio como siempre — eso es robustez ante el servicio
caído, no una regla de negocio para desactivarlo a propósito. No queda ningún botón ni env var
para apagar la IA deliberadamente.

---

## Que queda pendiente

### Backlog post-Sprint 10 (ver tests/coverage_report.md)
- Parser de Tema II (probabilidad general): coverage 2/31. Falta mejorar la detección de patrones sin señales fuertes de Bayes.
- Parser de Tema IV/V/VI (continuas): coverage muy bajo porque los enunciados usan lenguaje de ingeniería (confiabilidad, tiempos de servicio) con menos palabras-clave. Pendiente desde antes del 2º parcial: el parser NL nunca llegó a soportar continuas (`MODELO_PATTERNS` solo tiene discretos) — la app las cubre solo vía widgets guiados, no vía texto libre.
- Extracción NL de componentes para TCL en casos heterogéneos (hoy solo captura "k variables con media μ y varianza σ²" o listas `E(Xi)=..., V(Xi)=...`).
- Subir el umbral de `test_parse_coverage` a medida que se mejore la cobertura.

### Backlog post-Sprint v2 (heredado de `estadistica_v2.md`, eliminado — contenido migrado acá)
- **`compound_type=bayes_then_pascal`** (prioridad alta, no implementado): Bayes seguido de Pascal condicional encadenado — no integrado en `compound_solver.py`.
- **`compound_type=multi_distribution`** (prioridad alta, no implementado): cadenas de 3+ distribuciones — no integrado.
- **UI dedicada para CustomPMF** (prioridad media): hoy `models/discrete/custom_pmf.py` solo se alcanza vía el parser NL, no hay widgets dedicados en el sidebar.
- **Exportar machete desde la UI** (prioridad baja): no hay botón de descarga de `TEORIA/MACHETE.md` (o su render) desde la app.
- **Evaluación del fallback LLM en test automatizado** (prioridad media): el corpus de 11 ejercicios "hard" (de los PDFs de final) no está automatizado porque depende del fallback LLM no determinístico — solo validado manualmente (`MANUAL_REGRESSION_CHECKLIST.md`).
- **Ampliar corpus RAG a los 8 PDFs completos de TEORIA/** (prioridad media): hoy el RAG indexa lo que hay en `TEORIA/MACHETE.md` + lo que se haya cacheado; no cubre los 8 PDFs fuente completos.
- **Aproximaciones nuevas Pascal→Normal / Hiper→Normal** (prioridad baja): no implementadas en `approximations/approximator.py` (hoy: Hiper→Bi, Bi→N, Bi→Po, Po→N, Gamma→N).

### WS0 / WS5 del plan del 2º parcial — no completados en esta sesión
- **Setup de graphify**: time-boxed por el plan, quedó stalled/bloqueado — no se reintentó para no demorar el trabajo del parcial.
- **Soporte de continuas en el parser NL** (ver arriba): deliberadamente deprioritizado — la entrada guiada por widgets cubre el caso de uso inmediato del parcial.

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
1.5. **Referencia a guia** (`_detect_guide_exercise`): detecta `"tema X ejercicio Y"` / `"guia tema 2 ej 23"` y retorna `status="guide_exercise"` con `tema` y `numero`. El `streamlit_interpreter` lo resuelve: abre el índice (`guide_index/indexer.py`, lazy + cache), extrae el enunciado del PDF, lo muestra al usuario, y re-parsea con el mismo NLParser
2. **Problemas compuestos** (`_detect_compound`): detecta cadenas de distribuciones y retorna `status="compound"` con config. Tipos actuales: `hiper_binomial` (muestreo por caja + conteo de rechazos) y `pascal_conditional` (P(N>x | N>y))
3. **Detectar modo**: Datos Agrupados (keywords o ≥3 patrones `X-Y`) / Probabilidad (bayes, a priori, P(A|B), mutuamente excluyentes, etc.) / Modelos de Probabilidad
4. **Detectar modelo**: keywords en `MODELO_PATTERNS`
5. **Extraer params**: regex en `PARAM_PATTERNS` + `EXTRA_PARAM_PATTERNS`
6. **Detectar consulta**: cdf_left / cdf_right / probability / range / full_analysis

Multi-turno: si faltan datos, retorna `need_more_info` con pregunta. El turno siguiente combina el contexto previo.

Al recibir `"complete"`: `apply_sc_to_session(sc, st.session_state)` cambia el modo y pre-rellena widgets, luego `st.rerun()`.

Al recibir `"compound"`: el solver `solve_compound(config)` arma la solución (lista de pasos, cada uno con su `CalcResult`) y `render_compound_main()` la renderiza.

### Extracción NL avanzada (dentro del modo Probabilidad)
- `_extract_prob_natural_language()`: detecta múltiples patrones `"probabilidad de X es de Y%"` y los clasifica en marginal, `ambas` → P(A∩B), `nada/ninguna` → P(A'∩B'). Auto-rellena P(A), P(B), P(A∩B), P(A'∩B') en los widgets.
- `_extract_bayes_data()`: si hay 2N porcentajes o 2N decimales en el texto, asume primera mitad = priors y segunda = likelihoods. Intenta extraer labels desde palabras capitalizadas del texto.

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
7. **Problemas compuestos desacoplados**: el parser (`_detect_compound()` en `nl_parser.py`) solo retorna config; el solver (`compound_solver.py`) no depende del parser. Para agregar un tipo nuevo: implementar `solve_<name>()`, agregar branch en `solve_compound()`, y agregar `_try_<name>()` al parser. La UI (`compound_ui.py`) es genérica — cualquier solver que devuelva `{title, description?, steps: [{num, title, description, notation, calc_result, result_label, result_value}], conditional?, final_value}` se renderiza sin tocar UI.
8. **`solve_two_events()` generico**: `probability/basic.py` expone un solver iterativo que acepta cualquier combinación de datos conocidos (P(A), P(B), P(A∩B), P(A∪B), P(A'∩B'), P(A|B), P(B|A)) y deriva el resto paso a paso. El UI `probability_ui.py` usa multiselect para que el usuario elija qué datos aporta.
9. **Aproximaciones como tab opcional, no reemplazo**: la pestaña "Aproximaciones" corre después del cálculo exacto y muestra **todas** las aproximaciones canónicas aplicables al modelo + consulta actual, con su condición evaluada (verde ✅ si cumple, naranja ⚠️ si no — pero igual se calcula y muestra el error). Cada aproximación devuelve `ApproximationResult` con `approx_value`, `exact_value`, `abs_error`, `rel_error_pct` y un `CalcResult` paso a paso. La corrección de continuidad ±0.5 está incluida en Bi→Normal y Po→Normal. Gamma→Normal usa Wilson-Hilferty: Y=(Xλ/r)^(1/3) ~ N(1−1/(9r), 1/(9r)). Para agregar una nueva aproximación: escribir `_origen_to_destino()` en `approximations/approximator.py`, agregar el branch en `try_approximations()`, escribir el test en `tests/test_approximations.py`.

---

## Sprint 7: motor de aproximaciones

Módulo: `approximations/approximator.py`. Entry point: `try_approximations(model_name, params, query_type, query_params) -> list[ApproximationResult]`.

Aproximaciones implementadas:

| De | A | Condición | Técnica |
|----|---|-----------|---------|
| Hipergeométrico | Binomial | n/N ≤ 0.01 | p=R/N, mismo n |
| Binomial | Normal | np≥10 y n(1−p)≥10 | μ=np, σ=√(np(1−p)), **corrección ±0.5** |
| Binomial | Poisson | p ≤ 0.005 | m=np |
| Poisson | Normal | m ≥ 15 | μ=m, σ=√m, **corrección ±0.5** |
| Gamma | Normal | siempre (mejora con r grande) | Wilson-Hilferty: Y=(Xλ/r)^(1/3) ~ N(1−1/(9r), 1/(9r)) |

Tests (`tests/test_approximations.py`, 7/7 OK):
- `Fg(20/4;0.3)` exacto=0.8488 (valor de guía), WH=0.8497, err=8.6e-4
- `Bi(100,0.6) P(X≤65)`: exacto=0.8697, Normal+cc=0.8692, err=4.5e-4
- `Bi(200,0.003) P(X≥1)`: exacto=0.4517, Poisson=0.4512, err=4.9e-4
- `Po(m=25) P(X≤27)`: exacto=0.7002, Normal+cc=0.6915, err=8.7e-3
- `Hiper(1000,50,5) P(X≤2)`: exacto=0.9989, Binomial=0.9988, err=6.0e-5
- `Gamma(r=30,lam=1) F(28)`: err=1.4e-4 (WH mejor con r grande)

UI: `ui/components/approximations_ui.py::render_approximations_tab()` muestra, por cada aproximación aplicable:
- Badge ✅/⚠️ en el título
- Condición evaluada (verde/naranja)
- Parámetros destino (μ, σ, m, p, etc.)
- 3 métricas: valor aproximado, valor exacto, error absoluto + % relativo
- Expander "Paso a paso" que renderiza el `CalcResult` al nivel de detalle actual

Integración:
- `app_streamlit.py` agrega 5ta tab "Aproximaciones" en modo discreto. Mapea `modelo` + inputs a params/query_params antes de llamar al motor.
- `ui/components/continuous_ui.py::_render_approximations()` agrega 4ta tab en modo continuo. Solo Gamma tiene aproximación; las demás muestran mensaje informativo.

---

## Sprint 10: Multinomial + TCL + coverage tests

### Multinomial (discreto multivariado)
Modelo en `models/discrete/multinomial.py` — **no hereda** de `DiscreteModel` porque el resultado es un vector `r = (r1,…,rk)` con `sum(r)=n`. API: `probability(r_vector)`, `probability_value`, `mean_vector`, `variance_vector`, `covariance(i,j)` (todos `CalcResult`), `marginal_binomial(i) → Binomial(n, p_i)`. La UI dedicada (`ui/components/multinomial_ui.py`) se dispatcha desde `app_streamlit.py` cuando `modelo in _MULTIVARIATE_DISCRETE`, evitando el flujo univariado.

Verificado: `Multinomial(10, [0.2,0.3,0.5]).probability_value([2,3,5]) = 0.085050` (manual: `10!/(2!3!5!)·0.2²·0.3³·0.5⁵`).

### TCL / Suma de VA (nuevo modo)
Módulo `tcl/sum_of_rvs.py` + modo `"TCL / Suma de VA"` en el selector de `app_streamlit.py`. Dados k componentes con E(Xi), V(Xi) y `count` (número de copias iid), computa `S = Σ Xi` y aplica TCL: `S ~ N(ΣμI·countI, ΣσI²·countI)`. Consultas: `cdf_left`, `cdf_right`, `range`, `fractile`. Constructor auxiliar `from_model_instances(models, counts)` permite alimentar con instancias de modelos existentes (Binomial, Normal, etc.). Heurística `tcl_condition_met(30)` para advertir cuando k < 30.

UI con `st.data_editor` (Nombre, E(Xi), V(Xi), Cantidad) + 3 tabs: Cálculo, Momentos paso a paso, Componentes. NL parser detecta con keywords `tcl`, `teorema central`, `suma de [k] variables` y extrae componentes desde `"k variables con media μ y varianza σ²"`.

### Test suite contra la guía
`tests/test_guide_corpus.py` itera los 180 ejercicios, clasifica el resultado del parser (`complete` / `follow_up` / `error`) y genera `tests/coverage_report.md` con la lista de ejercicios que fallaron. Baseline Sprint 10: **31/180 complete (17.2%)** — los próximos sprints van a mover la aguja mejorando el parser de los temas con menor coverage (ver tabla). Tests: `test_parse_coverage` (umbral ≥25), `test_known_answers` (5/5 OK: Bi/Pa/Po/Multinomial), `test_parse_stability` (determinismo).

Unitarios en `tests/test_sprint10.py` (8/8 OK): Multinomial `probability`/`mean/variance/covariance`/`marginal_binomial`/`characteristics_summary`/validación + SumOfRVs `iid(30 Bernoullis)`/`mezcla N+N`/`steps ≥3 niveles`/`from_model_instances`.
