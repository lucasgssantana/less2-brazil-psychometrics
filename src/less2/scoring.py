"""Pontuação das escalas a partir dos itens brutos."""
import pandas as pd
from . import config as C


def recode(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for i in C.REV_LESS:
        out[f"less_{i}"] = (C.LESS_MAX + 1) - out[f"less_{i}"]
    for i in C.REV_DERS:
        out[f"ders_{i}"] = (C.DERS_MAX + 1) - out[f"ders_{i}"]
    return out


def score(df: pd.DataFrame) -> pd.DataFrame:
    r = recode(df)
    s = pd.DataFrame(index=r.index)
    s["less_total"] = r[[f"less_{i}" for i in range(1, 29)]].sum(axis=1)
    s["less_core24"] = r[[f"less_{i}" for i in range(1, 29) if i not in C.LESS_CORE24_DROP]].sum(axis=1)
    for k, items in C.LESS_FACTORS.items():
        s[k] = r[[f"less_{i}" for i in items]].mean(axis=1)
    s["ders_total"] = r[[f"ders_{i}" for i in range(1, 37)]].sum(axis=1)
    for k, items in C.DERS_SUBSCALES.items():
        s[f"ders_{k}"] = r[[f"ders_{i}" for i in items]].sum(axis=1)
    s["erq_reavaliacao"] = r[[f"eqr_{i}" for i in C.ERQ_REAPPRAISAL]].mean(axis=1)
    s["erq_supressao"] = r[[f"eqr_{i}" for i in C.ERQ_SUPPRESSION]].mean(axis=1)
    for k, items in C.DASS.items():
        s[f"dass_{k}"] = r[[f"dass_{i}" for i in items]].sum(axis=1) * 2
    s["genero"] = df["genero"]
    s["idade"] = df["idade"]
    return s


def less_items(df: pd.DataFrame) -> pd.DataFrame:
    return recode(df)[[f"less_{i}" for i in range(1, 29)]]
