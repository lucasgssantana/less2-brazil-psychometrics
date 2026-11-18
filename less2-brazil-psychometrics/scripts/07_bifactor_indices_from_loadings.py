"""Lê cargas padronizadas exportadas pelo R (outputs/r/bifactor_loadings.csv: colunas item, lambda_G, lambda_S) e calcula ω, ωH, ECV, PUC, ωHS."""
from _common import *
from less2.bifactor_indices import bifactor_indices
raw, out = parse()
f = out / "r" / "bifactor_loadings.csv"
if not f.exists():
    raise SystemExit(f"Arquivo ausente: {f}. Rode r/02_cfa_models.R antes.")
d = pd.read_csv(f).sort_values("item")
groups = {k: [i - 1 for i in v] for k, v in C.LESS_FACTORS.items()}
res = bifactor_indices(d.lambda_G, d.lambda_S, groups)
(out / "tables" / "tabela3_indices_bifatoriais.json").write_text(json.dumps(res, indent=2, default=float)); print(res)
