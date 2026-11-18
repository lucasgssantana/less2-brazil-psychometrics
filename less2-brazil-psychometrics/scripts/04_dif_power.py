"""Triagem de DIF por gênero (critérios a/b do manuscrito) e Tabela S1 (sensibilidade, F não central)."""
from _common import *
import statsmodels.api as sm
from scipy import stats, optimize
from less2.stats_utils import holm

raw, out = parse(); analytic, union, excluded, flow, S = load(raw)
L = less_items(analytic); n = len(L); g = S.genero.values.astype(float)
z = ((S.less_total - S.less_total.mean()) / S.less_total.std(ddof=1)).values
rows = []
for i in range(1, 29):
    y = L[f"less_{i}"].values
    fit = lambda cols: sm.OLS(y, sm.add_constant(np.column_stack(cols))).fit().rsquared
    r0, r1, r2_ = fit([z]), fit([z, g]), fit([z, g, z * g])
    pu = stats.f.sf((r1 - r0) / ((1 - r1) / (n - 3)), 1, n - 3); pn = stats.f.sf((r2_ - r1) / ((1 - r2_) / (n - 4)), 1, n - 4)
    rows.append(dict(item=i, R2_base=r0, dR2_uniforme=r1 - r0, p_uniforme=pu, dR2_nao_uniforme=r2_ - r1, p_nao_uniforme=pn))
D = pd.DataFrame(rows); D["p_uniforme_holm28"] = holm(D.p_uniforme); D["p_nao_uniforme_holm28"] = holm(D.p_nao_uniforme)
D["sinal_uniforme(a)"] = (D.dR2_uniforme > 0.02) & (D.p_uniforme_holm28 < 0.05)
D["sinal_nao_uniforme(b)"] = D.p_nao_uniforme < 0.01
D.round(4).to_csv(out / "tables" / "dif_por_item.csv", index=False, sep=";", decimal=",")

# Tabela S1: poder do teste F de incremento de R2, lambda = f2 * N (N = 238), gl = 1 e n-4
base = D.R2_base.mean(); dfd = n - 4
def power(dr2, b, alpha):
    lam = dr2 / (1 - b) * n; return stats.ncf.sf(stats.f.ppf(1 - alpha, 1, dfd), 1, dfd, lam)
def thr(b, alpha, target=0.8): return optimize.brentq(lambda x: power(x, b, alpha) - target, 1e-5, 0.5)
aH = 0.05 / 28
grid = pd.DataFrame([dict(dR2=d, f2=d / (1 - base), poder_a05=power(d, base, .05), poder_holm=power(d, base, aH), poder_a01=power(d, base, .01)) for d in (.01, .02, .03, .04, .05, .06, .08, .10)])
grid.round(4).to_csv(out / "tables" / "tabelaS1_sensibilidade.csv", index=False, sep=";", decimal=",")
lim = dict(R2_base_media=base, R2_base_min=D.R2_base.min(), R2_base_max=D.R2_base.max(),
           limiar_uniforme_a05=thr(base, .05), limiar_uniforme_holm=thr(base, aH), limiar_nao_uniforme_a01=thr(base, .01),
           limiar_base0_a05=thr(0, .05), limiar_base0_holm=thr(0, aH), limiar_base0_a01=thr(0, .01),
           itens_sinalizados_b=D.loc[D["sinal_nao_uniforme(b)"], "item"].tolist(), itens_sinalizados_a=D.loc[D["sinal_uniforme(a)"], "item"].tolist())
(out / "tables" / "dif_limiares.json").write_text(json.dumps(lim, indent=2, default=float), encoding="utf-8"); print(json.dumps(lim, default=float))
