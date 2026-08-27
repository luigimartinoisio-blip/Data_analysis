"""Hydrogeophysical cross-plotting engine in Plotly and Matplotlib."""

from typing import List, Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go

from src.visualization.config import (
    CATEGORIE_QP,
    ETICHETTE_QP,
    LABEL_VARIABILI,
    MARKER_DEFAULT,
    PALETTE_COLORI,
)


def ottieni_lista_qp_per_categoria(categoria: str) -> List[str]:
    """Returns the list of quadrupole identifiers for a given category."""
    if categoria in CATEGORIE_QP:
        return CATEGORIE_QP[categoria]
    if categoria in ("Tutte", "All", "All Quadrupoles"):
        tutti: List[str] = []
        for v in CATEGORIE_QP.values():
            tutti.extend(v)
        return tutti
    return [categoria]


def crea_cross_plot_plotly(
    df: pd.DataFrame,
    var_x: str,
    categoria_o_qp: str = "All",
    var_y_tipo: str = "rho_25",
    filtra_qc: bool = False,
    soglia_qc_eps: float = 5.0,
    log_x: bool = False,
    log_y: bool = False,
    titolo_personalizzato: Optional[str] = None,
) -> go.Figure:
    """Generates an interactive Plotly cross-plot with rich hover tooltips."""
    fig = go.Figure()
    qps = ottieni_lista_qp_per_categoria(categoria_o_qp)

    campione = df["campione_id"].iloc[0] if "campione_id" in df.columns else ""
    x_label = LABEL_VARIABILI.get(var_x, var_x)

    if var_y_tipo == "rho_25":
        y_label = LABEL_VARIABILI.get("rho_25", "Calibrated Resistivity ρ₂₅ [Ω·m]")
        for qp in qps:
            col_rho = f"rho25_{qp}"
            col_eps = f"eps_{qp}"
            if col_rho not in df.columns:
                continue

            df_qp = df.copy()
            if filtra_qc and col_eps in df_qp.columns:
                df_qp = df_qp[(df_qp[col_eps] < soglia_qc_eps) | (df_qp[col_eps].isna())]

            df_plot = df_qp.dropna(subset=[var_x, col_rho])
            if df_plot.empty:
                continue

            color = PALETTE_COLORI.get(qp, "blue")
            label = ETICHETTE_QP.get(qp, qp)

            # Rich hover tooltip
            hover_text = [
                f"<b>{label}</b><br>"
                f"Timestep: {row.get('time_step_id', '')}<br>"
                f"Time: {row.get('datetime_nominale', '')}<br>"
                f"{x_label}: {row[var_x]:.2f}<br>"
                f"ρ₂₅: {row[col_rho]:.2f} Ω·m<br>"
                f"θ: {row.get('theta_vol_pct', np.nan):.2f}%<br>"
                f"ψ: {row.get('suzione_media_kpa', np.nan):.2f} kPa<br>"
                f"ε_rec: {row.get(col_eps, np.nan):.2f}%"
                for _, row in df_plot.iterrows()
            ]

            fig.add_trace(
                go.Scatter(
                    x=df_plot[var_x],
                    y=df_plot[col_rho],
                    mode="lines+markers",
                    name=label,
                    marker=dict(size=7, color=color, symbol="circle"),
                    line=dict(width=1.8, color=color),
                    hoverinfo="text",
                    hovertext=hover_text,
                )
            )

    else:
        y_label = LABEL_VARIABILI.get(var_y_tipo, var_y_tipo)
        df_plot = df.dropna(subset=[var_x, var_y_tipo])
        if not df_plot.empty:
            fig.add_trace(
                go.Scatter(
                    x=df_plot[var_x],
                    y=df_plot[var_y_tipo],
                    mode="lines+markers",
                    name=y_label,
                    marker=dict(size=7.5, color="darkblue"),
                    line=dict(width=2.2, color="darkblue"),
                )
            )

    titolo = titolo_personalizzato or f"Sample {campione} — {y_label} vs {x_label}"
    fig.update_layout(
        title=dict(text=titolo, x=0.5, font=dict(size=15)),
        xaxis=dict(
            title=x_label,
            type="log" if log_x else "linear",
            showgrid=True,
            gridcolor="lightgrey",
            zeroline=False,
        ),
        yaxis=dict(
            title=y_label,
            type="log" if log_y else "linear",
            showgrid=True,
            gridcolor="lightgrey",
            zeroline=False,
        ),
        template="plotly_white",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.35,
            xanchor="center",
            x=0.5,
            bordercolor="lightgrey",
            borderwidth=1,
            font=dict(size=9.5),
        ),
        margin=dict(l=60, r=40, t=50, b=80),
        hovermode="closest",
    )
    return fig


def crea_cross_plot_matplotlib(
    df: pd.DataFrame,
    var_x: str,
    categoria_o_qp: str = "All",
    filtra_qc: bool = False,
    soglia_qc_eps: float = 5.0,
    log_x: bool = False,
    log_y: bool = False,
    figsize: tuple = (10, 6),
    dpi: int = 300,
) -> plt.Figure:
    """Generates high-resolution publication-quality figure with standard palette."""
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    qps = ottieni_lista_qp_per_categoria(categoria_o_qp)
    campione = df["campione_id"].iloc[0] if "campione_id" in df.columns else ""
    x_label = LABEL_VARIABILI.get(var_x, var_x)

    for qp in qps:
        col_rho = f"rho25_{qp}"
        col_eps = f"eps_{qp}"
        if col_rho not in df.columns:
            continue

        df_qp = df.copy()
        if filtra_qc and col_eps in df_qp.columns:
            df_qp = df_qp[(df_qp[col_eps] < soglia_qc_eps) | (df_qp[col_eps].isna())]

        df_plot = df_qp.dropna(subset=[var_x, col_rho])
        if df_plot.empty:
            continue

        color = PALETTE_COLORI.get(qp, "blue")
        label = ETICHETTE_QP.get(qp, qp)

        ax.plot(
            df_plot[var_x],
            df_plot[col_rho],
            marker=MARKER_DEFAULT,
            color=color,
            label=label,
            linewidth=1.8,
            markersize=6,
        )

    if log_x:
        ax.set_xscale("log")
    if log_y:
        ax.set_yscale("log")

    ax.set_xlabel(x_label, fontsize=12)
    ax.set_ylabel("Calibrated Apparent Resistivity ρ₂₅ [Ω·m]", fontsize=12)
    ax.set_title(f"Sample {campione} — Calibrated Resistivity vs {x_label}", fontsize=14)
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.legend(bbox_to_anchor=(0.5, -0.2), loc="upper center", ncol=3, frameon=True)
    fig.tight_layout()
    return fig
