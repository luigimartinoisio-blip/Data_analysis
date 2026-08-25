"""Test unitari per i 20 quadripoli rappresentativi e il calcolo dell'Anisotropy Ratio (AR)."""

import pytest

from src.core.geometria import ArrayCilindrico16
from src.core.quadripoli import Orientazione
from src.core.schemi_rappresentativi import (
    CategoriaRappresentativa,
    Schema20QuadripoliRappresentativi,
)


@pytest.fixture
def schema():
    return Schema20QuadripoliRappresentativi(ArrayCilindrico16())


def test_conteggio_totale_quadripoli(schema):
    # Devono esserci esattamente 8 coppie QP (16 quadripoli) + 4 Wenner = 20 quadripoli
    tutti = schema.tutti_i_quadripoli()
    assert len(tutti) == 20
    assert len(schema.coppie_qp) == 8
    assert len(schema.wenner) == 4


def test_quadripoli_upper_horizontal(schema):
    # 6 quadripoli: qp1_0°, qp2_0°, qp3_90°
    qp1 = schema.coppie_qp["qp1_0"]
    assert qp1.tupla_dir == (1, 5, 13, 9)
    assert qp1.tupla_rec == (13, 9, 1, 5)
    assert qp1.orientazione == Orientazione.DEG_0
    assert qp1.categoria == CategoriaRappresentativa.HORIZONTAL_UPPER

    qp2 = schema.coppie_qp["qp2_0"]
    assert qp2.tupla_dir == (2, 6, 14, 10)
    assert qp2.tupla_rec == (14, 10, 2, 6)
    assert qp2.orientazione == Orientazione.DEG_0

    qp3 = schema.coppie_qp["qp3_90"]
    assert qp3.tupla_dir == (6, 10, 2, 14)
    assert qp3.tupla_rec == (2, 14, 6, 10)
    assert qp3.orientazione == Orientazione.DEG_90


def test_quadripoli_lower_horizontal(schema):
    # 6 quadripoli: qp4_0°, qp5_0°, qp6_90°
    qp4 = schema.coppie_qp["qp4_0"]
    assert qp4.tupla_dir == (3, 7, 15, 11)
    assert qp4.tupla_rec == (15, 11, 3, 7)
    assert qp4.orientazione == Orientazione.DEG_0
    assert qp4.categoria == CategoriaRappresentativa.HORIZONTAL_LOWER

    qp5 = schema.coppie_qp["qp5_0"]
    assert qp5.tupla_dir == (4, 8, 16, 12)
    assert qp5.tupla_rec == (16, 12, 4, 8)
    assert qp5.orientazione == Orientazione.DEG_0

    qp6 = schema.coppie_qp["qp6_90"]
    assert qp6.tupla_dir == (7, 11, 3, 15)
    assert qp6.tupla_rec == (3, 15, 7, 11)
    assert qp6.orientazione == Orientazione.DEG_90


def test_quadripoli_dipole_dipole(schema):
    # 4 quadripoli: qp7_0°, qp8_90°
    qp7 = schema.coppie_qp["qp7_0"]
    assert qp7.tupla_dir == (1, 2, 3, 4)
    assert qp7.tupla_rec == (3, 4, 1, 2)
    assert qp7.orientazione == Orientazione.DEG_0
    assert qp7.categoria == CategoriaRappresentativa.VERTICAL_DIPOLE_DIPOLE

    qp8 = schema.coppie_qp["qp8_90"]
    assert qp8.tupla_dir == (5, 6, 7, 8)
    assert qp8.tupla_rec == (7, 8, 5, 6)
    assert qp8.orientazione == Orientazione.DEG_90


def test_quadripoli_wenner(schema):
    # 4 quadripoli: W1_0°, W2_90°, W3_0°, W4_90°
    w1 = schema.wenner["W1_0"]
    assert w1.tupla_elettrodi == (1, 4, 2, 3)
    assert w1.orientazione == Orientazione.DEG_0
    assert w1.linea_verticale == 1

    w2 = schema.wenner["W2_90"]
    assert w2.tupla_elettrodi == (5, 8, 6, 7)
    assert w2.orientazione == Orientazione.DEG_90
    assert w2.linea_verticale == 2

    w3 = schema.wenner["W3_0"]
    assert w3.tupla_elettrodi == (9, 12, 10, 11)
    assert w3.orientazione == Orientazione.DEG_0
    assert w3.linea_verticale == 3

    w4 = schema.wenner["W4_90"]
    assert w4.tupla_elettrodi == (13, 16, 14, 15)
    assert w4.orientazione == Orientazione.DEG_90
    assert w4.linea_verticale == 4


def test_calcolo_ar_su_schemi_rappresentativi(schema):
    # Simulazione resistività per Upper Horizontal
    # qp1_0 = 100, qp2_0 = 100 -> media(0°) = 100
    # qp3_90 = 250 -> media(90°) = 250
    # AR_upper = 250 / 100 = 2.5
    mappa = {
        "qp1_0": 100.0,
        "qp2_0": 100.0,
        "qp3_90": 250.0,
    }
    ar_upper = schema.calcola_ar_categoria(CategoriaRappresentativa.HORIZONTAL_UPPER, mappa)
    assert pytest.approx(ar_upper, 1e-5) == 2.5

    # Simulazione resistività per Wenner
    # W1_0 = 80, W3_0 = 120 -> media(0°) = 100
    # W2_90 = 150, W4_90 = 150 -> media(90°) = 150
    # AR_wenner = 150 / 100 = 1.5
    mappa_wenner = {
        "W1_0": 80.0,
        "W2_90": 150.0,
        "W3_0": 120.0,
        "W4_90": 150.0,
    }
    ar_w = schema.calcola_ar_categoria(CategoriaRappresentativa.VERTICAL_WENNER, mappa_wenner)
    assert pytest.approx(ar_w, 1e-5) == 1.5
