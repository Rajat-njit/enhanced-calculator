from datetime import datetime
from app.calculation import Calculation

def test_calculation_dataclass_exists():
    c = Calculation("add", 1.0, 2.0, 3.0, datetime.now())
    assert c.operation == "add"
