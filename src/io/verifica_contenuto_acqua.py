"""Script di verifica del calcolo del contenuto d'acqua per tutti i campioni."""

from pathlib import Path

from src.io.hyprop import ParserHypropExcel


def main() -> None:
    base_hyprop = Path("projects/Hyprop_geotom_01Carl/data/raw/Measurement/Hyprop")
    parser = ParserHypropExcel()

    header = f"{'ID':<6} | {'m_dry (g)':<9} | {'Vol (cm3)':<9} | {'m_net_0':<9} | {'theta_calc'}"
    print(header)
    print("-" * 60)

    for d in sorted(base_hyprop.iterdir()):
        if not d.is_dir():
            continue
        xlsx = list(d.glob("*.xlsx"))
        if not xlsx:
            continue
        dati = parser.leggi_file(xlsx[0], id_campione=d.name)
        m_net_0 = dati.serie_misure["Net weight [g]"].dropna().iloc[0]
        theta_calc = ((m_net_0 - dati.peso_secco_g) / dati.volume_campione_cm3) * 100.0
        theta_decl = dati.contenuto_acqua_saturo_vol_pct
        th_str = f"{theta_calc:.2f}% (dich: {theta_decl:.2f}%)"
        v_dry = f"{dati.peso_secco_g:<9.1f}"
        v_vol = f"{dati.volume_campione_cm3:<9.1f}"
        v_m0 = f"{m_net_0:<9.2f}"
        print(f"{d.name:<6} | {v_dry} | {v_vol} | {v_m0} | {th_str}")


if __name__ == "__main__":
    main()
