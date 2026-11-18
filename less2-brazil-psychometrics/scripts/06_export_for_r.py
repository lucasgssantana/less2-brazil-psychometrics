"""Exporta os 28 itens da LESS-II já recodificados (sem id) para os scripts em R. Saída em data/processed/ (NÃO versionada)."""
from _common import *
raw, out = parse(); analytic, union, excluded, flow, S = load(raw)
dest = ROOT / "data" / "processed"; dest.mkdir(parents=True, exist_ok=True)
L = less_items(analytic).reset_index(drop=True)
L.to_csv(dest / "less_items_recodificados.csv", index=False, sep=";")
pd.DataFrame({"genero": S.genero.values}).to_csv(dest / "genero.csv", index=False, sep=";"); print("ok", L.shape)
