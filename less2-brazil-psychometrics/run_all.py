"""Roda os scripts Python na ordem. Uso: python run_all.py --raw-dir data/raw --out-dir outputs"""
import subprocess, sys, argparse
from pathlib import Path
ap = argparse.ArgumentParser(); ap.add_argument("--raw-dir", default="data/raw"); ap.add_argument("--out-dir", default="outputs"); a = ap.parse_args()
steps = ["01_sample_flow", "02_descriptives_reliability_norms", "03_criterion_validity", "04_dif_power", "05_attrition", "06_export_for_r"]
for s in steps:
    print(f"\n=== {s}"); subprocess.run([sys.executable, str(Path("scripts") / f"{s}.py"), "--raw-dir", a.raw_dir, "--out-dir", a.out_dir], check=True)
print("\nPróximo passo (local, requer R): Rscript r/01_polychoric_efa.R && Rscript r/02_cfa_models.R && python scripts/07_bifactor_indices_from_loadings.py")
