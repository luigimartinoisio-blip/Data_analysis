"""Parser e funzioni I/O per file di sequenza (.flw) e acquisizioni GeoTom."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd

from src.core.geometria import ArrayCilindrico16
from src.core.quadripoli import ClassificatoreQuadripoli, Quadripolo
from src.core.schemi_rappresentativi import Schema20QuadripoliRappresentativi

# Mappatura standard dei campioni (sia notazione di campagna che mineralogica) ai file .flw
MAPPA_CAMPIONI_SEQUENZE: Dict[str, str] = {
    # Nomenclatura di campagna
    "1a": "LastSeq_file.flw",
    "1b": "LastSeq_file.flw",
    "2a": "LastSeq_file.flw",
    "2b": "LastSeq_file.flw",
    "3a": "LastSeq_file.flw",
    "3b": "LastSeq_file.flw",
    "4b": "LastSeq_file.flw",
    "5a": "SEQ_May2026.flw",
    "6a": "SEQ_May2026.flw",
    "Sand_R": "SEQ_June2026.flw",
    # Nomenclatura gruppo mineralogico (ML)
    "ML1": "SEQ_May2026.flw",  # 5a
    "ML2": "SEQ_May2026.flw",  # 5b
    "ML3": "LastSeq_file.flw",  # 1a
    "ML4": "LastSeq_file.flw",  # 1b
    "ML5": "LastSeq_file.flw",  # 2a
    "ML6": "LastSeq_file.flw",  # 2b
    "ML7": "LastSeq_file.flw",  # 3a
    "ML8": "LastSeq_file.flw",  # 3b
    "ML9": "LastSeq_file.flw",  # 4b
    "ML10": "SEQ_May2026.flw",  # 6a
}


@dataclass
class SequenzaGeoTom:
    """Rappresentazione strutturata di una sequenza di misura GeoTom (.flw)."""

    nome_file: str
    percorso_file: Path
    metadati: Dict[str, Any] = field(default_factory=dict)
    numero_punti_dichiarato: int = 0
    quadripoli: List[Quadripolo] = field(default_factory=list)
    dataframe: pd.DataFrame = field(default_factory=pd.DataFrame)


class ParserSequenzaGeoTom:
    """Parser per file di sequenza GeoTom (.flw / Flow)."""

    def __init__(
        self,
        array_geom: Optional[ArrayCilindrico16] = None,
        schema_rappresentativo: Optional[Schema20QuadripoliRappresentativi] = None,
    ) -> None:
        self.array_geom = array_geom or ArrayCilindrico16()
        self.schema_rap = schema_rappresentativo or Schema20QuadripoliRappresentativi(
            self.array_geom
        )
        self.classificatore = ClassificatoreQuadripoli(self.array_geom)

    def leggi_flw(self, percorso: str | Path) -> SequenzaGeoTom:
        """Legge e analizza un file di sequenza GeoTom .flw."""
        p = Path(percorso)
        if not p.exists():
            raise FileNotFoundError(f"File sequenza non trovato: {p}")

        metadati: Dict[str, Any] = {}
        quaterne: List[Tuple[int, int, int, int]] = []

        with open(p, "r", encoding="utf-8", errors="replace") as f:
            for riga in f:
                riga_pulita = riga.strip()
                if not riga_pulita:
                    continue

                # Commenti intestazione GeoTom
                if riga_pulita.startswith("//"):
                    continue

                # Chiavi metadati (es. Type: Flow, Name: Hyprop, Nr of points: 289)
                if ":" in riga_pulita and not riga_pulita.startswith("$"):
                    parti = riga_pulita.split(":", 1)
                    chiave = parti[0].strip()
                    valore = parti[1].strip()
                    metadati[chiave] = valore
                    continue

                # Righe di quadripoli (A, B, M, N, $0...)
                # Token separati da tab o spazi
                tokens = re.split(r"\s+", riga_pulita)
                if len(tokens) >= 4:
                    try:
                        a = int(tokens[0])
                        b = int(tokens[1])
                        m = int(tokens[2])
                        n = int(tokens[3])
                        quaterne.append((a, b, m, n))
                    except ValueError:
                        # Non è una riga con numeri interi di elettrodi
                        continue

        nr_punti_dichiarato = int(metadati.get("Nr of points", len(quaterne)))

        # Classificazione di tutti i quadripoli
        quadripoli: List[Quadripolo] = []
        record_df = []

        for idx, (a, b, m, n) in enumerate(quaterne, start=1):
            q = self.classificatore.classifica(a, b, m, n)
            quadripoli.append(q)

            codice_rap = self.schema_rap.ottieni_codice_quadripolo(a, b, m, n)
            gruppo_rap = self.schema_rap.ottieni_gruppo_qp(a, b, m, n)

            record_df.append(
                {
                    "indice_misura": idx,
                    "a": a,
                    "b": b,
                    "m": m,
                    "n": n,
                    "categoria": q.categoria.value,
                    "orientazione": q.orientazione.value,
                    "linea_verticale": q.linea_verticale,
                    "anello_orizzontale": q.anello_orizzontale,
                    "quota_media_cm": q.quota_media_cm,
                    "codice_rappresentativo": codice_rap,
                    "gruppo_rappresentativo": gruppo_rap,
                    "e_rappresentativo": gruppo_rap is not None,
                }
            )

        df = pd.DataFrame(record_df)

        return SequenzaGeoTom(
            nome_file=p.name,
            percorso_file=p,
            metadati=metadati,
            numero_punti_dichiarato=nr_punti_dichiarato,
            quadripoli=quadripoli,
            dataframe=df,
        )


def ottieni_file_sequenza_campione(
    id_campione: str,
    cartella_sequenze: str | Path = "projects/Hyprop_geotom_01Carl/data/raw/Sequenze",
) -> Path:
    """Restituisce il percorso completo al file .flw per un determinato campione."""
    if id_campione not in MAPPA_CAMPIONI_SEQUENZE:
        raise KeyError(
            f"Campione '{id_campione}' non riconosciuto. Campioni validi: "
            f"{list(MAPPA_CAMPIONI_SEQUENZE.keys())}"
        )

    nome_file = MAPPA_CAMPIONI_SEQUENZE[id_campione]
    percorso = Path(cartella_sequenze) / nome_file
    return percorso
