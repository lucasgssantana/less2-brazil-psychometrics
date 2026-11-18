"""Tabela 5 (Spearman + IC bootstrap + Holm), Tabela 6 (validade incremental, AUC), Tabela 7 (grupos conhecidos)."""
from _common import *
import statsmodels.api as sm
from scipy import stats
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold, cross_val_predict
from sklearn.metrics import roc_auc_score
from less2.stats_utils import spearman_ci, holm, cohen_d, rank_biserial

raw, out = parse(); analytic, union, excluded, flow, S = load(raw)
scores = {"Total-28": "less_total", "Core-24": "less_core24", "F1": "F1", "F2": "F2", "F3": "F3", "F4": "F4", "F5": "F5"}
crit = {"DERS total": "ders_total", "DERS Estrategias": "ders_Estrategias", "DERS Clareza": "ders_Clareza", "DERS Nao_aceitacao": "ders_Nao_aceitacao",
        "DERS Impulsos": "ders_Impulsos", "DERS Metas": "ders_Metas", "DERS Consciencia": "ders_Consciencia",
        "ERQ Reavaliacao": "erq_reavaliacao", "ERQ Supressao": "erq_supressao",
        "DASS Depressao": "dass_Depressao", "DASS Ansiedade": "dass_Ansiedade", "DASS Estresse": "dass_Estresse"}
# ---- Tabela 5
rows = []
for cn, cc in crit.items():
    for sn, sc in scores.items():
        rho, p = stats.spearmanr(S[sc], S[cc]); rows.append(dict(criterio=cn, escore=sn, rho=rho, p=p))
t5 = pd.DataFrame(rows); t5["p_holm_84"] = holm(t5.p)   # FAMÍLIA = 84 testes (assunção: confirmar no manuscrito)
ci = {(cn, "Total-28"): spearman_ci(S["less_total"], S[cc], 1000, C.SEED) for cn, cc in crit.items()}
t5["IC95_inf"] = [ci[(r.criterio, r.escore)][1] if r.escore == "Total-28" else np.nan for r in t5.itertuples()]
t5["IC95_sup"] = [ci[(r.criterio, r.escore)][2] if r.escore == "Total-28" else np.nan for r in t5.itertuples()]
t5.round(4).to_csv(out / "tables" / "tabela5_spearman_long.csv", index=False, sep=";", decimal=",")
t5.pivot(index="criterio", columns="escore", values="rho").loc[list(crit)][list(scores)].round(2).to_csv(out / "tables" / "tabela5_spearman_wide.csv", sep=";", decimal=",")

# ---- Tabela 6
def r2(y, X):
    return sm.OLS(y, sm.add_constant(X)).fit().rsquared
def boot_delta(y, a, b, n=2000, seed=C.SEED):
    rng = np.random.default_rng(seed); N = len(y); d = np.empty(n)
    for k in range(n):
        i = rng.integers(0, N, N); d[k] = r2(y[i], np.column_stack([a[i], b[i]])) - r2(y[i], a[i])
    return np.percentile(d, [2.5, 97.5])
rows = []; ders = S.ders_total.values; less = S.less_total.values
for dom in C.DASS:
    y = S[f"dass_{dom}"].values; cut = C.DASS_MODERATE_CUT[dom]
    rd, rl, rb = r2(y, ders), r2(y, less), r2(y, np.column_stack([ders, less]))
    zs = lambda v: (v - v.mean()) / v.std(ddof=1)
    fit = sm.OLS(zs(y), sm.add_constant(np.column_stack([zs(ders), zs(less)]))).fit(cov_type="HC3")
    lo, hi = boot_delta(y, ders, less)
    yb = (y >= cut).astype(int); aucs = []
    for cols in ([ders], [ders, less]):
        M = np.column_stack(cols); M = (M - M.mean(0)) / M.std(0)
        pr = cross_val_predict(LogisticRegression(), M, yb, cv=KFold(10, shuffle=True, random_state=C.SEED), method="predict_proba")[:, 1]
        aucs.append(roc_auc_score(yb, pr))
    rows.append(dict(desfecho=dom, R2_DERS=rd, R2_LESS=rl, R2_ambas=rb, dR2_LESS_alem_DERS=rb - rd, IC95_inf=lo, IC95_sup=hi,
                     dR2_DERS_alem_LESS=rb - rl, beta_DERS=fit.params[1], beta_LESS=fit.params[2], AUC_DERS=aucs[0], AUC_ambas=aucs[1], prevalencia_moderado_pct=100 * yb.mean()))
pd.DataFrame(rows).round(3).to_csv(out / "tables" / "tabela6_incremental.csv", index=False, sep=";", decimal=",")

# ---- Tabela 7
rows = []
for dom in C.DASS:
    y = S[f"dass_{dom}"]; m = y >= C.DASS_MODERATE_CUT[dom]; a, b = S.less_total[m], S.less_total[~m]
    rows.append(dict(dominio=dom, n_abaixo=int((~m).sum()), n_moderado_ou_mais=int(m.sum()), M_abaixo=b.mean(), M_moderado=a.mean(), d=cohen_d(a, b), r_rb=rank_biserial(a, b)))
pd.DataFrame(rows).round(2).to_csv(out / "tables" / "tabela7_grupos_conhecidos.csv", index=False, sep=";", decimal=",")
print(pd.DataFrame(rows).round(2).to_string(index=False)); print(pd.DataFrame(rows).shape)
