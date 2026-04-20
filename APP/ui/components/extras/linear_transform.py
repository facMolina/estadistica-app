"""Calculadora: E(a + b·X), V(a + b·X) por linealidad de la esperanza."""

from __future__ import annotations

import math

import streamlit as st

from calculation.statistics_common import format_number
from calculation.step_engine import StepBuilder
from calculation.step_types import CalcResult
from ui.components.extras._base import ExtraCalculator
from ui.components.step_display import render_calc_result


def _fmt(v: float) -> str:
    return format_number(v)


def _is_nan(v) -> bool:
    try:
        return v is None or math.isnan(float(v))
    except (TypeError, ValueError):
        return True


class LinearTransformCalculator(ExtraCalculator):
    """`g(X) = a + b·X` — calcula E(g(X)) y V(g(X)) con paso a paso.

    Vale para cualquier modelo con ``mean()`` y ``variance()``. La fórmula no
    depende del modelo: E(a + bX) = a + b·E(X) por linealidad, y
    V(a + bX) = b²·V(X) porque la constante no aporta varianza.
    """

    name = "Esperanza y varianza de a + b·X"
    short_name = "E(a + bX)"
    description = (
        "Transformación lineal de la variable: "
        "E(a + b·X) = a + b·E(X) y V(a + b·X) = b²·V(X)."
    )
    families = {"discrete", "custom_pmf", "continuous"}

    # ------------------------------------------------------------------
    # Cálculo puro — testeable sin Streamlit
    # ------------------------------------------------------------------

    def compute_expectation(
        self, model, a: float, b: float, *, g_label: str = "g"
    ) -> CalcResult:
        mean_res = model.mean()
        mu = float(mean_res.final_value) if mean_res.final_value is not None else float("nan")

        sb = StepBuilder(f"E({g_label}(X))")
        sb.add_step(
            "Linealidad de la esperanza",
            latex=rf"E({g_label}(X)) = E(a + b \cdot X) = a + b \cdot E(X)",
            latex_sub=rf"a = {_fmt(a)},\quad b = {_fmt(b)}",
            latex_res="",
            level_min=1,
        )
        sb.add_step(
            "Lectura de E(X) del modelo",
            latex=r"E(X) = \mu_X",
            latex_sub=rf"E(X) = {_fmt(mu)}",
            latex_res=rf"E(X) = {_fmt(mu)}",
            result=mu,
            level_min=2,
        )
        eg = a + b * mu
        sb.add_step(
            f"Resultado de E({g_label}(X))",
            latex=rf"E({g_label}(X)) = a + b \cdot E(X)",
            latex_sub=rf"E({g_label}(X)) = {_fmt(a)} + {_fmt(b)} \cdot {_fmt(mu)}",
            latex_res=rf"E({g_label}(X)) = {_fmt(eg)}",
            result=eg,
            level_min=1,
        )
        return sb.build(final_value=eg, final_latex=_fmt(eg))

    def compute_variance(
        self, model, a: float, b: float, *, g_label: str = "g"
    ) -> CalcResult:
        var_res = model.variance()
        var = float(var_res.final_value) if var_res.final_value is not None else float("nan")

        sb = StepBuilder(f"V({g_label}(X))")
        sb.add_step(
            "Varianza de una transformación lineal",
            latex=rf"V({g_label}(X)) = V(a + b \cdot X) = b^2 \cdot V(X)",
            latex_sub=rf"a = {_fmt(a)} \text{{ no aporta varianza}};\quad b = {_fmt(b)}",
            latex_res="",
            level_min=1,
        )
        sb.add_step(
            "Lectura de V(X) del modelo",
            latex=r"V(X) = \sigma^2_X",
            latex_sub=rf"V(X) = {_fmt(var)}",
            latex_res=rf"V(X) = {_fmt(var)}",
            result=var,
            level_min=2,
        )
        vg = (b ** 2) * var
        sigma_g = math.sqrt(vg) if vg >= 0 and not _is_nan(vg) else float("nan")
        sb.add_step(
            f"Resultado de V({g_label}(X))",
            latex=rf"V({g_label}(X)) = b^2 \cdot V(X)",
            latex_sub=rf"V({g_label}(X)) = ({_fmt(b)})^2 \cdot {_fmt(var)}",
            latex_res=(
                rf"V({g_label}(X)) = {_fmt(vg)},\quad "
                rf"\sigma_{{{g_label}}} = |b| \cdot \sigma_X = {_fmt(sigma_g)}"
            ),
            result=vg,
            level_min=1,
        )
        return sb.build(final_value=vg, final_latex=_fmt(vg))

    # ------------------------------------------------------------------
    # Render Streamlit
    # ------------------------------------------------------------------

    def render(self, model, model_label: str, detail_level: int) -> None:
        st.subheader(f"Transformación lineal — {model_label}")
        st.caption(self.description)

        c1, c2, c3 = st.columns([1, 1, 1])
        with c1:
            a = st.number_input(
                "a (constante)",
                value=0.0,
                step=1.0,
                format="%.4f",
                key="extras_linear_a",
            )
        with c2:
            b = st.number_input(
                "b (coeficiente de X)",
                value=1.0,
                step=1.0,
                format="%.4f",
                key="extras_linear_b",
            )
        with c3:
            g_label = st.text_input(
                "Nombre de g(X)",
                value="g",
                max_chars=12,
                key="extras_linear_label",
            )
        g_label = (g_label or "g").strip() or "g"

        try:
            mean_val = model.mean().final_value
            var_val = model.variance().final_value
        except Exception as exc:
            st.error(f"No se pudo obtener E(X) y V(X) del modelo: {exc}")
            return

        if _is_nan(mean_val) or _is_nan(var_val):
            st.error(
                "El modelo actual no expone E(X) o V(X) numéricos; "
                "la transformación lineal no se puede calcular."
            )
            return

        st.markdown("**Fórmula planteada**")
        st.latex(rf"{g_label}(X) = a + b \cdot X")
        st.latex(rf"{g_label}(X) = {_fmt(a)} + {_fmt(b)} \cdot X")

        st.markdown("---")
        st.markdown(f"**Esperanza — E({g_label}(X))**")
        e_res = self.compute_expectation(model, float(a), float(b), g_label=g_label)
        render_calc_result(e_res, detail_level)

        st.markdown("---")
        st.markdown(f"**Varianza — V({g_label}(X))**")
        v_res = self.compute_variance(model, float(a), float(b), g_label=g_label)
        render_calc_result(v_res, detail_level)

        self._maybe_render_pointwise_table(model, a, b, g_label)

    # ------------------------------------------------------------------
    # Tabla pedagógica x → g(x)·P(x) (solo para discretos con dominio chico)
    # ------------------------------------------------------------------

    def _maybe_render_pointwise_table(self, model, a: float, b: float, g_label: str) -> None:
        xs = self._enumerate_discrete_domain(model)
        if xs is None or len(xs) == 0 or len(xs) > 20:
            return

        with st.expander(f"Ver tabla x → {g_label}(x)·P(x) (suma da E({g_label}(X)))"):
            try:
                rows = []
                acc = 0.0
                for x in xs:
                    p = float(model.probability_value(x))
                    g = a + b * x
                    contrib = g * p
                    acc += contrib
                    rows.append(
                        {
                            "x": x,
                            "P(x)": p,
                            f"{g_label}(x) = a + b·x": g,
                            f"{g_label}(x)·P(x)": contrib,
                        }
                    )
                st.dataframe(rows, use_container_width=True, hide_index=True)
                st.caption(
                    f"Σ {g_label}(x)·P(x) = {_fmt(acc)} "
                    f"(coincide con E({g_label}(X)))."
                )
            except Exception as exc:
                st.caption(f"No se pudo construir la tabla: {exc}")

    @staticmethod
    def _enumerate_discrete_domain(model):
        if hasattr(model, "domain_list"):
            try:
                return list(model.domain_list())
            except Exception:
                return None
        if hasattr(model, "domain"):
            try:
                d = model.domain()
                if isinstance(d, tuple) and len(d) == 2:
                    lo, hi = d
                    if isinstance(lo, int) and isinstance(hi, int) and hi - lo <= 100:
                        return list(range(lo, hi + 1))
            except Exception:
                return None
        return None
