"""Idealized Landslide Slope Profile showing exact spatial and depth distribution."""

from pathlib import Path
from typing import Dict, Tuple

import numpy as np
import pandas as pd
import plotly.graph_objects as go

# Geomorphological Sectors, Spatial Distance X [m], Elevation Z [m], Depth [cm], and Label
SAMPLE_SLOPE_SPECS: Dict[str, Tuple[float, float, str, str, str]] = {
    # Sector: Detachment
    "ML9": (10.0, 90.0, "Detachment Sector", "Depth: -50 cm", "4b (-50 cm)"),
    "ML7": (36.0, 82.0, "Detachment Sector", "Surface (0 cm)", "3a (0 cm)"),
    "ML8": (36.0, 77.0, "Detachment Sector", "Depth: -50 cm", "3b (-50 cm)"),
    # Sector: Counterslope
    "ML5": (72.0, 73.0, "Counterslope Sector", "Surface (0 cm)", "2a (0 cm)"),
    "ML6": (72.0, 68.0, "Counterslope Sector", "Depth: -50 cm", "2b (-50 cm)"),
    # Sector: Steep Slope
    "ML3": (93.0, 52.0, "Steep Slope Sector", "Surface (0 cm)", "1a (0 cm)"),
    "ML4": (93.0, 47.0, "Steep Slope Sector", "Depth: -50 cm", "1b (-50 cm)"),
    "ML1": (108.0, 36.0, "Steep Slope Sector", "Surface (0 cm)", "5a (0 cm)"),
    # Sector: Undisturbed Basal Outcrop
    "ML10": (317.0, 10.0, "Undisturbed Basal Clay", "Surface (0 cm)", "6a (0 cm)"),
}

SECTOR_COLORS: Dict[str, str] = {
    "Detachment Sector": "rgb(214, 39, 40)",
    "Counterslope Sector": "rgb(255, 127, 14)",
    "Steep Slope Sector": "rgb(44, 160, 44)",
    "Undisturbed Basal Clay": "rgb(31, 119, 180)",
}

TOPO_DIR = Path("projects/Hyprop_geotom_01Carl/data/raw/topography")


def carica_punti_topografia() -> Tuple[np.ndarray, np.ndarray]:
    """Carica i punti (X, Z) del profilo topografico da file se presente, o usa i nodi rilevati."""
    # Controlla se esiste un file topografia dedicato con coordinate X, Z
    for fn in ["profilo_topografia.csv", "topografia.csv", "profilo.xlsx", "profilo.csv"]:
        f_path = TOPO_DIR / fn
        if f_path.exists():
            try:
                if f_path.suffix == ".xlsx":
                    df = pd.read_excel(f_path, sheet_name=0)
                else:
                    df = pd.read_csv(f_path)
                if df.shape[1] >= 2:
                    x = pd.to_numeric(df.iloc[:, 0], errors="coerce").dropna().to_numpy()
                    z = pd.to_numeric(df.iloc[:, 1], errors="coerce").dropna().to_numpy()
                    if len(x) >= 2 and len(x) == len(z):
                        return x, z
            except Exception:
                pass

    # Nodi rilevati lungo il profilo di 350 metri
    x_topo = np.array([0, 10, 25, 36, 50, 72, 85, 93, 108, 120, 150, 200, 260, 317, 345])
    z_topo = np.array([100, 95, 88, 82, 77, 73, 62, 52, 36, 25, 20, 15, 12, 10, 8])
    return x_topo, z_topo


def crea_profilo_versante_plotly(campione_attivo: str = "ML3") -> go.Figure:
    """Generates an idealized landslide topographic profile highlighting position and depth."""
    fig = go.Figure()

    # 1. Topography curve
    x_topo, z_topo = carica_punti_topografia()
    z_min_topo = float(np.min(z_topo))
    y_min_axis = z_min_topo - 5.0  # Asse Y parte da 5 metri sotto la quota più bassa

    x_smooth = np.linspace(float(x_topo[0]), float(x_topo[-1]), 300)
    z_smooth = np.interp(x_smooth, x_topo, z_topo)

    # Shaded ground topography
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
        ("Detachment Sector", 0, 50, "rgba(214, 39, 40, 0.08)"),
        ("Counterslope Sector", 50, 80, "rgba(255, 127, 14, 0.08)"),
        ("Steep Slope Sector", 80, 130, "rgba(44, 160, 44, 0.08)"),
        ("Undisturbed Basal Clay", 280, float(x_topo[-1]), "rgba(31, 119, 180, 0.08)"),
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
        ("ML7", "ML8"),  # 3a (0cm) and 3b (-50cm) at x = 36 m
        ("ML5", "ML6"),  # 2a (0cm) and 2b (-50cm) at x = 72 m
        ("ML3", "ML4"),  # 1a (0cm) and 1b (-50cm) at x = 93 m
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

    # Vertical connector for ML9 (-50cm) at x = 10 m to ground surface
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

    # 4. Inactive samples (Sand_R excluded)
    other_x, other_y, other_text, other_names = [], [], [], []
    active_x, active_y, active_text, active_sec, active_depth = None, None, None, None, None

    for s_name, (sx, sz, s_sec, s_depth, s_code) in SAMPLE_SLOPE_SPECS.items():
        tip = (
            f"<b>Sample {s_name} ({s_code})</b><br>"
            f"Sector: {s_sec}<br>"
            f"Profile Distance: {sx:.0f} m<br>"
            f"{s_depth}<br>"
            f"Rel. Elevation: {sz:.1f} m"
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

    # 5. Highlight Active Sample (if in natural samples)
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

    titolo = (
        f"Slope Profile: <b>{campione_attivo}</b> [{active_depth or ''} — {active_sec or ''}]"
        if active_sec
        else f"Slope Profile (Lab Reference: {campione_attivo})"
    )
    fig.update_layout(
        title=dict(
            text=titolo,
            x=0.5,
            font=dict(size=12),
        ),
        xaxis=dict(
            title="Profile Distance from Crest [m]",
            showgrid=True,
            gridcolor="lightgrey",
            zeroline=False,
            range=[-10, float(x_topo[-1]) + 15],
        ),
        yaxis=dict(
            title="Relative Elevation [m]",
            showgrid=True,
            gridcolor="lightgrey",
            zeroline=False,
            range=[y_min_axis, float(np.max(z_topo)) + 15],
        ),
        template="plotly_white",
        margin=dict(l=40, r=20, t=35, b=35),
        showlegend=False,
    )
    return fig
