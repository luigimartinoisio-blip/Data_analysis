"""Test unitari per il modulo geometria dell'array cilindrico."""

import pytest

from src.core.geometria import ArrayCilindrico16


def test_inizializzazione_array_16_elettrodi():
    array = ArrayCilindrico16()
    assert len(array.elettrodi) == 16

    # Test quote z con la correzione: 4.0, 3.0, 2.0, 1.0 cm
    assert array.quote_z_cm[1] == 4.0
    assert array.quote_z_cm[2] == 3.0
    assert array.quote_z_cm[3] == 2.0
    assert array.quote_z_cm[4] == 1.0


def test_linee_verticali():
    array = ArrayCilindrico16()
    # Linea 1 (0°): elettrodi 1, 2, 3, 4
    l1 = array.ottieni_linea(1)
    assert l1 == (1, 2, 3, 4)
    for eid in l1:
        el = array.ottieni_elettrodo(eid)
        assert el.linea == 1
        assert el.angolo_deg == 0.0

    # Linea 2 (90°): 5, 6, 7, 8
    assert array.ottieni_linea(2) == (5, 6, 7, 8)
    # Linea 3 (180°): 9, 10, 11, 12
    assert array.ottieni_linea(3) == (9, 10, 11, 12)
    # Linea 4 (270°): 13, 14, 15, 16
    assert array.ottieni_linea(4) == (13, 14, 15, 16)


def test_anelli_orizzontali():
    array = ArrayCilindrico16()
    # Anello 1 (z=4.0 cm): 1, 5, 9, 13
    assert array.ottieni_anello(1) == (1, 5, 9, 13)
    # Anello 2 (z=3.0 cm): 2, 6, 10, 14
    assert array.ottieni_anello(2) == (2, 6, 10, 14)
    # Anello 3 (z=2.0 cm): 3, 7, 11, 15
    assert array.ottieni_anello(3) == (3, 7, 11, 15)
    # Anello 4 (z=1.0 cm): 4, 8, 12, 16
    assert array.ottieni_anello(4) == (4, 8, 12, 16)


def test_distanza_3d():
    array = ArrayCilindrico16(raggio_cilindro_cm=4.0)
    # Distanza verticale tra elettrodo 1 (z=4) e 2 (z=3) sulla stessa linea (dx=0, dy=0, dz=1)
    d_vert = array.distanza_3d(1, 2)
    assert pytest.approx(d_vert, 1e-5) == 1.0

    # Distanza diametrale tra elettrodo 1 (0°, z=4) e 9 (180°, z=4) (diametro = 2*4.0 = 8.0 cm)
    d_diam = array.distanza_3d(1, 9)
    assert pytest.approx(d_diam, 1e-5) == 8.0
