"""Landslide Slope Profile loaded dynamically from survey CSV files."""

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import numpy as np
import pandas as pd
import plotly.graph_objects as go

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
    "ML10": ("Undisturbed Basal Clay", "Surface (0 cm)", "6a (0 cm)", False),
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
    "ML10": (317.0, 583.0, "Undisturbed Basal Clay", "Surface (0 cm)", "6a (0 cm)"),
}

SECTOR_COLORS: Dict[str, str] = {
    "Detachment Sector": "rgb(214, 39, 40)",
    "Counterslope Sector": "rgb(255, 127, 14)",
    "Steep Slope Sector": "rgb(44, 160, 44)",
    "Undisturbed Basal Clay": "rgb(31, 119, 180)",
}


def carica_profilo_topografico() -> Tuple[np.ndarray, np.ndarray]:
    """Carica la curva topografica reale (distance, quota_z) dal file CSV."""
    if PROFILO_CSV.exists():
        df = pd.read_csv(PROFILO_CSV)
        if "distance" in df.columns and "quota_z" in df.columns:
            return df["distance"].to_numpy(dtype=float), df["quota_z"].to_numpy(dtype=float)

    # Fallback sicuro con quote altimetriche reali (m s.l.m.)
    x_fb = np.array([0, 10, 36, 72, 93, 108, 150, 200, 260, 317, 326], dtype=float)
    z_fb = np.array([629, 627, 625, 623, 619, 615, 608, 600, 592, 583, 581], dtype=float)
    return x_fb, z_fb


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
        # Offset visivo di -2.0 m per i campioni prelevati a -50 cm per distinguerli graficamente
        z_point = (z_surf - 2.0) if is_deep else z_surf

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
    """Generates the topographic profile using real survey CSV data."""
    fig = go.Figure()

    # 1. Topografia reale dal rilievo
    x_topo, z_topo = carica_profilo_topografico()
    campioni = carica_posizioni_campioni(x_topo, z_topo)

    z_min_topo = float(np.min(z_topo))
    z_max_topo = float(np.max(z_topo))
    y_min_axis = z_min_topo - 5.0  # Asse Y parte da 5 metri sotto la quota minima (576 m)

    # Linea del profilo topografico reale
    fig.add_trace(
        go.Scatter(
            x=x_topo,
            y=z_topo,
            mode="lines",
            line=dict(color="rgb(90, 60, 40)", width=3.0),
            fill="tozeroy",
            fillcolor="rgba(215, 200, 180, 0.35)",
            hoverinfo="skip",
            name="Topographic Surface",
        )
    )

    # 2. Settori geomorfologici colorati sullo sfondo
    sectors = [
        ("Detachment Sector", 0, 50, "rgba(214, 39, 40, 0.08)"),
        ("Counterslope Sector", 50, 80, "rgba(255, 127, 14, 0.08)"),
        ("Steep Slope Sector", 80, 130, "rgba(44, 160, 44, 0.08)"),
        ("Undisturbed Basal Clay", 280, float(x_topo[-1]) + 5, "rgba(31, 119, 180, 0.08)"),
    ]

    for _, x0, x1, col in sectors:
        fig.add_vrect(
            x0=x0,
            x1=x1,
            fillcolor=col,
            layer="below",
            line_width=0,
        )

    # 3. Linee tratteggiate verticali che collegano le coppie Superficie / -50cm
    depth_pairs = [
        ("ML7", "ML8"),  # 3a (0cm) e 3b (-50cm) a x = 36 m
        ("ML5", "ML6"),  # 2a (0cm) e 2b (-50cm) a x = 72 m
        ("ML3", "ML4"),  # 1a (0cm) e 1b (-50cm) a x = 93 m
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

    # Linea verticale tratteggiata per ML9 (-50cm) dalla superficie
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

    # 4. Campioni inattivi (cerchi grigi)
    other_x, other_y, other_text, other_names = [], [], [], []
    active_data = campioni.get(campione_attivo)

    for s_id, info in campioni.items():
        tip = (
            f"<b>Sample {s_id} ({info['field_code']})</b><br>"
            f"Sector: {info['sector']}<br>"
            f"Distance from Crest: {info['x']:.0f} m<br>"
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
                marker=dict(size=8, color="rgb(100, 100, 100)", symbol="circle"),
                text=other_names,
                textposition="top right",
                textfont=dict(size=9, color="rgb(60, 60, 60)"),
                hoverinfo="text",
                hovertext=other_text,
                name="Other Samples",
            )
        )

    # 5. Evidenziazione del Campione Attivo
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
                    size=14,
                    color=sec_col,
                    symbol="circle",
                    line=dict(width=2.5, color="black"),
                ),
                text=[f"<b>{campione_attivo}</b> ({active_data['depth_label']})"],
                textposition="bottom center",
                textfont=dict(size=11, color="black"),
                hoverinfo="text",
                hovertext=[act_tip],
                name=f"Active: {campione_attivo}",
            )
        )

    if active_data:
        d_lbl = active_data["depth_label"]
        sec_lbl = active_data["sector"]
        titolo = f"Slope Profile: <b>{campione_attivo}</b> [{d_lbl} - {sec_lbl}]"
    else:
        titolo = f"Slope Profile ({campione_attivo})"

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
            showgrid=True,
            gridcolor="lightgrey",
            zeroline=False,
            range=[y_min_axis, z_max_topo + 6],
        ),
        template="plotly_white",
        margin=dict(l=50, r=20, t=35, b=35),
        showlegend=False,
    )
    return fig
