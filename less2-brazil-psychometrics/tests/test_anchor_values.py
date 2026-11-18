"""Valores-âncora do manuscrito v19. Exige os dados privados em data/raw/ (senão, os testes são pulados)."""
import sys, subprocess, json; from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
import pytest, pandas as pd
RAW = ROOT / "data" / "raw"
pytestmark = pytest.mark.skipif(not (RAW / "USP.CSV").exists(), reason="dados privados ausentes em data/raw/")

@pytest.fixture(scope="module")
def out(tmp_path_factory):
    o = tmp_path_factory.mktemp("out")
    for s in ("01_sample_flow", "02_descriptives_reliability_norms", "03_criterion_validity", "04_dif_power", "05_attrition"):
        subprocess.run([sys.executable, str(ROOT / "scripts" / f"{s}.py"), "--raw-dir", str(RAW), "--out-dir", str(o)], check=True, capture_output=True)
    return o / "tables"

def test_flow(out):
    f = json.load(open(out / "flow.json"))
    assert f["identificadores_nos_arquivos"] == 265 and f["amostra_analitica"] == 238 and f["celulas_divergentes"] == 0
    assert sum(v for k, v in f["exclusoes_por_motivo"].items() if k.startswith("abandono")) == 25

def test_descriptives(out):
    r = json.load(open(out / "resumo_descritivo.json"))
    assert (r["n"], r["mulheres"], r["homens"]) == (238, 182, 56)
    assert r["less_total_M"] == pytest.approx(95.8, abs=0.05) and r["less_total_DP"] == pytest.approx(19.7, abs=0.05)
    assert r["alfa_ders36"] == pytest.approx(0.95, abs=0.005)
    assert r["KMO_pearson"] == pytest.approx(0.873, abs=0.001) and r["bartlett_chi2"] == pytest.approx(2300.0, abs=0.5)

def test_incremental(out):
    t = pd.read_csv(out / "tabela6_incremental.csv", sep=";", decimal=",").set_index("desfecho")
    assert t.loc["Depressao", "dR2_LESS_alem_DERS"] == pytest.approx(0.098, abs=0.002)
    assert t.loc["Ansiedade", "dR2_LESS_alem_DERS"] == pytest.approx(0.029, abs=0.002)
    assert t.loc["Estresse", "dR2_LESS_alem_DERS"] == pytest.approx(0.031, abs=0.002)

def test_dif_and_power(out):
    d = pd.read_csv(out / "dif_por_item.csv", sep=";", decimal=",").set_index("item")
    assert d.loc[18, "dR2_nao_uniforme"] == pytest.approx(0.025, abs=0.001) and d.loc[18, "p_nao_uniforme"] == pytest.approx(0.005, abs=0.001)
    lim = json.load(open(out / "dif_limiares.json"))
    assert lim["limiar_uniforme_holm"] == pytest.approx(0.050, abs=0.001) and lim["limiar_nao_uniforme_a01"] == pytest.approx(0.037, abs=0.001)
    assert lim["itens_sinalizados_a"] == [] and lim["itens_sinalizados_b"] == [18]

def test_attrition(out):
    t = pd.read_csv(out / "tabelaS2_atrito.csv", sep=";", decimal=",")
    a = t[t.conjunto.str.startswith("25") & (t.variavel == "ERQ reavaliação")].iloc[0]
    assert a.p == pytest.approx(0.044, abs=0.001) and a.n_desist == 11
