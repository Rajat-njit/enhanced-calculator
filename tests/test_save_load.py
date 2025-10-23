from pathlib import Path
from app.history import History
from app.calculation import Calculation
from datetime import datetime

def make_calc(i):
    return Calculation("add", i, i + 1, (2 * i + 1), datetime.now())

def test_save_and_load_cycle(tmp_path):
    hist = History()
    for i in range(3):
        hist.add(make_calc(i))
    csv_path = tmp_path / "history.csv"

    hist.save_to_csv(csv_path)
    assert csv_path.exists()

    hist2 = History()
    hist2.load_from_csv(csv_path)
    assert len(hist2.list()) == 3
    assert hist2.list()[0].operation == "add"

def test_load_missing_file_raises(tmp_path):
    hist = History()
    try:
        hist.load_from_csv(tmp_path / "missing.csv")
    except Exception as e:
        assert "not found" in str(e)
