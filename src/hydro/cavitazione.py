"""Rilevamento delle soglie di cavitazione e Air Entry Point dei tensiometri HYPROP.

Distinzione fisica fondamentale:
1. Cavitazione del tensiometro (Stop tensiometro):
   Avviene quando si raggiunge la tensione limite nell'acqua metastabile del fusto,
   formando bolle di vapore acqueo (ebollizione a pressione negativa).
   La continuità idraulica si interrompe e la lettura crolla a ~950 hPa (pressione vapore/ambiente).
2. Air Entry Point del tensiometro (AEP tensiometro):
   Avviene quando la suzione supera la pressione di bolla della coppetta ceramica
   (~8.8 bar = 8800 hPa). L'aria entra nella ceramica e la lettura scende a 0 hPa.
3. Air Entry Value del suolo (AEV suolo):
   Proprietà idraulica intrinseca del terreno indagato, del tutto indipendente
   dai limiti strumentali e dalla cavitazione dei tensiometri.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class EventiTensiometro:
    """Indici, timestamp e valori di cavitazione e AEP per un singolo tensiometro."""

    idx_cavitazione: int
    t_cavitazione: Optional[pd.Timestamp]
    valore_cavitazione_hpa: float
    t_air_entry_point: Optional[pd.Timestamp]
    valore_air_entry_hpa: float = 8800.0  # 8.8 bar standard ceramica HYPROP


@dataclass(frozen=True)
class PuntiCavitazioneEsperimento:
    """Stato di cavitazione e AEP di entrambi i tensiometri (Top e Bottom)."""

    top: EventiTensiometro
    bottom: EventiTensiometro


def individua_eventi_tensiometri(
    df_meas: pd.DataFrame,
    t_aep_top: Optional[pd.Timestamp] = None,
    t_aep_bottom: Optional[pd.Timestamp] = None,
    col_t_top: str = "Tension Top [hPa]",
    col_t_bottom: str = "Tension Bottom [hPa]",
    col_tempo: str = "Date / Time",
    soglia_crollo_hpa: float = 300.0,
    pressione_aep_hpa: float = 8800.0,
) -> PuntiCavitazioneEsperimento:
    """Individua il punto di cavitazione (ebollizione/rottura) per ciascun tensiometro."""
    serie_top = df_meas[col_t_top].to_numpy()
    serie_bot = df_meas[col_t_bottom].to_numpy()
    tempi = pd.to_datetime(df_meas[col_tempo]) if col_tempo in df_meas.columns else None

    idx_cav_top = _trova_indice_cavitazione_singolo(serie_top, soglia_crollo_hpa)
    idx_cav_bot = _trova_indice_cavitazione_singolo(serie_bot, soglia_crollo_hpa)

    t_cav_top = tempi.iloc[idx_cav_top] if tempi is not None and idx_cav_top < len(tempi) else None
    t_cav_bot = tempi.iloc[idx_cav_bot] if tempi is not None and idx_cav_bot < len(tempi) else None

    eventi_top = EventiTensiometro(
        idx_cavitazione=idx_cav_top,
        t_cavitazione=t_cav_top,
        valore_cavitazione_hpa=float(serie_top[idx_cav_top]),
        t_air_entry_point=t_aep_top,
        valore_air_entry_hpa=pressione_aep_hpa,
    )

    eventi_bot = EventiTensiometro(
        idx_cavitazione=idx_cav_bot,
        t_cavitazione=t_cav_bot,
        valore_cavitazione_hpa=float(serie_bot[idx_cav_bot]),
        t_air_entry_point=t_aep_bottom,
        valore_air_entry_hpa=pressione_aep_hpa,
    )

    return PuntiCavitazioneEsperimento(top=eventi_top, bottom=eventi_bot)


def _trova_indice_cavitazione_singolo(
    valori: np.ndarray,
    soglia_crollo_hpa: float,
) -> int:
    """Individua l'ultimo punto prima della formazione di vapore e crollo della pressione."""
    n = len(valori)
    if n == 0:
        return 0

    idx_max = int(np.nanargmax(valori))
    for i in range(idx_max, n - 1):
        delta = valori[i] - valori[i + 1]
        if delta > soglia_crollo_hpa:
            return i

    return idx_max
