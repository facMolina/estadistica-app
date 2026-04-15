"""
Procesamiento de datos agrupados en intervalos (Tema I).

Todas las funciones trabajan sobre una tabla de frecuencias con intervalos [a, b)
y retornan CalcResult con paso a paso usando el mismo motor que los modelos de
probabilidad.
"""

import math
from typing import List, Tuple, Optional
from calculation.step_types import CalcResult
from calculation.step_engine import StepBuilder
from calculation.statistics_common import format_number


class GroupedData:
    """
    Datos agrupados en k intervalos [a_i, b_i) con frecuencias fi.

    Parametros:
        intervals : lista de tuplas (a, b) — limites de cada intervalo
        frequencies : lista de enteros fi — frecuencia absoluta de cada intervalo
    """

    def __init__(self, intervals: List[Tuple[float, float]], frequencies: List[int]):
        if len(intervals) != len(frequencies):
            raise ValueError("intervals y frequencies deben tener la misma longitud")
        if not intervals:
            raise ValueError("Debe haber al menos un intervalo")
        if any(f < 0 for f in frequencies):
            raise ValueError("Las frecuencias deben ser >= 0")

        self.intervals = intervals
        self.frequencies = frequencies
        self.k = len(intervals)
        self.n = sum(frequencies)
        # Puntos medios
        self.xi = [(a + b) / 2 for a, b in intervals]
        # Anchos de clase
        self.hi = [b - a for a, b in intervals]

    # ------------------------------------------------------------------
    # Tabla completa
    # ------------------------------------------------------------------

    def build_table(self) -> List[dict]:
        """
        Retorna lista de filas con:
          intervalo, xi, fi, fri, Fi, fi_xi, fi_xi2, Gi
        Fi y Gi son frecuencias relativas acumuladas (0 a 1).
        """
        rows = []
        cum_fi = 0
        for i in range(self.k):
            a, b = self.intervals[i]
            fi = self.frequencies[i]
            xi = self.xi[i]
            fri = fi / self.n if self.n > 0 else 0.0
            cum_fi += fi
            Fi = cum_fi / self.n if self.n > 0 else 0.0
            rows.append({
                "Intervalo": f"[{format_number(a)} – {format_number(b)})",
                "xi": xi,
                "fi": fi,
                "fri": round(fri, 6),
                "Fi": round(Fi, 6),
                "Gi": round(1 - Fi + fri, 6),   # P(x >= a_i) = 1 - F(a_i-)
                "fi·xi": round(fi * xi, 6),
                "fi·xi²": round(fi * xi ** 2, 6),
            })
        return rows

    # ------------------------------------------------------------------
    # Media
    # ------------------------------------------------------------------

    def mean(self) -> CalcResult:
        """x̄ = Σ(fi·xi) / n"""
        n = self.n
        builder = StepBuilder("Media")
        builder.add_step(
            desc="La media para datos agrupados se calcula usando los puntos medios xi = (a+b)/2",
            latex=r"\bar{x} = \frac{\sum f_i \cdot x_i}{n}",
            level_min=1,
        )

        # Tabla de fi·xi
        sum_fixi = 0.0
        for i in range(self.k):
            a, b = self.intervals[i]
            fi = self.frequencies[i]
            xi = self.xi[i]
            fixi = fi * xi
            sum_fixi += fixi
            builder.add_step(
                desc=f"x_{i+1} = ({format_number(a)}+{format_number(b)})/2 = {format_number(xi)}"
                     f"  →  f_{i+1}·x_{i+1} = {fi}·{format_number(xi)} = {format_number(fixi)}",
                latex=rf"f_{{{i+1}}} \cdot x_{{{i+1}}} = {fi} \cdot {format_number(xi)} = {format_number(fixi)}",
                result=fixi,
                level_min=3,
            )

        builder.add_step(
            desc=f"Σ fi·xi = {format_number(sum_fixi)}  |  n = {n}",
            latex=rf"\sum f_i \cdot x_i = {format_number(sum_fixi)}",
            result=sum_fixi,
            level_min=2,
        )

        mu = sum_fixi / n if n > 0 else 0.0
        builder.add_step(
            desc=f"x̄ = {format_number(sum_fixi)} / {n} = {format_number(mu)}",
            latex=rf"\bar{{x}} = \frac{{{format_number(sum_fixi)}}}{{{n}}} = {format_number(mu)}",
            result=mu,
            level_min=1,
        )
        return builder.build(final_value=mu, final_latex=rf"\bar{{x}} = {format_number(mu)}")

    # ------------------------------------------------------------------
    # Varianza y desvio
    # ------------------------------------------------------------------

    def _variance_components(self) -> Tuple[float, float]:
        """Retorna (Sn², sum_fixi2) para reutilizar en varianza y desvio."""
        mu = self.mean().final_value
        n = self.n
        sum_fixi2 = sum(self.frequencies[i] * self.xi[i] ** 2 for i in range(self.k))
        sn2 = sum_fixi2 / n - mu ** 2 if n > 0 else 0.0
        return sn2, sum_fixi2

    def variance_n(self) -> CalcResult:
        """Sn² = Σ(fi·xi²)/n − x̄²  (varianza poblacional)"""
        n = self.n
        mu = self.mean().final_value
        builder = StepBuilder("Varianza Sn²")
        builder.add_step(
            desc="Varianza poblacional (denominador n)",
            latex=r"S_n^2 = \frac{\sum f_i \cdot x_i^2}{n} - \bar{x}^2",
            level_min=1,
        )

        sum_fixi2 = 0.0
        for i in range(self.k):
            fi = self.frequencies[i]
            xi = self.xi[i]
            fixi2 = fi * xi ** 2
            sum_fixi2 += fixi2
            builder.add_step(
                desc=f"f_{i+1}·x_{i+1}² = {fi}·{format_number(xi)}² = {format_number(fixi2)}",
                latex=rf"f_{{{i+1}}} \cdot x_{{{i+1}}}^2 = {fi} \cdot {format_number(xi)}^2 = {format_number(fixi2)}",
                result=fixi2,
                level_min=3,
            )

        builder.add_step(
            desc=f"Σ fi·xi² = {format_number(sum_fixi2)}",
            latex=rf"\sum f_i \cdot x_i^2 = {format_number(sum_fixi2)}",
            result=sum_fixi2,
            level_min=2,
        )
        sn2 = sum_fixi2 / n - mu ** 2 if n > 0 else 0.0
        builder.add_step(
            desc=f"Sn² = {format_number(sum_fixi2)}/{n} − {format_number(mu)}² = "
                 f"{format_number(sum_fixi2/n)} − {format_number(mu**2)} = {format_number(sn2)}",
            latex=rf"S_n^2 = \frac{{{format_number(sum_fixi2)}}}{{{n}}} - {format_number(mu)}^2 = {format_number(sn2)}",
            result=sn2,
            level_min=1,
        )
        return builder.build(final_value=sn2, final_latex=rf"S_n^2 = {format_number(sn2)}")

    def variance_n1(self) -> CalcResult:
        """Sn-1² = n/(n-1) · Sn²  (varianza muestral corregida)"""
        n = self.n
        sn2 = self.variance_n().final_value
        sn12 = n / (n - 1) * sn2 if n > 1 else 0.0
        builder = StepBuilder("Varianza Sn-1²")
        builder.add_step(
            desc="Varianza muestral corregida (denominador n-1): aplica factor de Bessel",
            latex=r"S_{n-1}^2 = \frac{n}{n-1} \cdot S_n^2",
            level_min=1,
        )
        builder.add_step(
            desc=f"Sn-1² = ({n}/{n-1}) · {format_number(sn2)} = {format_number(sn12)}",
            latex=rf"S_{{n-1}}^2 = \frac{{{n}}}{{{n-1}}} \cdot {format_number(sn2)} = {format_number(sn12)}",
            result=sn12,
            level_min=2,
        )
        return builder.build(final_value=sn12, final_latex=rf"S_{{n-1}}^2 = {format_number(sn12)}")

    def std_dev_n(self) -> CalcResult:
        sn2 = self.variance_n().final_value
        sn = math.sqrt(sn2)
        builder = StepBuilder("Desvio Sn")
        builder.add_step(
            desc="Desvio estandar poblacional",
            latex=r"S_n = \sqrt{S_n^2}",
            level_min=1,
        )
        builder.add_step(
            desc=f"Sn = sqrt({format_number(sn2)}) = {format_number(sn)}",
            latex=rf"S_n = \sqrt{{{format_number(sn2)}}} = {format_number(sn)}",
            result=sn,
            level_min=2,
        )
        return builder.build(final_value=sn, final_latex=rf"S_n = {format_number(sn)}")

    def std_dev_n1(self) -> CalcResult:
        sn12 = self.variance_n1().final_value
        sn1 = math.sqrt(sn12)
        builder = StepBuilder("Desvio Sn-1")
        builder.add_step(
            desc="Desvio estandar muestral corregido",
            latex=r"S_{n-1} = \sqrt{S_{n-1}^2}",
            level_min=1,
        )
        builder.add_step(
            desc=f"Sn-1 = sqrt({format_number(sn12)}) = {format_number(sn1)}",
            latex=rf"S_{{n-1}} = \sqrt{{{format_number(sn12)}}} = {format_number(sn1)}",
            result=sn1,
            level_min=2,
        )
        return builder.build(final_value=sn1, final_latex=rf"S_{{n-1}} = {format_number(sn1)}")

    def cv_n(self) -> CalcResult:
        mu = self.mean().final_value
        sn = self.std_dev_n().final_value
        cv = (sn / mu * 100) if mu != 0 else float("inf")
        builder = StepBuilder("Coef. de Variacion Cvn")
        builder.add_step(
            desc="Cv = (Sn / x̄) · 100%",
            latex=r"Cv_n = \frac{S_n}{\bar{x}} \cdot 100\%",
            level_min=1,
        )
        builder.add_step(
            desc=f"Cvn = ({format_number(sn)} / {format_number(mu)}) · 100 = {format_number(cv)}%",
            latex=rf"Cv_n = \frac{{{format_number(sn)}}}{{{format_number(mu)}}} \cdot 100 = {format_number(cv)}\%",
            result=cv,
            level_min=2,
        )
        interp = "Conjunto homogeneo (Cv < 30%)" if cv < 30 else "Conjunto heterogeneo (Cv >= 30%)"
        builder.add_step(desc=interp, level_min=1)
        return builder.build(final_value=cv, final_latex=rf"Cv_n = {format_number(cv)}\%")

    def cv_n1(self) -> CalcResult:
        mu = self.mean().final_value
        sn1 = self.std_dev_n1().final_value
        cv = (sn1 / mu * 100) if mu != 0 else float("inf")
        builder = StepBuilder("Coef. de Variacion Cvn-1")
        builder.add_step(
            desc="Cv = (Sn-1 / x̄) · 100%",
            latex=r"Cv_{n-1} = \frac{S_{n-1}}{\bar{x}} \cdot 100\%",
            level_min=1,
        )
        builder.add_step(
            desc=f"Cvn-1 = ({format_number(sn1)} / {format_number(mu)}) · 100 = {format_number(cv)}%",
            latex=rf"Cv_{{n-1}} = \frac{{{format_number(sn1)}}}{{{format_number(mu)}}} \cdot 100 = {format_number(cv)}\%",
            result=cv,
            level_min=2,
        )
        interp = "Conjunto homogeneo (Cv < 30%)" if cv < 30 else "Conjunto heterogeneo (Cv >= 30%)"
        builder.add_step(desc=interp, level_min=1)
        return builder.build(final_value=cv, final_latex=rf"Cv_{{n-1}} = {format_number(cv)}\%")

    # ------------------------------------------------------------------
    # Frecuencias acumuladas relativas — base para F(x), percentiles
    # ------------------------------------------------------------------

    def _cum_abs(self) -> List[int]:
        """Frecuencias absolutas acumuladas al final de cada intervalo."""
        cum = []
        total = 0
        for f in self.frequencies:
            total += f
            cum.append(total)
        return cum

    def _F_at(self, x: float) -> float:
        """
        F(x) = fraccion de datos <= x.
        Usa interpolacion lineal dentro del intervalo que contiene x.
        """
        cum_abs = self._cum_abs()
        n = self.n
        if n == 0:
            return 0.0
        if x <= self.intervals[0][0]:
            return 0.0
        if x >= self.intervals[-1][1]:
            return 1.0
        cum_prev = 0
        for i, (a, b) in enumerate(self.intervals):
            if a <= x < b:
                # Interpolacion lineal: F(x) = (cum_prev + fi*(x-a)/h) / n
                fi = self.frequencies[i]
                h = b - a
                return (cum_prev + fi * (x - a) / h) / n
            if x >= b:
                cum_prev = cum_abs[i]
        return 1.0

    # ------------------------------------------------------------------
    # Probabilidades empiricas
    # ------------------------------------------------------------------

    def prob_range(self, a: float, b: float) -> CalcResult:
        """P(a < x < b) usando frecuencias relativas acumuladas."""
        fa = self._F_at(a)
        fb = self._F_at(b)
        prob = fb - fa
        builder = StepBuilder(f"P({format_number(a)} < x < {format_number(b)})")
        builder.add_step(
            desc="Probabilidad empirica de un intervalo: P(a < x < b) = F(b) − F(a)",
            latex=rf"P({format_number(a)} < x < {format_number(b)}) = F({format_number(b)}) - F({format_number(a)})",
            level_min=1,
        )
        builder.add_step(
            desc=f"F({format_number(b)}) = {format_number(fb, 4)}  (fraccion de datos <= {format_number(b)})",
            latex=rf"F({format_number(b)}) = {format_number(fb, 4)}",
            result=fb,
            level_min=2,
        )
        builder.add_step(
            desc=f"F({format_number(a)}) = {format_number(fa, 4)}  (fraccion de datos <= {format_number(a)})",
            latex=rf"F({format_number(a)}) = {format_number(fa, 4)}",
            result=fa,
            level_min=2,
        )
        builder.add_step(
            desc=f"P = {format_number(fb, 4)} − {format_number(fa, 4)} = {format_number(prob, 4)} = {format_number(prob*100, 2)}%",
            latex=rf"P = {format_number(fb, 4)} - {format_number(fa, 4)} = {format_number(prob, 4)}",
            result=prob,
            level_min=1,
        )
        return builder.build(
            final_value=prob,
            final_latex=rf"P({format_number(a)} < x < {format_number(b)}) = {format_number(prob*100, 2)}\%",
        )

    def prob_conditional(self, given_above: float, find_below: float) -> CalcResult:
        """
        P(x < find_below | x > given_above)
        = P(given_above < x < find_below) / P(x > given_above)
        """
        f_above = self._F_at(given_above)
        f_below = self._F_at(find_below)
        p_num = max(0.0, f_below - f_above)      # P(given_above < x < find_below)
        p_denom = 1.0 - f_above                   # P(x > given_above)
        prob = p_num / p_denom if p_denom > 1e-15 else 0.0

        builder = StepBuilder(
            f"P(x<{format_number(find_below)} | x>{format_number(given_above)})"
        )
        builder.add_step(
            desc="Probabilidad condicional empirica",
            latex=(rf"P\!\left(x < {format_number(find_below)} \mid x > {format_number(given_above)}\right)"
                   rf" = \frac{{P({format_number(given_above)} < x < {format_number(find_below)})}}{{P(x > {format_number(given_above)})}}"),
            level_min=1,
        )
        builder.add_step(
            desc=f"F({format_number(find_below)}) = {format_number(f_below, 4)}",
            latex=rf"F({format_number(find_below)}) = {format_number(f_below, 4)}",
            result=f_below,
            level_min=2,
        )
        builder.add_step(
            desc=f"F({format_number(given_above)}) = {format_number(f_above, 4)}",
            latex=rf"F({format_number(given_above)}) = {format_number(f_above, 4)}",
            result=f_above,
            level_min=2,
        )
        builder.add_step(
            desc=f"Numerador P({format_number(given_above)}<x<{format_number(find_below)}) = {format_number(f_below,4)} − {format_number(f_above,4)} = {format_number(p_num, 4)}",
            latex=rf"P_{{num}} = {format_number(f_below,4)} - {format_number(f_above,4)} = {format_number(p_num, 4)}",
            result=p_num,
            level_min=2,
        )
        builder.add_step(
            desc=f"Denominador P(x>{format_number(given_above)}) = 1 − {format_number(f_above, 4)} = {format_number(p_denom, 4)}",
            latex=rf"P_{{den}} = 1 - {format_number(f_above,4)} = {format_number(p_denom, 4)}",
            result=p_denom,
            level_min=2,
        )
        builder.add_step(
            desc=f"P = {format_number(p_num,4)} / {format_number(p_denom,4)} = {format_number(prob,4)} = {format_number(prob*100,2)}%",
            latex=rf"P = \frac{{{format_number(p_num,4)}}}{{{format_number(p_denom,4)}}} = {format_number(prob,4)}",
            result=prob,
            level_min=1,
        )
        return builder.build(
            final_value=prob,
            final_latex=rf"P = {format_number(prob*100, 2)}\%",
        )

    # ------------------------------------------------------------------
    # Mediana
    # ------------------------------------------------------------------

    def median(self) -> CalcResult:
        """Me = L + h · (n/2 − F_{i-1}) / fi  (interpolacion lineal)"""
        n = self.n
        target = n / 2.0
        builder = StepBuilder("Mediana")
        builder.add_step(
            desc="La mediana es el valor que divide al 50% de las observaciones: buscar intervalo donde n/2 cae en la acumulada",
            latex=r"Me = L + h \cdot \frac{n/2 - F_{i-1}}{f_i}",
            level_min=1,
        )
        builder.add_step(
            desc=f"n/2 = {n}/2 = {format_number(target)}",
            latex=rf"\frac{{n}}{{2}} = \frac{{{n}}}{{2}} = {format_number(target)}",
            result=target,
            level_min=2,
        )

        cum_prev = 0
        for i, (a, b) in enumerate(self.intervals):
            cum_curr = cum_prev + self.frequencies[i]
            if cum_curr >= target:
                h = b - a
                fi = self.frequencies[i]
                me = a + h * (target - cum_prev) / fi if fi > 0 else a
                builder.add_step(
                    desc=f"La mediana esta en el intervalo [{format_number(a)}, {format_number(b)}): "
                         f"F acumulada antes = {cum_prev}, fi = {fi}",
                    latex=rf"\text{{Intervalo mediano: }} [{format_number(a)},\ {format_number(b)})",
                    level_min=2,
                )
                builder.add_step(
                    desc=(f"Me = {format_number(a)} + {format_number(h)} · "
                          f"({format_number(target)} − {cum_prev}) / {fi} = {format_number(me)}"),
                    latex=(rf"Me = {format_number(a)} + {format_number(h)} \cdot "
                           rf"\frac{{{format_number(target)} - {cum_prev}}}{{{fi}}} = {format_number(me)}"),
                    result=me,
                    level_min=1,
                )
                return builder.build(final_value=me, final_latex=rf"Me = {format_number(me)}")
            cum_prev = cum_curr

        return builder.build(final_value=float(self.intervals[-1][1]),
                             final_latex="Me = (no encontrada)")

    # ------------------------------------------------------------------
    # Fractil
    # ------------------------------------------------------------------

    def fractile(self, alpha: float) -> CalcResult:
        """
        x(α) = L + h · (n·α − F_{i-1}) / fi
        donde α ∈ (0,1) es la fraccion acumulada buscada.
        """
        n = self.n
        target = n * alpha
        builder = StepBuilder(f"Fractil x({format_number(alpha)})")
        builder.add_step(
            desc=f"El fractil x(α) es el valor tal que F(x) = α = {format_number(alpha)} ({format_number(alpha*100)}% de los datos estan por debajo)",
            latex=rf"x(\alpha) = L + h \cdot \frac{{n \cdot \alpha - F_{{i-1}}}}{{f_i}}",
            level_min=1,
        )
        builder.add_step(
            desc=f"n·α = {n}·{format_number(alpha)} = {format_number(target)}  (frecuencia acumulada objetivo)",
            latex=rf"n \cdot \alpha = {n} \cdot {format_number(alpha)} = {format_number(target)}",
            result=target,
            level_min=2,
        )

        cum_prev = 0
        for i, (a, b) in enumerate(self.intervals):
            cum_curr = cum_prev + self.frequencies[i]
            if cum_curr >= target:
                h = b - a
                fi = self.frequencies[i]
                frac = a + h * (target - cum_prev) / fi if fi > 0 else a
                builder.add_step(
                    desc=f"El fractil esta en [{format_number(a)}, {format_number(b)}): "
                         f"F acumulada antes = {cum_prev}, fi = {fi}",
                    latex=rf"\text{{Intervalo: }} [{format_number(a)},\ {format_number(b)})",
                    level_min=2,
                )
                builder.add_step(
                    desc=(f"x({format_number(alpha)}) = {format_number(a)} + {format_number(h)} · "
                          f"({format_number(target)} − {cum_prev}) / {fi} = {format_number(frac)}"),
                    latex=(rf"x({format_number(alpha)}) = {format_number(a)} + {format_number(h)} \cdot "
                           rf"\frac{{{format_number(target)} - {cum_prev}}}{{{fi}}} = {format_number(frac)}"),
                    result=frac,
                    level_min=1,
                )
                return builder.build(
                    final_value=frac,
                    final_latex=rf"x({format_number(alpha)}) = {format_number(frac)}",
                )
            cum_prev = cum_curr

        return builder.build(final_value=float(self.intervals[-1][1]),
                             final_latex="x(α) = (no encontrado)")
