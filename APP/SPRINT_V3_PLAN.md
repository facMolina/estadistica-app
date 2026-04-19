# Sprint v3 — Pestaña "Cálculos extra" (registry extensible)

> **Estado:** planificado, **NO ejecutado**.
> Ejecutar cuando el usuario lo apruebe.

## Context

El usuario está resolviendo ejercicios del tipo:

> *"La multa es de $2000 fijos por partido, más $1500 adicionales por cada falta técnica. ¿Cuál es el costo esperado por partido?"*

Esto es `E(a + b·X)` — el cálculo es trivial por linealidad de la esperanza (`a + b·E(X)`), pero la app no lo expone: hoy hay que ir al tab Características, leer `E(X)` y hacer la cuenta a mano. Pasa con cualquier modelo (Binomial, Poisson, CustomPMF, Normal, Exponencial…) en problemas de costo, multa, premio, ingreso, indemnización, etc.

El usuario pide una pestaña dedicada **"Cálculos extra"** preparada para iterar — que **sirva ahora** para `E(a + b·X)` y que mañana podamos sumarle más calculadoras (transformaciones cuadráticas, esperanza condicional, MGF, función de utilidad, etc.) sin tener que rediseñar la UI cada vez.

Decisión de alcance (confirmada): aparece en **discretas estándar + CustomPMF + continuas**. Multinomial y TCL quedan fuera (no tienen un E(X) escalar canónico).

Decisión de fórmula (1ra iteración): solo **lineal `g(X) = a + b·X`**. Lineal cubre el 95% de los casos y vale para cualquier modelo con `mean()` y `variance()`. La cuadrática `+c·X²` para discretas es directa (Σ g(x)²·P(x)) pero para continuas necesita E(X³), E(X⁴) — scope creep. La dejamos para una segunda iteración como otra calculadora aparte si surge la necesidad.

## Diseño: registry extensible

```
ui/components/extras/
    __init__.py          # exporta render_extras_tab + EXTRA_CALCULATORS
    _base.py             # clase abstracta ExtraCalculator
    linear_transform.py  # 1ra calculadora: E(a + b·X), V(a + b·X)
    _registry.py         # lista de calculadoras registradas
```

**Contrato (`_base.py`)**

```python
class ExtraCalculator(ABC):
    name: str           # ej: "Esperanza de a + b·X"
    short_name: str     # ej: "E(a + bX)"  (para tabs/selectbox)
    description: str    # ayuda contextual
    # families soportadas: subset of {"discrete", "custom_pmf", "continuous"}
    families: set[str]

    def applies_to(self, family: str, model) -> bool:
        # default: family in self.families
        ...

    @abstractmethod
    def render(self, model, model_label: str, detail_level: int) -> None: ...
```

**Dispatcher (`__init__.py`)**

```python
def render_extras_tab(model, model_label: str, family: str, detail_level: int):
    apps = [c for c in EXTRA_CALCULATORS if c.applies_to(family, model)]
    if not apps:
        st.info("No hay cálculos extra disponibles para este modelo.")
        return
    if len(apps) == 1:
        apps[0].render(model, model_label, detail_level)
    else:
        choice = st.selectbox("Cálculo", [c.short_name for c in apps],
                              format_func=lambda s: s,
                              help="Calculadoras adicionales sobre la distribución actual")
        sel = next(c for c in apps if c.short_name == choice)
        st.caption(sel.description)
        sel.render(model, model_label, detail_level)
```

`family` lo manda el call site (`"discrete"`, `"custom_pmf"`, `"continuous"`) — así una calculadora puede aplicar selectivamente sin tener que importar y `isinstance`-checkear cada modelo.

## Calculadora #1 — `linear_transform.py`

**`LinearTransformCalculator`** — `families = {"discrete", "custom_pmf", "continuous"}`.

UI (st.number_input): `a` (default 0.0), `b` (default 1.0). Etiqueta libre opcional para `g` (default "g").

Render:

1. **Fórmula**: `g(X) = a + b·X` (LaTeX).
2. **Inputs sustituidos**: ej. `Multa(X) = 2000 + 1500·X`.
3. **Esperanza** — `StepBuilder` con 3 pasos:
   - L1: `E(g(X)) = E(a + b·X) = a + b·E(X)` (linealidad).
   - L2: leer `E(X)` con `model.mean().final_value`, sustituir.
   - L1: resultado numérico + LaTeX.
4. **Varianza** — `StepBuilder` con 3 pasos:
   - L1: `V(g(X)) = V(a + b·X) = b²·V(X)` (la constante `a` no aporta).
   - L2: leer `V(X)` con `model.variance().final_value`, sustituir.
   - L1: resultado + `σ_g = |b|·σ_X`.
5. **Render con `render_calc_result`** (ya estandarizado).
6. Para CustomPMF/discretas con dominio chico (≤20 valores), opcionalmente mostrar una mini-tabla `x | P(x) | g(x) | g(x)·P(x)` para que el alumno vea la suma — útil pedagógicamente. Detrás de un `st.expander("Ver tabla x → g(x)")`. Skip para continuas.

Validaciones:
- Si `model.mean()` o `model.variance()` lanza/devuelve NaN, mostrar `st.error` y abortar.
- `a` y `b` aceptan negativos y decimales.

## Archivos a tocar

### Nuevos

| Archivo | Contenido |
|---|---|
| `APP/ui/components/extras/__init__.py` | exporta `render_extras_tab(model, model_label, family, detail_level)` y `EXTRA_CALCULATORS` |
| `APP/ui/components/extras/_base.py` | `ExtraCalculator` (ABC) |
| `APP/ui/components/extras/_registry.py` | `EXTRA_CALCULATORS = [LinearTransformCalculator()]` |
| `APP/ui/components/extras/linear_transform.py` | calculadora `E(a+bX)` + `V(a+bX)` |

### Existentes

1. **`APP/app_streamlit.py`** — flujo discreto estándar (líneas ~540 y ~614)
   - Cambiar `st.tabs([... "Aproximaciones"])` → agregar `"Cálculos extra"` (6ta tab).
   - Después del bloque `with tab_approx:`, agregar:
     ```python
     with tab_extras:
         render_extras_tab(model, f"{modelo}({title_params})", "discrete", detail_level)
     ```
   - Import en el header: `from ui.components.extras import render_extras_tab`.

2. **`APP/ui/components/custom_pmf_ui.py`** — línea 256
   - 4 → 5 tabs: `tab_calc, tab_chars, tab_table, tab_graphs, tab_extras = st.tabs([..., "Cálculos extra"])`.
   - Bloque `with tab_extras:` con `render_extras_tab(model, f"CustomPMF({cfg.get('expr', model.expr)})", "custom_pmf", detail_level)`.

3. **`APP/ui/components/continuous_ui.py`** — línea 252
   - 4 → 5 tabs.
   - Bloque `with tab_extras:` con `render_extras_tab(model, f"{modelo}({title_params})", "continuous", detail_level)`.

### Tests

**`APP/tests/test_qa_smoke.py`** — agregar bloque al final de `qa_custom_pmf` o sección nueva `[13] Cálculos extra`:

```python
from ui.components.extras import EXTRA_CALCULATORS
from ui.components.extras.linear_transform import LinearTransformCalculator

# Smoke import
_check("import extras tab", any(isinstance(c, LinearTransformCalculator)
                                 for c in EXTRA_CALCULATORS))

# E(2000 + 1500·X) sobre PMF (x²-x+2)/30 dom {0..4} (ej del usuario)
m = CustomPMF(expr="(x**2 - x + 2)/k", domain=[0,1,2,3,4])
calc = LinearTransformCalculator()
e_g = calc.compute_expectation(m, a=2000.0, b=1500.0).final_value  # helper testeable
v_g = calc.compute_variance(m, a=2000.0, b=1500.0).final_value
_check("E(2000+1500X) = 6500", _close(e_g, 6500.0, 1e-6), f"E={e_g}")
_check("V(2000+1500X) = 1500²·1.8 = 4_050_000",
       _close(v_g, 4_050_000.0, 1e-3), f"V={v_g}")

# Sobre Binomial(10, 0.5): E(X)=5, V(X)=2.5 → E(2000+1500X)=9500
b = Binomial(n=10, p=0.5)
e_g2 = calc.compute_expectation(b, a=2000.0, b=1500.0).final_value
_check("Binomial E(2000+1500X) = 9500", _close(e_g2, 9500.0, 1e-6), f"E={e_g2}")

# Sobre Normal(mu=10, sigma=2): E(3+2X) = 23, V = 4·4 = 16
from models.continuous.normal import Normal
n = Normal(mu=10, sigma=2)
v_g3 = calc.compute_variance(n, a=3.0, b=2.0).final_value
_check("Normal V(3+2X) = 16", _close(v_g3, 16.0, 1e-6), f"V={v_g3}")
```

Para que el test sea posible sin levantar Streamlit, la calculadora expone dos métodos puros (`compute_expectation(model, a, b) -> CalcResult`, `compute_variance(model, a, b) -> CalcResult`) que **`render(...)` reusa internamente**. Esto evita acoplar el test al render de Streamlit.

También sumar `"ui.components.extras"` a la lista de imports validados en `qa_ui_imports`.

## Funciones/utilities reusados (no se duplican)

- `calculation/step_engine.py::StepBuilder` — construir el árbol de steps.
- `calculation/statistics_common.py::format_number` — formateo de números.
- `ui/components/step_display.py::render_calc_result` — render estándar.
- `model.mean()`, `model.variance()` de `DiscreteModel`/`ContinuousBase`/`CustomPMF`.

## Verificación end-to-end

```bat
cd C:\Users\PC\Desktop\ESTADISTICA\APP
C:\Python314\python tests\test_qa_smoke.py
```
Esperado: **59/59 OK** (55 actuales + 4 nuevos del extras).

Smoke manual en `http://localhost:8501`:
1. **CustomPMF** — pegar `P(X=x)=(x²-x+2)/k para x en {0,1,2,3,4}`. Ir al nuevo tab **"Cálculos extra"** → `a=2000, b=1500` → debe mostrar `E(g(X)) = 2000 + 1500·3 = 6500` con steps.
2. **Binomial** — sidebar `n=10, p=0.5`. Tab Cálculos extra → `a=0, b=1` (default) → debe mostrar `E(X)=5`. Cambiar `a=2000, b=1500` → `9500`.
3. **Normal** — `μ=10, σ=2`. Tab Cálculos extra → `a=3, b=2` → `E(g)=23`, `V(g)=16`, `σ_g=4`.
4. Verificar que el tab aparece **también en Poisson, Pascal, Hipergeométrico, Hiper-Pascal, Exponencial, Gamma, Weibull, etc.** (todas las distribuciones con `mean()` y `variance()`).
5. Verificar que el tab **NO aparece** en Multinomial, TCL, Datos Agrupados, Probabilidad, Consultas Teóricas (no se tocan esos flujos).

## Cómo agregar la próxima calculadora

1. Crear `APP/ui/components/extras/<nombre>.py` con clase que herede `ExtraCalculator`.
2. Registrarla en `_registry.py` apendendo a `EXTRA_CALCULATORS`.
3. Listo — aparece automáticamente en el selectbox de la pestaña en cada flujo donde `applies_to` matchee.

Ejemplos pensados (no implementar ahora):
- `QuadraticTransform` — `E(a + bX + cX²)` para discretas (Σ g(x)²·P(x)).
- `MGFEvaluator` — `M_X(t) = E(e^{tX})`.
- `UtilityCalculator` — `E(u(X))` con `u(x)` parsable (logarítmica, exponencial, etc.).
- `ProbabilityOfTransformation` — `P(g(X) > c)` resolviendo en términos de X.
