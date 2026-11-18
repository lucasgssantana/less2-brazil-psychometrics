import sys; from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import pandas as pd
from less2 import config as C
from less2.scoring import recode

def test_reverse_lists():
    assert len(C.REV_LESS) == 8 and len(C.REV_DERS) == 11
    assert sorted(C.REV_DERS) == [1, 2, 6, 7, 8, 10, 17, 20, 22, 24, 34]

def test_partitions_cover_items_once():
    flat = lambda d: sorted(i for v in d.values() for i in v)
    assert flat(C.DERS_SUBSCALES) == list(range(1, 37))
    assert flat(C.LESS_14) == list(range(1, 29))
    assert flat(C.LESS_FACTORS) == list(range(1, 29))
    assert sorted(C.ERQ_REAPPRAISAL + C.ERQ_SUPPRESSION) == list(range(1, 11))
    assert sorted(i for v in C.DASS.values() for i in v) == list(range(1, 22))

def test_recode_values():
    df = pd.DataFrame({c: [1] for c in C.ALL_ITEMS})
    r = recode(df)
    assert r["less_4"][0] == 6 and r["less_1"][0] == 1      # LESS: 7 - x
    assert r["ders_34"][0] == 5 and r["ders_3"][0] == 1     # DERS: 6 - x
    assert r["ders_28"][0] == 1                              # item 28 da DERS NAO é reverso
