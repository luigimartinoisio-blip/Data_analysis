"""Script di esecuzione per il riallineamento dei nomi dei file GeoTom."""

from pathlib import Path

from src.io.riallinea_timesteps import esegui_riallineamento_nomi


def main() -> None:
    base_dir = Path("projects/Hyprop_geotom_01Carl/data/raw/Measurement")
    target_dirs = ["TL_ERT_5a", "TL_ERT_6a", "TL_ERT_Sand_R"]

    for tdir in target_dirs:
        p = base_dir / tdir
        print(f"=== Esecuzione riallineamento per {tdir} ===")
        logs = esegui_riallineamento_nomi(p)
        print(f"Rinominati {len(logs)} file.")
        if logs:
            print(f"Primo: {logs[0]}")
            print(f"Ultimo: {logs[-1]}")
        print()


if __name__ == "__main__":
    main()
