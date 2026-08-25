"""Script e funzioni per l'audit e il riallineamento orario dei timestep nei file GeoTom."""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


def estrai_timestamp_file_geotom(fpath: Path) -> Optional[datetime]:
    """Legge la data e ora effettiva di acquisizione dalle righe di misura di un file GeoTom."""
    with open(fpath, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 11 and parts[0].isdigit():
                date_str = parts[-2]
                time_str = parts[-1]
                try:
                    return datetime.strptime(f"{date_str} {time_str}", "%d.%m.%Y %H:%M:%S")
                except ValueError:
                    pass
    return None


def estrai_id_dal_nome(fname: str) -> Optional[int]:
    """Estrae l'ID numerico dal suffisso del file (es. '_014' -> 14)."""
    m = re.search(r"_(\d+)\.txt$", fname, re.IGNORECASE)
    return int(m.group(1)) if m else None


def analizza_directory_campione(
    cartella_campione: Path,
) -> Dict[str, object]:
    """Esegue l'audit temporale su tutti i file di una cartella di campionamento."""
    files = sorted(list(cartella_campione.glob("*.txt")))
    if not files:
        return {"cartella": cartella_campione.name, "errore": "Nessun file .txt"}

    elenco: List[Tuple[Path, int, datetime]] = []
    for f in files:
        fid = estrai_id_dal_nome(f.name)
        dt = estrai_timestamp_file_geotom(f)
        if fid is not None and dt is not None:
            elenco.append((f, fid, dt))

    elenco.sort(key=lambda x: x[2])  # Ordina per timestamp cronologico reale
    if not elenco:
        return {"cartella": cartella_campione.name, "errore": "Timestamp non leggibili"}

    t0 = elenco[0][2]
    piani_rinomina: List[Tuple[Path, Path, int, int]] = []

    for f, fid_attuale, dt in elenco:
        delta_ore = (dt - t0).total_seconds() / 3600.0
        id_reale = 1 + int(round(delta_ore))

        if fid_attuale != id_reale:
            # Sostituisci il suffisso numerico _XXX.txt con il nuovo _YYY.txt
            nuovo_nome = re.sub(
                r"_(\d+)\.txt$",
                f"_{id_reale:03d}.txt",
                f.name,
                flags=re.IGNORECASE,
            )
            nuovo_percorso = f.parent / nuovo_nome
            piani_rinomina.append((f, nuovo_percorso, fid_attuale, id_reale))

    return {
        "cartella": cartella_campione.name,
        "n_file": len(elenco),
        "t0": t0,
        "t_end": elenco[-1][2],
        "durata_ore": (elenco[-1][2] - t0).total_seconds() / 3600.0,
        "disallineati": len(piani_rinomina) > 0,
        "piani_rinomina": piani_rinomina,
    }


def esegui_riallineamento_nomi(cartella_campione: Path) -> List[str]:
    """Rinomina fisicamente i file per riallineare gli ID all'ora reale dall'inizio t0.

    Operazione condotta a ritroso per prevenire collisioni di nome.
    """
    analisi = analizza_directory_campione(cartella_campione)
    piani = analisi.get("piani_rinomina", [])
    if not piani:
        return [f"Nessun file da rinominare in {cartella_campione.name}."]

    # Ordina a ritroso per ID reale decrescente (per evitare sovrascritture di file esistenti)
    piani_ordinati = sorted(piani, key=lambda x: x[3], reverse=True)
    log_operazioni = []

    for vecchio_path, nuovo_path, id_vecchio, id_nuovo in piani_ordinati:
        if vecchio_path.exists():
            vecchio_path.rename(nuovo_path)
            msg = (
                f"[{cartella_campione.name}] {vecchio_path.name} (ID {id_vecchio:03d}) "
                f"-> {nuovo_path.name} (ID {id_nuovo:03d})"
            )
            log_operazioni.append(msg)

    return log_operazioni
