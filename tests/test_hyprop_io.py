"""Test unitari per il parser I/O dei file Excel HYPROP2."""

from pathlib import Path

import pytest

from src.io.hyprop import ParserHypropExcel

PERCORSO_ML3_EXCEL = Path("projects/Hyprop_geotom_01Carl/data/raw/Measurement/Hyprop/ML3/ML3.xlsx")


def test_parsing_hyprop_ml3():
    assert PERCORSO_ML3_EXCEL.exists()

    parser = ParserHypropExcel()
    dati = parser.leggi_file(PERCORSO_ML3_EXCEL, id_campione="ML3")

    # Verifica ID e metadati
    assert dati.id_campione == "ML3"
    assert dati.peso_secco_g == 348.5
    assert dati.volume_campione_cm3 == 251.0
    assert dati.densita_secca_g_cm3 == 1.39
    assert dati.porosita == 0.48
    assert pytest.approx(dati.contenuto_acqua_saturo_vol_pct, 1e-2) == 46.47

    # Verifica serie misure ad alta frequenza
    assert len(dati.serie_misure) == 896
    assert "Tension Bottom [hPa]" in dati.serie_misure.columns
    assert "Tension Top [hPa]" in dati.serie_misure.columns
    assert "Temperature [°C]" in dati.serie_misure.columns
    assert "Weight change [g]" in dati.serie_misure.columns

    # Verifica curve e parametri van Genuchten
    assert len(dati.curva_ritenzione_esperimento) == 100
    assert len(dati.curva_ritenzione_fittata) == 500
    assert pytest.approx(dati.parametri_fitting.alpha_1_per_cm, 1e-4) == 0.0371
    assert pytest.approx(dati.parametri_fitting.n, 1e-3) == 1.111
    assert pytest.approx(dati.parametri_fitting.k_sat_cm_per_d, 1e-2) == 1.40
