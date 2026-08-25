from pathlib import Path

from src.hydro.estensione_suzione import estendi_serie_suzione_hyprop
from src.io.hyprop import ParserHypropExcel


def main() -> None:
    base_hyprop = Path("projects/Hyprop_geotom_01Carl/data/raw/Measurement/Hyprop")
    parser = ParserHypropExcel()

    header = f"{'Campione':<8} | {'File Excel':<38} | {'Righe':<6} | {'Theta_s':<8} | {'Stato'}"
    print(header)
    print("-" * 75)

    for d in sorted(base_hyprop.iterdir()):
        if not d.is_dir():
            continue
        xlsx_files = list(d.glob("*.xlsx"))
        if not xlsx_files:
            print(f"{d.name:<8} | {'-- NESSUN FILE --':<38} | {'--':<6} | {'--':<8} | VUOTO")
            continue
        f = xlsx_files[0]
        try:
            dati = parser.leggi_file(f, id_campione=d.name)
            df_ext = estendi_serie_suzione_hyprop(dati)
            th_s = f"{dati.contenuto_acqua_saturo_vol_pct:.2f}%"
            msg = f"OK ({len(df_ext)} pti)"
            print(f"{d.name:<8} | {f.name:<38} | {len(dati.serie_misure):<6} | {th_s:<8} | {msg}")
        except Exception as e:
            print(f"{d.name:<8} | {f.name:<38} | ERRORE: {e}")


if __name__ == "__main__":
    main()
