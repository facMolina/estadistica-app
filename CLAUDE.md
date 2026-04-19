# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## First step on every session

Before doing anything else, **read `README.md`** at this same level. It contains
the canonical instructions to prepare the environment and launch the app
(`start.bat` on Windows, `./start.sh` on macOS/Linux), plus troubleshooting for
the most common failure modes. Use it as the source of truth when the user
asks "how do I run this?" or when you need to start the app as part of a task.

## What this project is

A Python/Streamlit app that solves Statistics exercises (UADE - Ing. Sergio Anibal Dopazo) showing full **step-by-step workings** of each calculation. The web UI works offline with no API key; the CLI mode uses the Anthropic API.

All application code lives in `APP/`. Theory PDFs are in `TEORIA/`. The exercise guide PDF is at the repo root.

## Running the app locally

All commands must be run from `APP/`. Requires **Python 3.9+**.

### Windows

```bat
cd C:\Users\PC\Desktop\ESTADISTICA\APP

:: Install dependencies (once)
C:\Python314\python -m pip install -r requirements.txt

:: Web UI (no API key required, works offline)
C:\Python314\python -m streamlit run app_streamlit.py

:: CLI mode (requires ANTHROPIC_API_KEY in APP/.env)
C:\Python314\python main.py
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
```

The app opens automatically at `http://localhost:8501`.

**Note (Windows):** The `.venv` in `APP/` was originally created on macOS and does not work on Windows — packages must be installed directly into the system Python (`C:\Python314\python`).

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

Standalone tests (no pytest required) live in `APP/tests/`. Run from `APP/`:

```bat
C:\Python314\python tests/test_approximations.py
```

Expected: 7/7 OK. Key verified value: `Fg(20/4;0.3)=0.8488` via Wilson-Hilferty.

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
