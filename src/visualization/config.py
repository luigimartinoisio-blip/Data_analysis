"""Plot styling configuration, color palette, and quadrupole metadata in English."""

from typing import Dict, List, Optional

import numpy as np
import pandas as pd

# Quadrupole categories
CATEGORIE_QP: Dict[str, List[str]] = {
    "Upper": ["qp1", "qp2", "qp3"],
    "Lower": ["qp4", "qp5", "qp6"],
    "Dipole-dipole": ["qp7", "qp8"],
    "Wenner": ["W1", "W3", "W2", "W4"],
}

# Strict project color palette
PALETTE_COLORI: Dict[str, str] = {
    "qp1": "dimgrey",
    "qp2": "darkgrey",
    "qp3": "black",  # Upper Horizontal
    "qp4": "indianred",
    "qp5": "firebrick",
    "qp6": "darkred",  # Lower Horizontal
    "qp7": "darkblue",
    "qp8": "royalblue",  # Vertical Dipole-Dipole
    "W1": "darkgreen",
    "W3": "forestgreen",  # Vertical Wenner 0°
    "W2": "limegreen",
    "W4": "yellowgreen",  # Vertical Wenner 90°
}

# Accurate single-ring and vertical descriptions in English
ETICHETTE_QP: Dict[str, str] = {
    "qp1": "qp1 (Ring 1, z = 4.0 cm, 0°)",
    "qp2": "qp2 (Ring 2, z = 3.0 cm, 0°)",
    "qp3": "qp3 (Ring 2, z = 3.0 cm, 90°)",
    "qp4": "qp4 (Ring 3, z = 2.0 cm, 0°)",
    "qp5": "qp5 (Ring 4, z = 1.0 cm, 0°)",
    "qp6": "qp6 (Ring 3, z = 2.0 cm, 90°)",
    "qp7": "qp7 (Vertical Dipole-Dipole, 0°)",
    "qp8": "qp8 (Vertical Dipole-Dipole, 90°)",
    "W1": "W1 (Vertical Wenner, 0°, Outer)",
    "W3": "W3 (Vertical Wenner, 0°, Inner)",
    "W2": "W2 (Vertical Wenner, 90°, Outer)",
    "W4": "W4 (Vertical Wenner, 90°, Inner)",
}

# English labels for physical and hydraulic variables
LABEL_VARIABILI: Dict[str, str] = {
    "ore_trascorse_da_t0": "Elapsed Time [hours]",
    "theta_vol_pct": "Volumetric Water Content θ [Vol%]",
    "contenuto_acqua_grav_pct": "Gravimetric Water Content w [%]",
    "suzione_media_kpa": "Matric Suction [kPa]",
    "suzione_top_estesa_kpa": "Matric Suction Upper [kPa]",
    "suzione_bottom_estesa_kpa": "Matric Suction Lower [kPa]",
    "log10_suzione_kpa": "log₁₀(Suction [kPa])",
    "peso_netto_g": "Net Weight [g]",
    "temperatura_C": "Temperature [°C]",
    "grado_saturazione_Sr": "Degree of Saturation Sr [-]",
    "rho_25": "Calibrated Apparent Resistivity ρ₂₅ [Ω·m]",
    "rho25_geom_upper": "Geometric Mean Upper ρ₂₅ [Ω·m]",
    "rho25_geom_lower": "Geometric Mean Lower ρ₂₅ [Ω·m]",
    "rho25_geom_dipole": "Geometric Mean Dipole-dipole ρ₂₅ [Ω·m]",
    "rho25_geom_wenner": "Geometric Mean Wenner ρ₂₅ [Ω·m]",
}

MARKER_DEFAULT: str = "o"

# van Genuchten alpha fitting parameter [1/hPa] per sample
VALORI_VG_ALPHA_HPA: Dict[str, float] = {
    "ML1": 0.02490,
    "ML10": 0.02310,
    "ML3": 0.03710,
    "ML4": 0.06310,
    "ML5": 0.00514,
    "ML6": 0.00631,
    "ML7": 0.07420,
    "ML8": 0.08390,
    "ML9": 0.03660,
    "Sand_R": 0.01790,
}


def calcola_valore_aep_per_variabile(
    df: pd.DataFrame,
    campione_id: str,
    var_x: str,
) -> Optional[float]:
    """Calculates X-axis coordinate at Air Entry Point (AEP) for Time, Suction, or Water Content."""
    alpha = VALORI_VG_ALPHA_HPA.get(campione_id)
    if not alpha or alpha <= 0:
        return None

    # AEP matric suction: 1/alpha in hPa -> divide by 10 for kPa
    psi_aep_kpa = (1.0 / alpha) / 10.0

    if var_x == "suzione_media_kpa":
        return psi_aep_kpa

    if var_x == "log10_suzione_kpa":
        return float(np.log10(psi_aep_kpa)) if psi_aep_kpa > 0 else None

    # For other variables: interpolate along suzione_media_kpa
    if var_x in [
        "ore_trascorse_da_t0",
        "theta_vol_pct",
        "contenuto_acqua_grav_pct",
        "grado_saturazione_Sr",
        "suzione_top_estesa_kpa",
        "suzione_bottom_estesa_kpa",
    ]:
        if "suzione_media_kpa" in df.columns and var_x in df.columns:
            df_valid = df.dropna(subset=["suzione_media_kpa", var_x]).sort_values(
                "suzione_media_kpa"
            )
            if len(df_valid) >= 2:
                psi_arr = df_valid["suzione_media_kpa"].to_numpy(dtype=float)
                x_arr = df_valid[var_x].to_numpy(dtype=float)
                return float(np.interp(psi_aep_kpa, psi_arr, x_arr))

    return None
