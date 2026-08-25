"""Modello geometrico 3D per l'array di elettrodi nel cilindro Hyprop."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass(frozen=True)
class Elettrodo:
    """Rappresentazione geometrica di un singolo elettrodo nel cilindro.

    Attributi:
        id_elettrodo: Identificativo numerico univoco (1 - 16).
        linea: Numero della linea verticale (1, 2, 3 o 4).
        anello: Indice del livello/anello da cima a fondo (1 = top, 4 = bottom).
        angolo_deg: Posizione angolare in gradi rispetto all'asse di riferimento
            (0°, 90°, 180°, 270°).
        raggio_cm: Distanza radiale dall'asse centrale del cilindro in cm.
        quota_z_cm: Quota verticale rispetto alla base del cilindro (z=0 cm) in cm.
        x_cm: Coordinata cartesiana X in cm.
        y_cm: Coordinata cartesiana Y in cm.
    """

    id_elettrodo: int
    linea: int
    anello: int
    angolo_deg: float
    raggio_cm: float
    quota_z_cm: float
    x_cm: float
    y_cm: float


class ArrayCilindrico16:
    """Gestione della geometria dell'array a 16 micro-elettrodi (4 linee x 4 quote).

    Convenzioni:
    - Linea 1: theta = 0°, elettrodi [1, 2, 3, 4]
    - Linea 2: theta = 90°, elettrodi [5, 6, 7, 8]
    - Linea 3: theta = 180°, elettrodi [9, 10, 11, 12]
    - Linea 4: theta = 270°, elettrodi [13, 14, 15, 16]
    - Quote z: anello 1 = 4.0 cm, anello 2 = 3.0 cm, anello 3 = 2.0 cm, anello 4 = 1.0 cm.
    """

    # Quote verticali standard in cm (rispetto a z=0 cm alla base)
    QUOTE_Z_STANDARD_CM: Dict[int, float] = {
        1: 4.0,  # Anello 1 (Superiore)
        2: 3.0,  # Anello 2 (Medio-superiore)
        3: 2.0,  # Anello 3 (Medio-inferiore)
        4: 1.0,  # Anello 4 (Inferiore)
    }

    # Angoli per le 4 direttrici verticali
    ANGOLI_LINEE_DEG: Dict[int, float] = {
        1: 0.0,
        2: 90.0,
        3: 180.0,
        4: 270.0,
    }

    def __init__(
        self,
        raggio_cilindro_cm: float = 4.0,
        altezza_cilindro_cm: float = 5.0,
        quote_z_cm: Dict[int, float] | None = None,
    ) -> None:
        """Inizializza l'array geometrico a 16 elettrodi.

        Parametri:
            raggio_cilindro_cm: Raggio interno del cilindro in cm (default 4.0 cm per
                cilindro Hyprop standard 250 cm³).
            altezza_cilindro_cm: Altezza totale del cilindro in cm (default 5.0 cm).
            quote_z_cm: Dizionario personalizzato delle quote z per anello (opzionale).
        """
        self.raggio_cilindro_cm = raggio_cilindro_cm
        self.altezza_cilindro_cm = altezza_cilindro_cm
        self.quote_z_cm = quote_z_cm if quote_z_cm is not None else self.QUOTE_Z_STANDARD_CM

        self._elettrodi: Dict[int, Elettrodo] = {}
        self._costruisci_array()

    def _costruisci_array(self) -> None:
        """Genera le istanze degli elettrodi con le loro coordinate 3D."""
        id_attuale = 1
        for linea_idx in range(1, 5):
            angolo_deg = self.ANGOLI_LINEE_DEG[linea_idx]
            angolo_rad = math.radians(angolo_deg)
            x = self.raggio_cilindro_cm * math.cos(angolo_rad)
            y = self.raggio_cilindro_cm * math.sin(angolo_rad)

            for anello_idx in range(1, 5):
                z = self.quote_z_cm[anello_idx]
                self._elettrodi[id_attuale] = Elettrodo(
                    id_elettrodo=id_attuale,
                    linea=linea_idx,
                    anello=anello_idx,
                    angolo_deg=angolo_deg,
                    raggio_cm=self.raggio_cilindro_cm,
                    quota_z_cm=z,
                    x_cm=round(x, 6),
                    y_cm=round(y, 6),
                )
                id_attuale += 1

    def ottieni_elettrodo(self, id_elettrodo: int) -> Elettrodo:
        """Restituisce l'elettrodo corrispondente all'ID specificato (1-16)."""
        if id_elettrodo not in self._elettrodi:
            raise KeyError(
                f"Elettrodo ID {id_elettrodo} non valido. Deve essere compreso tra 1 e 16."
            )
        return self._elettrodi[id_elettrodo]

    @property
    def elettrodi(self) -> Dict[int, Elettrodo]:
        """Dizionario di tutti i 16 elettrodi indicizzati per ID."""
        return self._elettrodi

    def ottieni_tutti_elettrodi(self) -> List[Elettrodo]:
        """Restituisce la lista ordinata di tutti i 16 elettrodi."""
        return list(self._elettrodi.values())

    def distanza_3d(self, id_e1: int, id_e2: int) -> float:
        """Calcola la distanza euclidea 3D in cm tra due elettrodi."""
        e1 = self.ottieni_elettrodo(id_e1)
        e2 = self.ottieni_elettrodo(id_e2)
        dx = e1.x_cm - e2.x_cm
        dy = e1.y_cm - e2.y_cm
        dz = e1.quota_z_cm - e2.quota_z_cm
        return math.sqrt(dx**2 + dy**2 + dz**2)

    def ottieni_anello(self, indice_anello: int) -> Tuple[int, ...]:
        """Restituisce gli ID degli elettrodi appartenenti a uno specifico anello (1-4)."""
        if indice_anello not in (1, 2, 3, 4):
            raise ValueError(
                f"Indice anello non valido: {indice_anello}. Scegliere tra 1, 2, 3, 4."
            )
        return tuple(e.id_elettrodo for e in self._elettrodi.values() if e.anello == indice_anello)

    def ottieni_linea(self, indice_linea: int) -> Tuple[int, ...]:
        """Restituisce gli ID degli elettrodi appartenenti a una specifica linea verticale (1-4)."""
        if indice_linea not in (1, 2, 3, 4):
            raise ValueError(f"Indice linea non valido: {indice_linea}. Scegliere tra 1, 2, 3, 4.")
        return tuple(e.id_elettrodo for e in self._elettrodi.values() if e.linea == indice_linea)
