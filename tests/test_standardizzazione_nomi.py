"""Test unitari per la mappatura e standardizzazione della nomenclatura campioni."""

from src.io.standardizza_nomi_file import (
    MAPPA_CAMPAGNA_A_MINERALOGICO,
    MAPPA_MINERALOGICO_A_CAMPAGNA,
)


def test_tavola_equivalenza_mineralogica():
    # Verifica equivalenze esatte
    assert MAPPA_CAMPAGNA_A_MINERALOGICO["5a"] == "ML1"
    assert MAPPA_CAMPAGNA_A_MINERALOGICO["5b"] == "ML2"
    assert MAPPA_CAMPAGNA_A_MINERALOGICO["1a"] == "ML3"
    assert MAPPA_CAMPAGNA_A_MINERALOGICO["1b"] == "ML4"
    assert MAPPA_CAMPAGNA_A_MINERALOGICO["2a"] == "ML5"
    assert MAPPA_CAMPAGNA_A_MINERALOGICO["2b"] == "ML6"
    assert MAPPA_CAMPAGNA_A_MINERALOGICO["3a"] == "ML7"
    assert MAPPA_CAMPAGNA_A_MINERALOGICO["3b"] == "ML8"
    assert MAPPA_CAMPAGNA_A_MINERALOGICO["4b"] == "ML9"
    assert MAPPA_CAMPAGNA_A_MINERALOGICO["6a"] == "ML10"
    assert MAPPA_CAMPAGNA_A_MINERALOGICO["Sand_R"] == "Sand_R"

    # Verifica inversa
    assert MAPPA_MINERALOGICO_A_CAMPAGNA["ML1"] == "5a"
    assert MAPPA_MINERALOGICO_A_CAMPAGNA["ML3"] == "1a"
    assert MAPPA_MINERALOGICO_A_CAMPAGNA["ML9"] == "4b"
    assert MAPPA_MINERALOGICO_A_CAMPAGNA["ML10"] == "6a"
