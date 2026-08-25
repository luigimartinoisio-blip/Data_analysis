"""Test unitari per il parser dei file di sequenza GeoTom (.flw)."""

from pathlib import Path

import pytest

from src.io.geotom import (
    ParserSequenzaGeoTom,
    ottieni_file_sequenza_campione,
)

CARTELLA_SEQUENZE = Path("projects/Hyprop_geotom_01Carl/data/raw/Sequenze")


@pytest.fixture
def parser():
    return ParserSequenzaGeoTom()


def test_parsing_lastseq_file(parser):
    file_path = CARTELLA_SEQUENZE / "LastSeq_file.flw"
    assert file_path.exists()

    seq = parser.leggi_flw(file_path)
    assert seq.numero_punti_dichiarato == 289
    assert len(seq.quadripoli) == 289
    assert len(seq.dataframe) == 289

    # Verifica copertura di tutti i 12 gruppi rappresentativi (qp1..qp8 + W1..W4)
    df_rap = seq.dataframe[seq.dataframe["e_rappresentativo"]]
    assert df_rap["gruppo_rappresentativo"].nunique() == 12


def test_parsing_seq_may2026(parser):
    file_path = CARTELLA_SEQUENZE / "SEQ_May2026.flw"
    assert file_path.exists()

    seq = parser.leggi_flw(file_path)
    assert seq.numero_punti_dichiarato == 312
    assert len(seq.quadripoli) == 312
    assert len(seq.dataframe) == 312

    # Verifica copertura dei 12 gruppi rappresentativi
    df_rap = seq.dataframe[seq.dataframe["e_rappresentativo"]]
    assert df_rap["gruppo_rappresentativo"].nunique() == 12


def test_parsing_seq_june2026(parser):
    file_path = CARTELLA_SEQUENZE / "SEQ_June2026.flw"
    assert file_path.exists()

    seq = parser.leggi_flw(file_path)
    assert seq.numero_punti_dichiarato == 180
    assert len(seq.quadripoli) == 180
    assert len(seq.dataframe) == 180

    # In SEQ_June2026 (180 misure per Sand_R), verifichiamo la copertura dei gruppi
    df_rap = seq.dataframe[seq.dataframe["e_rappresentativo"]]
    assert df_rap["gruppo_rappresentativo"].nunique() == 12


def test_mappatura_campioni():
    # Campioni frana superficie e 50 cm
    assert ottieni_file_sequenza_campione("1a").name == "LastSeq_file.flw"
    assert ottieni_file_sequenza_campione("1b").name == "LastSeq_file.flw"
    assert ottieni_file_sequenza_campione("4b").name == "LastSeq_file.flw"

    # Campioni maggio
    assert ottieni_file_sequenza_campione("5a").name == "SEQ_May2026.flw"
    assert ottieni_file_sequenza_campione("6a").name == "SEQ_May2026.flw"

    # Outgroup sabbia Archie
    assert ottieni_file_sequenza_campione("Sand_R").name == "SEQ_June2026.flw"
