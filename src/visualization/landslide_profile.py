"""Idealized Landslide Slope Profile showing exact spatial and depth distribution."""

from typing import Dict, Tuple

import numpy as np
import plotly.graph_objects as go

# Geomorphological Sectors, Spatial X [m], Elevation Z [m], Depth [cm], and Depth Label
SAMPLE_SLOPE_SPECS: Dict[str, Tuple[float, float, str, str, str]] = {
    # Sector: Detachment
    "ML9": (15.0, 92.0, "Detachment Sector", "Depth: -50 cm", "4b (-50 cm)"),
    "ML7": (35.0, 80.0, "Detachment Sector", "Surface (0 cm)", "3a (0 cm)"),
    "ML8": (35.0, 75.0, "Detachment Sector", "Depth: -50 cm", "3b (-50 cm)"),
    # Sector: Counterslope
    "ML5": (58.0, 70.0, "Counterslope Sector", "Surface (0 cm)", "2a (0 cm)"),
    "ML6": (58.0, 65.0, "Counterslope Sector", "Depth: -50 cm", "2b (-50 cm)"),
    # Sector: Steep Slope
    "ML3": (88.0, 48.0, "Steep Slope Sector", "Surface (0 cm)", "1a (0 cm)"),
    "ML4": (88.0, 43.0, "Steep Slope Sector", "Depth: -50 cm", "1b (-50 cm)"),
    "ML1": (108.0, 30.0, "Steep Slope Sector", "Surface (0 cm)", "5a (0 cm)"),
    # Sector: Undisturbed Basal Outcrop
    "ML10": (132.0, 13.0, "Undisturbed Basal Clay", "Surface (0 cm)", "6a (0 cm)"),
    # Outgroup
    "Sand_R": (150.0, 8.0, "Archie Sand Reference", "Lab Benchmark", "Sand_R"),
}

SECTOR_COLORS: Dict[str, str] = {
    "Detachment Sector": "rgb(214, 39, 40)",
    "Counterslope Sector": "rgb(255, 127, 14)",
    "Steep Slope Sector": "rgb(44, 160, 44)",
    "Undisturbed Basal Clay": "rgb(31, 119, 180)",
    "Archie Sand Reference": "rgb(148, 103, 189)",
}


def crea_profilo_versante_plotly(campione_attivo: str = "ML3") -> go.Figure:
    """Generates an idealized landslide topographic profile highlighting position and depth."""
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
            line=dict(color="rgb(90, 65, 45)", width=2.5),
            fill="tozeroy",
            fillcolor="rgba(215, 200, 180, 0.35)",
            hoverinfo="skip",
            name="Topographic Surface",
        )
    )

    # 2. Sector background shaded zones
    sectors = [
        ("Detachment Sector", 0, 45, "rgba(214, 39, 40, 0.08)"),
        ("Counterslope Sector", 45, 70, "rgba(255, 127, 14, 0.08)"),
        ("Steep Slope Sector", 70, 120, "rgba(44, 160, 44, 0.08)"),
        ("Undisturbed Basal Clay", 120, 160, "rgba(31, 119, 180, 0.08)"),
    ]

    for _, x0, x1, col in sectors:
        fig.add_vrect(
            x0=x0,
            x1=x1,
            fillcolor=col,
            layer="below",
            line_width=0,
        )

    # 3. Vertical dashed connector lines for Surface / -50cm pairs
    depth_pairs = [
        ("ML7", "ML8"),  # 3a (0cm) and 3b (-50cm)
        ("ML5", "ML6"),  # 2a (0cm) and 2b (-50cm)
        ("ML3", "ML4"),  # 1a (0cm) and 1b (-50cm)
    ]
    for s_top, s_bot in depth_pairs:
        top_spec = SAMPLE_SLOPE_SPECS[s_top]
        bot_spec = SAMPLE_SLOPE_SPECS[s_bot]
        fig.add_trace(
            go.Scatter(
                x=[top_spec[0], bot_spec[0]],
                y=[top_spec[1], bot_spec[1]],
                mode="lines",
                line=dict(color="rgba(100, 100, 100, 0.6)", width=1.5, dash="dash"),
                hoverinfo="skip",
                showlegend=False,
            )
        )

    # Vertical connector for ML9 (-50cm) to ground surface
    ml9_x, ml9_z = SAMPLE_SLOPE_SPECS["ML9"][0], SAMPLE_SLOPE_SPECS["ML9"][1]
    ground_z_ml9 = float(np.interp(ml9_x, x_topo, z_topo))
    fig.add_trace(
        go.Scatter(
            x=[ml9_x, ml9_x],
            y=[ground_z_ml9, ml9_z],
            mode="lines",
            line=dict(color="rgba(100, 100, 100, 0.6)", width=1.5, dash="dash"),
            hoverinfo="skip",
            showlegend=False,
        )
    )

    # 4. Inactive samples
    other_x, other_y, other_text, other_names = [], [], [], []
    active_x, active_y, active_text, active_sec, active_depth = None, None, None, None, None

    for s_name, (sx, sz, s_sec, s_depth, s_code) in SAMPLE_SLOPE_SPECS.items():
        tip = (
            f"<b>Sample {s_name} ({s_code})</b><br>"
            f"Sector: {s_sec}<br>"
            f"{s_depth}<br>"
            f"Rel. Elevation: {sz} m"
        )
        if s_name == campione_attivo:
            active_x, active_y, active_text, active_sec, active_depth = sx, sz, tip, s_sec, s_depth
        else:
            other_x.append(sx)
            other_y.append(sz)
            other_text.append(tip)
            other_names.append(f"{s_name}")

    if other_x:
        fig.add_trace(
            go.Scatter(
                x=other_x,
                y=other_y,
                mode="markers+text",
                marker=dict(size=8, color="rgb(110, 110, 110)", symbol="circle"),
                text=other_names,
                textposition="top right",
                textfont=dict(size=9, color="rgb(70, 70, 70)"),
                hoverinfo="text",
                hovertext=other_text,
                name="Other Samples",
            )
        )

    # 5. Highlight Active Sample
    if active_x is not None and active_y is not None:
        sec_col = SECTOR_COLORS.get(active_sec, "red")
        fig.add_trace(
            go.Scatter(
                x=[active_x],
                y=[active_y],
                mode="markers+text",
                marker=dict(
                    size=14,
                    color=sec_col,
                    symbol="circle",
                    line=dict(width=2.5, color="black"),
                ),
                text=[f"<b>{campione_attivo}</b> ({active_depth})"],
                textposition="bottom center",
                textfont=dict(size=11, color="black"),
                hoverinfo="text",
                hovertext=[active_text],
                name=f"Active: {campione_attivo}",
            )
        )

    titolo = f"Slope Location: <b>{campione_attivo}</b> [{active_depth or ''} — {active_sec or ''}]"
    fig.update_layout(
        title=dict(
            text=titolo,
            x=0.5,
            font=dict(size=12),
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
