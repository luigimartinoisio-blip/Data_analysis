"""Fattori geometrici K calibrati sperimentalmente per l'array cilindrico Hyprop-GeoTom."""

from __future__ import annotations

from typing import Dict, Optional

import numpy as np
import pandas as pd

from src.core.quadripoli import CategoriaQuadripolo, Quadripolo

# Dizionario dei fattori geometrici K calibrati sperimentalmente (in metri)
# Calibrazione eseguita con soluzione a conducibilità nota nel portacampione ABS:
# rho_cal = 1 / sigma_fluid -> K = rho_cal / (dV / I)
FATTORE_K_ANELLO_1_Z4: float = 0.187194  # Anello 1 (z = 4 cm, superiore)
FATTORE_K_ANELLO_2_Z3: float = 0.210141452  # Anello 2 (z = 3 cm, medio-superiore)
FATTORE_K_ANELLO_3_Z2: float = 0.210141452  # Anello 3 (z = 2 cm, medio-inferiore)
FATTORE_K_ANELLO_4_Z1: float = 0.19681829  # Anello 4 (z = 1 cm, inferiore)
FATTORE_K_DIPOLO_DIPOLO: float = 0.228686003  # Array verticali Dipolo-Dipolo
FATTORE_K_WENNER: float = 0.05011339  # Array verticali Wenner

MAPPA_FATTORI_K_ANELLI: Dict[int, float] = {
    1: FATTORE_K_ANELLO_1_Z4,
    2: FATTORE_K_ANELLO_2_Z3,
    3: FATTORE_K_ANELLO_3_Z2,
    4: FATTORE_K_ANELLO_4_Z1,
}

MAPPA_FATTORI_K_GRUPPI_RAPPRESENTATIVI: Dict[str, float] = {
    "qp1_0": FATTORE_K_ANELLO_1_Z4,
    "qp2_0": FATTORE_K_ANELLO_2_Z3,
    "qp3_90": FATTORE_K_ANELLO_2_Z3,
    "qp4_0": FATTORE_K_ANELLO_3_Z2,
    "qp5_0": FATTORE_K_ANELLO_4_Z1,
    "qp6_90": FATTORE_K_ANELLO_3_Z2,
    "qp7_0": FATTORE_K_DIPOLO_DIPOLO,
    "qp8_90": FATTORE_K_DIPOLO_DIPOLO,
    "W1_0": FATTORE_K_WENNER,
    "W2_90": FATTORE_K_WENNER,
    "W3_0": FATTORE_K_WENNER,
    "W4_90": FATTORE_K_WENNER,
}


def ottieni_fattore_k_calibrato(
    quadripolo: Quadripolo,
    codice_gruppo: Optional[str] = None,
) -> float:
    """Restituisce il fattore geometrico K calibrato sperimentalmente (m) per un quadripolo.

    Regole di assegnazione:
    1. Se il codice di gruppo (es. 'qp1_0', 'W1_0') è fornito, lookup diretto.
    2. Se orizzontale su un anello specifico (1..4), lookup per anello.
    3. Se verticale Dipolo-Dipolo -> 0.228686003 m.
    4. Se verticale Wenner -> 0.05011339 m.
    """
    if codice_gruppo and codice_gruppo in MAPPA_FATTORI_K_GRUPPI_RAPPRESENTATIVI:
        return MAPPA_FATTORI_K_GRUPPI_RAPPRESENTATIVI[codice_gruppo]

    if quadripolo.categoria in (
        CategoriaQuadripolo.ORIZZONTALE_UPPER,
        CategoriaQuadripolo.ORIZZONTALE_LOWER,
        CategoriaQuadripolo.ORIZZONTALE_ALTRO,
    ):
        if quadripolo.anello_orizzontale in MAPPA_FATTORI_K_ANELLI:
            return MAPPA_FATTORI_K_ANELLI[quadripolo.anello_orizzontale]

    if quadripolo.categoria == CategoriaQuadripolo.VERTICALE_DIPOLO_DIPOLO:
        return FATTORE_K_DIPOLO_DIPOLO

    if quadripolo.categoria == CategoriaQuadripolo.VERTICALE_WENNER:
        return FATTORE_K_WENNER

    # Default di fallback per configurazioni miste 3D non tabulate
    return float("nan")


def ricalcola_resistivita_apparente(
    v_mv: float | np.ndarray | pd.Series,
    i_ma: float | np.ndarray | pd.Series,
    fattore_k: float | np.ndarray | pd.Series,
) -> float | np.ndarray | pd.Series:
    """Ricalcola la resistività apparente esatta dai valori fisici grezzi V (mV) e I (mA).

    Formula:
        R (Ohm) = V (mV) / I (mA)
        rho_m (Ohm*m) = K (m) * R (Ohm)
    """
    resistenza = v_mv / i_ma
    return fattore_k * resistenza
