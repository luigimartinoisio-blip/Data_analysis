"""Test unitari per i fattori geometrici K calibrati e il ricalcolo della resistività."""

import pytest

from src.core.fattori_geometrici import (
    FATTORE_K_ANELLO_1_Z4,
    FATTORE_K_ANELLO_2_Z3,
    FATTORE_K_ANELLO_3_Z2,
    FATTORE_K_ANELLO_4_Z1,
    FATTORE_K_DIPOLO_DIPOLO,
    FATTORE_K_WENNER,
    ricalcola_resistivita_apparente,
)
from src.core.schemi_rappresentativi import Schema20QuadripoliRappresentativi


def test_valori_fattori_k_calibrati():
    # Verifica valori esatti di calibrazione
    assert pytest.approx(FATTORE_K_ANELLO_1_Z4, 1e-6) == 0.187194
    assert pytest.approx(FATTORE_K_ANELLO_2_Z3, 1e-6) == 0.210141452
    assert pytest.approx(FATTORE_K_ANELLO_3_Z2, 1e-6) == 0.210141452
    assert pytest.approx(FATTORE_K_ANELLO_4_Z1, 1e-6) == 0.19681829
    assert pytest.approx(FATTORE_K_DIPOLO_DIPOLO, 1e-6) == 0.228686003
    assert pytest.approx(FATTORE_K_WENNER, 1e-6) == 0.05011339


def test_assegnazione_k_ai_quadripoli_rappresentativi():
    schema = Schema20QuadripoliRappresentativi()

    # qp1 (Anello 1, z=4 cm)
    qp1 = schema.coppie_qp["qp1_0"]
    assert pytest.approx(qp1.quadripolo_dir.fattore_k, 1e-6) == 0.187194
    assert pytest.approx(qp1.quadripolo_rec.fattore_k, 1e-6) == 0.187194

    # qp2, qp3 (Anello 2, z=3 cm)
    assert pytest.approx(schema.coppie_qp["qp2_0"].quadripolo_dir.fattore_k, 1e-6) == 0.210141452
    assert pytest.approx(schema.coppie_qp["qp3_90"].quadripolo_dir.fattore_k, 1e-6) == 0.210141452

    # qp4, qp6 (Anello 3, z=2 cm)
    assert pytest.approx(schema.coppie_qp["qp4_0"].quadripolo_dir.fattore_k, 1e-6) == 0.210141452
    assert pytest.approx(schema.coppie_qp["qp6_90"].quadripolo_dir.fattore_k, 1e-6) == 0.210141452

    # qp5 (Anello 4, z=1 cm)
    assert pytest.approx(schema.coppie_qp["qp5_0"].quadripolo_dir.fattore_k, 1e-6) == 0.19681829

    # Dipolo-dipolo (qp7, qp8)
    assert pytest.approx(schema.coppie_qp["qp7_0"].quadripolo_dir.fattore_k, 1e-6) == 0.228686003
    assert pytest.approx(schema.coppie_qp["qp8_90"].quadripolo_dir.fattore_k, 1e-6) == 0.228686003

    # Wenner (W1..W4)
    for w in schema.wenner.values():
        assert pytest.approx(w.quadripolo.fattore_k, 1e-6) == 0.05011339


def test_ricalcolo_resistivita():
    # Se V = 10 mV, I = 2 mA -> R = 5 Ohm. Con K = 0.210141452 m -> rho = 1.05070726 Ohm*m
    rho = ricalcola_resistivita_apparente(10.0, 2.0, 0.210141452)
    assert pytest.approx(rho, 1e-6) == 1.05070726
