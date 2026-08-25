"""Definizione e classificazione dei Quadripoli e delle Coppie di Quadripoli (QP)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Sequence, Set, Tuple

from src.core.geometria import ArrayCilindrico16


class CategoriaQuadripolo(str, Enum):
    """Categorie strutturali dei quadripoli nell'esperimento Hyprop-GeoTom."""

    VERTICALE_WENNER = "Verticale_Wenner"
    VERTICALE_DIPOLO_DIPOLO = "Verticale_DipoloDipolo"
    VERTICALE_ALTRO = "Verticale_Altro"
    ORIZZONTALE_UPPER = "Orizzontale_Upper"
    ORIZZONTALE_LOWER = "Orizzontale_Lower"
    ORIZZONTALE_ALTRO = "Orizzontale_Altro"
    TRIDIMENSIONALE = "Tridimensionale_Misto"


class Orientazione(str, Enum):
    """Orientazione azimuthale del quadripolo per analisi di anisotropia."""

    DEG_0 = "0°"
    DEG_90 = "90°"
    NON_APPLICABILE = "N/A"


class TipoCoppiaQuadripoli(str, Enum):
    """Tipologia di coppia di quadripoli (Quadrupole Pair - QP)."""

    DIRETTO_RECIPROCO = "Diretto_Reciproco"
    ANISOTROPIA_0_90 = "Anisotropia_0_90"


@dataclass(frozen=True)
class Quadripolo:
    """Rappresentazione formale di una misura a quattro elettrodi (A, B, M, N).

    Convenzione:
    - A, B: Elettrodi di iniezione di corrente
    - M, N: Elettrodi di misura del potenziale (Delta V = V_M - V_N)
    """

    a: int
    b: int
    m: int
    n: int
    categoria: CategoriaQuadripolo
    orientazione: Orientazione = Orientazione.NON_APPLICABILE
    linea_verticale: Optional[int] = None
    anello_orizzontale: Optional[int] = None
    quota_media_cm: float = 0.0
    fattore_k: Optional[float] = None

    @property
    def tupla_elettrodi(self) -> Tuple[int, int, int, int]:
        """Restituisce la quaterna (A, B, M, N)."""
        return (self.a, self.b, self.m, self.n)

    @property
    def elettrodi_unici(self) -> Set[int]:
        """Restituisce il set di elettrodi distinti utilizzati."""
        return {self.a, self.b, self.m, self.n}

    def crea_reciproco(self, array_geom: Optional[ArrayCilindrico16] = None) -> Quadripolo:
        """Genera il quadripolo reciproco scambiando corrente e potenziale: (M, N, A, B)."""
        classificatore = ClassificatoreQuadripoli(array_geom or ArrayCilindrico16())
        return classificatore.classifica(self.m, self.n, self.a, self.b, fattore_k=self.fattore_k)

    def chiave_canonica_diretta(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """Restituisce la chiave canonica dei dipoli: ((min(A,B), max(A,B)), (min(M,N), max(M,N))).

        Invariante per inversioni di polarità interne: AB MN == BA MN == AB NM == BA NM.
        """
        dipolo_ab = tuple(sorted((self.a, self.b)))
        dipolo_mn = tuple(sorted((self.m, self.n)))
        return (dipolo_ab, dipolo_mn)  # type: ignore[return-value]

    def chiave_canonica_reciproca(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """Restituisce una chiave indipendente sia da polarità interne che dal verso AB <-> MN."""
        dipolo_ab = tuple(sorted((self.a, self.b)))
        dipolo_mn = tuple(sorted((self.m, self.n)))
        return tuple(sorted((dipolo_ab, dipolo_mn)))  # type: ignore[return-value]


@dataclass(frozen=True)
class CoppiaQuadripoli:
    """Coppia formale di quadripoli (Quadrupole Pair - QP).

    Può rappresentare:
    1. Coppia Diretto-Reciproco (per QC su errore reciproco)
    2. Coppia di Anisotropia 0° - 90° (per il rapporto di resistività ortogonale)
    """

    tipo_coppia: TipoCoppiaQuadripoli
    quadripolo_1: Quadripolo
    quadripolo_2: Quadripolo
    descrizione: str = ""

    def calcola_errore_percentuale(self, valore_1: float, valore_2: float) -> float:
        """Calcola la discrepanza relativa percentuale tra i due valori misurati.

        Formula: |V1 - V2| / (0.5 * (|V1| + |V2|)) * 100
        """
        denominatore = 0.5 * (abs(valore_1) + abs(valore_2))
        if denominatore == 0.0:
            return 0.0
        return float(abs(valore_1 - valore_2) / denominatore * 100.0)

    def calcola_rapporto_anisotropia(self, rho_0: float, rho_90: float) -> float:
        """Calcola l'indice di rapporto di anisotropia elettrica (Anisotropy Ratio - AR).

        Formula:
            AR = rho_a(90°) / rho_a(0°)

        Baseline isotropa: AR = 1.
        """
        if rho_0 <= 0.0:
            return float("nan")
        return float(rho_90 / rho_0)


class ClassificatoreQuadripoli:
    """Algoritmo per la classificazione geometrica automatica dei quadripoli."""

    def __init__(self, array_geom: Optional[ArrayCilindrico16] = None) -> None:
        self.array_geom = array_geom or ArrayCilindrico16()

    def classifica(
        self,
        a: int,
        b: int,
        m: int,
        n: int,
        fattore_k: Optional[float] = None,
    ) -> Quadripolo:
        """Determina la categoria, l'orientazione e i parametri del quadripolo."""
        e_a = self.array_geom.ottieni_elettrodo(a)
        e_b = self.array_geom.ottieni_elettrodo(b)
        e_m = self.array_geom.ottieni_elettrodo(m)
        e_n = self.array_geom.ottieni_elettrodo(n)

        linee = {e_a.linea, e_b.linea, e_m.linea, e_n.linea}
        anelli = {e_a.anello, e_b.anello, e_m.anello, e_n.anello}
        quota_media = (e_a.quota_z_cm + e_b.quota_z_cm + e_m.quota_z_cm + e_n.quota_z_cm) / 4.0

        # Caso 1: Array Verticale (tutti gli elettrodi sulla stessa linea verticale)
        if len(linee) == 1:
            linea_vert = next(iter(linee))
            # Identificazione specifica Wenner vs Dipolo-Dipolo
            # Wenner standard (A - M - N - B lungo la linea ordinata per quota)
            seq_anelli = (e_a.anello, e_m.anello, e_n.anello, e_b.anello)
            # Dipolo-Dipolo standard (A - B - M - N lungo la linea)
            seq_dipolo = (e_a.anello, e_b.anello, e_m.anello, e_n.anello)

            if seq_anelli in ((1, 2, 3, 4), (4, 3, 2, 1)):
                categoria = CategoriaQuadripolo.VERTICALE_WENNER
            elif seq_dipolo in ((1, 2, 3, 4), (4, 3, 2, 1), (1, 2, 4, 3), (4, 3, 1, 2)):
                categoria = CategoriaQuadripolo.VERTICALE_DIPOLO_DIPOLO
            else:
                categoria = CategoriaQuadripolo.VERTICALE_ALTRO

            return Quadripolo(
                a=a,
                b=b,
                m=m,
                n=n,
                categoria=categoria,
                orientazione=Orientazione.NON_APPLICABILE,
                linea_verticale=linea_vert,
                anello_orizzontale=None,
                quota_media_cm=quota_media,
                fattore_k=fattore_k,
            )

        # Caso 2: Array Orizzontale (tutti gli elettrodi sullo stesso anello/quota)
        if len(anelli) == 1:
            anello_idx = next(iter(anelli))
            if anello_idx in (1, 2):
                categoria = CategoriaQuadripolo.ORIZZONTALE_UPPER
            elif anello_idx in (3, 4):
                categoria = CategoriaQuadripolo.ORIZZONTALE_LOWER
            else:
                categoria = CategoriaQuadripolo.ORIZZONTALE_ALTRO

            # Determinazione orientazione: 0° (lungo asse linee 1-3) o 90° (lungo asse linee 2-4)
            orientazione = self._determina_orientazione_orizzontale(
                e_a.linea, e_b.linea, e_m.linea, e_n.linea
            )

            return Quadripolo(
                a=a,
                b=b,
                m=m,
                n=n,
                categoria=categoria,
                orientazione=orientazione,
                linea_verticale=None,
                anello_orizzontale=anello_idx,
                quota_media_cm=quota_media,
                fattore_k=fattore_k,
            )

        # Caso 3: Configurazione 3D Mista
        # Verifichiamo se è prevalentemente Upper (anelli 1-2) o Lower (anelli 3-4)
        if all(anello in (1, 2) for anello in anelli):
            categoria = CategoriaQuadripolo.ORIZZONTALE_UPPER
        elif all(anello in (3, 4) for anello in anelli):
            categoria = CategoriaQuadripolo.ORIZZONTALE_LOWER
        else:
            categoria = CategoriaQuadripolo.TRIDIMENSIONALE

        orientazione = self._determina_orientazione_orizzontale(
            e_a.linea, e_b.linea, e_m.linea, e_n.linea
        )

        return Quadripolo(
            a=a,
            b=b,
            m=m,
            n=n,
            categoria=categoria,
            orientazione=orientazione,
            linea_verticale=None,
            anello_orizzontale=None,
            quota_media_cm=quota_media,
            fattore_k=fattore_k,
        )

    def _determina_orientazione_orizzontale(
        self, l_a: int, l_b: int, l_m: int, l_n: int
    ) -> Orientazione:
        """Determina l'orientazione tra asse 0° (Linee 1-3) e asse 90° (Linee 2-4)."""
        linee = {l_a, l_b, l_m, l_n}
        if linee.issubset({1, 3}):
            return Orientazione.DEG_0
        if linee.issubset({2, 4}):
            return Orientazione.DEG_90

        # Dipoli trasversali: verifica orientazione dipolo corrente (A, B) o potenziale (M, N)
        if {l_a, l_b} in ({1, 3}, {1, 2}, {3, 4}) and {l_m, l_n} in ({1, 3}, {1, 2}, {3, 4}):
            if 1 in {l_a, l_b} or 3 in {l_a, l_b}:
                return Orientazione.DEG_0
        if {l_a, l_b} in ({2, 4}, {2, 3}, {4, 1}) and {l_m, l_n} in ({2, 4}, {2, 3}, {4, 1}):
            if 2 in {l_a, l_b} or 4 in {l_a, l_b}:
                return Orientazione.DEG_90

        return Orientazione.NON_APPLICABILE

    def classifica_lista(
        self,
        quaterne: Sequence[Tuple[int, int, int, int]],
        fattori_k: Optional[Sequence[Optional[float]]] = None,
    ) -> List[Quadripolo]:
        """Classifica una sequenza di quaterne (A, B, M, N)."""
        risultati = []
        for i, (a, b, m, n) in enumerate(quaterne):
            k = fattori_k[i] if fattori_k is not None and i < len(fattori_k) else None
            risultati.append(self.classifica(a, b, m, n, fattore_k=k))
        return risultati

    def trova_coppie_reciproche(self, quadripoli: Sequence[Quadripolo]) -> List[CoppiaQuadripoli]:
        """Identifica tutte le coppie diretto-reciproco presenti nella lista di quadripoli."""
        mappa_reciproci: Dict[Tuple[int, int, int, int], Quadripolo] = {
            q.tupla_elettrodi: q for q in quadripoli
        }
        coppie: List[CoppiaQuadripoli] = []
        processati: Set[Tuple[Tuple[int, int], Tuple[int, int]]] = set()

        for q in quadripoli:
            tupla_rec = (q.m, q.n, q.a, q.b)
            chiave = q.chiave_canonica_reciproca()
            if chiave in processati:
                continue

            if tupla_rec in mappa_reciproci:
                q_rec = mappa_reciproci[tupla_rec]
                desc = f"Diretto {q.tupla_elettrodi} <-> Reciproco {q_rec.tupla_elettrodi}"
                coppie.append(
                    CoppiaQuadripoli(
                        tipo_coppia=TipoCoppiaQuadripoli.DIRETTO_RECIPROCO,
                        quadripolo_1=q,
                        quadripolo_2=q_rec,
                        descrizione=desc,
                    )
                )
                processati.add(chiave)

        return coppie
