import pytest
from datetime import datetime
from app.history import History
from app.calculation import Calculation
from app.exceptions import HistoryError


def make_calc(i):
    return Calculation("add", i, i, i + i, datetime.now())


def test_add_and_list_history():
    h = History(max_size=5)
    for i in range(3):
        h.add(make_calc(i))
    items = h.list()
    assert len(items) == 3
    assert items[-1].result == 4

def test_history_size_limit():
    h = History(max_size=3)
    for i in range(5):
        h.add(make_calc(i))
    items = h.list()
    assert len(items) == 3
    # Should keep the last 3 only
    assert [c.a for c in items] == [2, 3, 4]

def test_clear_history():
    h = History()
    for i in range(3):
        h.add(make_calc(i))
    h.clear()
    assert len(h) == 0
    assert h.list() == []

def test_add_non_calculation_raises():
    h = History()
    with pytest.raises(HistoryError):
        h.add("not a calc")
        
def test_last_returns_latest_item():
    h = History()
    calc = make_calc(5)
    h.add(calc)
    assert h.last() == calc

def test_save_to_csv_failure(monkeypatch):
    hist = History()
    # simulate pandas failure
    monkeypatch.setattr("pandas.DataFrame.to_csv", lambda *a, **k: (_ for _ in ()).throw(Exception("boom")))
    with pytest.raises(HistoryError):
        hist.save_to_csv("bad.csv")

def test_load_from_csv_malformed(tmp_path):
    f = tmp_path / "bad.csv"
    f.write_text("not,a,valid,csv")
    hist = History()
    # Should not crash; should handle gracefully
    hist.load_from_csv(f)
    assert isinstance(hist.list(), list)
