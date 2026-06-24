# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## First step on every session

Before doing anything else, **read `README.md`** at this same level. It contains
the canonical instructions to prepare the environment and launch the app
(`start.bat` on Windows, `./start.sh` on macOS/Linux), plus troubleshooting for
the most common failure modes. Use it as the source of truth when the user
asks "how do I run this?" or when you need to start the app as part of a task.

## Workflow rule — leave the app running

After finishing any feature or sprint, leave Streamlit running in the background so the user can test immediately. Default port `8501`; if taken, try `8502+` and report which URL. Do not kill the process at the end of the turn.

## What this project is

A Python/Streamlit app that solves Statistics exercises (UADE - Ing. Sergio Anibal Dopazo) showing full **step-by-step workings** of each calculation. The web UI works offline with no API key; the CLI mode uses the Anthropic API.

All application code lives in `APP/`. Theory PDFs are in `TEORIA/`. The exercise guide PDF is at the repo root.

## App modes (sidebar)

| Mode | Entry point | Purpose |
|------|-------------|---------|
| Modelos de Probabilidad | `app_streamlit.py` + `ui/components/continuous_ui.py` | Discrete (5) + continuous (9) + Multinomial + CustomPMF |
| Datos Agrupados | `ui/components/data_processing_ui.py` | Tabla de frecuencias, media/var/CV, mediana, fractil, histograma, ogiva |
| Probabilidad | `ui/components/probability_ui.py` | Two-event solver + Bayes / Probabilidad Total |
| TCL / Suma de VA | `ui/components/tcl_ui.py` | Suma de independientes + aprox. normal |
| Consultas Teóricas | `ui/components/theory_ui.py` | RAG sobre `TEORIA/` + Ollama |
| Formulario / Reconocimiento | `ui/components/formulario_ui.py` | Referencia estática offline, sin cálculo: tabla "qué distribución uso", reglas de derivación de parámetros, plantillas, tabla Z, errores comunes — con buscador por palabra clave |

## Running the app locally

For day-to-day use, double-click `start.bat` (Windows) or run `./start.sh` (macOS/Linux) from the repo root. The scripts set up Ollama, precargan el modelo y lanzan Streamlit en `http://localhost:8501`.

When you need to invoke Python directly (debugging, one-off tests), use the commands below. All commands must be run from `APP/`. Requires **Python 3.9+**.

### Windows

```bat
cd C:\Users\PC\Documents\estadistica-app\APP

:: Install dependencies (once)
C:\Python314\python -m pip install -r requirements.txt

:: Web UI (no API key required, works offline)
C:\Python314\python -m streamlit run app_streamlit.py

:: CLI mode (requires ANTHROPIC_API_KEY in APP/.env)
C:\Python314\python main.py
C:\Python314\python main.py --streamlit
```

### macOS / Linux

```bash
cd /path/to/ESTADISTICA/APP

# Create and activate virtual environment (recommended, once)
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies (once)
pip install -r requirements.txt

# Web UI (no API key required, works offline)
python -m streamlit run app_streamlit.py

# CLI mode (requires ANTHROPIC_API_KEY in APP/.env)
python main.py
python main.py --streamlit
```

The app opens automatically at `http://localhost:8501`.

**Note (Windows):** The `.venv` in `APP/` was originally created on macOS and does not work on Windows — packages must be installed directly into the system Python (`C:\Python314\python`).

## Optional: Ollama (local LLM)

Two features degrade silently without a local Ollama service:

- **Consultas Teóricas** — returns "Respuesta no disponible momentáneamente."
- **NL parser LLM fallback** — the regex parser still runs; only the smart retry is skipped.

Setup (once): install Ollama, then `ollama pull qwen3:8b` and `ollama pull nomic-embed-text`. The `start.bat` / `start.sh` scripts handle the service lifecycle. Config lives in `APP/config/settings.py` (`OLLAMA_HOST`, `OLLAMA_MODEL=qwen3:8b`, fallback `qwen2.5:14b-instruct`).

**Qwen3 thinking mode:** `qwen3:8b` reasons by default (separate `message.thinking` field in Ollama's `/api/chat` response — never leaks into `message.content`, even in `json_mode`). `OllamaClient.chat()` accepts a `think: bool | None` param (maps to Ollama's `think` request field, supported since 0.30); the NL parser's LLM fallback (`interpreter/nl_parser.py::_fallback_with_llm`) passes `think=False` because the thinking pass adds ~10s/call with no benefit for a strict-JSON contract — confirmed via `tests/test_guide_corpus.py` (180-exercise corpus, ~48 LLM fallbacks): 8m39s with `think=False` vs. 35+ min stalled with thinking on. `theory/answerer.py`'s free-text RAG answers keep thinking on (single ad-hoc query, not batch, possible quality benefit).

There is no manual on/off toggle — the app always attempts to use Ollama; if the service isn't running, `OllamaClient.is_available()`'s ping fails and the two features above degrade silently. The word "Ollama" is intentionally absent from any file under `ui/` (see `tests/test_ui_invisibility.py`'s literal-scan gate).

## Architecture overview

The central design pattern is that **every calculation returns a `CalcResult`** (never a plain number). This carries a tree of `Step` objects plus `final_value` and `final_latex`.

```
User input (sidebar widgets or NL text)
        ↓
NLParser (interpreter/nl_parser.py)   ← regex/keywords, no API key
        ↓ structured dict
Model class (models/discrete/*.py)
        ↓ CalcResult
UI components (ui/components/)        ← render steps, graphs, table
```

**Step filtering**: each `Step` has `detail_level_min` (1=always, 2=intermediate+, 3=max only). `CalcResult.get_steps_for_level(n)` filters recursively. The sidebar dropdown controls which level the user sees.

**`StepBuilder`** (`calculation/step_engine.py`): builder pattern with stack-based nesting. `add_step()` / `add_substep()` / `merge_result()` compose the tree. `build()` returns a `CalcResult`.

**Model base classes** (`models/base.py`): `DiscreteModel` and `ContinuousModel` (abstract). Completed discrete models: Binomial, Poisson, Pascal, Hipergeometrico, Hiper-Pascal — use `binomial.py` as the template.

**NL interpreter** (`interpreter/nl_parser.py`): pure regex/keyword parser in 5 phases — cathedra notation bypass → guide exercise detection (step 0.3) → compound detection (step 0.5) → model detection → parameter extraction → query type detection. Multi-turn: returns `need_more_info` with a follow-up question when parameters are missing. Can also return `status: "compound"` for chained distributions (hiper+binomial, pascal conditional) dispatched via `calculation/compound_solver.py`, or `status: "guide_exercise"` for references like "tema III ejercicio 8" resolved via `guide_index/`.

**Approximations engine** (`approximations/approximator.py`): `try_approximations(model_name, params, query_type, query_params)` returns a list of `ApproximationResult` (both safe and unsafe applications, with ✅/⚠️ badges). Implemented: Hiper→Bi, Bi→N (continuity correction), Bi→Po, Po→N (cc), Gamma→N (Wilson-Hilferty). Shown as the extra tab in the discrete/continuous flows.

## Running tests

Standalone tests (no pytest) live in `APP/tests/`. Run from `APP/`.

Full regression (covers Sprints 7/9/10/v2):

```bat
C:\Python314\python tests\test_regression_v2.py
```

Focused suites:

- `test_approximations.py` — Sprint 7 engine, 7/7 OK, key value `Fg(20/4;0.3)=0.8488`.
- `test_guide_corpus.py` — itera los 180 ejercicios de la guía, escribe `coverage_report.md`.
- `test_guide_index.py` — indexador del PDF (8/8 OK).
- `test_sprint10.py` — Multinomial + TCL (8/8 OK).
- `test_theory_flow.py`, `test_ollama_client.py`, `test_ui_invisibility.py`, `test_parser_llm_fallback.py` — Sprint v2 (skip si Ollama está off).
- `test_examenes_2do_parcial.py` — 2º parcial: resuelve los modelos/parciales reales de `EJEMPLOS/` end-to-end (derivación de parámetros, redondeo cátedra, Bayes continuo, esperanza condicional). 9/9 OK. No está encadenado en `test_regression_v2.py`; correr suelto.
- `MANUAL_REGRESSION_CHECKLIST.md` — 20 flujos UI a pasar a mano.

## Detailed guidance

`APP/CLAUDE.md` contains the full reference for this codebase:
- Step-by-step instructions for adding a new discrete or continuous model (4 files to update)
- All utility functions in `calculation/`
- NL parser extension points (`MODELO_PATTERNS`, `CATHEDRA_PATTERNS`, `PARAM_PATTERNS`, `REQUIRED_PARAMS`)
- Pending sprints and their scope
- Known-correct answers from the exercise guide for verification
- Model formulas quick reference (all discrete and continuous distributions)
- Approximation conditions table
- Parser examples that break the flow (to fix with new rules)

Other historical / forward-looking docs at the repo root:
- `context.md` — longer-form project notes, decisions, and pending backlog.

## Current implementation status

| Component | Status |
|-----------|--------|
| Step engine (`calculation/`) | Done |
| Binomial, Poisson, Pascal, Hipergeometrico, Hiper-Pascal | Done |
| Datos Agrupados (mean, variance, CV, median, fractile, ogive). Frequency table in cátedra notation (Li, Ls, Ci, fai, fi, Fai, Fi, Gai, Gi, Ci·fai, (Ci−x̄)²·fai) | Done |
| Probabilidad: generic two-event solver (any combination of P(A), P(B), P(A∩B), P(A∪B), P(A'∩B'), P(A\|B), P(B\|A)) + Bayes/Total Probability | Done |
| NL parser — all 4 modes (distributions, datos agrupados, probabilidad de eventos, Bayes) + 5 discrete + NL probability extraction | Done |
| Streamlit UI — 4 modes, 4 tabs for distributions | Done |
| CLI with Claude API | Done |
| Continuous models (Normal, Log-Normal, Exponential, Gamma/Erlang, Weibull, Gumbel Max/Min, Pareto, Uniforme) | Done (Sprint 6) |
| Compound problems (hiper+binomial, pascal conditional) | Done |
| Approximations engine (Hiper→Bi, Bi→N cc, Bi→Po, Po→N cc, Gamma→N Wilson-Hilferty) + tests + UI tab | Done (Sprint 7) |
| Guide PDF exercise mode ("tema III ejercicio 8" → extract enunciado → NL parser) | Done (Sprint 9) |
| Multinomial (discrete multivariate) + TCL / Sum of RVs module + guide corpus test suite | Done (Sprint 10) |
| CustomPMF + local reasoning fallback + Consultas Teóricas (RAG + LaTeX) + invisibility gate — optional local service, app degrades silently without it | Done (Sprint v2) |
| 2º parcial: cátedra rounding (`statistics_common._custom_round`, half-up ≥5) + Z-table (`calculation/normal_table.py`) + parameter derivation from indirect data (`models/continuous/derivations.py`: percentiles, mean+variance, mean+mode, mean+rate...) + cátedra step-by-step for Normal/Log-Normal (table lookup) and Gamma (Poisson method / Wilson-Hilferty) + conditional expectation (tail/cap) + Bayes continuo (`probability/bayes_continuo.py`) + Formulario mode | Done (2026-06-23) |
| Sprint v3: extensible "Cálculos extra" tab (`ui/components/extras/`, registry pattern) — `LinearTransformCalculator` for `E(a+b·X)`/`V(a+b·X)`, wired into discrete, CustomPMF and continuous flows | Done (2026-06-23) |
