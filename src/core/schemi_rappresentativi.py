"""Definizione e gestione dei 20 Quadripoli Rappresentativi e delle Quadrupole Pairs (qp)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Tuple

import numpy as np

from src.core.correzioni import calcola_indice_ar
from src.core.fattori_geometrici import MAPPA_FATTORI_K_GRUPPI_RAPPRESENTATIVI
from src.core.geometria import ArrayCilindrico16
from src.core.quadripoli import (
    ClassificatoreQuadripoli,
    Orientazione,
    Quadripolo,
)


class CategoriaRappresentativa(str, Enum):
    """Macro-categorie dei quadripoli rappresentativi."""

    HORIZONTAL_UPPER = "Horizontal_Upper"
    HORIZONTAL_LOWER = "Horizontal_Lower"
    VERTICAL_DIPOLE_DIPOLE = "Vertical_Dipole_Dipole"
    VERTICAL_WENNER = "Vertical_Wenner"


@dataclass(frozen=True)
class GruppoRappresentativoQP:
    """Rappresentazione di una coppia diretta-reciproca (qp) nei quadripoli rappresentativi."""

    codice: str  # es. "qp1_0", "qp8_90"
    etichetta_latex: str  # es. "qp1_{0^\\circ}"
    categoria: CategoriaRappresentativa
    orientazione: Orientazione  # 0° o 90°
    quadripolo_dir: Quadripolo
    quadripolo_rec: Quadripolo

    @property
    def tupla_dir(self) -> Tuple[int, int, int, int]:
        return self.quadripolo_dir.tupla_elettrodi

    @property
    def tupla_rec(self) -> Tuple[int, int, int, int]:
        return self.quadripolo_rec.tupla_elettrodi

    def calcola_rho_media_coppia(self, rho_dir: float, rho_rec: float) -> float:
        """Calcola la resistività apparente media della coppia reciproca."""
        return float((rho_dir + rho_rec) / 2.0)


@dataclass(frozen=True)
class SingoloRappresentativoWenner:
    """Rappresentazione di una configurazione Wenner singola (W1..W4)."""

    codice: str  # es. "W1_0", "W2_90"
    etichetta_latex: str  # es. "W1_{0^\\circ}"
    categoria: CategoriaRappresentativa
    orientazione: Orientazione
    linea_verticale: int
    quadripolo: Quadripolo

    @property
    def tupla_elettrodi(self) -> Tuple[int, int, int, int]:
        return self.quadripolo.tupla_elettrodi


class Schema20QuadripoliRappresentativi:
    """Gestione dei 20 quadripoli rappresentativi (8 coppie qp + 4 Wenner).

    Struttura:
    - Upper Horizontal:
      * qp1_0° : (1, 5, 13, 9)  <-> (13, 9, 1, 5)   [Anello 1, z=4 cm, 0°]
      * qp2_0° : (2, 6, 14, 10) <-> (14, 10, 2, 6)  [Anello 2, z=3 cm, 0°]
      * qp3_90°: (6, 10, 2, 14) <-> (2, 14, 6, 10)  [Anello 2, z=3 cm, 90°]
    - Lower Horizontal:
      * qp4_0° : (3, 7, 15, 11) <-> (15, 11, 3, 7)  [Anello 3, z=2 cm, 0°]
      * qp5_0° : (4, 8, 16, 12) <-> (16, 12, 4, 8)  [Anello 4, z=1 cm, 0°]
      * qp6_90°: (7, 11, 3, 15) <-> (3, 15, 7, 11)  [Anello 3, z=2 cm, 90°]
    - Vertical Dipole-Dipole:
      * qp7_0° : (1, 2, 3, 4)   <-> (3, 4, 1, 2)    [Linea 1, 0°]
      * qp8_90°: (5, 6, 7, 8)   <-> (7, 8, 5, 6)    [Linea 2, 90°]
    - Vertical Wenner:
      * W1_0°  : (1, 4, 2, 3)                       [Linea 1, 0°]
      * W2_90° : (5, 8, 6, 7)                       [Linea 2, 90°]
      * W3_0°  : (9, 12, 10, 11)                    [Linea 3, 0°]
      * W4_90° : (13, 16, 14, 15)                   [Linea 4, 90°]
    """

    DEFINIZIONI_QP: List[
        Tuple[
            str,
            str,
            CategoriaRappresentativa,
            Orientazione,
            Tuple[int, int, int, int],
            Tuple[int, int, int, int],
        ]
    ] = [
        # Upper Horizontal (6 quadripoli: 4 a 0°, 2 a 90°)
        (
            "qp1_0",
            r"qp1_{0^\circ}",
            CategoriaRappresentativa.HORIZONTAL_UPPER,
            Orientazione.DEG_0,
            (1, 5, 13, 9),
            (13, 9, 1, 5),
        ),
        (
            "qp2_0",
            r"qp2_{0^\circ}",
            CategoriaRappresentativa.HORIZONTAL_UPPER,
            Orientazione.DEG_0,
            (2, 6, 14, 10),
            (14, 10, 2, 6),
        ),
        (
            "qp3_90",
            r"qp3_{90^\circ}",
            CategoriaRappresentativa.HORIZONTAL_UPPER,
            Orientazione.DEG_90,
            (6, 10, 2, 14),
            (2, 14, 6, 10),
        ),
        # Lower Horizontal (6 quadripoli: 4 a 0°, 2 a 90°)
        (
            "qp4_0",
            r"qp4_{0^\circ}",
            CategoriaRappresentativa.HORIZONTAL_LOWER,
            Orientazione.DEG_0,
            (3, 7, 15, 11),
            (15, 11, 3, 7),
        ),
        (
            "qp5_0",
            r"qp5_{0^\circ}",
            CategoriaRappresentativa.HORIZONTAL_LOWER,
            Orientazione.DEG_0,
            (4, 8, 16, 12),
            (16, 12, 4, 8),
        ),
        (
            "qp6_90",
            r"qp6_{90^\circ}",
            CategoriaRappresentativa.HORIZONTAL_LOWER,
            Orientazione.DEG_90,
            (7, 11, 3, 15),
            (3, 15, 7, 11),
        ),
        # Vertical Dipole-Dipole (4 quadripoli: 2 a 0°, 2 a 90°)
        (
            "qp7_0",
            r"qp7_{0^\circ}",
            CategoriaRappresentativa.VERTICAL_DIPOLE_DIPOLE,
            Orientazione.DEG_0,
            (1, 2, 3, 4),
            (3, 4, 1, 2),
        ),
        (
            "qp8_90",
            r"qp8_{90^\circ}",
            CategoriaRappresentativa.VERTICAL_DIPOLE_DIPOLE,
            Orientazione.DEG_90,
            (5, 6, 7, 8),
            (7, 8, 5, 6),
        ),
    ]

    DEFINIZIONI_WENNER: List[
        Tuple[str, str, CategoriaRappresentativa, Orientazione, int, Tuple[int, int, int, int]]
    ] = [
        # Vertical Wenner (4 quadripoli: 2 a 0°, 2 a 90°)
        (
            "W1_0",
            r"W1_{0^\circ}",
            CategoriaRappresentativa.VERTICAL_WENNER,
            Orientazione.DEG_0,
            1,
            (1, 4, 2, 3),
        ),
        (
            "W2_90",
            r"W2_{90^\circ}",
            CategoriaRappresentativa.VERTICAL_WENNER,
            Orientazione.DEG_90,
            2,
            (5, 8, 6, 7),
        ),
        (
            "W3_0",
            r"W3_{0^\circ}",
            CategoriaRappresentativa.VERTICAL_WENNER,
            Orientazione.DEG_0,
            3,
            (9, 12, 10, 11),
        ),
        (
            "W4_90",
            r"W4_{90^\circ}",
            CategoriaRappresentativa.VERTICAL_WENNER,
            Orientazione.DEG_90,
            4,
            (13, 16, 14, 15),
        ),
    ]

    def __init__(self, array_geom: Optional[ArrayCilindrico16] = None) -> None:
        self.array_geom = array_geom or ArrayCilindrico16()
        self.classificatore = ClassificatoreQuadripoli(self.array_geom)

        self.coppie_qp: Dict[str, GruppoRappresentativoQP] = {}
        self.wenner: Dict[str, SingoloRappresentativoWenner] = {}
        self._mappa_canonica_diretta_a_codice: Dict[
            Tuple[Tuple[int, int], Tuple[int, int]], str
        ] = {}
        self._mappa_canonica_reciproca_a_gruppo: Dict[
            Tuple[Tuple[int, int], Tuple[int, int]], str
        ] = {}

        self._costruisci_schemi()

    def _costruisci_schemi(self) -> None:
        """Istanzia e indicizza tutti i 20 quadripoli con invarianza di polarità e fattori K."""
        for cod, latex, cat, orient, t_dir, t_rec in self.DEFINIZIONI_QP:
            k = MAPPA_FATTORI_K_GRUPPI_RAPPRESENTATIVI.get(cod)
            q_dir = self.classificatore.classifica(*t_dir, fattore_k=k)
            q_rec = self.classificatore.classifica(*t_rec, fattore_k=k)
            gruppo = GruppoRappresentativoQP(
                codice=cod,
                etichetta_latex=latex,
                categoria=cat,
                orientazione=orient,
                quadripolo_dir=q_dir,
                quadripolo_rec=q_rec,
            )
            self.coppie_qp[cod] = gruppo

            # Mappatura per chiave canonica diretta (invariante per A <-> B e M <-> N)
            self._mappa_canonica_diretta_a_codice[q_dir.chiave_canonica_diretta()] = f"{cod}_dir"
            self._mappa_canonica_diretta_a_codice[q_rec.chiave_canonica_diretta()] = f"{cod}_rec"
            self._mappa_canonica_reciproca_a_gruppo[q_dir.chiave_canonica_reciproca()] = cod

        for cod, latex, cat, orient, linea, t_w in self.DEFINIZIONI_WENNER:
            k = MAPPA_FATTORI_K_GRUPPI_RAPPRESENTATIVI.get(cod)
            q_w = self.classificatore.classifica(*t_w, fattore_k=k)
            singolo = SingoloRappresentativoWenner(
                codice=cod,
                etichetta_latex=latex,
                categoria=cat,
                orientazione=orient,
                linea_verticale=linea,
                quadripolo=q_w,
            )
            self.wenner[cod] = singolo
            # Wenner non ha reciproci: mappatura strettamente limitata alla quaterna diretta
            self._mappa_canonica_diretta_a_codice[q_w.chiave_canonica_diretta()] = cod
            self._mappa_canonica_reciproca_a_gruppo[q_w.chiave_canonica_diretta()] = cod

    def tutti_i_quadripoli(self) -> List[Quadripolo]:
        """Restituisce la lista esatta dei 20 quadripoli rappresentativi."""
        elenco: List[Quadripolo] = []
        for qp in self.coppie_qp.values():
            elenco.extend([qp.quadripolo_dir, qp.quadripolo_rec])
        for w in self.wenner.values():
            elenco.append(w.quadripolo)
        return elenco

    def ottieni_codice_quadripolo(self, a: int, b: int, m: int, n: int) -> Optional[str]:
        """Restituisce il codice identificativo (es. 'qp1_0_dir', 'W1_0') per la quaterna.

        Invariante per inversioni di polarità: AB MN == BA MN == AB NM == BA NM.
        """
        chiave_dir = (tuple(sorted((a, b))), tuple(sorted((m, n))))
        return self._mappa_canonica_diretta_a_codice.get(chiave_dir)  # type: ignore[arg-type]

    def ottieni_gruppo_qp(self, a: int, b: int, m: int, n: int) -> Optional[str]:
        """Restituisce il gruppo QP di appartenenza (es. 'qp1_0', 'W1_0') per la quaterna."""
        dipolo_ab = tuple(sorted((a, b)))
        dipolo_mn = tuple(sorted((m, n)))
        chiave_rec = tuple(sorted((dipolo_ab, dipolo_mn)))
        return self._mappa_canonica_reciproca_a_gruppo.get(chiave_rec)  # type: ignore[arg-type]

    def calcola_ar_categoria(
        self,
        categoria: CategoriaRappresentativa,
        mappa_resistivita: Dict[str, float],
    ) -> float:
        """Calcola l'Anisotropy Ratio AR = rho_a(90°) / rho_a(0°) per una determinata categoria.

        Parametri:
            categoria: Macro-categoria (Upper, Lower, Dipole-Dipole, Wenner).
            mappa_resistivita: Mappa codice quadripolo/coppia -> valore di rho_a.
        """
        valori_0: List[float] = []
        valori_90: List[float] = []

        if categoria in (
            CategoriaRappresentativa.HORIZONTAL_UPPER,
            CategoriaRappresentativa.HORIZONTAL_LOWER,
            CategoriaRappresentativa.VERTICAL_DIPOLE_DIPOLE,
        ):
            for qp in self.coppie_qp.values():
                if qp.categoria == categoria:
                    # Verifica se è fornito il valore per il gruppo qp o per i singoli rami
                    if qp.codice in mappa_resistivita:
                        val = mappa_resistivita[qp.codice]
                    else:
                        v_dir = mappa_resistivita.get(f"{qp.codice}_dir", np.nan)
                        v_rec = mappa_resistivita.get(f"{qp.codice}_rec", np.nan)
                        val = float(np.nanmean([v_dir, v_rec]))

                    if not np.isnan(val):
                        if qp.orientazione == Orientazione.DEG_0:
                            valori_0.append(val)
                        elif qp.orientazione == Orientazione.DEG_90:
                            valori_90.append(val)

        elif categoria == CategoriaRappresentativa.VERTICAL_WENNER:
            for w in self.wenner.values():
                val = mappa_resistivita.get(w.codice, np.nan)
                if not np.isnan(val):
                    if w.orientazione == Orientazione.DEG_0:
                        valori_0.append(val)
                    elif w.orientazione == Orientazione.DEG_90:
                        valori_90.append(val)

        if not valori_0 or not valori_90:
            return float("nan")

        media_0 = float(np.mean(valori_0))
        media_90 = float(np.mean(valori_90))
        return calcola_indice_ar(media_90, media_0)  # type: ignore[return-value]
