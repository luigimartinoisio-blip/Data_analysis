"""Test unitari per il modulo processing e la sincronizzazione GeoTom-HYPROP."""

from pathlib import Path

import pytest

from src.processing.sincronizzazione import ElaboratoreCampioneIntegrato

DIR_ERT_ML3 = Path("projects/Hyprop_geotom_01Carl/data/raw/Measurement/ERT/ML3")
FILE_HYPROP_ML3 = Path("projects/Hyprop_geotom_01Carl/data/raw/Measurement/Hyprop/ML3/ML3.xlsx")


def test_elaborazione_integrata_ml3():
    assert DIR_ERT_ML3.exists()
    assert FILE_HYPROP_ML3.exists()

    elaboratore = ElaboratoreCampioneIntegrato(
        id_campione="ML3",
        cartella_ert=DIR_ERT_ML3,
        file_hyprop_xlsx=FILE_HYPROP_ML3,
    )

    df = elaboratore.elabora_tutti_i_timestep()

    # Verifica dimensioni (141 file ERT per ML3)
    assert len(df) == 141

    # Verifica colonne attese
    assert "campione_id" in df.columns
    assert "time_step_id" in df.columns
    assert "datetime_baricentro_ert" in df.columns
    assert "temperatura_C" in df.columns
    assert "theta_vol_pct" in df.columns
    assert "suzione_media_kpa" in df.columns
    assert "rho25_qp1" in df.columns
    assert "eps_qp1" in df.columns
    assert "rho25_W1" in df.columns
    assert "qualita_qc_pass" in df.columns

    # Verifica valori fisici ragionevoli
    # Contenuto volumetrico d'acqua deve iniziare attorno a ~46.5% e calare nel tempo
    assert pytest.approx(df["theta_vol_pct"].iloc[0], 1e-1) == 46.5
    assert df["theta_vol_pct"].iloc[-1] < df["theta_vol_pct"].iloc[0]

    # La resistività rho25 deve aumentare all'aumentare dell'asciugamento
    assert df["rho25_qp1"].iloc[-1] > df["rho25_qp1"].iloc[0]

    # Verifica errori di reciprocità bassi (< 5%) all'inizio
    assert df["eps_qp1"].iloc[0] < 5.0
