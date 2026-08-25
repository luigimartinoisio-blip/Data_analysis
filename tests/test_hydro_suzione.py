"""Test unitari per il modulo hydro: cavitazione ed estensione suzione HYPROP."""

from pathlib import Path

import pytest

from src.hydro.cavitazione import individua_eventi_tensiometri
from src.hydro.estensione_suzione import (
    RegimeValiditaSuzione,
    estendi_serie_suzione_hyprop,
)
from src.io.hyprop import ParserHypropExcel

PERCORSO_ML3_EXCEL = Path("projects/Hyprop_geotom_01Carl/data/raw/Measurement/Hyprop/ML3/ML3.xlsx")


def test_individua_eventi_tensiometri_ml3():
    parser = ParserHypropExcel()
    dati = parser.leggi_file(PERCORSO_ML3_EXCEL, id_campione="ML3")

    eventi = individua_eventi_tensiometri(
        dati.serie_misure,
        t_aep_top=dati.air_entry_point_top,
        t_aep_bottom=dati.air_entry_point_bottom,
    )

    # In ML3 il tensiometro Top cavita a riga 369 (circa 1999.45 hPa)
    assert eventi.top.idx_cavitazione == 369
    assert pytest.approx(eventi.top.valore_cavitazione_hpa, 1e-1) == 1999.45
    assert eventi.top.t_air_entry_point == dati.air_entry_point_top

    # Il tensiometro Bottom cavita a riga 681 (circa 2723.51 hPa)
    assert eventi.bottom.idx_cavitazione == 681
    assert pytest.approx(eventi.bottom.valore_cavitazione_hpa, 1e-1) == 2723.51
    assert eventi.bottom.t_air_entry_point == dati.air_entry_point_bottom


def test_estensione_hyprop_ml3():
    parser = ParserHypropExcel()
    dati = parser.leggi_file(PERCORSO_ML3_EXCEL, id_campione="ML3")

    df_esteso = estendi_serie_suzione_hyprop(dati)

    assert len(df_esteso) == len(dati.serie_misure)
    assert "tension_top_estesa_hpa" in df_esteso.columns
    assert "tension_bottom_estesa_hpa" in df_esteso.columns
    assert "psi_media_geometrica_hpa" in df_esteso.columns
    assert "regime_validita" in df_esteso.columns

    # Verifica punto terminale estensione Top ad AEP (deve raggiungere 8800 hPa)
    riga_aep_top = df_esteso[df_esteso["Date / Time"] == dati.air_entry_point_top]
    assert len(riga_aep_top) == 1
    assert pytest.approx(riga_aep_top["tension_top_estesa_hpa"].iloc[0], 1e-1) == 8800.0

    # Verifica regimi di validità
    regimi = df_esteso["regime_validita"].unique().tolist()
    assert RegimeValiditaSuzione.DIRETTO_ENTRAMBI.value in regimi
    assert RegimeValiditaSuzione.ESTESO_TOP_DIRETTO_BOT.value in regimi
    assert RegimeValiditaSuzione.POST_AIR_ENTRY_TOP.value in regimi

    # Verifica che oltre AEP top la suzione media sia impostata a NaN (fuori validità)
    riga_post = df_esteso[
        df_esteso["regime_validita"] == RegimeValiditaSuzione.POST_AIR_ENTRY_TOP.value
    ]
    assert riga_post["psi_media_geometrica_hpa"].isna().all()
