"""Modulo Core per geometria, quadripoli, fattori geometrici e correzioni fisiche."""

from src.core.correzioni import (
    applica_filtri_qualita,
    calcola_errore_reciproco,
    calcola_indice_ar,
    calcola_resistenza,
    calcola_resistivita_apparente,
    correggi_temperatura_hayashi,
)
from src.core.fattori_geometrici import (
    FATTORE_K_ANELLO_1_Z4,
    FATTORE_K_ANELLO_2_Z3,
    FATTORE_K_ANELLO_3_Z2,
    FATTORE_K_ANELLO_4_Z1,
    FATTORE_K_DIPOLO_DIPOLO,
    FATTORE_K_WENNER,
    MAPPA_FATTORI_K_ANELLI,
    MAPPA_FATTORI_K_GRUPPI_RAPPRESENTATIVI,
    ottieni_fattore_k_calibrato,
    ricalcola_resistivita_apparente,
)
from src.core.geometria import ArrayCilindrico16, Elettrodo
from src.core.quadripoli import (
    CategoriaQuadripolo,
    ClassificatoreQuadripoli,
    CoppiaQuadripoli,
    Orientazione,
    Quadripolo,
    TipoCoppiaQuadripoli,
)
from src.core.schemi_rappresentativi import (
    CategoriaRappresentativa,
    GruppoRappresentativoQP,
    Schema20QuadripoliRappresentativi,
    SingoloRappresentativoWenner,
)

__all__ = [
    "ArrayCilindrico16",
    "CategoriaQuadripolo",
    "CategoriaRappresentativa",
    "ClassificatoreQuadripoli",
    "CoppiaQuadripoli",
    "Elettrodo",
    "FATTORE_K_ANELLO_1_Z4",
    "FATTORE_K_ANELLO_2_Z3",
    "FATTORE_K_ANELLO_3_Z2",
    "FATTORE_K_ANELLO_4_Z1",
    "FATTORE_K_DIPOLO_DIPOLO",
    "FATTORE_K_WENNER",
    "GruppoRappresentativoQP",
    "MAPPA_FATTORI_K_ANELLI",
    "MAPPA_FATTORI_K_GRUPPI_RAPPRESENTATIVI",
    "Orientazione",
    "Quadripolo",
    "Schema20QuadripoliRappresentativi",
    "SingoloRappresentativoWenner",
    "TipoCoppiaQuadripoli",
    "applica_filtri_qualita",
    "calcola_errore_reciproco",
    "calcola_indice_ar",
    "calcola_resistenza",
    "calcola_resistivita_apparente",
    "correggi_temperatura_hayashi",
    "ottieni_fattore_k_calibrato",
    "ricalcola_resistivita_apparente",
]
