# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

A Python app that solves Statistics exercises (UADE - Ing. Sergio Anibal Dopazo) showing the **full step-by-step workings** of each calculation. Two phases:

1. **Phase 1 - CLI** (`main.py`, pending): User describes the problem in natural text → Claude API interprets it → identifies the probability model → extracts parameters → launches the web interface.
2. **Phase 2 - Web** (`app_streamlit.py`): Streamlit interface with 4 tabs: step-by-step calculation, model characteristics, full distribution table, interactive Plotly graphs.

## Running the app

```bash
# From APP/
source .venv/bin/activate          # Python 3.13.6 virtualenv already created
streamlit run app_streamlit.py     # Opens at http://localhost:8501
```

The `.env` file (pending creation) must contain `ANTHROPIC_API_KEY` for the CLI phase.

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
4. Register the model in `app_streamlit.py` sidebar selector and instantiation block.

**Reference implementation**: `models/discrete/binomial.py` — the only completed model, use it as the template for all others.

## Useful utilities in `calculation/`

- `combinatorics.py`: `comb(n,r)` (cached), `comb_with_steps(n,r)` → `CalcResult` with full factorial breakdown.
- `statistics_common.py`: generic discrete distribution helpers — `compute_cdf_left_discrete`, `compute_cdf_right_discrete`, `compute_partial_expectation_left/right`, `find_mode_discrete`, `find_median_discrete`, `build_full_table_discrete`, `format_number`, `format_fraction`.
- `settings.py`: `DETAIL_MAX=3`, `DETAIL_INTERMEDIATE=2`, `DETAIL_BASIC=1`, `MAX_SUMMATION_TERMS=1000`, `EPSILON=1e-10`, `EULER_MASCHERONI`, paths to TEORIA/ and the guide PDF.

## UI rendering

- `ui/components/step_display.py`: renders a `CalcResult` using `st.expander` for sub-steps.
- `ui/components/summary_panel.py`: renders `all_characteristics()` dict.
- `ui/components/graph_panel.py`: 3 Plotly charts — stem plot for P(r), step functions for F(r) and G(r).
- `ui/components/table_panel.py`: DataFrame from `full_table()` + CSV download.
- `display/graph_builder.py`: `build_probability_polygon()` and `build_cdf_plot()` — Plotly figure factories.

## Pending sprints (in order)

| Sprint | Content |
|--------|---------|
| **5** | Discrete models: Pascal, Hipergeometrico, Hiper-Pascal, Poisson, Multinomial |
| **6** | Continuous models: Normal, Log-Normal, Exponential, Gamma/Erlang, Weibull, Uniform, Gumbel Min/Max, Pareto |
| **7** | Approximations engine + TCL (Hyper→Binom, Binom→Normal, Binom→Poisson, Poisson→Normal, Gamma→Normal) |
| **8** | CLI with Claude API (`main.py`, `interpreter/`) |
| **9** | Guide mode: parse "tema X ej Y" → read PDF → send to Claude API |
| **2/3** | Topic I (Data Processing) and Topic II (Basic Probability) — deprioritized |

## Model formulas quick reference

**Discrete (pending):**
- Pascal: `P(n) = C(n-1,r-1)*p^r*(1-p)^(n-r)` | E=r/p | V=r(1-p)/p²
- Hipergeometrico: `P(r) = C(R,r)*C(N-R,n-r)/C(N,n)` | E=n*R/N | domain: max(0,n-(N-R)) ≤ r ≤ min(n,R)
- Hiper-Pascal: `P(n) = (r/n)*P_h(r/n;N;R)` | E=r*(N+1)/(R+1)
- Poisson: `P(r) = e^(-m)*m^r/r!` | E=V=m | use MAX_SUMMATION_TERMS for infinite domain

**Continuous (pending):** Normal (Z-standardization), Log-Normal, Exponential, Gamma/Erlang, Weibull, Gumbel Min/Max, Pareto, Uniform. Use `scipy.stats` for CDFs; show the transformation step-by-step.

## Verification: known correct answers from the guide

When implementing models, verify against these:
- **Binomial**: Gb(3/10;0.25)=0.4744, Fb(4/12;0.45)=0.3044, Gb(10/14;0.75)=0.7415
- **Pascal**: Fpa(12/5;0.42)=0.6175, P(n≤8)=0.4967
- **Normal**: P(x<24000)=94.52%, P(x>840)=2.28%
- **Poisson**: P(r=0/m=5)=0.0067, Fg(20/4;0.3)=Gpo(4/6)=0.8488
- **Gamma**: P(x<150)=44.22%
