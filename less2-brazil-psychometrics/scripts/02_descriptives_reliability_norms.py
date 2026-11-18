"""Tabela 1 (parte descritiva), Tabela 4 (Pearson/SB), Tabela 8 (normas), KMO/Bartlett, alfas das escalas."""
from _common import *
from scipy import stats
from less2.stats_utils import cronbach_alpha

raw, out = parse(); analytic, union, excluded, flow, S = load(raw)
L = less_items(analytic); R = recode(analytic); n = len(L)

# Tabela 1 (descritivas). Assimetria = momento amostral (scipy, bias=True) -> confirmar convenção no texto.
rows = []
tot = L.sum(axis=1)
for i in range(1, 29):
    x = L[f"less_{i}"]; rest = tot - x
    rows.append(dict(item=i, M=x.mean(), DP=x.std(ddof=1), assimetria=stats.skew(x), piso_pct=100 * (x == x.min()).mean() if False else 100 * (x == 1).mean(),
                     teto_pct=100 * (x == 6).mean(), r_item_resto=np.corrcoef(x, rest)[0, 1]))
t1 = pd.DataFrame(rows).round(3); t1.to_csv(out / "tables" / "tabela1_descritivas_itens.csv", index=False, sep=";", decimal=",")

# Tabela 4 (apenas Pearson e Spearman-Brown; policórica/ordinal em R)
rows = []
for nome, (a, b) in C.LESS_14.items():
    r = np.corrcoef(L[f"less_{a}"], L[f"less_{b}"])[0, 1]; rows.append(dict(subescala=nome, itens=f"{a}, {b}", r_pearson=r, alfa_SB=2 * r / (1 + r)))
t4 = pd.DataFrame(rows).sort_values("alfa_SB", ascending=False).round(2); t4.to_csv(out / "tables" / "tabela4_subescalas_pearson.csv", index=False, sep=";", decimal=",")

# KMO e Bartlett (matriz de PEARSON)
Rm = np.corrcoef(L.values.T); p = Rm.shape[0]
chi = -(n - 1 - (2 * p + 5) / 6) * np.log(np.linalg.det(Rm)); dfb = p * (p - 1) // 2
Ri = np.linalg.inv(Rm); P = -Ri / np.sqrt(np.outer(np.diag(Ri), np.diag(Ri))); np.fill_diagonal(P, 0); R0 = Rm.copy(); np.fill_diagonal(R0, 0)
kmo = (R0 ** 2).sum() / ((R0 ** 2).sum() + (P ** 2).sum())

# Tabela 8 (normas; percentis lineares)
q = [5, 10, 25, 50, 75, 90, 95]
t8 = pd.DataFrame({"percentil": q, "Total-28": np.percentile(S.less_total, q), "Core-24": np.percentile(S.less_core24, q)}).round(1)
t8.to_csv(out / "tables" / "tabela8_normas.csv", index=False, sep=";", decimal=",")

der = R[[f"ders_{i}" for i in range(1, 37)]]
summary = dict(n=n, mulheres=int((analytic.genero == 1).sum()), homens=int((analytic.genero == 0).sum()),
               idade_M=analytic.idade.mean(), idade_DP=analytic.idade.std(ddof=1), idade_Mdn=analytic.idade.median(),
               less_total_M=S.less_total.mean(), less_total_DP=S.less_total.std(ddof=1), less_core24_M=S.less_core24.mean(), less_core24_DP=S.less_core24.std(ddof=1),
               alfa_less28=cronbach_alpha(L), alfa_ders36=cronbach_alpha(der),
               alfa_ders_subescalas={k: cronbach_alpha(R[[f"ders_{i}" for i in v]]) for k, v in C.DERS_SUBSCALES.items()},
               alfa_erq_reav=cronbach_alpha(R[[f"eqr_{i}" for i in C.ERQ_REAPPRAISAL]]), alfa_erq_sup=cronbach_alpha(R[[f"eqr_{i}" for i in C.ERQ_SUPPRESSION]]),
               alfa_dass={k: cronbach_alpha(R[[f"dass_{i}" for i in v]]) for k, v in C.DASS.items()},
               KMO_pearson=kmo, bartlett_chi2=chi, bartlett_gl=dfb, bartlett_p=float(stats.chi2.sf(chi, dfb)),
               shapiro_p=float(stats.shapiro(S.less_total)[1]), assimetria_total=float(stats.skew(S.less_total)),
               genero_d=float(__import__("less2.stats_utils", fromlist=["x"]).cohen_d(S.less_total[S.genero == 0], S.less_total[S.genero == 1])),
               corr_core_total=float(np.corrcoef(S.less_core24, S.less_total)[0, 1]), rho_idade=float(stats.spearmanr(S.idade, S.less_total)[0]))
(out / "tables" / "resumo_descritivo.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False, default=float), encoding="utf-8")
print(json.dumps(summary, ensure_ascii=False, default=float)[:1500])
