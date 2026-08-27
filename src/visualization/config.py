"""Plot styling configuration, color palette, and quadrupole metadata in English."""

from typing import Dict, List

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
    "suzione_media_kpa": "Matric Suction Mean ψ_mean [kPa]",
    "suzione_top_estesa_kpa": "Matric Suction Upper ψ_up [kPa]",
    "suzione_bottom_estesa_kpa": "Matric Suction Lower ψ_low [kPa]",
    "log10_suzione_kpa": "log₁₀(Suction [kPa])",
    "peso_netto_g": "Net Weight [g]",
    "temperatura_C": "Temperature [°C]",
    "grado_saturazione_Sr": "Degree of Saturation Sr [-]",
    "rho_25": "Calibrated Resistivity ρ₂₅ [Ω·m]",
    "rho25_geom_upper": "Geometric Mean Upper ρ₂₅,up [Ω·m]",
    "rho25_geom_lower": "Geometric Mean Lower ρ₂₅,low [Ω·m]",
    "rho25_geom_dipole": "Geometric Mean Dipole-dipole ρ₂₅,dip [Ω·m]",
    "rho25_geom_wenner": "Geometric Mean Wenner ρ₂₅,wen [Ω·m]",
}

MARKER_DEFAULT: str = "o"
