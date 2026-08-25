"""Script di riepilogo audit per tutti i campioni."""

from pathlib import Path

from src.io.riallinea_timesteps import analizza_directory_campione


def main() -> None:
    base_dir = Path("projects/Hyprop_geotom_01Carl/data/raw/Measurement/ERT")
    dirs = sorted([d for d in base_dir.iterdir() if d.is_dir()])

    print(f"{'Cartella':<22} | {'N° File':<7} | {'Durata Reale':<12} | {'File Disallineati':<17}")
    print("-" * 65)

    for d in dirs:
        res = analizza_directory_campione(d)
        n_file = res.get("n_file", 0)
        durata = f"{res.get('durata_ore', 0):.1f} ore"
        n_disall = len(res.get("piani_rinomina", []))  # type: ignore[arg-type]
        print(f"{d.name:<22} | {n_file:<7} | {durata:<12} | {n_disall:<17}")


if __name__ == "__main__":
    main()
