"""Modulo per la standardizzazione della nomenclatura campioni (ML1..ML10, Sand_R)."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Tuple

# Tabella di equivalenza ufficiale tra nomenclatura di campagna e gruppo mineralogico
MAPPA_CAMPAGNA_A_MINERALOGICO: Dict[str, str] = {
    "5a": "ML1",
    "5b": "ML2",
    "1a": "ML3",
    "1b": "ML4",
    "2a": "ML5",
    "2b": "ML6",
    "3a": "ML7",
    "3b": "ML8",
    "4b": "ML9",
    "6a": "ML10",
    "Sand_R": "Sand_R",
}

MAPPA_MINERALOGICO_A_CAMPAGNA: Dict[str, str] = {
    v: k for k, v in MAPPA_CAMPAGNA_A_MINERALOGICO.items()
}

MAPPA_DIR_A_ID_MINERALOGICO: Dict[str, str] = {
    "TL_ERT_5a": "ML1",
    "TL_ERT_1a": "ML3",
    "TL_ERT_1b": "ML4",
    "TL_ERT_2a": "ML5",
    "TL_ERT_2b": "ML6",
    "TL_ERT_3a": "ML7",
    "TL_ERT_3b": "ML8",
    "TL_ERT_4b": "ML9",
    "TL_ERT_6a": "ML10",
    "TL_ERT_Sand_R": "Sand_R",
    "ML1": "ML1",
    "ML3": "ML3",
    "ML4": "ML4",
    "ML5": "ML5",
    "ML6": "ML6",
    "ML7": "ML7",
    "ML8": "ML8",
    "ML9": "ML9",
    "ML10": "ML10",
    "Sand_R": "Sand_R",
}


def rinomina_file_in_directory(
    cartella: Path,
    id_standard: str,
) -> List[Tuple[Path, Path]]:
    """Rinomina tutti i file .txt nella directory adottando il formato {id_standard}_{num}.txt."""
    files = sorted(list(cartella.glob("*.txt")))
    rinominati: List[Tuple[Path, Path]] = []

    for f in files:
        m = re.search(r"_(\d+)\.txt$", f.name, re.IGNORECASE)
        if not m:
            continue
        num_str = m.group(1)
        nuovo_nome = f"{id_standard}_{num_str}.txt"
        nuovo_path = f.parent / nuovo_nome
        if f.name != nuovo_nome:
            f.rename(nuovo_path)
            rinominati.append((f, nuovo_path))

    return rinominati


def esegui_standardizzazione_globale(
    base_dir: Path = Path("projects/Hyprop_geotom_01Carl/data/raw/Measurement/ERT"),
) -> Dict[str, int]:
    """Esegue la ridenominazione standard per tutte le cartelle campioni."""
    risultati: Dict[str, int] = {}

    for d in sorted(base_dir.iterdir()):
        if not d.is_dir():
            continue
        id_ml = MAPPA_DIR_A_ID_MINERALOGICO.get(d.name)
        if not id_ml:
            continue

        rinominati = rinomina_file_in_directory(d, id_ml)
        risultati[d.name] = len(rinominati)

    return risultati
