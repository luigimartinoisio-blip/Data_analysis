"""3D interactive ABS cylinder model with blue (A, B) and red (M, N) electrodes."""

from typing import Dict, List, Optional, Tuple

import numpy as np
import plotly.graph_objects as go

from src.core.geometria import ArrayCilindrico16

# Quadrupole (A, B, M, N) mapping
QUATERNE_QP: Dict[str, Tuple[int, int, int, int]] = {
    "qp1": (1, 5, 13, 9),
    "qp2": (2, 6, 14, 10),
    "qp3": (6, 10, 2, 14),
    "qp4": (3, 7, 15, 11),
    "qp5": (4, 8, 16, 12),
    "qp6": (7, 11, 3, 15),
    "qp7": (1, 2, 3, 4),
    "qp8": (5, 6, 7, 8),
    "W1": (1, 4, 2, 3),
    "W2": (5, 8, 6, 7),
    "W3": (9, 12, 10, 11),
    "W4": (13, 16, 14, 15),
}


def crea_figura_cilindro_3d(
    quadripoli_attivi: Optional[List[str]] = None,
    mostra_anelli: bool = True,
    raggio_cm: float = 4.0,
    altezza_cm: float = 5.0,
) -> go.Figure:
    """3D Plotly visualization of cylinder highlighting A, B (blue) and M, N (red)."""
    fig = go.Figure()
    array_geo = ArrayCilindrico16(raggio_cilindro_cm=raggio_cm, altezza_cilindro_cm=altezza_cm)

    # 1. Wireframe cylinder
    theta_grid = np.linspace(0, 2 * np.pi, 36)
    z_grid = np.linspace(0, altezza_cm, 10)
    theta_mesh, z_mesh = np.meshgrid(theta_grid, z_grid)
    x_mesh = raggio_cm * np.cos(theta_mesh)
    y_mesh = raggio_cm * np.sin(theta_mesh)

    fig.add_trace(
        go.Surface(
            x=x_mesh,
            y=y_mesh,
            z=z_mesh,
            opacity=0.12,
            colorscale=[[0, "lightblue"], [1, "lightblue"]],
            showscale=False,
            hoverinfo="skip",
            name="ABS Cylinder",
        )
    )

    # 2. Horizontal ring guidelines at z = 4, 3, 2, 1 cm
    if mostra_anelli:
        for z_val in [4.0, 3.0, 2.0, 1.0]:
            x_ring = raggio_cm * np.cos(theta_grid)
            y_ring = raggio_cm * np.sin(theta_grid)
            z_ring = np.full_like(theta_grid, z_val)
            fig.add_trace(
                go.Scatter3d(
                    x=x_ring,
                    y=y_ring,
                    z=z_ring,
                    mode="lines",
                    line=dict(color="rgba(120, 120, 120, 0.4)", width=2),
                    hoverinfo="skip",
                    showlegend=False,
                )
            )

    # 3. Identify active (A, B) and (M, N) electrodes
    current_electrodes: set[int] = set()  # A, B -> Blue
    potential_electrodes: set[int] = set()  # M, N -> Red

    if quadripoli_attivi:
        for qp in quadripoli_attivi:
            if qp in QUATERNE_QP:
                a, b, m, n = QUATERNE_QP[qp]
                current_electrodes.add(a)
                current_electrodes.add(b)
                potential_electrodes.add(m)
                potential_electrodes.add(n)

    # 4. Separate electrode coordinates
    tutti_elettrodi = array_geo.ottieni_tutti_elettrodi()

    inact_x, inact_y, inact_z, inact_txt = [], [], [], []
    curr_x, curr_y, curr_z, curr_txt, curr_lbl = [], [], [], [], []
    pot_x, pot_y, pot_z, pot_txt, pot_lbl = [], [], [], [], []

    for el in tutti_elettrodi:
        base_info = (
            f"<b>Electrode #{el.id_elettrodo}</b><br>"
            f"Line: {el.linea} ({el.angolo_deg:.0f}°)<br>"
            f"Ring: {el.anello} (z={el.quota_z_cm} cm)"
        )
        if el.id_elettrodo in current_electrodes:
            curr_x.append(el.x_cm)
            curr_y.append(el.y_cm)
            curr_z.append(el.quota_z_cm)
            curr_txt.append(f"<b>[Current Electrode (A/B)]</b><br>{base_info}")
            curr_lbl.append(str(el.id_elettrodo))
        elif el.id_elettrodo in potential_electrodes:
            pot_x.append(el.x_cm)
            pot_y.append(el.y_cm)
            pot_z.append(el.quota_z_cm)
            pot_txt.append(f"<b>[Potential Electrode (M/N)]</b><br>{base_info}")
            pot_lbl.append(str(el.id_elettrodo))
        else:
            inact_x.append(el.x_cm)
            inact_y.append(el.y_cm)
            inact_z.append(el.quota_z_cm)
            inact_txt.append(base_info)

    # Inactive electrodes (grey)
    if inact_x:
        fig.add_trace(
            go.Scatter3d(
                x=inact_x,
                y=inact_y,
                z=inact_z,
                mode="markers+text",
                marker=dict(size=5, color="grey", opacity=0.5),
                text=[
                    str(el.id_elettrodo)
                    for el in tutti_elettrodi
                    if el.id_elettrodo not in (current_electrodes | potential_electrodes)
                ],
                textposition="top center",
                hoverinfo="text",
                hovertext=inact_txt,
                name="Inactive",
            )
        )

    # Current electrodes (A, B) -> Blue Circles
    if curr_x:
        fig.add_trace(
            go.Scatter3d(
                x=curr_x,
                y=curr_y,
                z=curr_z,
                mode="markers+text",
                marker=dict(size=9, color="blue", symbol="circle"),
                text=curr_lbl,
                textposition="top center",
                hoverinfo="text",
                hovertext=curr_txt,
                name="A, B (Current)",
            )
        )

    # Potential electrodes (M, N) -> Red Circles
    if pot_x:
        fig.add_trace(
            go.Scatter3d(
                x=pot_x,
                y=pot_y,
                z=pot_z,
                mode="markers+text",
                marker=dict(size=9, color="red", symbol="circle"),
                text=pot_lbl,
                textposition="top center",
                hoverinfo="text",
                hovertext=pot_txt,
                name="M, N (Potential)",
            )
        )

    # 3D Camera and Clean Layout
    titolo = f"Geometry: {', '.join(quadripoli_attivi)}" if quadripoli_attivi else "Electrode Array"
    fig.update_layout(
        title=dict(text=titolo, font=dict(size=13), x=0.5),
        scene=dict(
            xaxis=dict(title="X [cm]", range=[-5, 5], showbackground=False),
            yaxis=dict(title="Y [cm]", range=[-5, 5], showbackground=False),
            zaxis=dict(title="Z [cm]", range=[0, 6], showbackground=False),
            aspectmode="manual",
            aspectratio=dict(x=1, y=1, z=1.2),
            camera=dict(eye=dict(x=1.6, y=1.6, z=1.1)),
        ),
        margin=dict(l=10, r=10, t=35, b=10),
        legend=dict(
            orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5, font=dict(size=10)
        ),
        template="plotly_white",
    )
    return fig
