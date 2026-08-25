"""Script per la generazione del report di qualità sui reciproci e statistiche campioni."""

from pathlib import Path

import numpy as np
import pandas as pd


def main() -> None:
    cartella_proc = Path("projects/Hyprop_geotom_01Carl/data/processed")
    tabelle_dir = cartella_proc / "tabelle_campioni"

    report_righe = []

    for f in sorted(tabelle_dir.glob("*_serie_integrata.csv")):
        df = pd.read_csv(f)
        campione = df["campione_id"].iloc[0]

        # Colonne eps
        eps_cols = [c for c in df.columns if c.startswith("eps_qp")]
        eps_values = df[eps_cols].to_numpy().flatten()
        eps_valid = eps_values[~np.isnan(eps_values)]

        n_tot_passi = len(df)
        pct_qc_pass = (
            (df["qualita_qc_pass"].sum() / n_tot_passi) * 100.0 if n_tot_passi > 0 else 0.0
        )
        eps_medio = float(np.mean(eps_valid)) if len(eps_valid) > 0 else np.nan
        eps_mediano = float(np.median(eps_valid)) if len(eps_valid) > 0 else np.nan
        pct_eps_sotto_5 = (
            (np.count_nonzero(eps_valid < 5.0) / len(eps_valid)) * 100.0
            if len(eps_valid) > 0
            else 0.0
        )

        t_min = df["temperatura_C"].min()
        t_max = df["temperatura_C"].max()
        theta_ini = (
            df["theta_vol_pct"].dropna().iloc[0]
            if not df["theta_vol_pct"].dropna().empty
            else np.nan
        )
        theta_fin = (
            df["theta_vol_pct"].dropna().iloc[-1]
            if not df["theta_vol_pct"].dropna().empty
            else np.nan
        )

        report_righe.append(
            {
                "campione_id": campione,
                "n_timestep": n_tot_passi,
                "theta_iniziale_pct": round(theta_ini, 2),
                "theta_finale_pct": round(theta_fin, 2),
                "temp_min_C": round(t_min, 1),
                "temp_max_C": round(t_max, 1),
                "eps_rec_medio_pct": round(eps_medio, 2),
                "eps_rec_mediano_pct": round(eps_mediano, 2),
                "misure_eps_sotto_5pct": round(pct_eps_sotto_5, 1),
                "timestep_qc_pass_pct": round(pct_qc_pass, 1),
            }
        )

    df_rep = pd.DataFrame(report_righe)
    out_rep_csv = cartella_proc / "report_qualita_reciproci.csv"
    df_rep.to_csv(out_rep_csv, index=False)
    print(df_rep.to_string(index=False))


if __name__ == "__main__":
    main()
