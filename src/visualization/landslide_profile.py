"""Landslide Slope Profile with smooth 1:1 true-scale interpolation."""

from pathlib import Path
from typing import Any, Dict, Tuple

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.signal import savgol_filter

# Always resolve paths relative to repository root
BASE_DIR = Path(__file__).resolve().parents[2]
TOPO_DIR = BASE_DIR / "projects" / "Hyprop_geotom_01Carl" / "data" / "raw" / "topography"
PROFILO_CSV = TOPO_DIR / "profilo_sampling_point.csv"
POSIZIONI_CSV = TOPO_DIR / "posizioni_sampling_point.csv"

# Sector classification and depth specification for samples (Sand_R strictly excluded)
SAMPLE_METADATA: Dict[str, Tuple[str, str, str, bool]] = {
    # sample_id: (sector, depth_label, field_code, is_deep)
    "ML9": ("Detachment Sector", "Depth: -50 cm", "4b (-50 cm)", True),
    "ML7": ("Detachment Sector", "Surface (0 cm)", "3a (0 cm)", False),
    "ML8": ("Detachment Sector", "Depth: -50 cm", "3b (-50 cm)", True),
    "ML5": ("Counterslope Sector", "Surface (0 cm)", "2a (0 cm)", False),
    "ML6": ("Counterslope Sector", "Depth: -50 cm", "2b (-50 cm)", True),
    "ML3": ("Steep Slope Sector", "Surface (0 cm)", "1a (0 cm)", False),
    "ML4": ("Steep Slope Sector", "Depth: -50 cm", "1b (-50 cm)", True),
    "ML1": ("Steep Slope Sector", "Surface (0 cm)", "5a (0 cm)", False),
    "ML10": ("Undisturbed Outside Landslide", "Surface (0 cm)", "6a (0 cm)", False),
}

# Geomorphological Sectors, Spatial Distance X [m], Elevation Z [m a.s.l.], Depth, and Label
SAMPLE_SLOPE_SPECS: Dict[str, Tuple[float, float, str, str, str]] = {
    # sample_id: (distance_m, elevation_z_m, sector, depth_label, field_code)
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

SECTOR_COLORS: Dict[str, str] = {
    "Detachment Sector": "rgb(214, 39, 40)",
    "Counterslope Sector": "rgb(255, 127, 14)",
    "Steep Slope Sector": "rgb(44, 160, 44)",
    "Undisturbed Outside Landslide": "rgb(31, 119, 180)",
}


def carica_profilo_topografico_interpolato() -> Tuple[np.ndarray, np.ndarray, float, float]:
    """Carica i dati topografici e genera una curva continua interpolata senza scalini."""
    if PROFILO_CSV.exists():
        df = pd.read_csv(PROFILO_CSV)
        if "distance" in df.columns and "quota_z" in df.columns:
            x_raw = df["distance"].to_numpy(dtype=float)
            z_raw = df["quota_z"].to_numpy(dtype=float)

            # Smooth curve using Savitzky-Golay filter to eliminate step artifacts
            window = min(25, len(z_raw) if len(z_raw) % 2 == 1 else len(z_raw) - 1)
            z_filt = savgol_filter(z_raw, window_length=window, polyorder=3)

            # High-density interpolation for continuous profile
            x_dense = np.linspace(float(x_raw[0]), float(x_raw[-1]), 500)
            z_dense = np.interp(x_dense, x_raw, z_filt)
            return x_dense, z_dense, float(np.min(z_filt)), float(np.max(z_filt))

    # Fallback
    x_fb = np.linspace(0, 326, 300)
    z_fb = np.linspace(629, 581, 300)
    return x_fb, z_fb, 581.0, 629.0


def carica_posizioni_campioni(x_topo: np.ndarray, z_topo: np.ndarray) -> Dict[str, Dict[str, Any]]:
    """Carica le posizioni metriche dei campioni e calcola quota di superficie e profondità."""
    dist_map: Dict[str, float] = {
        "ML9": 10.0,
        "ML7": 36.0,
        "ML8": 36.0,
        "ML5": 72.0,
        "ML6": 72.0,
        "ML3": 93.0,
        "ML4": 93.0,
        "ML1": 108.0,
        "ML10": 317.0,
    }

    if POSIZIONI_CSV.exists():
        try:
            df_pos = pd.read_csv(POSIZIONI_CSV, header=None, names=["sample", "distance"])
            for _, row in df_pos.iterrows():
                s_id = str(row["sample"]).strip()
                if s_id in SAMPLE_METADATA:
                    dist_map[s_id] = float(row["distance"])
        except Exception:
            pass

    campioni_dict: Dict[str, Dict[str, Any]] = {}
    for s_id, (sec, d_lbl, f_code, is_deep) in SAMPLE_METADATA.items():
        dist_x = dist_map.get(s_id, 0.0)
        z_surf = float(np.interp(dist_x, x_topo, z_topo))
        # Visual depth offset (-1.5 m in 1:1 true scale)
        z_point = (z_surf - 1.5) if is_deep else z_surf

        campioni_dict[s_id] = {
            "x": dist_x,
            "z_surf": z_surf,
            "z_point": z_point,
            "sector": sec,
            "depth_label": d_lbl,
            "field_code": f_code,
            "is_deep": is_deep,
        }
    return campioni_dict


def crea_profilo_versante_plotly(campione_attivo: str = "ML3") -> go.Figure:
    """Generates the continuous 1:1 true-scale topographic profile."""
    fig = go.Figure()

    # 1. Continuous interpolated topography (1:1 scale)
    x_topo, z_topo, z_min, z_max = carica_profilo_topografico_interpolato()
    campioni = carica_posizioni_campioni(x_topo, z_topo)

    y_min_axis = z_min - 5.0  # 5 metri sotto la quota più bassa (576 m)

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
            name="Topographic Surface",
        )
    )

    # 2. Sector background shaded zones (0-45m, 45-75m, 75-112m, >112m)
    sectors = [
        ("Detachment Sector (0-45m)", 0, 45, "rgba(214, 39, 40, 0.09)"),
        ("Counterslope Sector (45-75m)", 45, 75, "rgba(255, 127, 14, 0.09)"),
        ("Steep Slope Sector (75-112m)", 75, 112, "rgba(44, 160, 44, 0.09)"),
        (
            "Undisturbed Outside Landslide (>112m)",
            112,
            float(x_topo[-1]) + 5,
            "rgba(31, 119, 180, 0.08)",
        ),
    ]

    for sec_name, x0, x1, col in sectors:
        fig.add_vrect(
            x0=x0,
            x1=x1,
            fillcolor=col,
            layer="below",
            line_width=0,
            annotation_text=sec_name.split(" ")[0],
            annotation_position="top left",
            annotation_font=dict(size=9, color="rgba(80, 80, 80, 0.7)"),
        )

    # 3. Vertical dashed connector lines for Surface / -50cm pairs
    depth_pairs = [
        ("ML7", "ML8"),  # 3a (0cm) and 3b (-50cm) at x = 36 m
        ("ML5", "ML6"),  # 2a (0cm) and 2b (-50cm) at x = 72 m
        ("ML3", "ML4"),  # 1a (0cm) and 1b (-50cm) at x = 93 m
    ]
    for s_top, s_bot in depth_pairs:
        if s_top in campioni and s_bot in campioni:
            c_top = campioni[s_top]
            c_bot = campioni[s_bot]
            fig.add_trace(
                go.Scatter(
                    x=[c_top["x"], c_bot["x"]],
                    y=[c_top["z_point"], c_bot["z_point"]],
                    mode="lines",
                    line=dict(color="rgba(70, 70, 70, 0.7)", width=1.5, dash="dash"),
                    hoverinfo="skip",
                    showlegend=False,
                )
            )

    # Line for ML9 (-50cm) from ground surface
    if "ML9" in campioni:
        c_ml9 = campioni["ML9"]
        fig.add_trace(
            go.Scatter(
                x=[c_ml9["x"], c_ml9["x"]],
                y=[c_ml9["z_surf"], c_ml9["z_point"]],
                mode="lines",
                line=dict(color="rgba(70, 70, 70, 0.7)", width=1.5, dash="dash"),
                hoverinfo="skip",
                showlegend=False,
            )
        )

    # 4. Inactive samples (small grey dots)
    other_x, other_y, other_text, other_names = [], [], [], []
    active_data = campioni.get(campione_attivo)

    for s_id, info in campioni.items():
        tip = (
            f"<b>Sample {s_id} ({info['field_code']})</b><br>"
            f"Sector: {info['sector']}<br>"
            f"Distance: {info['x']:.0f} m<br>"
            f"{info['depth_label']}<br>"
            f"Elevation: {info['z_surf']:.1f} m a.s.l."
        )
        if s_id != campione_attivo:
            other_x.append(info["x"])
            other_y.append(info["z_point"])
            other_text.append(tip)
            other_names.append(s_id)

    if other_x:
        fig.add_trace(
            go.Scatter(
                x=other_x,
                y=other_y,
                mode="markers+text",
                marker=dict(size=7, color="rgb(100, 100, 100)", symbol="circle"),
                text=other_names,
                textposition="top right",
                textfont=dict(size=9, color="rgb(60, 60, 60)"),
                hoverinfo="text",
                hovertext=other_text,
                name="Other Samples",
            )
        )

    # 5. Highlight Active Sample
    if active_data:
        sec_col = SECTOR_COLORS.get(active_data["sector"], "red")
        act_tip = (
            f"<b>Sample {campione_attivo} ({active_data['field_code']})</b><br>"
            f"Sector: {active_data['sector']}<br>"
            f"Distance: {active_data['x']:.0f} m<br>"
            f"{active_data['depth_label']}<br>"
            f"Elevation: {active_data['z_surf']:.1f} m a.s.l."
        )
        fig.add_trace(
            go.Scatter(
                x=[active_data["x"]],
                y=[active_data["z_point"]],
                mode="markers+text",
                marker=dict(
                    size=12,
                    color=sec_col,
                    symbol="circle",
                    line=dict(width=2.2, color="black"),
                ),
                text=[f"<b>{campione_attivo}</b> ({active_data['depth_label']})"],
                textposition="bottom center",
                textfont=dict(size=10.5, color="black"),
                hoverinfo="text",
                hovertext=[act_tip],
                name=f"Active: {campione_attivo}",
            )
        )

    if active_data:
        d_lbl = active_data["depth_label"]
        sec_lbl = active_data["sector"]
        titolo = f"1:1 True-Scale Slope Profile: <b>{campione_attivo}</b> [{d_lbl} - {sec_lbl}]"
    else:
        titolo = f"1:1 True-Scale Slope Profile ({campione_attivo})"

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
            range=[-5, float(x_topo[-1]) + 10],
        ),
        yaxis=dict(
            title="Elevation [m a.s.l.]",
            scaleanchor="x",  # 1:1 TRUE SCALE (same unit for X and Y)
            scaleratio=1.0,
            showgrid=True,
            gridcolor="lightgrey",
            zeroline=False,
            range=[y_min_axis, z_max + 6],
        ),
        template="plotly_white",
        margin=dict(l=50, r=20, t=35, b=35),
        showlegend=False,
    )
    return fig
