"""Construccion de graficos con Plotly."""

import plotly.graph_objects as go
from typing import List, Dict, Optional


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
