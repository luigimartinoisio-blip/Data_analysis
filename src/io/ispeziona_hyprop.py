"""Script di ispezione dettagliata dei fogli Excel HYPROP."""

import sys
from pathlib import Path

import pandas as pd


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    excel_path = Path("projects/Hyprop_geotom_01Carl/data/raw/Measurement/Hyprop/ML3/ML3.xlsx")

    print("=== METADATI FOGLIO Information ===")
    df_info = pd.read_excel(excel_path, sheet_name="Information")
    for _, row in df_info.dropna(subset=["Parameter Name"]).iterrows():
        pname = str(row["Parameter Name"]).strip()
        val = row["Value"]
        print(f"{pname:<35} : {val}")

    print("\n=== FOGLIO Measurements (Prime e ultime 3 righe) ===")
    df_meas = pd.read_excel(excel_path, sheet_name="Measurements")
    print(df_meas.head(3))
    print("...")
    print(df_meas.tail(3))
    print("Righe totali:", len(df_meas))

    print("\n=== PARAMETRI DI FITTING (van Genuchten / Mualem) ===")
    df_fit = pd.read_excel(excel_path, sheet_name="Fitting-Parameter value")
    print(df_fit)


if __name__ == "__main__":
    main()
