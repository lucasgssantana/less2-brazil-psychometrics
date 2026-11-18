"""Sem dados individuais: reproduz a Tabela 3 do manuscrito a partir das cargas publicadas na Tabela 1 (arredondadas a 2 casas)."""
import sys, json; from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
import pytest
from less2.bifactor_indices import bifactor_indices
from less2.config import LESS_FACTORS

def test_table3_reproduced():
    d = json.load(open(ROOT / "tests" / "fixtures" / "bifactor_loadings_manuscript.json"))
    r = bifactor_indices(d["lg"], d["ls"], {k: [i - 1 for i in v] for k, v in LESS_FACTORS.items()})
    assert r["omega"] == pytest.approx(0.916, abs=0.003)
    assert r["omega_h"] == pytest.approx(0.839, abs=0.003)
    assert r["ecv"] == pytest.approx(0.588, abs=0.003)
    assert r["puc"] == pytest.approx(0.788, abs=0.001)
    for k, v in {"F1": 0.017, "F2": 0.184, "F3": 0.635, "F4": 0.128, "F5": 0.318}.items():
        assert r["omega_hs"][k] == pytest.approx(v, abs=0.005)
