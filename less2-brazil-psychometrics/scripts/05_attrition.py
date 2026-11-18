"""Viés de atrito (Tabela S2): desistentes vs. 238 completantes. Só usa arquivos de trabalho auditáveis."""
from _common import *
from scipy import stats
from less2.data import _read, RAW_FILES
from less2.stats_utils import holm

raw, out = parse(); analytic, union, excluded, flow, S = load(raw)
ab_ids = excluded.index[excluded.motivo.str.startswith("abandono")]
ref_ids = _read(raw / RAW_FILES[1]).index
sets = {"25 desistentes (todos os arquivos de trabalho)": ab_ids, "23 desistentes ausentes do banco reformado": ab_ids.difference(ref_ids)}
R = recode(union.loc[ab_ids, C.ALL_ITEMS].apply(pd.to_numeric, errors="coerce"))
P = pd.DataFrame(index=R.index)
P["idade"] = pd.to_numeric(union.loc[ab_ids, "idade"], errors="coerce")
P["ders_total"] = R[[f"ders_{i}" for i in range(1, 37)]].sum(axis=1, min_count=36)
P["erq_reav"] = R[[f"eqr_{i}" for i in C.ERQ_REAPPRAISAL]].mean(axis=1, skipna=False)
P["erq_sup"] = R[[f"eqr_{i}" for i in C.ERQ_SUPPRESSION]].mean(axis=1, skipna=False)
P["genero"] = pd.to_numeric(union.loc[ab_ids, "genero"], errors="coerce")
comp = pd.DataFrame({"idade": S.idade, "ders_total": S.ders_total, "erq_reav": S.erq_reavaliacao, "erq_sup": S.erq_supressao, "genero": S.genero})
rows = []
for nome, ids in sets.items():
    d = P.loc[ids]; ps = []
    for v, lab in (("idade", "Idade"), ("ders_total", "DERS total"), ("erq_reav", "ERQ reavaliação"), ("erq_sup", "ERQ supressão")):
        a, b = d[v].dropna(), comp[v].dropna(); u = stats.mannwhitneyu(a, b, alternative="two-sided")
        rows.append(dict(conjunto=nome, variavel=lab, n_desist=len(a), M_desist=a.mean(), Mdn_desist=a.median(), M_comp=b.mean(), Mdn_comp=b.median(), U=u.statistic, p=u.pvalue)); ps.append(u.pvalue)
    g = d.genero
    t1 = [[(comp.genero == 1).sum(), (comp.genero == 0).sum()], [(g == 1).sum(), (g == 0).sum()]]
    t2 = [[(comp.genero == 1).sum(), (comp.genero == 0).sum()], [(g == 1).sum(), g.isin([0, 2]).sum()]]
    p1, p2 = stats.fisher_exact(t1)[1], stats.fisher_exact(t2)[1]
    rows.append(dict(conjunto=nome, variavel="Gênero (Fisher, 1 vs 0)", n_desist=int(g.isin([0, 1]).sum()), p=p1))
    rows.append(dict(conjunto=nome, variavel="Gênero (Fisher, 1 vs 0+2)", n_desist=int(g.isin([0, 1, 2]).sum()), p=p2))
    ps.append(p1)   # Holm sobre 5 comparações (4 testes U + Fisher 1 vs 0)
    h = holm(ps); idx = [k for k, r in enumerate(rows) if r["conjunto"] == nome and not str(r["variavel"]).endswith("0+2)")]
    for k, hp in zip(idx, h): rows[k]["p_holm5"] = hp
T = pd.DataFrame(rows); T.round(3).to_csv(out / "tables" / "tabelaS2_atrito.csv", index=False, sep=";", decimal=","); print(T.round(3).to_string(index=False))
