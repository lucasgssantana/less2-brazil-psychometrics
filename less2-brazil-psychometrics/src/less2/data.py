"""Leitura dos arquivos de trabalho e construção AUDITÁVEL da amostra analítica (regra, não lista de ids)."""
from pathlib import Path
import numpy as np
import pandas as pd
from .config import ALL_ITEMS, N_ITEMS

RAW_FILES = ("USP.CSV", "BANCO_DE_DADOS_REFORMADO.csv")


def _read(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, sep=";", encoding="utf-8-sig", on_bad_lines="skip", low_memory=False)
    df.columns = df.columns.str.strip()
    df = df[df["id_registro"].notna()].copy()
    df["id_registro"] = df["id_registro"].astype(int)
    return df.drop_duplicates("id_registro").set_index("id_registro")


def load_union(raw_dir):
    """USP.CSV tem prioridade; BANCO_DE_DADOS_REFORMADO.csv completa os ids ausentes.
    Confere que ids comuns são idênticos item a item (auditoria de consistência)."""
    raw_dir = Path(raw_dir)
    usp, ref = (_read(raw_dir / f) for f in RAW_FILES)
    common = usp.index.intersection(ref.index)
    a = usp.loc[common, ALL_ITEMS].apply(pd.to_numeric, errors="coerce")
    b = ref.loc[common, ALL_ITEMS].apply(pd.to_numeric, errors="coerce")
    divergent = int(((a != b) & ~(a.isna() & b.isna())).sum().sum())
    union = pd.concat([usp, ref.loc[ref.index.difference(usp.index)]])
    meta = dict(n_usp=len(usp), n_reformado=len(ref), n_comuns=len(common),
                celulas_divergentes=divergent, n_uniao=len(union))
    return union, meta


def build_analytic_sample(raw_dir):
    """Inclusão: (i) gênero codificado 0/1 e (ii) 95 itens respondidos nas quatro escalas.
    Exclusões são classificadas pela etapa em que o participante parou."""
    union, meta = load_union(raw_dir)
    X = union[ALL_ITEMS].apply(pd.to_numeric, errors="coerce")
    gender = pd.to_numeric(union["genero"], errors="coerce")
    include = X.notna().all(axis=1) & gender.isin([0, 1])
    n_by = {p: X[[f"{p}_{i}" for i in range(1, n + 1)]].notna().sum(axis=1) for p, n in N_ITEMS.items()}

    def reason(i):
        if pd.isna(gender.loc[i]) and pd.notna(union.loc[i, "genero"]):
            return "erro_de_exportacao (campo genero invalido)"
        if sum(int(n_by[p].loc[i]) for p in n_by) == 0:
            return "abandono: nenhum item"
        if n_by["eqr"].loc[i] == 0:
            return "abandono: apos a DERS"
        if n_by["less"].loc[i] == 0:
            return "abandono: apos DERS e ERQ"
        if n_by["dass"].loc[i] == 0:
            return "abandono: durante/apos a LESS-II"
        return "item_ausente_pontual"

    excluded = pd.DataFrame({"motivo": [reason(i) for i in union.index[~include]]}, index=union.index[~include])
    flow = {"identificadores_nos_arquivos": int(len(union)), "amostra_analitica": int(include.sum()),
            "exclusoes_por_motivo": excluded["motivo"].value_counts().to_dict(), **meta}
    analytic = union.loc[include].copy()
    analytic[ALL_ITEMS] = X.loc[include]
    analytic["genero"] = gender.loc[include].astype(int)
    analytic["idade"] = pd.to_numeric(analytic["idade"], errors="coerce")
    return analytic, union, excluded, flow
