import pytest
from app.calculation import Calculation
from app.calculator_config import load_config
from app.exceptions import OperationError, ValidationError


cfg = load_config()  # uses defaults


def test_calculation_add_basic():
    calc = Calculation.create("add", 2, 3, cfg)
    assert calc.result == pytest.approx(5.0)
    assert calc.operation == "add"
    assert calc.timestamp is not None


@pytest.mark.parametrize("name,a,b,expected", [
    ("subtract", 10, 4, 6),
    ("multiply", 3, 5, 15),
    ("divide", 10, 2, 5),
    ("power", 2, 3, 8),
    ("root", 9, 2, 3),
    ("modulus", 10, 3, 1),
    ("int_divide", 7, 3, 2.0),
    ("percent", 50, 200, 25.0),
    ("abs_diff", 5, 8, 3.0),
])
def test_valid_operations(name, a, b, expected):
    calc = Calculation.create(name, a, b, cfg)
    assert calc.result == pytest.approx(expected, rel=1e-9)


@pytest.mark.parametrize("name,a,b", [
    ("divide", 1, 0),
    ("modulus", 1, 0),
    ("int_divide", 1, 0),
    ("percent", 1, 0),
    ("root", 9, 0),
])
def test_invalid_zero_denominator(name, a, b):
    with pytest.raises(OperationError):
        Calculation.create(name, a, b, cfg)


def test_invalid_numeric_inputs_raise():
    with pytest.raises(ValidationError):
        Calculation.create("add", "abc", 5, cfg)


def test_out_of_range_inputs_raise():
    with pytest.raises(ValidationError):
        Calculation.create("multiply", 1e8, 2, cfg)
