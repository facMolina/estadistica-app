# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## First step on every session

Before doing anything else, **read `../README.md`**. It has the canonical
instructions to prepare the environment and launch the app (`start.bat` on
Windows, `./start.sh` on macOS/Linux) and troubleshooting for the most common
failure modes. Treat it as the source of truth when the user asks how to run
the app or when you need to start it as part of a task.

## Workflow rule — leave the app running

After finishing any feature or sprint, **always leave Streamlit running in the background** so the user can test immediately. Default port `8501`; if taken, try `8502+` and report which URL.

```bat
C:\Python314\python -m streamlit run app_streamlit.py --server.headless true --server.port 8501
```

Report the URL (`http://localhost:8501`) in the final message. Do not kill the process at the end of the turn.

## What this project is

A Python app that solves Statistics exercises (UADE - Ing. Sergio Anibal Dopazo) showing the **full step-by-step workings** of each calculation. Two modes:

1. **Web** (`app_streamlit.py`): Streamlit interface with sidebar NL interpreter (regex-based, no API key), 4 tabs: step-by-step calculation, model characteristics, full distribution table, interactive Plotly graphs.
2. **CLI** (`main.py`): User describes problem in natural text → Claude API interprets it → writes session_config.json → launches Streamlit with pre-populated parameters.

The **web interface is fully functional without an API key**. The NL interpreter in the sidebar uses `interpreter/nl_parser.py` (regex/keywords, no external dependencies). The CLI mode requires `ANTHROPIC_API_KEY` in `.env`.

## Running the app locally

Requires **Python 3.9+**. All commands run from `APP/`.

### Windows

```bat
:: Install dependencies (once)
C:\Python314\python -m pip install -r requirements.txt

:: Web UI — no API key needed, works offline
C:\Python314\python -m streamlit run app_streamlit.py

:: CLI mode — requires ANTHROPIC_API_KEY in APP/.env
C:\Python314\python main.py
C:\Python314\python main.py --streamlit
```

### macOS / Linux

```bash
# Create and activate virtual environment (once)
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies (once)
pip install -r requirements.txt

# Web UI — no API key needed, works offline
python -m streamlit run app_streamlit.py

# CLI mode — requires ANTHROPIC_API_KEY in APP/.env
python main.py
python main.py --streamlit
```

App opens at `http://localhost:8501`.

**Note (Windows):** the `.venv` in `APP/` was originally created on macOS — on Windows install packages directly into system Python (`C:\Python314\python`) instead of using the venv.

## Architecture: the step-by-step engine

Every calculation returns a `CalcResult` (not a plain number). This is the central design pattern:

```
StepBuilder → add_step(level_min=N) → build() → CalcResult
                                                      ↓
                                          get_steps_for_level(N) → filtered Steps
                                                                          ↓
                                                                    UI renders
```

**`Step`** (`calculation/step_types.py`): has `description`, `latex_formula`, `latex_substituted`, `latex_result`, `numeric_result`, `sub_steps` (recursive), and `detail_level_min`:
- `1` = always shown (DETAIL_BASIC)
- `2` = intermediate and max (DETAIL_INTERMEDIATE)
- `3` = max detail only (DETAIL_MAX)

**`StepBuilder`** (`calculation/step_engine.py`): builder pattern with a stack-based nesting system. Key methods: `add_step()`, `add_substep()`, `begin_substeps()/end_substeps()`, `merge_result()` (embeds another CalcResult's steps as sub-steps).

**`CalcResult`**: holds the step tree + `final_value` (float) + `final_latex`. The `get_steps_for_level(n)` method filters the tree recursively.

## Adding a new continuous model

1. Create `models/continuous/my_model.py` inheriting `ContinuousBase` from `models/continuous/_base.py`.
2. Store `self._dist = scipy.stats.xxx(...)` for numerical CDF/PPF.
3. Implement: `name()`, `params_dict()`, `domain()`, `latex_formula()`, `density_value(x)`, `density(x)`, `cdf_left(x)`, `mean()`, `variance()`, `mode()`, `median()`, `skewness()`, `kurtosis()`. Override `display_domain()` if the default ±4σ isn't appropriate.
4. `cdf_right`, `std_dev`, `cv`, `partial_expectation_left`, `fractile` are provided by `ContinuousBase` — override only if you need a closed-form version.
5. Register in:
   - `ui/components/continuous_ui.py` → `CONTINUOUS_MODELS` list, `_instantiate()`, sidebar inputs
   - `config/model_catalog.py` → `IMPLEMENTED_MODELS`

**Reference implementation**: `models/continuous/normal.py`. All 9 continuous models are implemented.

## Adding a new discrete model

1. Create `models/discrete/my_model.py` inheriting `DiscreteModel` from `models/base.py`.
2. Implement all abstract methods. The minimum required interface:
   - `name()`, `params_dict()`, `domain()` → metadata
   - `probability_value(r)` → pure float (used internally for table/CDF loops)
   - `probability(r)`, `cdf_left(r)`, `cdf_right(r)` → return `CalcResult`
   - `mean()`, `variance()`, `std_dev()`, `mode()`, `median()`, `cv()`, `skewness()`, `kurtosis()` → return `CalcResult`
   - `partial_expectation_left(r)` → return `CalcResult`
   - `latex_formula()` → raw LaTeX string
3. `full_table()` and `all_characteristics()` are already implemented in the base class using `probability_value` — no need to override.
4. Register the model in:
   - `app_streamlit.py` sidebar selector and instantiation block
   - `config/model_catalog.py` → `IMPLEMENTED_MODELS` set
   - `interpreter/nl_parser.py` → `MODELO_PATTERNS`, `PARAM_PATTERNS`, `REQUIRED_PARAMS`, optionally `CATHEDRA_PATTERNS`
   - This file (`CLAUDE.md`) → update parser section and pending sprints table

**Reference implementation**: `models/discrete/binomial.py` — use it as the template. Completed discrete models: Binomial, Poisson, Pascal, Hipergeometrico, Hiper-Pascal.

## Compound problems (chained distributions)

Some guide exercises require chaining two distributions. These are dispatched via
`calculation/compound_solver.py::solve_compound(config)` and rendered by
`ui/components/compound_ui.py::render_compound_main(solution, detail_level)`.

Current compound types:
- **`hiper_binomial`**: Hipergeométrico (sampling per box) → Binomial (across boxes).
  Config keys: `box_N`, `box_R`, `sample_n`, `num_boxes`, `reject_r`, `query_type`, `query_r`.
- **`pascal_conditional`**: Pascal with conditional probability P(N>query | N>condition).
  Config keys: `r_success`, `p`, `condition_n`, `query_n`.

Detection: `NLParser._detect_compound()` runs in parse step 0.5 (between cátedra bypass
and mode detection) and returns `status: "compound"` with the config dict.

Adding a new compound type:
1. Implement `solve_<name>(config)` in `compound_solver.py`.
2. Add the dispatch branch in `solve_compound()`.
3. Extend `_detect_compound()` with a new `_try_<name>()` method in `nl_parser.py`.

## Approximations engine (Sprint 7)

Module: `approximations/approximator.py`. Entry point: `try_approximations(model_name, params, query_type, query_params) -> list[ApproximationResult]`.

Each element returned is an `ApproximationResult` dataclass with: `from_model`, `to_model`, `condition_met: bool`, `condition_str`, `target_params`, `target_params_str`, `approx_value`, `exact_value`, `abs_error`, `calc_result` (full step-by-step `CalcResult`), and a `rel_error_pct` property.

**Important**: all applicable approximations are returned regardless of whether the condition is met — the UI shows a green ✅ / orange ⚠️ badge so the student can see what the error would be when applying an approximation outside its safe range.

Implemented approximations:

| From | To | Condition | Notes |
|------|----|-----------|-------|
| Hipergeometrico | Binomial | `n/N ≤ 0.01` | `p = R/N`, same `n` |
| Binomial | Normal | `np ≥ 10 ∧ n(1−p) ≥ 10` | `μ=np`, `σ=√(np(1−p))`, continuity correction ±0.5 |
| Binomial | Poisson | `p ≤ 0.005` | `m = np` |
| Poisson | Normal | `m ≥ 15` | `μ=m`, `σ=√m`, continuity correction ±0.5 |
| Gamma | Normal | always applicable | Wilson-Hilferty: `Y = (Xλ/r)^(1/3) ~ N(1−1/(9r), 1/(9r))` |

Continuity correction is applied via `_binomial_normal_query(mu, sigma, query_type, r, query_params)` — used by both Bi→N and Po→N. Query types supported: `probability`, `cdf_left`, `cdf_right`, `range`.

**UI**: `ui/components/approximations_ui.py::render_approximations_tab(model_name, params, query_type, query_params, detail_level)`. Renders, per approximation: condition evaluated, target params, 3 metrics (approx/exact/error + relative %), and an expander with full step-by-step.

Integration:
- Discrete flow: 5th tab in `app_streamlit.py`. Maps current `modelo` + sidebar inputs to `params` and `query_params` dicts before calling the engine.
- Continuous flow: 4th tab added in `continuous_ui.py::render_continuous_main()`. Only Gamma has an approximation; other continuous models show an informational message.

**Tests**: `tests/test_approximations.py` (standalone, no pytest required). Run from `APP/`:
```bat
C:\Python314\python tests/test_approximations.py
```
Expected: 7/7 OK. Key verified values: `Fg(20/4;0.3)=0.8488` (guide value) via Wilson-Hilferty, Bi(100,0.6)→Normal+cc, Bi(200,0.003)→Poisson, Po(25)→Normal+cc, Hiper(1000,50,5)→Binomial, Gamma(r=30)→N (WH mejora a r grande).

Adding a new approximation:
1. Write `_origen_to_destino(params, query_type, query_params) -> Optional[ApproximationResult]` in `approximator.py`, using `StepBuilder` for the `calc_result`.
2. Add the dispatch branch in `try_approximations()`.
3. If origin is a continuous model not yet listed, extend `_render_approximations()` in `continuous_ui.py` to map model params → approximator params.
4. Write a test in `tests/test_approximations.py` asserting `approx_value` is close to `exact_value` within a tolerance.

## Modo guía PDF (Sprint 9)

Módulo: `guide_index/indexer.py`. El usuario escribe `"tema III ejercicio 8"` en el intérprete NL y la app extrae el enunciado del PDF oficial (`GUIA_PATH`), lo pasa por el mismo `NLParser.parse()` y muestra el enunciado + resultado.

Flujo:
1. `NLParser._detect_guide_exercise(text)` corre como Paso 0.3 (entre cátedra bypass y compound). Matchea `(?:guia )?tema (romano|digito|palabra) (ejercicio|ej|problema|prob) N`. Retorna `{"status": "guide_exercise", "tema", "numero"}`.
2. `interpreter/streamlit_interpreter.py::interpret_turn()`:
   - Llama `load_or_build_index()` (lazy + cache en `guide_index/index.json`).
   - `get_exercise(idx, tema, numero)` → `{tema, numero, text, resp, tema_title}` o `None`.
   - Agrega un mensaje `role=assistant` al historial con `_format_enunciado(ex)` (Markdown).
   - **Re-parsea** `ex["text"]` con el mismo `NLParser` — el enunciado del PDF entra al pipeline normal (cátedra → compound → modo → modelo → params → query).
   - Si el re-parse falla (error/need_more_info), devuelve `nl_input_prefill: ex["text"]` para que la UI lo copie al text_area.
   - El retorno siempre trae `enunciado_from_guide=True`, `tema`, `numero`, `enunciado_text`, `expected_resp` (via `_enrich()`).
3. `app_streamlit.py`: muestra un expander `Tema X — Ejercicio N (de la guía)` en el main area cuando hay `st.session_state["last_guide_enunciado"]`. El text_area se pre-llena con el enunciado en follow-up/error.

Indexer (`guide_index/indexer.py`):
- `build_index(pdf_path)`: abre el PDF con PyMuPDF, limpia el header de cada página (`Ing. Sergio Aníbal Dopazo ... N de 36`), detecta los 7 `TEMA X -` headers en orden, acumula el body de cada tema y splitea ejercicios por regex `^(\d+)\)\s+`. Separa enunciado/Resp por `\n\s*Resp\s*:\s*`.
- `load_or_build_index()`: lee `GUIA_INDEX_CACHE`; reconstruye si el mtime del PDF > mtime del cache o si el JSON está corrupto.
- `get_exercise(idx, tema, numero)`: normaliza tema a romano mayúsculas (`"3"`, `"III"`, `"iii"`, `"tres"` → `"III"`).
- `config.settings.resolve_guia_path()`: busca el PDF por glob si `GUIA_PATH` no existe (para lidiar con variantes NFD/NFC del nombre).

Counts conocidos: Tema I=5, II=31, III=33, IV=27, V=27, VI=40, VII=17 (180 totales).

Tests (`tests/test_guide_index.py`, 8/8 OK): smoke del indexer, contenido de Tema II ej 23, normalización de tema, errores para tema/número inválidos, detección del parser, persistencia del cache, end-to-end con `interpret_turn`, error para Tema IX inexistente.

## Multinomial (discreto multivariado) — Sprint 10

Modelo en `models/discrete/multinomial.py`. **No hereda** de `DiscreteModel` porque
el "resultado" es un vector `r = (r1,…,rk)` con `sum(r)=n`, no un escalar.

API:
- `Multinomial(n, p_vector, labels=None)` — valida `sum(p)≈1`, `pi≥0`, `k≥2`.
- `probability(r_vector) -> CalcResult` — fórmula completa con steps nivel 1/2/3.
- `probability_value(r_vector) -> float` — fast path sin steps.
- `mean_vector()`, `variance_vector()`, `covariance(i,j)` — todos devuelven `CalcResult`.
- `marginal_binomial(i) -> Binomial(n, p_i)` (i 1-indexed).
- `characteristics_summary() -> list[dict]` — tabla para UI.

UI: `ui/components/multinomial_ui.py` con `st.data_editor` (columnas Categoría, pi, ri).
Consultas: probabilidad conjunta, marginal, características. Se dispatchea desde
`app_streamlit.py` cuando `modelo in _MULTIVARIATE_DISCRETE` sin entrar al flujo univariado.

NL parser: en `nl_parser.py` se añadió `MODELO_PATTERNS["Multinomial"]`, extracción vectorial
(`_P_LIST`, `_match_vector`), `_parse_multinomial` y el bypass `if model == "Multinomial"`.
Verificado: `multinomial n=10 probabilidades 0.2;0.3;0.5 conteos 2;3;5` → P(2,3,5)=0.085050.

## TCL / Suma de VA independientes — Sprint 10

Módulo `tcl/sum_of_rvs.py`. Dados k componentes independientes con E/V conocidas,
computa `S = Σ Xi` y aproxima `S ~ N(ΣμI·countI, ΣσI²·countI)` vía TCL.

API:
- `Component(name, mean, variance, count=1)` — `count` multiplica para k copias iid.
- `SumOfRVs(components)` → `expected_value_raw/value()`, `variance_raw/()`, `std_dev_raw/()`.
- `probability(query_type, **query_params)`: `'cdf_left'` (param `s`), `'cdf_right'` (s),
  `'range'` (a,b), `'fractile'` (alpha) — todos devuelven `CalcResult` con
  estandarización `Z = (s-μS)/σS` y `Φ(Z)` vía `scipy.stats.norm`.
- `from_model_instances(models, counts, names)` — constructor desde instancias de modelos existentes.
- `tcl_condition_met(threshold=30)` — heurística para k ≥ 30.

UI: nuevo modo `"TCL / Suma de VA"` en el radio de `app_streamlit.py`.
`ui/components/tcl_ui.py` usa `st.data_editor` (Nombre, E(Xi), V(Xi), Cantidad).

NL parser: `_is_tcl` detecta keywords (`tcl`, `teorema central`, `suma de [k] variables`),
`_parse_tcl` extrae componentes con patrón `k variables con media μ y varianza σ²` o
`E(Xi)=μ, V(Xi)=σ²`. Consulta detectada vía regex: `S<=s`, `S>=s`, `entre a y b`, fractil.

## Tests contra la guía — Sprint 10

`tests/test_guide_corpus.py` (standalone) itera los 180 ejercicios del PDF y clasifica
el resultado del parser en `complete`, `follow_up`, `error`. Genera `tests/coverage_report.md`
con la lista de ejercicios que fallan (backlog para próximos sprints).

Baseline Sprint 10: 31/180 complete (umbral del test: ≥25).
Desglose por tema: I=5/5, II=2/31, III=17/33, IV=1/27, V=1/27, VI=2/40, VII=3/17.
Tests incluidos: `test_parse_coverage`, `test_known_answers` (5/5 OK: Binomial/Pascal/Poisson/Multinomial),
`test_parse_stability` (determinismo sobre 9 muestras).

Unitarios Sprint 10 en `tests/test_sprint10.py` (8/8 OK): probability/momentos/marginal/validación
de Multinomial + 5 tests de SumOfRVs (iid, mezcla N+N, steps, `from_model_instances`).

## Useful utilities in `calculation/`

- `combinatorics.py`: `comb(n,r)` (cached), `comb_with_steps(n,r)` → `CalcResult` with full factorial breakdown.
- `statistics_common.py`: generic discrete distribution helpers — `compute_cdf_left_discrete`, `compute_cdf_right_discrete`, `compute_partial_expectation_left/right`, `find_mode_discrete`, `find_median_discrete`, `build_full_table_discrete`, `format_number`, `format_fraction`.
- `settings.py`: `DETAIL_MAX=3`, `DETAIL_INTERMEDIATE=2`, `DETAIL_BASIC=1`, `MAX_SUMMATION_TERMS=1000`, `EPSILON=1e-10`, `EULER_MASCHERONI`, paths to TEORIA/ and the guide PDF.

## UI rendering

- `ui/components/step_display.py`: renders a `CalcResult` using `st.expander` for sub-steps.
- `ui/components/summary_panel.py`: renders `all_characteristics()` dict.
- `ui/components/graph_panel.py`: 3 Plotly charts — stem plot for P(r), step functions for F(r) and G(r).
- `ui/components/table_panel.py`: DataFrame from `full_table()` + CSV download.
- `ui/components/data_processing_ui.py`: Datos Agrupados mode — `st.data_editor` for Li/Ls/fai table, calculates and displays grouped stats (mean, variance, CV, median, fractile), histogram + ogive via Plotly. Frequency table uses cátedra notation: Li, Ls, Ci, fai, fi, Fai, Fi, Gai, Gi, Ci·fai, (Ci−x̄)²·fai.
- `ui/components/probability_ui.py`: Probabilidad mode — two sub-modes: "Probabilidad de eventos" (generic solver: user selects any combination of known data from P(A), P(B), P(A∩B), P(A∪B), P(A'∩B'), P(A|B), P(B|A) via multiselect; the app derives the rest step-by-step using `solve_two_events()`) and "Bayes / Probabilidad Total" (`st.data_editor` for Hipotesis/P(Hi)/P(E|Hi) table, full Bayes theorem step-by-step).
- `ui/components/continuous_ui.py`: Continuous models — `render_continuous_sidebar(sc)` returns `{model, model_name, title_params, query_type, query_params, model_error}`; `render_continuous_main(cfg, detail_level)` renders 3 tabs (Cálculo, Características, Gráfico). Supports: density, cdf_left, cdf_right, range, fractile queries.
- `display/graph_builder.py`: `build_probability_polygon()`, `build_cdf_plot()`, `build_histogram()`, `build_ogiva()`, `build_density_plot()` — Plotly figure factories. `build_density_plot(model, title, query_type, x_val, x_a, x_b)` shades the appropriate probability area.
- `probability/basic.py`: `CalcResult`-returning functions for intersection, union, complement, conditional, independence check. Also `solve_two_events(knowns, name_A, name_B)` — generic solver that takes any combination of known probability data and iteratively derives P(A), P(B), P(A∩B) with step-by-step CalcResult.
- `probability/bayes.py`: `BayesCalc` class — `solve()`, `posteriors()`, `prob_evidence()`, `full_table()`.

## Sprints status

| Sprint | Content | Status |
|--------|---------|--------|
| **5** | Discrete models: Poisson, Pascal, Hipergeometrico, Hiper-Pascal | **DONE** (2026-04-15) |
| **2** | Topic I: Grouped data statistics (mean, variance, CV, median, fractile, ogive) | **DONE** (2026-04-14) |
| **3** | Topic II: Classical probability, conditional, Bayes | **DONE** (2026-04-15) |
| **6** | Continuous models: Normal, Log-Normal, Exponential, Gamma/Erlang, Weibull, Uniform, Gumbel Min/Max, Pareto | **DONE** (2026-04-15) |
| **—** | Compound problems (hiper+binomial, pascal conditional) | DONE (2026-04-17) |
| **7** | Approximations engine (Hiper→Bi, Bi→N cc, Bi→Po, Po→N cc, Gamma→N Wilson-Hilferty) + 7 tests + UI tab | **DONE (2026-04-17)** |
| **9** | Guide mode: parse "tema X ej Y" → read PDF → NL parser | **DONE (2026-04-17)** |
| **10** | TCL (sum of independent RVs), Multinomial, full test suite | **DONE (2026-04-18)** |
| **v2** | Local reasoning fallback + Consultas Teóricas + CustomPMF + invisibility gate | **DONE (2026-04-18)** |

## Sprint v2 — local fallback + Consultas Teóricas

Alcance **invisible** para el usuario final. Toda la infra técnica (`llm/`, `theory/`,
prompts, logs) vive solo en archivos técnicos; la UI no muestra ningún artefacto.

### Piezas nuevas

- `llm/ollama_client.py` — cliente único contra `http://127.0.0.1:11434`. Métodos
  `is_available()` (cache 30s), `chat(messages, json_mode=...)`, `embed(texts)`,
  `list_models()`. Config en `config/settings.py` (`OLLAMA_HOST/MODEL/TIMEOUT/...`).
  Primary `qwen2.5:14b-instruct`, fallback `qwen2.5:7b-instruct`, embeddings
  `nomic-embed-text`. Maneja `OllamaUnavailable` en silencio.
- `interpreter/nl_parser.py` — `_fallback_with_llm(text, regex_result)` +
  `_validate_llm_output(obj)`. Se invoca solo si el regex devolvió
  `need_more_info|error|unknown`. Gate `confidence ≥ 0.6` + validación de shape.
  Campo `_source` (privado) indica `"regex"|"llm"`; la UI lo ignora.
- `theory/machete_builder.py` — seed de `TEORIA/MACHETE.md` con fórmulas por tema
  (editable manualmente).
- `theory/rag_index.py` — RAG con PyMuPDF + `nomic-embed-text` + cosine en numpy.
  Fallback BM25-lite si no hay embeddings. Cache en `theory/_cache/rag_index.pkl`
  con invalidación por fingerprint de mtime+size.
- `theory/answerer.py` — compone respuesta teórica grounded por los chunks RAG.
  Si el servicio no responde o hay error, devuelve `"Respuesta no disponible
  momentáneamente."` sin explicación técnica.
- `ui/components/theory_ui.py` — modo `Consultas Teóricas` con `st.chat_input` y
  memoria en `st.session_state["theory_history"]` (capado a 12 turnos).
- `models/discrete/custom_pmf.py` — PMF casera con normalizador `k`.
  `CustomPMF(expr, domain, k_var="k")` con `eval()` en namespace restringido
  (`{abs, min, max, sqrt, exp, log, factorial, pi, e}`). Auto-normaliza con
  `k = Σ f(x) con k=1`. Registrado en `config/model_catalog.py`.
- Parser regex nuevo para PMF custom: detecta `P(X=x) = ...`, extrae dominio
  de `x ∈ {0,1,2,3}` y k_var. Si falta dominio → `need_more_info`.
- `_parse_tcl` extendido: captura `"3 mesas de 50 kg con desvío 2"` →
  `Component(name="Mesa", count=3, mean=50, variance=4)`.

### Scripts

- `scripts/bootstrap.bat` — verifica instalación local, pullea modelos,
  arranca el servicio en background. Log silencioso en `logs/bootstrap.log`.

### Tests nuevos (Sprint v2)

- `tests/test_ollama_client.py` — 4/4 (skip si servicio off).
- `tests/test_parser_llm_fallback.py` — 4/4.
- `tests/test_theory_flow.py` — 4/4 (machete + RAG + LaTeX + invisibilidad).
- `tests/test_ui_invisibility.py` — 4/4 (gate literal sobre archivos UI).
- `tests/test_regression_v2.py` — orquestador que encadena Sprints 7/9/10/v2.
- `tests/MANUAL_REGRESSION_CHECKLIST.md` — 20 flujos manuales UI.

### Extender

- Agregar palabra prohibida al gate de invisibilidad → `_FORBIDDEN_LITERALS` en
  `tests/test_ui_invisibility.py`.
- Cambiar modelo primario → env `OLLAMA_MODEL`.
- Rebuild machete → `python theory/machete_builder.py`.
- Rebuild RAG → borrar `theory/_cache/rag_index.pkl`.

### End-to-end

```bat
cd C:\Users\PC\Desktop\ESTADISTICA\APP
scripts\bootstrap.bat
C:\Python314\python tests\test_regression_v2.py
C:\Python314\python -m streamlit run app_streamlit.py
```

## Model formulas quick reference

**Discrete (implemented):**
- Binomial: `P(r) = C(n,r)*p^r*(1-p)^(n-r)` | E=np | V=np(1-p)
- Pascal: `P(n) = C(n-1,r-1)*p^r*(1-p)^(n-r)` | E=r/p | V=r(1-p)/p²
- Hipergeometrico: `P(r) = C(R,r)*C(N-R,n-r)/C(N,n)` | E=n*R/N | domain: max(0,n-(N-R)) ≤ r ≤ min(n,R)
- Hiper-Pascal: `P(n) = (r/n)*P_h(r/n;N;R)` | E=r*(N+1)/(R+1)
- Poisson: `P(r) = e^(-m)*m^r/r!` | E=V=m | uses MAX_SUMMATION_TERMS for infinite domain

**Continuous (implemented — Sprint 6):**
- Normal(mu, sigma): Z=(x-μ)/σ → Φ(Z); E=μ, V=σ², Mo=Me=μ, As=0, Ku=3
- LogNormal(m, D): Y=ln(x), Z=(Y-m)/D; E=e^(m+D²/2), Mo=e^(m-D²), Me=e^m
- Exponencial(lam): F=1-e^(-λx); E=1/λ, V=1/λ², As=2, Ku=9
- Gamma(r, lam): F=incomplete gamma; E=r/λ, V=r/λ², As=2/√r, Ku=3+6/r
- Weibull(beta, omega): F=1-e^(-(x/β)^ω); E=β·Γ(1+1/ω)
- GumbelMax/GumbelMin(beta, theta): F=e^(-e^(-z)) / F=1-e^(-e^z); E=θ±β·C (C=Euler)
- Pareto(theta, b): F=1-(θ/x)^b for x≥θ; E=bθ/(b-1) for b>1
- Uniforme(a, b): F=(x-a)/(b-a); E=(a+b)/2, V=(b-a)²/12

## Verification: known correct answers from the guide

When implementing models, verify against these:
- **Binomial**: Gb(3/10;0.25)=0.4744, Fb(4/12;0.45)=0.3044, Gb(10/14;0.75)=0.7415
- **Pascal**: Fpa(12/5;0.42)=0.6175, P(n≤8)=0.4967
- **Normal**: P(x<24000)=94.52%, P(x>840)=2.28%
- **Poisson**: P(r=0/m=5)=0.0067, Fg(20/4;0.3)=Gpo(4/6)=0.8488
- **Gamma**: P(x<150)=44.22%

## Parser de lenguaje natural (`interpreter/nl_parser.py`)

Parser regex/keywords para interpretar texto estadístico en texto libre → dict estructurado.
Sin dependencias externas ni API key. Se itera: cada modelo nuevo o ejemplo que "rompa" el flujo
debe agregar una regla acá y en el parser.

### Detección de modo (antes de buscar modelo)

El parser detecta en qué modo debe operar antes de buscar el modelo de distribución:

| Modo detectado | Señales |
|----------------|---------|
| **Datos Agrupados** | keywords: `ogiva`, `histograma`, `datos agrupados`, `fractil`, `cuartil`, `marca de clase`; o bien ≥3 patrones `X-Y` en el texto |
| **Probabilidad** | keywords fuertes: `bayes`, `a priori`, `a posteriori`, `probabilidad total`, `mutuamente excluyentes`, `complemento de`; o notación `P(A\|B)` / `P(A)=valor`; o ≥2 señales medias (`complemento`, `independientes`, `urna`, `bolillas`, `eventos`, `ambas`, `no producir nada`); o 2+ patrones `"probabilidad de ... es de X%"` en lenguaje natural |
| **Modelos de Probabilidad** | cualquier keyword de `MODELO_PATTERNS` o notación cátedra |

Si el parser detecta modo Datos Agrupados o Probabilidad, `streamlit_interpreter.py` llama a `apply_sc_to_session()` que cambia `st.session_state["app_mode"]` y pre-rellena los widgets correspondientes antes del `st.rerun()`.

### Cómo agregar soporte para un modelo nuevo

1. Agregar keywords en `MODELO_PATTERNS` dentro de `nl_parser.py`
2. Agregar patrones de extracción de params en `PARAM_PATTERNS`
3. Agregar params requeridos + preguntas de follow-up en `REQUIRED_PARAMS`
4. Si el modelo tiene notación cátedra propia (como `Fb()/Gb()/Pb()` para Binomial), agregar regex en `CATHEDRA_PATTERNS`
5. Testear con ejemplos reales de la Guia de ejercicios

### Modelos soportados actualmente

| Modelo | Keywords principales | Notación cátedra |
|--------|---------------------|-----------------|
| Binomial | `binomial`, `bernoulli`, `moneda`, `dado`, `ensayos independientes`, `con reposición`, `fallada/fallado`, `avería` | `Fb(r/n;p)`, `Gb(r/n;p)`, `Pb(r/n;p)` |
| Poisson | `poisson`, `llegadas`, `tasa de`, `lambda`, `m=N` | `Fpo(r/m)`, `Gpo(r/m)`, `Ppo(r/m)` |
| Pascal | `pascal`, `binomial negativa`, `hasta obtener`, `r-ésimo éxito` | `Fpa(n/r;p)`, `Gpa(n/r;p)`, `Ppa(n/r;p)` |
| Hipergeométrico | `hipergeometrico`, `sin reposición`, `lote`, `partida` | `Fh(r/n;N;R)`, `Gh(r/n;N;R)`, `Ph(r/n;N;R)` |
| Hiper-Pascal | `hiper-pascal` | `Fhpa(n/r;N;R)`, `Ghpa(n/r;N;R)`, `Phpa(n/r;N;R)` |

**Nota cátedra Pascal**: `Fpa(n/r;p)` — el primer número es el query (ensayos), el segundo es el param r (éxitos buscados).

### Ejemplos validados contra Tema III de la Guía de ejercicios

```
# Notación cátedra (bypass completo)
Fb(4/12;0.45)                              → cdf_left,  n=12, p=0.45, r=4
Gb(3/10;0.25)                              → cdf_right, n=10, p=0.25, r=3
Fb(4/8;0.60)                               → cdf_left,  n=8,  p=0.60, r=4
Gb(10/14;0.75)                             → cdf_right, n=14, p=0.75, r=10

# Parámetros explícitos
Binomial n=12 p=0.45, calcular F(4)        → cdf_left,  n=12, p=0.45, r=4
15 ensayos con p=0.4, acumulada hasta 6    → cdf_left,  n=15, p=0.4,  r=6

# Porcentajes
Un tirador tiene 80% de aciertos. En 8 disparos, exactamente 6   → probability, n=8,  p=0.80, r=6
Binomial 10 pruebas con 30% de exito, exactamente 4              → probability, n=10, p=0.30, r=4
Proceso con 1% de defectuosas, muestra de 10, encontrar alguna   → cdf_right,  n=10, p=0.01, r=1

# Lenguaje coloquial
Se lanza una moneda 15 veces, exactamente 4 caras                → probability, n=15, p=0.5, r=4
Moneda 20 veces, al menos 8 caras                                → cdf_right,  n=20, p=0.5, r=8
Proceso con 10% defectuosas, muestra de 15, 2 o menos           → cdf_left,   n=15, p=0.1, r=2

# Problemas compuestos (retornan status="compound")
15 cajas de 10 piezas con 2 defectuosas. De cada caja se toma muestra de 2,
se rechaza si hay alguna defectuosa. P(se rechacen menos de 3 cajas)
  → compound_type="hiper_binomial", box_N=10, box_R=2, sample_n=2,
    num_boxes=15, query_type="cdf_left", query_r=2

Pedido de 20 piezas buenas, 10% defectuosas. Luego de fabricar 25 piezas
no se había alcanzado. P(necesitar más de 30 piezas)
  → compound_type="pascal_conditional", r_success=20, p=0.9,
    condition_n=25, query_n=30
```

### Patrones clave en el parser (no obvios)
- `"alguna"` → `cdf_right` con `r=1` (al menos una)
- `"hasta N"` → `cdf_left` con `r=N`
- `"N o menos"` → `cdf_left` con `r=N`; `"N o más"` → `cdf_right` con `r=N`
- `"N%"` → `p = N/100` (solo si el texto tiene `%` y p >= 1)
- Moneda → `p=0.5` automático; Dado → `p=1/6` automático
- `"disparos"`, `"unidades"`, `"latas"`, `"piezas"` → todos mapean a `n`
- `"fallada/fallado/fallo"` → detecta Binomial (defectos/fallas)
- 3+ patrones `X-Y` en el texto → modo Datos Agrupados (sin necesitar keyword explícita)
- `"bayes"`, `"a priori"`, `"probabilidad total"` → modo Probabilidad (Bayes)
- 2+ señales de evento (P(A|B), complemento, urna, ambas, etc.) → modo Probabilidad de eventos
- 2+ patrones "probabilidad de ... es de X%" → modo Probabilidad de eventos (extracción NL: "ambas" → P(A∩B), "nada" → P(A'∩B'), resto → marginales)

### Ejemplos que rompen el flujo (a corregir con reglas nuevas)

_Agregar acá cuando se encuentren durante el desarrollo._
