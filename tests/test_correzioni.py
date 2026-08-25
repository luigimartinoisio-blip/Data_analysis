"""Test unitari per il modulo correzioni fisiche e filtri di qualità."""

import numpy as np
import pandas as pd
import pytest

from src.core.correzioni import (
    applica_filtri_qualita,
    calcola_errore_reciproco,
    calcola_indice_ar,
    calcola_resistenza,
    calcola_resistivita_apparente,
    correggi_temperatura_hayashi,
)


def test_correzione_temperatura_hayashi():
    # Se Tm = 25°C, rho_25 deve essere esattamente uguale a rho_m
    assert correggi_temperatura_hayashi(100.0, 25.0) == 100.0

    # Se Tm = 20°C: rho_25 = 100 * [1 - 0.02 * (25 - 20)] = 100 * (1 - 0.10) = 90.0 Ohm*m
    assert pytest.approx(correggi_temperatura_hayashi(100.0, 20.0), 1e-5) == 90.0

    # Se Tm = 30°C: rho_25 = 100 * [1 - 0.02 * (25 - 30)] = 100 * (1 + 0.10) = 110.0 Ohm*m
    assert pytest.approx(correggi_temperatura_hayashi(100.0, 30.0), 1e-5) == 110.0

    # Test con array numpy
    rho_arr = np.array([100.0, 200.0])
    tm_arr = np.array([20.0, 25.0])
    res = correggi_temperatura_hayashi(rho_arr, tm_arr)
    assert np.allclose(res, [90.0, 200.0])


def test_calcolo_errore_reciproco():
    # Misura perfettamente reciproca
    assert calcola_errore_reciproco(50.0, 50.0) == 0.0

    # r_dir = 100, r_rec = 104 -> diff = 4, mean = 102 -> (4 / 102) * 100 = 3.9215%
    err = calcola_errore_reciproco(100.0, 104.0)
    assert pytest.approx(err, 1e-3) == 3.9215

    # Con Series pandas
    s_dir = pd.Series([100.0, 200.0])
    s_rec = pd.Series([100.0, 210.0])
    err_s = calcola_errore_reciproco(s_dir, s_rec)
    assert pytest.approx(err_s[0], 1e-5) == 0.0
    assert pytest.approx(err_s[1], 1e-3) == 4.878


def test_calcolo_resistenza_e_resistivita():
    # V = 10 mV, I = 2 mA -> R = 5 Ohm
    assert calcola_resistenza(10.0, 2.0) == 5.0

    # R = 5 Ohm, K = 0.5 m -> rho = 2.5 Ohm*m
    assert calcola_resistivita_apparente(5.0, 0.5) == 2.5


def test_filtri_qualita():
    df = pd.DataFrame(
        {
            "v_mv": [2.5, 0.5, 3.0, 1.2],  # riga 1 bocciata per V < 1.0 mV
            "errore_rec_pct": [1.5, 2.0, 7.5, 4.0],  # riga 2 bocciata per err > 5%
        }
    )

    df_filtrato = applica_filtri_qualita(df, soglia_min_v_mv=1.0, soglia_max_errore_rec_pct=5.0)
    # Dovrebbero rimanere solo riga 0 (2.5 mV, 1.5%) e riga 3 (1.2 mV, 4.0%)
    assert len(df_filtrato) == 2
    assert list(df_filtrato.index) == [0, 3]


def test_calcolo_indice_ar():
    # Isotropia: rho_90 == rho_0 -> AR = 1.0
    assert calcola_indice_ar(100.0, 100.0) == 1.0

    # rho_90 = 150.0, rho_0 = 100.0 -> AR = 1.5
    assert calcola_indice_ar(150.0, 100.0) == 1.5

    # Con Series pandas
    s_90 = pd.Series([100.0, 200.0])
    s_0 = pd.Series([100.0, 50.0])
    ar_s = calcola_indice_ar(s_90, s_0)
    assert ar_s[0] == 1.0
    assert ar_s[1] == 4.0
