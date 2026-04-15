"""Construccion de graficos con Plotly."""

import plotly.graph_objects as go
from typing import List, Dict, Optional, Tuple


def build_probability_polygon(table_data: List[Dict], title: str = "Poligono de Probabilidad",
                               highlight_r: Optional[int] = None) -> go.Figure:
    """Grafico de poligono de probabilidad (stem plot con linea punteada)."""
    rs = [row["r"] for row in table_data]
    ps = [row["P(r)"] for row in table_data]

    fig = go.Figure()

    # Barras verticales (stems)
    for r_val, p_val in zip(rs, ps):
        color = "red" if r_val == highlight_r else "steelblue"
        fig.add_trace(go.Scatter(
            x=[r_val, r_val], y=[0, p_val],
            mode="lines", line=dict(color=color, width=2),
            showlegend=False, hoverinfo="skip",
        ))

    # Puntos
    colors = ["red" if r_val == highlight_r else "steelblue" for r_val in rs]
    fig.add_trace(go.Scatter(
        x=rs, y=ps, mode="markers+lines",
        marker=dict(size=8, color=colors),
        line=dict(dash="dash", color="gray", width=1),
        name="P(r)",
        hovertemplate="r=%{x}<br>P(r)=%{y:.6f}<extra></extra>",
    ))

    fig.update_layout(
        title=title, xaxis_title="r", yaxis_title="P(r)",
        template="plotly_white", height=400,
        xaxis=dict(dtick=1),
    )
    return fig


def build_cdf_plot(table_data: List[Dict], cdf_col: str = "F(r)",
                    title: str = "Funcion de Distribucion Acumulada") -> go.Figure:
    """Grafico de funcion acumulada (escalon para discretas)."""
    rs = [row["r"] for row in table_data]
    vals = [row[cdf_col] for row in table_data]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=rs, y=vals, mode="lines+markers",
        marker=dict(size=6, color="steelblue"),
        line=dict(shape="hv", color="steelblue", width=2),
        name=cdf_col,
        hovertemplate=f"r=%{{x}}<br>{cdf_col}=%{{y:.6f}}<extra></extra>",
    ))

    fig.update_layout(
        title=title, xaxis_title="r", yaxis_title=cdf_col,
        template="plotly_white", height=400,
        xaxis=dict(dtick=1), yaxis=dict(range=[-0.05, 1.05]),
    )
    return fig


# ---------------------------------------------------------------------------
# Graficos para datos agrupados (Sprint 2)
# ---------------------------------------------------------------------------

def build_histogram(intervals: List[Tuple[float, float]], frequencies: List[int],
                    title: str = "Histograma de Frecuencias") -> go.Figure:
    """
    Histograma de frecuencias relativas para datos agrupados.
    Las barras se posicionan en los puntos medios con ancho = amplitud del intervalo.
    """
    n = sum(frequencies)
    midpoints = [(a + b) / 2 for a, b in intervals]
    widths = [b - a for a, b in intervals]
    fris = [fi / n if n > 0 else 0 for fi in frequencies]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=midpoints,
        y=fris,
        width=widths,
        marker_color="steelblue",
        marker_line_color="white",
        marker_line_width=1.5,
        name="fri",
        customdata=[[a, b, fi] for (a, b), fi in zip(intervals, frequencies)],
        hovertemplate=(
            "[%{customdata[0]}, %{customdata[1]})<br>"
            "fi = %{customdata[2]}<br>"
            "fri = %{y:.4f}<extra></extra>"
        ),
    ))
    fig.update_layout(
        title=title,
        xaxis_title="x",
        yaxis_title="Frecuencia relativa (fri)",
        template="plotly_white",
        height=400,
        bargap=0,
    )
    return fig


def build_density_plot(model, title: str,
                       query_type: str = None,
                       x_val: float = None,
                       x_a: float = None,
                       x_b: float = None) -> go.Figure:
    """
    Curva de densidad para modelos continuos con área sombreada opcional.

    query_type: 'density'    → línea vertical en x_val
                'cdf_left'   → sombrea P(X ≤ x_val)
                'cdf_right'  → sombrea P(X ≥ x_val)
                'range'      → sombrea P(x_a ≤ X ≤ x_b)
                None / otro  → solo la curva
    """
    import numpy as np

    lo, hi = model.display_domain()
    xs = np.linspace(lo, hi, 500)
    ys = np.array([model.density_value(float(xi)) for xi in xs])

    fig = go.Figure()

    # ------------------------------------------------------------------
    # Área sombreada
    # ------------------------------------------------------------------
    def _shade(mask, label):
        sx, sy = xs[mask], ys[mask]
        if sx.size < 2:
            return
        fig.add_trace(go.Scatter(
            x=np.concatenate([[sx[0]], sx, [sx[-1]]]),
            y=np.concatenate([[0.0], sy, [0.0]]),
            fill="toself",
            fillcolor="rgba(70,130,180,0.30)",
            line=dict(width=0),
            showlegend=True,
            name=label,
            hoverinfo="skip",
        ))

    if query_type == "cdf_left" and x_val is not None:
        _shade(xs <= x_val, f"F({x_val:.4g})")

    elif query_type == "cdf_right" and x_val is not None:
        _shade(xs >= x_val, f"G({x_val:.4g})")

    elif query_type == "range" and x_a is not None and x_b is not None:
        _shade((xs >= x_a) & (xs <= x_b), f"P({x_a:.4g}≤X≤{x_b:.4g})")

    # ------------------------------------------------------------------
    # Curva principal
    # ------------------------------------------------------------------
    fig.add_trace(go.Scatter(
        x=list(xs), y=list(ys),
        mode="lines",
        line=dict(color="steelblue", width=2.5),
        name="f(x)",
        hovertemplate="x=%{x:.4f}<br>f(x)=%{y:.6f}<extra></extra>",
    ))

    # ------------------------------------------------------------------
    # Marcador puntual (densidad / fractil)
    # ------------------------------------------------------------------
    if query_type == "density" and x_val is not None:
        y_point = model.density_value(float(x_val))
        fig.add_vline(x=x_val, line_dash="dash", line_color="crimson",
                      annotation_text=f"x={x_val:.4g}",
                      annotation_position="top right")
        fig.add_trace(go.Scatter(
            x=[x_val], y=[y_point],
            mode="markers",
            marker=dict(size=10, color="crimson"),
            name=f"f({x_val:.4g}) = {y_point:.4f}",
        ))

    fig.update_layout(
        title=title,
        xaxis_title="x",
        yaxis_title="f(x)",
        template="plotly_white",
        height=420,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig


def build_ogiva(intervals: List[Tuple[float, float]], frequencies: List[int],
                title: str = "Ogiva — F(x) acumulada") -> go.Figure:
    """
    Ogiva de frecuencias relativas acumuladas F(x).
    Puntos: (Li_0, 0), (Ls_0, F_0), (Ls_1, F_1), ..., (Ls_k, 1).
    """
    n = sum(frequencies)
    xs = [intervals[0][0]]   # empieza en el limite inferior del primer intervalo
    ys = [0.0]
    cum = 0
    for (a, b), fi in zip(intervals, frequencies):
        cum += fi
        xs.append(b)
        ys.append(cum / n if n > 0 else 0.0)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=xs, y=ys,
        mode="lines+markers",
        marker=dict(size=7, color="steelblue", symbol="circle"),
        line=dict(color="steelblue", width=2),
        name="F(x)",
        hovertemplate="x=%{x}<br>F(x)=%{y:.4f}<extra></extra>",
    ))
    # Linea de referencia al 50% (mediana)
    fig.add_hline(y=0.5, line_dash="dash", line_color="gray",
                  annotation_text="Me (50%)", annotation_position="right")
    fig.update_layout(
        title=title,
        xaxis_title="x",
        yaxis_title="F(x)",
        template="plotly_white",
        height=400,
        yaxis=dict(range=[-0.05, 1.05]),
    )
    return fig
