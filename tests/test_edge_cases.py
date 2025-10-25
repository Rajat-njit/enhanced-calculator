import math
import pytest
from app.calculation import Calculation
from app.calculator_config import load_config
from app.exceptions import ValidationError, OperationError
from app.input_validators import validate_inputs
from app.exceptions import ValidationError

cfg = load_config()

# ---- String inputs ----
@pytest.mark.parametrize("a,b", [("5", "2"), ("3.5", "1.5"), ("-10", "4")])
def test_string_numbers_are_accepted(a,b):
    calc = Calculation.create("add", a, b, cfg)
    assert isinstance(calc.result, float)

@pytest.mark.parametrize("a,b", [("abc", 1), (1, "def")])
def test_invalid_string_rejected(a,b):
    with pytest.raises(ValidationError):
        Calculation.create("multiply", a, b, cfg)

# ---- Infinity / NaN ----
@pytest.mark.parametrize("a,b", [(float("inf"), 2), (2, float("nan"))])
def test_infinite_or_nan_inputs_raise(a,b):
    with pytest.raises(ValidationError):
        Calculation.create("add", a, b, cfg)

# ---- Root corner cases ----
def test_negative_even_root_rejected():
    with pytest.raises(OperationError):
        Calculation.create("root", -16, 2, cfg)

def test_negative_odd_root_allowed():
    calc = Calculation.create("root", -27, 3, cfg)
    assert math.isclose(calc.result, -3.0, rel_tol=1e-9)

# ---- Precision ----
def test_precision_rounding_applied():
    local_cfg = load_config()
    local_cfg = type(local_cfg)(**{**local_cfg.__dict__, "precision": 3})
    calc = Calculation.create("divide", 1, 3, local_cfg)
    assert len(str(calc.result).split(".")[1]) <= 3

# ---- Out-of-range ----
def test_inputs_exceeding_limit_raise():
    with pytest.raises(ValidationError):
        Calculation.create("add", 1e9, 1, cfg)

def test_validate_invalid_number_type():
    with pytest.raises(ValidationError):
        validate_inputs("add", "abc", 2, 1000000)

def test_validate_overflow_max_input():
    with pytest.raises(ValidationError):
        validate_inputs("add", 1e10, 1, 1_000_000)

def test_validate_zero_root():
    with pytest.raises(OperationError):
        validate_inputs("root", 4, 0, 1_000_000)

