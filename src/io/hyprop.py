"""Parser e strutture dati per i file di laboratorio HYPROP2 (.xlsx)."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional

import pandas as pd


@dataclass
class ParametriVanGenuchten:
    """Parametri del modello idraulico di van Genuchten - Mualem fittati da HYPROP-FIT."""

    alpha_1_per_cm: float = 0.0
    n: float = 0.0
    theta_r_vol_pct: float = 0.0
    theta_s_vol_pct: float = 0.0
    k_sat_cm_per_d: float = 0.0
    tau: float = 0.5


@dataclass
class DatiHyprop:
    """Rappresentazione strutturata completa di un esperimento HYPROP2."""

    id_campione: str
    percorso_file: Path
    metadati: Dict[str, Any] = field(default_factory=dict)
    serie_misure: pd.DataFrame = field(default_factory=pd.DataFrame)
    punti_spline: pd.DataFrame = field(default_factory=pd.DataFrame)
    curva_ritenzione_esperimento: pd.DataFrame = field(default_factory=pd.DataFrame)
    curva_conducibilita_esperimento: pd.DataFrame = field(default_factory=pd.DataFrame)
    curva_ritenzione_fittata: pd.DataFrame = field(default_factory=pd.DataFrame)
    curva_conducibilita_fittata: pd.DataFrame = field(default_factory=pd.DataFrame)
    parametri_fitting: ParametriVanGenuchten = field(default_factory=ParametriVanGenuchten)
    statistiche_fitting: Dict[str, float] = field(default_factory=dict)

    # Parametri fisici chiave del campione
    peso_secco_g: float = 0.0
    volume_campione_cm3: float = 250.0
    densita_secca_g_cm3: float = 0.0
    porosita: float = 0.0
    contenuto_acqua_saturo_vol_pct: float = 0.0
    t_start: Optional[pd.Timestamp] = None
    t_stop: Optional[pd.Timestamp] = None
    air_entry_point_top: Optional[pd.Timestamp] = None
    air_entry_point_bottom: Optional[pd.Timestamp] = None


class ParserHypropExcel:
    """Parser per file Excel (.xlsx) generati da METER LABROS SoilView / HYPROP-FIT."""

    def leggi_file(self, percorso: str | Path, id_campione: Optional[str] = None) -> DatiHyprop:
        """Legge ed estrae tutti i fogli e metadati dal file Excel HYPROP."""
        p = Path(percorso)
        if not p.exists():
            raise FileNotFoundError(f"File HYPROP non trovato: {p}")

        nome_campione = id_campione or p.stem

        # 1. Lettura Metadati dal foglio Information
        metadati: Dict[str, Any] = {}
        df_info = pd.read_excel(p, sheet_name="Information")
        for _, row in df_info.dropna(subset=["Parameter Name"]).iterrows():
            chiave = str(row["Parameter Name"]).strip().rstrip(":")
            metadati[chiave] = row["Value"]

        # Estrazione parametri fisici
        peso_secco = float(metadati.get("Dry soil weight [g]", 0.0) or 0.0)
        volume = float(metadati.get("Soil volume [cm3]", 250.0) or 250.0)
        densita = float(metadati.get("Density [g/cm3]", 0.0) or 0.0)
        porosita = float(metadati.get("Porosity [-]", 0.0) or 0.0)
        theta_s = float(metadati.get("Initial water content [Vol%]", 0.0) or 0.0)

        t_start = (
            pd.to_datetime(metadati.get("Start of measurement"))
            if "Start of measurement" in metadati
            else None
        )
        t_stop = (
            pd.to_datetime(metadati.get("Stop of measurement"))
            if "Stop of measurement" in metadati
            else None
        )

        aep_top = (
            pd.to_datetime(metadati.get("Tension top Air Entry Point/Stopp"))
            if "Tension top Air Entry Point/Stopp" in metadati
            else None
        )
        aep_bot = (
            pd.to_datetime(metadati.get("Tension bottom Air Entry Point"))
            if "Tension bottom Air Entry Point" in metadati
            else None
        )

        # 2. Serie Temporale Misure Continue
        df_meas = pd.read_excel(p, sheet_name="Measurements")
        if "Date / Time" in df_meas.columns:
            df_meas["Date / Time"] = pd.to_datetime(df_meas["Date / Time"])

        # 3. Spline Points
        df_spline = (
            pd.read_excel(p, sheet_name="Spline Points")
            if "Spline Points" in pd.ExcelFile(p).sheet_names
            else pd.DataFrame()
        )
        if "Date / Time" in df_spline.columns:
            df_spline["Date / Time"] = pd.to_datetime(df_spline["Date / Time"])

        # 4. Curve Sperimentali e Fittate
        fogli = pd.ExcelFile(p).sheet_names
        df_ret_exp = (
            pd.read_excel(p, sheet_name="Evaluation-Retention Θ(pF)")
            if "Evaluation-Retention Θ(pF)" in fogli
            else pd.DataFrame()
        )
        df_cond_exp = (
            pd.read_excel(p, sheet_name="Evaluation-Conductivity K(pF)")
            if "Evaluation-Conductivity K(pF)" in fogli
            else pd.DataFrame()
        )
        df_ret_fit = (
            pd.read_excel(p, sheet_name="Fitting-Retention Θ(pF)")
            if "Fitting-Retention Θ(pF)" in fogli
            else pd.DataFrame()
        )
        df_cond_fit = (
            pd.read_excel(p, sheet_name="Fitting-Conductivity K(pF)")
            if "Fitting-Conductivity K(pF)" in fogli
            else pd.DataFrame()
        )

        # 5. Parametri di Fitting van Genuchten
        def _to_float(val: Any, default: float = 0.0) -> float:
            if val is None or pd.isna(val):
                return default
            val_clean = str(val).replace("*", "").strip()
            try:
                return float(val_clean)
            except ValueError:
                return default

        vg = ParametriVanGenuchten()
        if "Fitting-Parameter value" in fogli:
            df_params = pd.read_excel(p, sheet_name="Fitting-Parameter value")
            p_dict = dict(zip(df_params["Parameter"], df_params["Value"]))
            vg = ParametriVanGenuchten(
                alpha_1_per_cm=_to_float(p_dict.get("alpha")),
                n=_to_float(p_dict.get("n")),
                theta_r_vol_pct=_to_float(p_dict.get("th_r")) * 100.0,
                theta_s_vol_pct=_to_float(p_dict.get("th_s")) * 100.0,
                k_sat_cm_per_d=_to_float(p_dict.get("Ks")),
                tau=_to_float(p_dict.get("tau"), default=0.5),
            )

        # 6. Statistiche Fitting
        stats: Dict[str, float] = {}
        if "Fitting-Statistical analysis" in fogli:
            df_stat = pd.read_excel(p, sheet_name="Fitting-Statistical analysis")
            for _, r in df_stat.dropna().iterrows():
                stats[str(r["Name"])] = float(r["Value"])

        return DatiHyprop(
            id_campione=nome_campione,
            percorso_file=p,
            metadati=metadati,
            serie_misure=df_meas,
            punti_spline=df_spline,
            curva_ritenzione_esperimento=df_ret_exp,
            curva_conducibilita_esperimento=df_cond_exp,
            curva_ritenzione_fittata=df_ret_fit,
            curva_conducibilita_fittata=df_cond_fit,
            parametri_fitting=vg,
            statistiche_fitting=stats,
            peso_secco_g=peso_secco,
            volume_campione_cm3=volume,
            densita_secca_g_cm3=densita,
            porosita=porosita,
            contenuto_acqua_saturo_vol_pct=theta_s,
            t_start=t_start,
            t_stop=t_stop,
            air_entry_point_top=aep_top,
            air_entry_point_bottom=aep_bot,
        )
