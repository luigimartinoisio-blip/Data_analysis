"""Funzioni matematiche di correzione termica e controllo qualità per dati geoelettrici."""

from __future__ import annotations

import numpy as np
import pandas as pd


def correggi_temperatura_hayashi(
    rho_m: float | np.ndarray | pd.Series,
    t_m: float | np.ndarray | pd.Series,
    t_ref: float = 25.0,
    alpha: float = 0.02,
) -> float | np.ndarray | pd.Series:
    """Applica la normalizzazione termica alla resistività apparente secondo Hayashi (2004).

    Formula:
        rho_25 = rho_m * [1 - alpha * (t_ref - t_m)]

    Parametri:
        rho_m: Resistività apparente misurata a temperatura t_m (Ohm*m).
        t_m: Temperatura media misurata nel campione (°C), sincrona da HYPROP2.
        t_ref: Temperatura di riferimento standard (°C), default 25.0 °C.
        alpha: Coefficiente di variazione termica della conducibilità (°C^-1), default 0.02.

    Restituisce:
        Resistività normalizzata a t_ref (rho_25).
    """
    return rho_m * (1.0 - alpha * (t_ref - t_m))


def calcola_errore_reciproco(
    r_dir: float | np.ndarray | pd.Series,
    r_rec: float | np.ndarray | pd.Series,
) -> float | np.ndarray | pd.Series:
    """Calcola l'errore reciproco percentuale tra misura diretta e misura reciproca.

    Formula:
        epsilon_rec (%) = |r_dir - r_rec| / [0.5 * (|r_dir| + |r_rec|)] * 100

    Parametri:
        r_dir: Resistenza o resistività apparente della misura diretta.
        r_rec: Resistenza o resistività apparente della misura reciproca.

    Restituisce:
        Errore reciproco percentuale (%). Restituisce 0.0 se entrambi i valori sono nulli.
    """
    denominatore = 0.5 * (np.abs(r_dir) + np.abs(r_rec))
    numeratore = np.abs(r_dir - r_rec)

    # Gestione divisione per zero in modo scalare o vettoriale
    if isinstance(denominatore, (pd.Series, np.ndarray)):
        risultato = np.where(denominatore == 0.0, 0.0, (numeratore / denominatore) * 100.0)
        if isinstance(r_dir, pd.Series):
            return pd.Series(risultato, index=r_dir.index)
        return risultato

    if denominatore == 0.0:
        return 0.0
    return float((numeratore / denominatore) * 100.0)


def calcola_indice_ar(
    rho_90: float | np.ndarray | pd.Series,
    rho_0: float | np.ndarray | pd.Series,
) -> float | np.ndarray | pd.Series:
    """Calcola l'indice di rapporto di anisotropia elettrica (Anisotropy Ratio - AR).

    Formula:
        AR = rho_a(90°) / rho_a(0°)

    Parametri:
        rho_90: Resistività apparente (o media) delle configurazioni orientate a 90°
            (perpendicolari all'asse di riferimento).
        rho_0: Resistività apparente (o media) delle configurazioni orientate a 0°
            (parallele all'asse di riferimento).

    Restituisce:
        Valore dell'indice AR (AR = 1 corrisponde alla baseline isotropa).
    """
    if isinstance(rho_0, (pd.Series, np.ndarray)):
        risultato = np.where(rho_0 == 0.0, np.nan, rho_90 / rho_0)
        if isinstance(rho_0, pd.Series):
            return pd.Series(risultato, index=rho_0.index)
        return risultato

    if rho_0 == 0.0:
        return float("nan")
    return float(rho_90 / rho_0)


def calcola_resistenza(
    v_mv: float | np.ndarray | pd.Series,
    i_ma: float | np.ndarray | pd.Series,
) -> float | np.ndarray | pd.Series:
    """Calcola la resistenza elettrica R (Ohm) a partire da d.d.p. (mV) e corrente (mA).

    Formula:
        R (Ohm) = (V (mV) / 1000) / (I (mA) / 1000) = V (mV) / I (mA)
    """
    return v_mv / i_ma


def calcola_resistivita_apparente(
    r_ohm: float | np.ndarray | pd.Series,
    fattore_k: float | np.ndarray | pd.Series,
) -> float | np.ndarray | pd.Series:
    """Calcola la resistività apparente rho_m (Ohm*m).

    Formula:
        rho_m = K * R
    Data la resistenza R (Ohm) e il fattore geometrico K (m).
    """
    return fattore_k * r_ohm


def applica_filtri_qualita(
    df: pd.DataFrame,
    col_v_mv: str = "v_mv",
    col_errore_rec: str | None = "errore_rec_pct",
    soglia_min_v_mv: float = 1.0,
    soglia_max_errore_rec_pct: float = 5.0,
) -> pd.DataFrame:
    """Applica i criteri di qualità metodologici al DataFrame delle misure geoelettriche.

    Criteri applicati:
    1. Differenza di potenziale |V| >= soglia_min_v_mv (default 1.0 mV).
    2. Errore reciproco <= soglia_max_errore_rec_pct (default 5.0%) se presente la colonna.

    Restituisce:
        Nuovo DataFrame contenente solo le righe che soddisfano tutti i criteri di qualità.
    """
    maschera = np.abs(df[col_v_mv]) >= soglia_min_v_mv

    if col_errore_rec is not None and col_errore_rec in df.columns:
        maschera = maschera & (df[col_errore_rec] <= soglia_max_errore_rec_pct)

    return df[maschera].copy()
