"""Modelo PMF casera (CustomPMF) — PMF discreta arbitraria con normalizador k.

Típicamente aparece en exámenes como:

    P(X = x) = (x + 2) / k      para x ∈ {0, 1, 2, 3}

donde k se determina imponiendo Σ P(X=x) = 1 sobre el dominio.

API paralela a DiscreteModel. No hereda porque el "parámetro" es una expresión
algebraica que debe evaluarse numéricamente por valor del dominio.
"""

from __future__ import annotations

import math
import re
from typing import Sequence

from calculation.step_types import CalcResult
from calculation.step_engine import StepBuilder
from calculation.statistics_common import format_number


_SAFE_FUNCS = {
    "abs": abs, "min": min, "max": max, "round": round,
    "sqrt": math.sqrt, "exp": math.exp, "log": math.log,
    "factorial": math.factorial, "pi": math.pi, "e": math.e,
}


class CustomPMF:
    """PMF discreta definida por una expresión simbólica sobre un dominio finito."""

    def __init__(
        self,
        expr: str,
        domain: Sequence[int],
        k_var: str = "k",
        *,
        auto_normalize: bool = True,
    ):
        if not expr or not isinstance(expr, str):
            raise ValueError("expr debe ser una string no vacía con la fórmula de P(X=x)")
        if not domain or any(not isinstance(x, (int, float)) for x in domain):
            raise ValueError("domain debe ser una lista de valores numéricos")
        self.expr = expr.strip()
        self.domain = [int(x) if float(x).is_integer() else float(x) for x in domain]
        self.k_var = k_var
        self._k_value: float | None = None
        if auto_normalize and self.k_var and self.k_var in self._free_symbols():
            self._k_value = self._compute_normalizer()

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _free_symbols(self) -> set[str]:
        ids = set(re.findall(r"[A-Za-z_][A-Za-z0-9_]*", self.expr))
        return ids - set(_SAFE_FUNCS.keys())

    def _eval_at(self, x, *, k: float | None = None) -> float:
        env = dict(_SAFE_FUNCS)
        env["x"] = x
        env["X"] = x
        if k is not None:
            env[self.k_var] = k
        return float(eval(self.expr, {"__builtins__": {}}, env))

    def _compute_normalizer(self) -> float:
        total_numerator = 0.0
        for x in self.domain:
            term = self._eval_at(x, k=1.0)
            total_numerator += term
        if total_numerator <= 0:
            raise ValueError(
                f"No se puede normalizar: Σ f(x) con k=1 es {total_numerator} (≤ 0)"
            )
        return total_numerator

    def _p(self, x) -> float:
        if x not in self.domain:
            return 0.0
        if self._k_value is not None:
            return self._eval_at(x, k=self._k_value)
        return self._eval_at(x)

    # ------------------------------------------------------------------
    # API pública
    # ------------------------------------------------------------------

    def name(self) -> str:
        return "CustomPMF"

    def params_dict(self) -> dict:
        d: dict = {"expr": self.expr, "domain": list(self.domain)}
        if self._k_value is not None:
            d[self.k_var] = self._k_value
        return d

    def domain_list(self) -> list:
        return list(self.domain)

    def probability_value(self, x) -> float:
        return self._p(x)

    def probability(self, x) -> CalcResult:
        sb = StepBuilder("CustomPMF")
        sb.add_step(
            "Definición de la PMF",
            latex=f"P(X=x) = {self._expr_latex()}",
            latex_sub=f"Dominio = {self.domain}",
            latex_res="",
            level_min=1,
        )
        if self._k_value is not None:
            sb.add_step(
                f"Normalización: calcular {self.k_var}",
                latex=f"\\sum_{{x \\in D}} f(x) = 1 \\Rightarrow {self.k_var} = \\sum_{{x}} g(x)",
                latex_sub=(
                    f"{self.k_var} = " + " + ".join(f"{self._eval_at(xv, k=1.0):.4g}" for xv in self.domain)
                ),
                latex_res=f"{self.k_var} = {format_number(self._k_value)}",
                level_min=2,
            )

        val = self._p(x)
        sb.add_step(
            f"Evaluación en x = {x}",
            latex=f"P(X={x}) = {self._expr_latex(x)}",
            latex_sub=f"= {self._eval_at(x, k=self._k_value) if self._k_value is not None else self._eval_at(x):.6f}",
            latex_res=f"P(X={x}) = {format_number(val)}",
            result=val,
            level_min=1,
        )
        return sb.build(final_value=val, final_latex=format_number(val))

    def cdf_left(self, r) -> CalcResult:
        sb = StepBuilder("CustomPMF")
        terms = [xv for xv in self.domain if xv <= r]
        total = sum(self._p(xv) for xv in terms)
        sb.add_step(
            f"F({r}) = P(X ≤ {r})",
            latex=f"F({r}) = \\sum_{{x \\le {r}}} P(X=x)",
            latex_sub=" + ".join(f"P(X={xv})" for xv in terms),
            latex_res=f"F({r}) = {format_number(total)}",
            result=total,
            level_min=1,
        )
        return sb.build(final_value=total, final_latex=format_number(total))

    def cdf_right(self, r) -> CalcResult:
        sb = StepBuilder("CustomPMF")
        terms = [xv for xv in self.domain if xv >= r]
        total = sum(self._p(xv) for xv in terms)
        sb.add_step(
            f"G({r}) = P(X ≥ {r})",
            latex=f"G({r}) = \\sum_{{x \\ge {r}}} P(X=x)",
            latex_sub=" + ".join(f"P(X={xv})" for xv in terms),
            latex_res=f"G({r}) = {format_number(total)}",
            result=total,
            level_min=1,
        )
        return sb.build(final_value=total, final_latex=format_number(total))

    def mean(self) -> CalcResult:
        sb = StepBuilder("CustomPMF")
        terms = [(xv, self._p(xv)) for xv in self.domain]
        total = sum(xv * pv for xv, pv in terms)
        sb.add_step(
            "Esperanza",
            latex="E(X) = \\sum_{x} x \\cdot P(X=x)",
            latex_sub=" + ".join(f"{xv}·{pv:.4g}" for xv, pv in terms),
            latex_res=f"E(X) = {format_number(total)}",
            result=total,
            level_min=1,
        )
        return sb.build(final_value=total, final_latex=format_number(total))

    def variance(self) -> CalcResult:
        sb = StepBuilder("CustomPMF")
        mu = sum(xv * self._p(xv) for xv in self.domain)
        ex2 = sum((xv ** 2) * self._p(xv) for xv in self.domain)
        var = ex2 - mu ** 2
        sb.add_step(
            "Varianza (teorema Koenig)",
            latex="V(X) = E(X^2) - [E(X)]^2",
            latex_sub=f"V(X) = {ex2:.4g} - ({mu:.4g})^2",
            latex_res=f"V(X) = {format_number(var)}",
            result=var,
            level_min=1,
        )
        return sb.build(final_value=var, final_latex=format_number(var))

    def std_dev(self) -> CalcResult:
        sb = StepBuilder("CustomPMF")
        v = self.variance().final_value
        s = math.sqrt(max(0.0, v))
        sb.add_step(
            "Desvío estándar",
            latex="\\sigma(X) = \\sqrt{V(X)}",
            latex_sub=f"\\sqrt{{{v:.4g}}}",
            latex_res=f"σ(X) = {format_number(s)}",
            result=s,
            level_min=1,
        )
        return sb.build(final_value=s, final_latex=format_number(s))

    # ------------------------------------------------------------------
    # Características (paridad con DiscreteModel)
    # ------------------------------------------------------------------

    def mode(self) -> CalcResult:
        sb = StepBuilder("CustomPMF")
        best_x = self.domain[0]
        best_p = self._p(best_x)
        for xv in self.domain[1:]:
            pv = self._p(xv)
            if pv > best_p:
                best_p, best_x = pv, xv
        terms = ", ".join(
            f"P(X={xv})={self._p(xv):.4g}" for xv in self.domain
        )
        sb.add_step(
            "Moda — valor con mayor probabilidad",
            latex="\\text{Mo} = \\arg\\max_x P(X=x)",
            latex_sub=terms,
            latex_res=f"Mo = {best_x}",
            result=best_x,
            level_min=1,
        )
        return sb.build(final_value=best_x, final_latex=str(best_x))

    def median(self) -> CalcResult:
        sb = StepBuilder("CustomPMF")
        cum = 0.0
        med = self.domain[-1]
        rows = []
        for xv in self.domain:
            cum += self._p(xv)
            rows.append((xv, cum))
            if cum >= 0.5 and med == self.domain[-1] and cum != 0.0:
                if not any(c >= 0.5 for _, c in rows[:-1]):
                    med = xv
        terms = "; ".join(f"F({xv})={cv:.4g}" for xv, cv in rows)
        sb.add_step(
            "Mediana — menor x tal que F(x) ≥ 0.5",
            latex="\\text{Me} = \\min\\{x : F(x) \\ge 0{,}5\\}",
            latex_sub=terms,
            latex_res=f"Me = {med}",
            result=med,
            level_min=1,
        )
        return sb.build(final_value=med, final_latex=str(med))

    def cv(self) -> CalcResult:
        sb = StepBuilder("CustomPMF")
        mu = sum(xv * self._p(xv) for xv in self.domain)
        var = sum((xv ** 2) * self._p(xv) for xv in self.domain) - mu ** 2
        sigma = math.sqrt(max(0.0, var))
        if abs(mu) < 1e-15:
            sb.add_step(
                "Coeficiente de variación — indefinido (E(X) = 0)",
                latex="CV = \\sigma / E(X)",
                latex_sub="E(X) = 0 \\Rightarrow CV \\text{ no definido}",
                latex_res="CV = —",
                result=float("nan"),
                level_min=1,
            )
            return sb.build(final_value=float("nan"), final_latex="—")
        cv_val = sigma / abs(mu)
        sb.add_step(
            "Coeficiente de variación",
            latex="CV = \\dfrac{\\sigma}{E(X)}",
            latex_sub=f"CV = \\dfrac{{{sigma:.4g}}}{{{mu:.4g}}}",
            latex_res=f"CV = {format_number(cv_val)}",
            result=cv_val,
            level_min=1,
        )
        return sb.build(final_value=cv_val, final_latex=format_number(cv_val))

    def skewness(self) -> CalcResult:
        sb = StepBuilder("CustomPMF")
        mu = sum(xv * self._p(xv) for xv in self.domain)
        var = sum((xv ** 2) * self._p(xv) for xv in self.domain) - mu ** 2
        sigma = math.sqrt(max(0.0, var))
        if sigma < 1e-15:
            sb.add_step(
                "Asimetría — indefinida (σ = 0)",
                latex="As = m_3 / \\sigma^3",
                latex_sub="\\sigma = 0",
                latex_res="As = —",
                result=float("nan"),
                level_min=1,
            )
            return sb.build(final_value=float("nan"), final_latex="—")
        m3 = sum(((xv - mu) ** 3) * self._p(xv) for xv in self.domain)
        as_val = m3 / (sigma ** 3)
        sb.add_step(
            "Coeficiente de asimetría (Fisher)",
            latex="As = \\dfrac{E[(X-\\mu)^3]}{\\sigma^3}",
            latex_sub=f"As = \\dfrac{{{m3:.4g}}}{{{sigma:.4g}^3}}",
            latex_res=f"As = {format_number(as_val)}",
            result=as_val,
            level_min=1,
        )
        return sb.build(final_value=as_val, final_latex=format_number(as_val))

    def kurtosis(self) -> CalcResult:
        sb = StepBuilder("CustomPMF")
        mu = sum(xv * self._p(xv) for xv in self.domain)
        var = sum((xv ** 2) * self._p(xv) for xv in self.domain) - mu ** 2
        sigma = math.sqrt(max(0.0, var))
        if sigma < 1e-15:
            sb.add_step(
                "Curtosis — indefinida (σ = 0)",
                latex="Ku = m_4 / \\sigma^4",
                latex_sub="\\sigma = 0",
                latex_res="Ku = —",
                result=float("nan"),
                level_min=1,
            )
            return sb.build(final_value=float("nan"), final_latex="—")
        m4 = sum(((xv - mu) ** 4) * self._p(xv) for xv in self.domain)
        ku = m4 / (sigma ** 4)
        sb.add_step(
            "Coeficiente de curtosis (no centrado)",
            latex="Ku = \\dfrac{E[(X-\\mu)^4]}{\\sigma^4}",
            latex_sub=f"Ku = \\dfrac{{{m4:.4g}}}{{{sigma:.4g}^4}}",
            latex_res=f"Ku = {format_number(ku)}",
            result=ku,
            level_min=1,
        )
        return sb.build(final_value=ku, final_latex=format_number(ku))

    # ------------------------------------------------------------------
    # Probabilidad condicional sobre eventos de la forma (op, val)
    # ------------------------------------------------------------------

    _OP_LATEX = {"=": "=", "<=": r"\le", "<": "<", ">=": r"\ge", ">": ">"}
    _OP_SYMBOL = {"=": "=", "<=": "≤", "<": "<", ">=": "≥", ">": ">"}

    def _event_filter(self, op: str, val):
        """Devuelve una función f(x) -> bool según el operador y valor.

        `op` ∈ {=, <=, <, >=, >, between}. Cuando `op == 'between'`,
        `val` debe ser una tupla (a, b) inclusive en ambos extremos.
        """
        if op == "=":
            v = int(val)
            return lambda x: x == v
        if op == "<=":
            v = int(val)
            return lambda x: x <= v
        if op == "<":
            v = int(val)
            return lambda x: x < v
        if op == ">=":
            v = int(val)
            return lambda x: x >= v
        if op == ">":
            v = int(val)
            return lambda x: x > v
        if op == "between":
            a, b = val
            a, b = int(a), int(b)
            lo, hi = min(a, b), max(a, b)
            return lambda x: lo <= x <= hi
        raise ValueError(f"Operador desconocido: {op}")

    def _event_str(self, op: str, val) -> str:
        """Render simbólico del evento, ej. 'X = 5', 'X > 2', '2 ≤ X ≤ 4'."""
        if op == "between":
            a, b = val
            lo, hi = min(int(a), int(b)), max(int(a), int(b))
            return f"{lo} ≤ X ≤ {hi}"
        return f"X {self._OP_SYMBOL[op]} {int(val)}"

    def _event_latex(self, op: str, val) -> str:
        if op == "between":
            a, b = val
            lo, hi = min(int(a), int(b)), max(int(a), int(b))
            return rf"{lo} \le X \le {hi}"
        return rf"X {self._OP_LATEX[op]} {int(val)}"

    def conditional(self, num_op: str, num_val, den_op: str, den_val) -> CalcResult:
        """P(A | B) = P(A ∩ B) / P(B) sobre el dominio discreto."""
        num_f = self._event_filter(num_op, num_val)
        den_f = self._event_filter(den_op, den_val)

        num_evt = self._event_str(num_op, num_val)
        den_evt = self._event_str(den_op, den_val)
        num_ltx = self._event_latex(num_op, num_val)
        den_ltx = self._event_latex(den_op, den_val)

        sb = StepBuilder("CustomPMF")
        sb.add_step(
            f"Probabilidad condicional P({num_evt} | {den_evt})",
            latex=rf"P(A \mid B) = \dfrac{{P(A \cap B)}}{{P(B)}}",
            latex_sub=rf"A: {num_ltx}\quad B: {den_ltx}",
            latex_res="",
            level_min=1,
        )

        den_xs = [x for x in self.domain if den_f(x)]
        p_den = sum(self._p(x) for x in den_xs)
        den_terms_ltx = " + ".join(f"P(X={x})" for x in den_xs) or "0"
        den_vals_ltx = " + ".join(format_number(self._p(x)) for x in den_xs) or "0"
        sb.add_step(
            f"Denominador: P({den_evt})",
            latex=rf"P(B) = \sum_{{x : {den_ltx}}} P(X=x)",
            latex_sub=f"{den_terms_ltx} = {den_vals_ltx}",
            latex_res=f"P(B) = {format_number(p_den)}",
            result=p_den,
            level_min=2,
        )

        if p_den <= 1e-15:
            sb.add_step(
                "Condición imposible: P(B) = 0",
                latex=rf"P(A \mid B) \text{{ no está definida}}",
                latex_sub="",
                latex_res="—",
                level_min=1,
            )
            return sb.build(final_value=float("nan"), final_latex="—")

        inter_xs = [x for x in self.domain if num_f(x) and den_f(x)]
        p_inter = sum(self._p(x) for x in inter_xs)
        inter_terms_ltx = " + ".join(f"P(X={x})" for x in inter_xs) or "0"
        inter_vals_ltx = " + ".join(format_number(self._p(x)) for x in inter_xs) or "0"
        sb.add_step(
            f"Numerador: P({num_evt} ∩ {den_evt})",
            latex=rf"P(A \cap B) = \sum_{{x : {num_ltx} \;\land\; {den_ltx}}} P(X=x)",
            latex_sub=f"{inter_terms_ltx} = {inter_vals_ltx}",
            latex_res=f"P(A \\cap B) = {format_number(p_inter)}",
            result=p_inter,
            level_min=2,
        )

        result = p_inter / p_den
        sb.add_step(
            f"Resultado P({num_evt} | {den_evt})",
            latex=rf"P(A \mid B) = \dfrac{{P(A \cap B)}}{{P(B)}}",
            latex_sub=rf"\dfrac{{{format_number(p_inter)}}}{{{format_number(p_den)}}}",
            latex_res=f"P(A \\mid B) = {format_number(result)}",
            result=result,
            level_min=1,
        )
        return sb.build(final_value=result, final_latex=format_number(result))

    def partial_expectation_left(self, r) -> CalcResult:
        sb = StepBuilder("CustomPMF")
        terms = [(xv, self._p(xv)) for xv in self.domain if xv <= r]
        h = sum(xv * pv for xv, pv in terms)
        f_r = sum(pv for _, pv in terms)
        sub = " + ".join(f"{xv}·{pv:.4g}" for xv, pv in terms) or "0"
        sb.add_step(
            f"H({r}) = expectativa parcial izquierda hasta {r}",
            latex=f"H({r}) = \\sum_{{x \\le {r}}} x \\cdot P(X=x)",
            latex_sub=sub,
            latex_res=f"H({r}) = {format_number(h)}",
            result=h,
            level_min=1,
        )
        if f_r > 1e-15:
            tm = h / f_r
            sb.add_step(
                f"Promedio truncado izquierdo M({r})",
                latex=f"M({r}) = H({r}) / F({r})",
                latex_sub=f"= {h:.4g} / {f_r:.4g}",
                latex_res=f"M({r}) = {format_number(tm)}",
                result=tm,
                level_min=2,
            )
        return sb.build(final_value=h, final_latex=format_number(h))

    def all_characteristics(self) -> dict:
        """Diccionario para `render_summary` (paridad con DiscreteModel)."""
        return {
            "Esperanza Matemática": self.mean(),
            "Varianza": self.variance(),
            "Desvío Estándar": self.std_dev(),
            "Moda": self.mode(),
            "Mediana": self.median(),
            "Coef. de Variación": self.cv(),
            "Coef. de Asimetría": self.skewness(),
            "Coef. de Kurtosis": self.kurtosis(),
        }

    def full_table(self) -> list[dict]:
        """Tabla con shape estándar discreto: r, P(r), F(r), G(r), H(r), J(r)."""
        rows: list[dict] = []
        cum_f = 0.0
        cum_h = 0.0
        for xv in self.domain:
            p = self._p(xv)
            cum_f += p
            cum_h += xv * p
            rows.append({"r": xv, "P(r)": p, "F(r)": cum_f, "H(r)": cum_h})
        cum_g = 0.0
        cum_j = 0.0
        for i in range(len(rows) - 1, -1, -1):
            cum_g += rows[i]["P(r)"]
            cum_j += rows[i]["r"] * rows[i]["P(r)"]
            rows[i]["G(r)"] = cum_g
            rows[i]["J(r)"] = cum_j
        return rows

    def latex_formula(self) -> str:
        return f"P(X=x) = {self._expr_latex()} \\quad, \\; x \\in {self.domain}"

    def _expr_latex(self, x_sub=None) -> str:
        expr = self.expr
        if x_sub is not None:
            expr = re.sub(r"\bx\b", str(x_sub), expr)
        return expr.replace("*", " \\cdot ")
