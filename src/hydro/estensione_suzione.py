"""Algoritmi per l'estensione tensiometrica e il calcolo della suzione secondo il modello HYPROP."""

from __future__ import annotations

from enum import Enum

import numpy as np
import pandas as pd

from src.hydro.cavitazione import (
    EventiTensiometro,
    individua_eventi_tensiometri,
)
from src.io.hyprop import DatiHyprop


class RegimeValiditaSuzione(str, Enum):
    """Regime di validità della suzione matriciale lungo l'esperimento."""

    DIRETTO_ENTRAMBI = "Diretto_Entrambi_Tensiometri"
    ESTESO_TOP_DIRETTO_BOT = "Esteso_Top_Diretto_Bottom"
    ESTESO_ENTRAMBI = "Esteso_Entrambi_Tensiometri"
    POST_AIR_ENTRY_TOP = "Oltre_Air_Entry_Top"


def calcola_estensione_tensiometro_hyprop(
    df_meas: pd.DataFrame,
    eventi: EventiTensiometro,
    col_tensione_misurata: str,
    col_tempo: str = "Date / Time",
) -> pd.Series:
    """Calcola la serie estesa di un tensiometro secondo l'algoritmo lineare HYPROP (Stop -> AEP).

    Formula:
        Per t <= t_cav: valore misurato reale
        Per t_cav < t <= t_aep:
            psi_estesa(t) = psi_cav + (psi_aep - psi_cav) * (t - t_cav) / (t_aep - t_cav)
        Per t > t_aep: NaN (aria entrata nella ceramica)
    """
    serie_estesa = pd.Series(np.nan, index=df_meas.index, dtype=float)
    tempi = pd.to_datetime(df_meas[col_tempo])

    # 1. Tratto pre-cavitazione misurato reale
    idx_cav = eventi.idx_cavitazione
    serie_estesa.iloc[: idx_cav + 1] = df_meas[col_tensione_misurata].iloc[: idx_cav + 1]

    # 2. Tratto esteso post-cavitazione fino all'Air Entry Point della ceramica
    t_cav = eventi.t_cavitazione
    t_aep = eventi.t_air_entry_point
    psi_cav = eventi.valore_cavitazione_hpa
    psi_aep = eventi.valore_air_entry_hpa

    if t_cav is not None and t_aep is not None and t_aep > t_cav:
        maschera_estesa = (tempi > t_cav) & (tempi <= t_aep)
        dt_totale = (t_aep - t_cav).total_seconds()
        dt_corrente = (tempi[maschera_estesa] - t_cav).dt.total_seconds()

        valori_estesi = psi_cav + (psi_aep - psi_cav) * (dt_corrente / dt_totale)
        serie_estesa.loc[maschera_estesa] = valori_estesi

    return serie_estesa


def estendi_serie_suzione_hyprop(
    dati_hyprop: DatiHyprop,
) -> pd.DataFrame:
    """Genera la serie temporale completa delle tensioni estese e della suzione media.

    Regole metodologiche:
    1. Tensione Top: misurata fino a Stop top + estensione HYPROP fino ad AEP top (8.8 bar).
    2. Tensione Bottom: misurata fino a Stop bottom + estensione HYPROP fino ad AEP (8.8 bar).
    3. Suzione media del campione: media geometrica psi_m = sqrt(psi_top_est * psi_bot_est).
    4. Validità suzione del campione: calcolabile solo fintanto che entrambi i tensiometri
       si trovano entro il loro campo di validità (misurato o esteso), ossia fino ad AEP top.
    """
    df = dati_hyprop.serie_misure.copy()
    eventi = individua_eventi_tensiometri(
        df,
        t_aep_top=dati_hyprop.air_entry_point_top,
        t_aep_bottom=dati_hyprop.air_entry_point_bottom,
    )

    # 1. Calcolo contenuto d'acqua volumetrico da bilancia
    peso_secco = dati_hyprop.peso_secco_g
    vol = dati_hyprop.volume_campione_cm3
    df["theta_vol_pct"] = ((df["Net weight [g]"] - peso_secco) / vol) * 100.0

    # 2. Pulizia misure grezze (imposta a NaN i dati spuri post-cavitazione)
    df["tension_top_misurata_hpa"] = df["Tension Top [hPa]"].copy()
    df["tension_bottom_misurata_hpa"] = df["Tension Bottom [hPa]"].copy()
    df.loc[df.index > eventi.top.idx_cavitazione, "tension_top_misurata_hpa"] = np.nan
    df.loc[df.index > eventi.bottom.idx_cavitazione, "tension_bottom_misurata_hpa"] = np.nan

    # 3. Calcolo serie estese secondo l'algoritmo HYPROP
    df["tension_top_estesa_hpa"] = calcola_estensione_tensiometro_hyprop(
        df, eventi.top, "Tension Top [hPa]"
    )
    df["tension_bottom_estesa_hpa"] = calcola_estensione_tensiometro_hyprop(
        df, eventi.bottom, "Tension Bottom [hPa]"
    )

    # 4. Calcolo suzione media geometrica e classificazione regime
    df["psi_media_geometrica_hpa"] = np.nan
    df["regime_validita"] = RegimeValiditaSuzione.POST_AIR_ENTRY_TOP.value

    # Maschere temporali
    t = pd.to_datetime(df["Date / Time"])
    t_cav_top = eventi.top.t_cavitazione
    t_aep_top = eventi.top.t_air_entry_point
    t_cav_bot = eventi.bottom.t_cavitazione

    # Fase 1: Entrambi misurati direttamente (t <= t_cav_top)
    mask_fase1 = t <= t_cav_top if t_cav_top else (df.index <= eventi.top.idx_cavitazione)
    val_top_f1 = np.maximum(df.loc[mask_fase1, "tension_top_misurata_hpa"], 0.0)
    val_bot_f1 = np.maximum(df.loc[mask_fase1, "tension_bottom_misurata_hpa"], 0.0)
    df.loc[mask_fase1, "psi_media_geometrica_hpa"] = np.sqrt(val_top_f1 * val_bot_f1)
    df.loc[mask_fase1, "regime_validita"] = RegimeValiditaSuzione.DIRETTO_ENTRAMBI.value

    # Fase 2: Top esteso, Bottom misurato direttamente (t_cav_top < t <= t_aep_top e t <= t_cav_bot)
    if t_cav_top and t_aep_top:
        mask_fase2 = (t > t_cav_top) & (t <= t_aep_top) & (t <= t_cav_bot)
        val_top_f2 = np.maximum(df.loc[mask_fase2, "tension_top_estesa_hpa"], 0.0)
        val_bot_f2 = np.maximum(df.loc[mask_fase2, "tension_bottom_misurata_hpa"], 0.0)
        df.loc[mask_fase2, "psi_media_geometrica_hpa"] = np.sqrt(val_top_f2 * val_bot_f2)
        df.loc[mask_fase2, "regime_validita"] = RegimeValiditaSuzione.ESTESO_TOP_DIRETTO_BOT.value

    # Calcolo log10(suzione) e pF per i punti validi
    df["log10_psi_hpa"] = np.log10(np.maximum(df["psi_media_geometrica_hpa"], 1e-3))
    df["pf"] = df["log10_psi_hpa"]

    return df
