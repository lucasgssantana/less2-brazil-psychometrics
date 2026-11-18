"""Fluxo amostral (265 -> 238) a partir de REGRA; gera flow.json e a Figura S1."""
from _common import *
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

raw, out = parse()
analytic, union, excluded, flow, S = load(raw)
(out / "tables" / "flow.json").write_text(json.dumps(flow, indent=2, ensure_ascii=False), encoding="utf-8")
excluded.to_csv(out / "tables" / "excluded_ids_motivos.csv")  # contém ids: NÃO versionar

ex = flow["exclusoes_por_motivo"]
ROTULOS = [("abandono: nenhum item", "nenhum item respondido"), ("abandono: apos a DERS", "após a DERS"),
           ("abandono: apos DERS e ERQ", "após a DERS e o ERQ"), ("abandono: durante/apos a LESS-II", "durante ou após a LESS-II")]
n_ab = sum(v for k, v in ex.items() if k.startswith("abandono"))
fig, ax = plt.subplots(figsize=(8, 4.6)); ax.axis("off"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
def box(x, y, w, h, t, ha="center"):
    ax.add_patch(plt.Rectangle((x, y), w, h, fill=False, lw=1.2))
    ax.text(x + (w / 2 if ha == "center" else 0.02), y + h / 2, t, ha=ha, va="center", fontsize=9, linespacing=1.3)
box(0.03, 0.78, 0.48, 0.18, f"Identificadores nos arquivos de trabalho\n(n = {flow['identificadores_nos_arquivos']})")
box(0.03, 0.40, 0.48, 0.18, "Protocolo completo (4 escalas, 95 itens)\ne gênero válido")
box(0.03, 0.04, 0.48, 0.18, f"Amostra analítica\n(n = {flow['amostra_analitica']})")
linhas = [f"Excluídos (n = {sum(ex.values())})", f"Abandono do protocolo (n = {n_ab}):"] + [f"   – {r}: {ex.get(k, 0)}" for k, r in ROTULOS]
linhas += [f"Erro de exportação: {ex.get('erro_de_exportacao (campo genero invalido)', 0)}", f"Item ausente pontual: {ex.get('item_ausente_pontual', 0)}"]
box(0.58, 0.46, 0.40, 0.44, "\n".join(linhas), ha="left")
ax.annotate("", xy=(0.27, 0.58), xytext=(0.27, 0.78), arrowprops=dict(arrowstyle="->"))
ax.annotate("", xy=(0.27, 0.22), xytext=(0.27, 0.40), arrowprops=dict(arrowstyle="->"))
ax.annotate("", xy=(0.58, 0.68), xytext=(0.27, 0.68), arrowprops=dict(arrowstyle="->"))
fig.savefig(out / "figures" / "FiguraS1_fluxo_amostral.png", dpi=300, bbox_inches="tight"); print(json.dumps(flow, ensure_ascii=False))
