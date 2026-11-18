import argparse, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import numpy as np, pandas as pd
from less2.data import build_analytic_sample
from less2.scoring import score, less_items, recode
from less2 import config as C

def parse():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw-dir", default=str(ROOT / "data" / "raw"))
    ap.add_argument("--out-dir", default=str(ROOT / "outputs"))
    a = ap.parse_args()
    out = Path(a.out_dir); (out / "tables").mkdir(parents=True, exist_ok=True); (out / "figures").mkdir(parents=True, exist_ok=True)
    return Path(a.raw_dir), out

def load(raw):
    analytic, union, excluded, flow = build_analytic_sample(raw)
    return analytic, union, excluded, flow, score(analytic)

def fmt(x, d=3): return f"{x:.{d}f}".replace(".", ",")
