"""Idealized Landslide Slope Profile showing sample spatial distribution."""

from typing import Dict, Tuple

import numpy as np
import plotly.graph_objects as go

# Geomorphological Sectors and Sample Coordinates (Distance X [m], Elevation Z [m])
SAMPLE_SLOPE_POSITIONS: Dict[str, Tuple[float, float, str]] = {
    "ML9": (15.0, 92.0, "Detachment Sector"),
    "ML8": (28.0, 84.0, "Detachment Sector"),
    "ML7": (38.0, 78.0, "Detachment Sector"),
    "ML6": (52.0, 72.0, "Counterslope Sector"),
    "ML5": (64.0, 68.0, "Counterslope Sector"),
    "ML4": (78.0, 58.0, "Steep Slope Sector"),
    "ML3": (92.0, 44.0, "Steep Slope Sector"),
    "ML1": (108.0, 30.0, "Steep Slope Sector"),
    "ML10": (132.0, 12.0, "Undisturbed Basal Clay"),
    "Sand_R": (148.0, 8.0, "Archie Sand Reference"),
}

SECTOR_COLORS: Dict[str, str] = {
    "Detachment Sector": "rgb(214, 39, 40)",
    "Counterslope Sector": "rgb(255, 127, 14)",
    "Steep Slope Sector": "rgb(44, 160, 44)",
    "Undisturbed Basal Clay": "rgb(31, 119, 180)",
    "Archie Sand Reference": "rgb(148, 103, 189)",
}


def crea_profilo_versante_plotly(campione_attivo: str = "ML3") -> go.Figure:
    """Generates an idealized landslide topographic profile highlighting sample position."""
    fig = go.Figure()

    # 1. Idealized topography curve
    x_topo = np.array([0, 10, 20, 35, 45, 55, 65, 75, 90, 105, 120, 130, 145, 160])
    z_topo = np.array([100, 95, 90, 80, 76, 71, 67, 60, 46, 32, 18, 13, 10, 8])

    # Dense smooth spline for topography
    x_smooth = np.linspace(0, 160, 200)
    z_smooth = np.interp(x_smooth, x_topo, z_topo)

    # Shaded topography area (ground)
    fig.add_trace(
        go.Scatter(
            x=x_smooth,
            y=z_smooth,
            mode="lines",
            line=dict(color="rgb(80, 60, 40)", width=2.5),
            fill="tozeroy",
            fillcolor="rgba(210, 195, 175, 0.35)",
            hoverinfo="skip",
            name="Topographic Surface",
        )
    )

    # 2. Sector background annotations / shaded boundaries
    sectors = [
        ("Detachment Sector", 0, 45, "rgba(214, 39, 40, 0.08)"),
        ("Counterslope Sector", 45, 70, "rgba(255, 127, 14, 0.08)"),
        ("Steep Slope Sector", 70, 120, "rgba(44, 160, 44, 0.08)"),
        ("Undisturbed Basal Clay", 120, 160, "rgba(31, 119, 180, 0.08)"),
    ]

    for sec_name, x0, x1, col in sectors:
        fig.add_vrect(
            x0=x0,
            x1=x1,
            fillcolor=col,
            layer="below",
            line_width=0,
        )

    # 3. Add other samples (grey/muted circles)
    other_x, other_y, other_text, other_names = [], [], [], []
    active_x, active_y, active_text, active_sec = None, None, None, None

    for s_name, (sx, sz, s_sec) in SAMPLE_SLOPE_POSITIONS.items():
        tip = f"<b>Sample {s_name}</b><br>Sector: {s_sec}<br>Relative Elevation: {sz} m"
        if s_name == campione_attivo:
            active_x, active_y, active_text, active_sec = sx, sz, tip, s_sec
        else:
            other_x.append(sx)
            other_y.append(sz)
            other_text.append(tip)
            other_names.append(s_name)

    if other_x:
        fig.add_trace(
            go.Scatter(
                x=other_x,
                y=other_y,
                mode="markers+text",
                marker=dict(size=9, color="rgb(100, 100, 100)", symbol="circle"),
                text=other_names,
                textposition="top center",
                textfont=dict(size=9, color="rgb(80, 80, 80)"),
                hoverinfo="text",
                hovertext=other_text,
                name="Other Samples",
            )
        )

    # 4. Highlight Active Sample with prominent glowing marker and annotation
    if active_x is not None and active_y is not None:
        sec_col = SECTOR_COLORS.get(active_sec, "red")
        fig.add_trace(
            go.Scatter(
                x=[active_x],
                y=[active_y],
                mode="markers+text",
                marker=dict(
                    size=15,
                    color=sec_col,
                    symbol="circle",
                    line=dict(width=3, color="black"),
                ),
                text=[f"<b>{campione_attivo}</b>"],
                textposition="bottom center",
                textfont=dict(size=12, color="black"),
                hoverinfo="text",
                hovertext=[active_text],
                name=f"Active Sample: {campione_attivo}",
            )
        )

    fig.update_layout(
        title=dict(
            text=f"Slope Profile: <b>{campione_attivo}</b> ({active_sec or ''})",
            x=0.5,
            font=dict(size=13),
        ),
        xaxis=dict(
            title="Profile Distance [m]",
            showgrid=True,
            gridcolor="lightgrey",
            zeroline=False,
            range=[-5, 165],
        ),
        yaxis=dict(
            title="Relative Elevation [m]",
            showgrid=True,
            gridcolor="lightgrey",
            zeroline=False,
            range=[0, 115],
        ),
        template="plotly_white",
        margin=dict(l=40, r=20, t=35, b=35),
        showlegend=False,
    )
    return fig
