"""Pipeline di elaborazione unificata e sincronizzazione idrogeofisica GeoTom-HYPROP."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

from src.core.correzioni import (
    calcola_errore_reciproco,
    correggi_temperatura_hayashi,
)
from src.core.fattori_geometrici import MAPPA_FATTORI_K_GRUPPI_RAPPRESENTATIVI
from src.core.schemi_rappresentativi import Schema20QuadripoliRappresentativi
from src.hydro.estensione_suzione import estendi_serie_suzione_hyprop
from src.io.hyprop import DatiHyprop, ParserHypropExcel

VOLUME_PORTACAMPIONE_CM3: float = 250.0
ALTEZZA_PORTACAMPIONE_CM: float = 5.0


@dataclass
class MisuraPuntoRawGeoTom:
    """Singola misura raw estratta da una riga di un file GeoTom."""

    a: int
    b: int
    m: int
    n: int
    i_ma: float
    dv_mv: float
    rho_geotom: float
    timestamp: datetime


def leggi_file_acquisizione_geotom(fpath: Path) -> List[MisuraPuntoRawGeoTom]:
    """Legge tutte le righe di misura fisica da un file .txt di time-step GeoTom."""
    misure: List[MisuraPuntoRawGeoTom] = []
    with open(fpath, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 11 and parts[0].isdigit():
                try:
                    a = int(parts[0])
                    b = int(parts[1])
                    m = int(parts[2])
                    n = int(parts[3])
                    i_ma = float(parts[5])
                    dv_mv = float(parts[6])
                    rho_geo = float(parts[7])
                    date_str = parts[-2]
                    time_str = parts[-1]
                    dt = datetime.strptime(f"{date_str} {time_str}", "%d.%m.%Y %H:%M:%S")
                    misure.append(
                        MisuraPuntoRawGeoTom(
                            a=a,
                            b=b,
                            m=m,
                            n=n,
                            i_ma=i_ma,
                            dv_mv=dv_mv,
                            rho_geotom=rho_geo,
                            timestamp=dt,
                        )
                    )
                except (ValueError, IndexError):
                    continue
    return misure


class ElaboratoreCampioneIntegrato:
    """Elabora, calibra e sincronizza le serie temporali GeoTom ed HYPROP di un campione."""

    def __init__(
        self,
        id_campione: str,
        cartella_ert: Path,
        file_hyprop_xlsx: Path,
        schema: Optional[Schema20QuadripoliRappresentativi] = None,
        volume_cm3: float = VOLUME_PORTACAMPIONE_CM3,
    ) -> None:
        self.id_campione = id_campione
        self.cartella_ert = cartella_ert
        self.file_hyprop_xlsx = file_hyprop_xlsx
        self.schema = schema or Schema20QuadripoliRappresentativi()
        self.volume_cm3 = volume_cm3

        self.parser_hyprop = ParserHypropExcel()
        self.dati_hyprop: Optional[DatiHyprop] = None
        self.df_hyprop_esteso: Optional[pd.DataFrame] = None

    def carica_dati_idrologici(self) -> None:
        """Carica e calcola la serie estesa HYPROP con suzione in kPa e volume standard."""
        self.dati_hyprop = self.parser_hyprop.leggi_file(
            self.file_hyprop_xlsx, id_campione=self.id_campione
        )
        # Forza il volume nominale di 250 cm3 se specificato
        self.dati_hyprop.volume_campione_cm3 = self.volume_cm3
        self.df_hyprop_esteso = estendi_serie_suzione_hyprop(self.dati_hyprop)

    def interpola_idrologia_al_tempo(self, t_target: datetime) -> Dict[str, Any]:
        """Interpola le variabili idrologiche HYPROP al secondo esatto t_target (baricentro ERT)."""
        if self.df_hyprop_esteso is None:
            raise ValueError("Dati HYPROP non caricati!")

        df_h = self.df_hyprop_esteso
        epoch = pd.Timestamp("1970-01-01")
        tempi_h = (pd.to_datetime(df_h["Date / Time"]) - epoch).dt.total_seconds().to_numpy()
        t_sec = (pd.to_datetime(t_target) - epoch).total_seconds()

        # Interpola variabili continue
        cols_continue = [
            "Temperature [°C]",
            "Net weight [g]",
            "theta_vol_pct",
            "tension_top_estesa_hpa",
            "tension_bottom_estesa_hpa",
            "psi_media_geometrica_hpa",
        ]

        risultati: Dict[str, Any] = {}
        for col in cols_continue:
            valori = df_h[col].to_numpy()
            # Rimuovi NaN per l'interpolazione
            validi = ~np.isnan(valori)
            if np.count_nonzero(validi) >= 2:
                f_int = interp1d(
                    tempi_h[validi],
                    valori[validi],
                    kind="linear",
                    bounds_error=False,
                    fill_value="extrapolate",
                )
                risultati[col] = float(f_int(t_sec))
            elif np.count_nonzero(validi) == 1:
                risultati[col] = float(valori[validi][0])
            else:
                risultati[col] = np.nan

        # Assegna regime suzione per vicinanza temporale
        idx_vicino = int(np.argmin(np.abs(tempi_h - t_sec)))
        risultati["regime_suzione"] = df_h["regime_validita"].iloc[idx_vicino]

        return risultati

    def elabora_tutti_i_timestep(self) -> pd.DataFrame:
        """Esegue l'intero workflow di calcolo geoelettrico e sincronizzazione idrologica."""
        self.carica_dati_idrologici()
        assert self.dati_hyprop is not None

        files_ert = sorted(list(self.cartella_ert.glob("*.txt")))
        if not files_ert:
            raise FileNotFoundError(f"Nessun file ERT in {self.cartella_ert}")

        # Identifica t0 dal primo file
        prime_misure = leggi_file_acquisizione_geotom(files_ert[0])
        t0 = prime_misure[0].timestamp if prime_misure else datetime.now()

        righe_output: List[Dict[str, Any]] = []

        for f_ert in files_ert:
            m_id = re.search(r"_(\d+)\.txt$", f_ert.name, re.IGNORECASE)
            ts_id = int(m_id.group(1)) if m_id else 0

            misure_step = leggi_file_acquisizione_geotom(f_ert)
            if not misure_step:
                continue

            t_inizio = misure_step[0].timestamp
            t_fine = misure_step[-1].timestamp
            durata_min = (t_fine - t_inizio).total_seconds() / 60.0
            t_baricentro = t_inizio + (t_fine - t_inizio) / 2
            ore_da_t0 = (t_baricentro - t0).total_seconds() / 3600.0
            dt_nominale = t_inizio.replace(minute=0, second=0, microsecond=0)

            # 1. Sincronizzazione Idrologica al Baricentro
            idro = self.interpola_idrologia_al_tempo(t_baricentro)
            t_m = idro.get("Temperature [°C]", 25.0)
            m_net = idro.get("Net weight [g]", np.nan)
            m_dry = self.dati_hyprop.peso_secco_g

            # Contenuti d'acqua
            theta_pct = (
                ((m_net - m_dry) / self.volume_cm3) * 100.0 if not np.isnan(m_net) else np.nan
            )
            w_pct = (
                ((m_net - m_dry) / m_dry) * 100.0 if not np.isnan(m_net) and m_dry > 0 else np.nan
            )
            porosita = self.dati_hyprop.porosita or 0.48
            sr = (
                (theta_pct / 100.0) / porosita
                if porosita > 0 and not np.isnan(theta_pct)
                else np.nan
            )

            # Suzione in kPa
            psi_top_kpa = (
                idro.get("tension_top_estesa_hpa", np.nan) / 10.0
                if not np.isnan(idro.get("tension_top_estesa_hpa", np.nan))
                else np.nan
            )
            psi_bot_kpa = (
                idro.get("tension_bottom_estesa_hpa", np.nan) / 10.0
                if not np.isnan(idro.get("tension_bottom_estesa_hpa", np.nan))
                else np.nan
            )
            psi_media_kpa = (
                idro.get("psi_media_geometrica_hpa", np.nan) / 10.0
                if not np.isnan(idro.get("psi_media_geometrica_hpa", np.nan))
                else np.nan
            )
            log10_psi_kpa = np.log10(psi_media_kpa) if psi_media_kpa > 0 else np.nan

            # 2. Mappatura ed Estrazione Geoelettrica dei 20 Quadripoli
            # Indicizza le misure per chiave canonica diretta
            mappa_misure_canoniche: Dict[
                Tuple[Tuple[int, int], Tuple[int, int]], MisuraPuntoRawGeoTom
            ] = {}
            for m in misure_step:
                chiave = (tuple(sorted((m.a, m.b))), tuple(sorted((m.m, m.n))))
                mappa_misure_canoniche[chiave] = m

            riga_record: Dict[str, Any] = {
                "campione_id": self.id_campione,
                "time_step_id": ts_id,
                "datetime_nominale": dt_nominale,
                "datetime_inizio_ert": t_inizio,
                "datetime_fine_ert": t_fine,
                "datetime_baricentro_ert": t_baricentro,
                "durata_misura_ert_min": round(durata_min, 2),
                "ore_trascorse_da_t0": round(ore_da_t0, 2),
                # Idrologia
                "temperatura_C": round(t_m, 2),
                "peso_netto_g": round(m_net, 2) if not np.isnan(m_net) else np.nan,
                "theta_vol_pct": round(theta_pct, 2) if not np.isnan(theta_pct) else np.nan,
                "contenuto_acqua_grav_pct": round(w_pct, 2) if not np.isnan(w_pct) else np.nan,
                "grado_saturazione_Sr": round(sr, 3) if not np.isnan(sr) else np.nan,
                "suzione_top_estesa_kpa": round(psi_top_kpa, 2)
                if not np.isnan(psi_top_kpa)
                else np.nan,
                "suzione_bottom_estesa_kpa": round(psi_bot_kpa, 2)
                if not np.isnan(psi_bot_kpa)
                else np.nan,
                "suzione_media_kpa": round(psi_media_kpa, 2)
                if not np.isnan(psi_media_kpa)
                else np.nan,
                "log10_suzione_kpa": round(log10_psi_kpa, 3)
                if not np.isnan(log10_psi_kpa)
                else np.nan,
                "regime_suzione": idro.get("regime_suzione", "Non_Definito"),
            }

            # 3. Calcolo rho25 ed eps per le 8 coppie qp1..qp8
            errori_reciproci: List[float] = []
            for num_qp in range(1, 9):
                # Trova gruppo corrispondente nello schema
                nome_gruppo = (
                    f"qp{num_qp}_0"
                    if f"qp{num_qp}_0" in self.schema.coppie_qp
                    else f"qp{num_qp}_90"
                )
                if nome_gruppo not in self.schema.coppie_qp:
                    riga_record[f"rho25_qp{num_qp}"] = np.nan
                    riga_record[f"eps_qp{num_qp}"] = np.nan
                    continue

                grp = self.schema.coppie_qp[nome_gruppo]
                k_fattore = MAPPA_FATTORI_K_GRUPPI_RAPPRESENTATIVI[nome_gruppo]

                # Ramo diretto
                ch_dir = grp.quadripolo_dir.chiave_canonica_diretta()
                m_dir = mappa_misure_canoniche.get(ch_dir)
                rho25_dir = np.nan
                if m_dir and m_dir.i_ma > 0:
                    r_dir = abs(m_dir.dv_mv) / m_dir.i_ma
                    rho_m_dir = k_fattore * r_dir
                    rho25_dir = correggi_temperatura_hayashi(rho_m_dir, t_m)

                # Ramo reciproco
                ch_rec = grp.quadripolo_rec.chiave_canonica_diretta()
                m_rec = mappa_misure_canoniche.get(ch_rec)
                rho25_rec = np.nan
                if m_rec and m_rec.i_ma > 0:
                    r_rec = abs(m_rec.dv_mv) / m_rec.i_ma
                    rho_m_rec = k_fattore * r_rec
                    rho25_rec = correggi_temperatura_hayashi(rho_m_rec, t_m)

                # Calcolo media e errore reciproco
                if not np.isnan(rho25_dir) and not np.isnan(rho25_rec):
                    eps = calcola_errore_reciproco(rho25_dir, rho25_rec)
                    rho25_media = (rho25_dir + rho25_rec) / 2.0
                    riga_record[f"rho25_qp{num_qp}"] = round(rho25_media, 3)
                    riga_record[f"eps_qp{num_qp}"] = round(eps, 2)
                    errori_reciproci.append(eps)
                elif not np.isnan(rho25_dir):
                    riga_record[f"rho25_qp{num_qp}"] = round(rho25_dir, 3)
                    riga_record[f"eps_qp{num_qp}"] = np.nan
                elif not np.isnan(rho25_rec):
                    riga_record[f"rho25_qp{num_qp}"] = round(rho25_rec, 3)
                    riga_record[f"eps_qp{num_qp}"] = np.nan
                else:
                    riga_record[f"rho25_qp{num_qp}"] = np.nan
                    riga_record[f"eps_qp{num_qp}"] = np.nan

            # 4. Calcolo rho25 per i 4 Wenner singoli W1..W4
            for num_w in range(1, 5):
                nome_w = f"W{num_w}_0" if f"W{num_w}_0" in self.schema.wenner else f"W{num_w}_90"
                if nome_w not in self.schema.wenner:
                    riga_record[f"rho25_W{num_w}"] = np.nan
                    continue

                singolo = self.schema.wenner[nome_w]
                k_w = MAPPA_FATTORI_K_GRUPPI_RAPPRESENTATIVI[nome_w]
                ch_w = singolo.quadripolo.chiave_canonica_diretta()
                m_w = mappa_misure_canoniche.get(ch_w)

                if m_w and m_w.i_ma > 0:
                    r_w = abs(m_w.dv_mv) / m_w.i_ma
                    rho_m_w = k_w * r_w
                    rho25_w = correggi_temperatura_hayashi(rho_m_w, t_m)
                    riga_record[f"rho25_W{num_w}"] = round(rho25_w, 3)
                else:
                    riga_record[f"rho25_W{num_w}"] = np.nan
            # 5. Calcolo Medie Geometriche di Resistività per Categorie
            # Upper (qp1, qp2, qp3)
            vals_up = [
                riga_record.get("rho25_qp1", np.nan),
                riga_record.get("rho25_qp2", np.nan),
                riga_record.get("rho25_qp3", np.nan),
            ]
            vals_up_valid = [v for v in vals_up if pd.notna(v) and v > 0]
            riga_record["rho25_geom_upper"] = (
                round(float(np.exp(np.mean(np.log(vals_up_valid)))), 3) if vals_up_valid else np.nan
            )

            # Lower (qp4, qp5, qp6)
            vals_low = [
                riga_record.get("rho25_qp4", np.nan),
                riga_record.get("rho25_qp5", np.nan),
                riga_record.get("rho25_qp6", np.nan),
            ]
            vals_low_valid = [v for v in vals_low if pd.notna(v) and v > 0]
            riga_record["rho25_geom_lower"] = (
                round(float(np.exp(np.mean(np.log(vals_low_valid)))), 3)
                if vals_low_valid
                else np.nan
            )

            # Dipole-dipole (qp7, qp8)
            vals_dip = [
                riga_record.get("rho25_qp7", np.nan),
                riga_record.get("rho25_qp8", np.nan),
            ]
            vals_dip_valid = [v for v in vals_dip if pd.notna(v) and v > 0]
            riga_record["rho25_geom_dipole"] = (
                round(float(np.exp(np.mean(np.log(vals_dip_valid)))), 3)
                if vals_dip_valid
                else np.nan
            )

            # Wenner (W1, W2, W3, W4)
            vals_wen = [
                riga_record.get("rho25_W1", np.nan),
                riga_record.get("rho25_W2", np.nan),
                riga_record.get("rho25_W3", np.nan),
                riga_record.get("rho25_W4", np.nan),
            ]
            vals_wen_valid = [v for v in vals_wen if pd.notna(v) and v > 0]
            riga_record["rho25_geom_wenner"] = (
                round(float(np.exp(np.mean(np.log(vals_wen_valid)))), 3)
                if vals_wen_valid
                else np.nan
            )

            # Controllo Qualità QC globale del timestep (eps medio < 5%)
            qc_pass = (np.mean(errori_reciproci) < 5.0) if errori_reciproci else False
            riga_record["qualita_qc_pass"] = qc_pass

            righe_output.append(riga_record)

        return pd.DataFrame(righe_output)


def esegui_elaborazione_globale(
    base_dir_ert: Path = Path("projects/Hyprop_geotom_01Carl/data/raw/Measurement/ERT"),
    base_dir_hyprop: Path = Path("projects/Hyprop_geotom_01Carl/data/raw/Measurement/Hyprop"),
    cartella_output: Path = Path("projects/Hyprop_geotom_01Carl/data/processed"),
) -> Dict[str, pd.DataFrame]:
    """Elabora tutti i campioni disponibili, esporta i CSV per campione e il dataset globale."""
    cartella_output.mkdir(parents=True, exist_ok=True)
    cartella_tabelle = cartella_output / "tabelle_campioni"
    cartella_tabelle.mkdir(parents=True, exist_ok=True)

    campioni_ert = sorted([d.name for d in base_dir_ert.iterdir() if d.is_dir()])
    schema = Schema20QuadripoliRappresentativi()
    risultati: Dict[str, pd.DataFrame] = {}
    tutti_i_df: List[pd.DataFrame] = []

    for id_campione in campioni_ert:
        dir_ert = base_dir_ert / id_campione
        dir_hyp = base_dir_hyprop / id_campione

        if not dir_hyp.exists():
            print(f"[{id_campione}] Cartella HYPROP non trovata, skip.")
            continue

        xlsx_files = list(dir_hyp.glob("*.xlsx"))
        if not xlsx_files:
            print(f"[{id_campione}] Nessun file Excel HYPROP, skip.")
            continue

        file_xlsx = xlsx_files[0]
        print(f"[{id_campione}] Inizio elaborazione ({dir_ert.name} + {file_xlsx.name})...")

        elaboratore = ElaboratoreCampioneIntegrato(
            id_campione=id_campione,
            cartella_ert=dir_ert,
            file_hyprop_xlsx=file_xlsx,
            schema=schema,
            volume_cm3=VOLUME_PORTACAMPIONE_CM3,
        )

        df_campione = elaboratore.elabora_tutti_i_timestep()
        file_out_csv = cartella_tabelle / f"{id_campione}_serie_integrata.csv"
        df_campione.to_csv(file_out_csv, index=False)
        print(f"[{id_campione}] Completato: {len(df_campione)} timestep -> {file_out_csv.name}")

        risultati[id_campione] = df_campione
        tutti_i_df.append(df_campione)

    # Dataset Globale concatenato
    if tutti_i_df:
        df_globale = pd.concat(tutti_i_df, ignore_index=True)
        file_globale_csv = cartella_output / "dataset_completo_tutti_campioni.csv"
        df_globale.to_csv(file_globale_csv, index=False)
        print(f"\n=== Dataset Globale: {len(df_globale)} record in {file_globale_csv.name} ===")

    return risultati
