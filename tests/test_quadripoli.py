"""Test unitari per la categorizzazione dei quadripoli e Quadrupole Pairs."""

import pytest

from src.core.geometria import ArrayCilindrico16
from src.core.quadripoli import (
    CategoriaQuadripolo,
    ClassificatoreQuadripoli,
    TipoCoppiaQuadripoli,
)


@pytest.fixture
def classificatore():
    return ClassificatoreQuadripoli(ArrayCilindrico16())


def test_classificazione_verticale_wenner(classificatore):
    # Su Linea 1 (elettrodi 1, 2, 3, 4): Wenner A=1, M=2, N=3, B=4
    q = classificatore.classifica(1, 4, 2, 3)
    assert q.categoria == CategoriaQuadripolo.VERTICALE_WENNER
    assert q.linea_verticale == 1


def test_classificazione_verticale_dipolo_dipolo(classificatore):
    # Su Linea 2 (elettrodi 5, 6, 7, 8): Dipolo-Dipolo A=5, B=6, M=7, N=8
    q = classificatore.classifica(5, 6, 7, 8)
    assert q.categoria == CategoriaQuadripolo.VERTICALE_DIPOLO_DIPOLO
    assert q.linea_verticale == 2


def test_classificazione_orizzontale_upper_lower(classificatore):
    # Anello 1 (z=4 cm): elettrodi 1, 5, 9, 13 -> Upper
    q_upper = classificatore.classifica(1, 5, 9, 13)
    assert q_upper.categoria == CategoriaQuadripolo.ORIZZONTALE_UPPER
    assert q_upper.anello_orizzontale == 1

    # Anello 4 (z=1 cm): elettrodi 4, 8, 12, 16 -> Lower
    q_lower = classificatore.classifica(4, 8, 12, 16)
    assert q_lower.categoria == CategoriaQuadripolo.ORIZZONTALE_LOWER
    assert q_lower.anello_orizzontale == 4


def test_coppie_reciproche(classificatore):
    # Creiamo due quadripoli reciproci: (1, 4, 2, 3) e (2, 3, 1, 4)
    q_dir = classificatore.classifica(1, 4, 2, 3)
    q_rec = classificatore.classifica(2, 3, 1, 4)

    lista = [q_dir, q_rec]
    coppie = classificatore.trova_coppie_reciproche(lista)

    assert len(coppie) == 1
    cp = coppie[0]
    assert cp.tipo_coppia == TipoCoppiaQuadripoli.DIRETTO_RECIPROCO

    # Test calcolo errore reciproco tra due misure simulate
    # R_dir = 100.0 Ohm, R_rec = 102.0 Ohm -> Errore: 2 / 101 * 100 = 1.98%
    err = cp.calcola_errore_percentuale(100.0, 102.0)
    assert pytest.approx(err, 1e-2) == 1.98


def test_coppia_anisotropia(classificatore):
    q_0 = classificatore.classifica(1, 9, 2, 10)
    q_90 = classificatore.classifica(5, 13, 6, 14)

    from src.core.quadripoli import CoppiaQuadripoli

    cp = CoppiaQuadripoli(
        tipo_coppia=TipoCoppiaQuadripoli.ANISOTROPIA_0_90,
        quadripolo_1=q_0,
        quadripolo_2=q_90,
    )
    # rho_0 = 100 Ohm*m, rho_90 = 400 Ohm*m -> AR = 400 / 100 = 4.0
    ar = cp.calcola_rapporto_anisotropia(100.0, 400.0)
    assert ar == 4.0
