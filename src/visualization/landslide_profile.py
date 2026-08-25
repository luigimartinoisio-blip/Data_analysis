"""Landslide Slope Profile with custom visual ratio 1.6:1 and stacked sample labels."""

from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.signal import savgol_filter

# Always resolve paths relative to repository root
BASE_DIR = Path(__file__).resolve().parents[2]
TOPO_DIR = BASE_DIR / "projects" / "Hyprop_geotom_01Carl" / "data" / "raw" / "topography"
PROFILO_CSV = TOPO_DIR / "profilo_sampling_point.csv"
POSIZIONI_CSV = TOPO_DIR / "posizioni_sampling_point.csv"

# Sector definitions and colors
SECTORS_DEF: List[Tuple[str, float, float, str]] = [
    ("Detachment Sector (0 - 45 m)", 0.0, 45.0, "rgb(214, 39, 40)"),
    ("Counterslope Sector (45 - 75 m)", 45.0, 75.0, "rgb(255, 127, 14)"),
    ("Steep Slope Sector (75 - 112 m)", 75.0, 112.0, "rgb(44, 160, 44)"),
    ("Undisturbed Outside Landslide (> 112 m)", 112.0, 330.0, "rgb(31, 119, 180)"),
]

SECTOR_COLORS: Dict[str, str] = {
    "Detachment Sector": "rgb(214, 39, 40)",
    "Counterslope Sector": "rgb(255, 127, 14)",
    "Steep Slope Sector": "rgb(44, 160, 44)",
    "Undisturbed Outside Landslide": "rgb(31, 119, 180)",
}

# Sampling locations grouped by spatial distance X
# Format: distance_x: (sector, [(sample_name, depth_label, field_code)])
SAMPLING_STATIONS: Dict[float, Tuple[str, List[Tuple[str, str, str]]]] = {
    10.0: (
        "Detachment Sector",
        [("ML9", "Depth: -50 cm", "4b")],
    ),
    36.0: (
        "Detachment Sector",
        [("ML7", "Surface: 0 cm", "3a"), ("ML8", "Depth: -50 cm", "3b")],
    ),
    72.0: (
        "Counterslope Sector",
        [("ML5", "Surface: 0 cm", "2a"), ("ML6", "Depth: -50 cm", "2b")],
    ),
    93.0: (
        "Steep Slope Sector",
        [("ML3", "Surface: 0 cm", "1a"), ("ML4", "Depth: -50 cm", "1b")],
    ),
    108.0: (
        "Steep Slope Sector",
        [("ML1", "Surface: 0 cm", "5a")],
    ),
    317.0: (
        "Undisturbed Outside Landslide",
        [("ML10", "Surface: 0 cm", "6a")],
    ),
}

# Flat metadata dictionary for individual sample lookup
SAMPLE_SLOPE_SPECS: Dict[str, Tuple[float, float, str, str, str]] = {
    "ML9": (10.0, 627.0, "Detachment Sector", "Depth: -50 cm", "4b (-50 cm)"),
    "ML7": (36.0, 625.0, "Detachment Sector", "Surface (0 cm)", "3a (0 cm)"),
    "ML8": (36.0, 625.0, "Detachment Sector", "Depth: -50 cm", "3b (-50 cm)"),
    "ML5": (72.0, 623.0, "Counterslope Sector", "Surface (0 cm)", "2a (0 cm)"),
    "ML6": (72.0, 623.0, "Counterslope Sector", "Depth: -50 cm", "2b (-50 cm)"),
    "ML3": (93.0, 619.0, "Steep Slope Sector", "Surface (0 cm)", "1a (0 cm)"),
    "ML4": (93.0, 619.0, "Steep Slope Sector", "Depth: -50 cm", "1b (-50 cm)"),
    "ML1": (108.0, 615.0, "Steep Slope Sector", "Surface (0 cm)", "5a (0 cm)"),
    "ML10": (317.0, 583.0, "Undisturbed Outside Landslide", "Surface (0 cm)", "6a (0 cm)"),
}


def carica_profilo_topografico_interpolato() -> Tuple[np.ndarray, np.ndarray, float, float]:
    """Carica i dati topografici e genera una curva continua interpolata senza scalini."""
    if PROFILO_CSV.exists():
        df = pd.read_csv(PROFILO_CSV)
        if "distance" in df.columns and "quota_z" in df.columns:
            x_raw = df["distance"].to_numpy(dtype=float)
            z_raw = df["quota_z"].to_numpy(dtype=float)

            # Savitzky-Golay smoothing to eliminate digital step discretization
            window = min(25, len(z_raw) if len(z_raw) % 2 == 1 else len(z_raw) - 1)
            z_filt = savgol_filter(z_raw, window_length=window, polyorder=3)

            x_dense = np.linspace(float(x_raw[0]), float(x_raw[-1]), 500)
            z_dense = np.interp(x_dense, x_raw, z_filt)
            return x_dense, z_dense, float(np.min(z_filt)), float(np.max(z_filt))

    # Fallback
    x_fb = np.linspace(0, 326, 300)
    z_fb = np.linspace(629, 581, 300)
    return x_fb, z_fb, 581.0, 629.0


def crea_profilo_versante_plotly(campione_attivo: str = "ML3") -> go.Figure:
    """Generates the topographic profile with 1.6:1 visual ratio, single surface points,

    stacked labels, sector legend, and exact title 'Landslide Slope Profile'.
    """
    fig = go.Figure()

    # 1. Continuous interpolated topography curve
    x_topo, z_topo, z_min, z_max = carica_profilo_topografico_interpolato()
    y_min_axis = z_min - 5.0  # Asse Y parte da 5m sotto la quota minima (576 m)

    # Shaded ground topography
    fig.add_trace(
        go.Scatter(
            x=x_topo,
            y=z_topo,
            mode="lines",
            line=dict(color="rgb(90, 60, 40)", width=2.8),
            fill="tozeroy",
            fillcolor="rgba(215, 200, 180, 0.35)",
            hoverinfo="skip",
            showlegend=False,
            name="Topographic Surface",
        )
    )

    # 2. Sector background shaded zones + Sector Legend entries
    for sec_name, x0, x1, col in SECTORS_DEF:
        # Shaded background box
        fig.add_vrect(
            x0=x0,
            x1=x1,
            fillcolor=col.replace("rgb", "rgba").replace(")", ", 0.08)"),
            layer="below",
            line_width=0,
        )
        # Dummy trace for sector legend
        fig.add_trace(
            go.Scatter(
                x=[None],
                y=[None],
                mode="markers",
                marker=dict(size=10, color=col, symbol="square"),
                name=sec_name,
                showlegend=True,
            )
        )

    # 3. Single surface point per sampling location with stacked labels
    for dist_x, (sector_name, samples_list) in SAMPLING_STATIONS.items():
        z_surf = float(np.interp(dist_x, x_topo, z_topo))
        sample_names = [s[0] for s in samples_list]
        is_active_station = campione_attivo in sample_names

        # Build clean stacked label
        lines_label = []
        tooltip_lines = [
            f"<b>Sector</b>: {sector_name}",
            f"<b>Distance</b>: {dist_x:.0f} m from crest",
            f"<b>Surface Elevation</b>: {z_surf:.1f} m a.s.l.",
            "<b>Samples at this station:</b>",
        ]

        for s_name, s_depth, s_code in samples_list:
            if s_name == campione_attivo:
                lines_label.append(f"<b>▶ {s_name} ({s_depth})</b>")
                tooltip_lines.append(f"• <b>[ACTIVE] {s_name} ({s_code})</b>: {s_depth}")
            else:
                lines_label.append(f"{s_name} ({s_depth})")
                tooltip_lines.append(f"• {s_name} ({s_code}): {s_depth}")

        stacked_text = "<br>".join(lines_label)
        tooltip_html = "<br>".join(tooltip_lines)

        if is_active_station:
            # Highlighted Active Station Point
            sec_col = SECTOR_COLORS.get(sector_name, "red")
            fig.add_trace(
                go.Scatter(
                    x=[dist_x],
                    y=[z_surf],
                    mode="markers+text",
                    marker=dict(
                        size=12,
                        color=sec_col,
                        symbol="circle",
                        line=dict(width=2.2, color="black"),
                    ),
                    text=[stacked_text],
                    textposition="top right" if dist_x < 250 else "top left",
                    textfont=dict(size=10, color="black"),
                    hoverinfo="text",
                    hovertext=[tooltip_html],
                    showlegend=False,
                    name=f"Active: {campione_attivo}",
                )
            )
        else:
            # Neutral Station Point
            fig.add_trace(
                go.Scatter(
                    x=[dist_x],
                    y=[z_surf],
                    mode="markers+text",
                    marker=dict(size=7.5, color="rgb(90, 90, 90)", symbol="circle"),
                    text=[stacked_text],
                    textposition="top right" if dist_x < 250 else "top left",
                    textfont=dict(size=8.5, color="rgb(70, 70, 70)"),
                    hoverinfo="text",
                    hovertext=[tooltip_html],
                    showlegend=False,
                    name=f"Station {dist_x:.0f}m",
                )
            )

    # 4. Strict Title: "Landslide Slope Profile"
    # Visual Ratio: 1 unit on X = 1.6x display space of Y -> scaleratio = 1 / 1.6 = 0.625
    fig.update_layout(
        title=dict(
            text="Landslide Slope Profile",
            x=0.5,
            font=dict(size=14, color="black"),
        ),
        xaxis=dict(
            title="Profile Distance from Crest [m]",
            showgrid=True,
            gridcolor="lightgrey",
            zeroline=False,
            range=[-10, float(x_topo[-1]) + 15],
        ),
        yaxis=dict(
            title="Elevation [m a.s.l.]",
            scaleanchor="x",
            scaleratio=0.625,  # X:Y visual display ratio = 1.6:1
            showgrid=True,
            gridcolor="lightgrey",
            zeroline=False,
            range=[y_min_axis, z_max + 12],
        ),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.22,
            xanchor="center",
            x=0.5,
            font=dict(size=9.5),
            title=dict(text="<b>Sectors:</b>", font=dict(size=10)),
        ),
        template="plotly_white",
        margin=dict(l=50, r=20, t=40, b=70),
        showlegend=True,
    )
    return fig
