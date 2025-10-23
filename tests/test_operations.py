import math
import pytest
from app.operations import (
    OperationFactory,
    Add, Subtract, Multiply, Divide,
)
from app.exceptions import OperationError


@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (-1, 2, 1),
    (1.5, 2.5, 4.0),
])
def test_add(a, b, expected):
    assert Add()(a, b) == pytest.approx(expected)


@pytest.mark.parametrize("a,b,expected", [
    (5, 2, 3),
    (2, 5, -3),
    (1.5, 0.5, 1.0),
])
def test_subtract(a, b, expected):
    assert Subtract()(a, b) == pytest.approx(expected)


@pytest.mark.parametrize("a,b,expected", [
    (3, 4, 12),
    (-2, 5, -10),
    (1.5, 2, 3.0),
])
def test_multiply(a, b, expected):
    assert Multiply()(a, b) == pytest.approx(expected)


def test_divide_normal():
    assert Divide()(10, 2) == 5.0


def test_divide_by_zero_raises():
    with pytest.raises(OperationError):
        Divide()(1, 0)

from app.operations import (
    Power, Root, Modulus, IntDivide, Percent, AbsDiff
)

def test_power():
    assert Power()(2, 3) == 8
    assert Power()(-2, 3) == -8

def test_root_basic():
    assert Root()(9, 2) == 3
    assert Root()(27, 3) == 3

def test_root_even_of_negative_raises():
    from app.exceptions import OperationError
    with pytest.raises(OperationError):
        Root()(-9, 2)

def test_modulus():
    assert Modulus()(10, 3) == 1
    with pytest.raises(OperationError):
        Modulus()(1, 0)

def test_int_divide_truncates_toward_zero():
    assert IntDivide()(7, 3) == 2.0   # 2.333 -> 2
    assert IntDivide()(-7, 3) == -2.0 # -2.333 -> -2
    assert IntDivide()(7, -3) == -2.0
    with pytest.raises(OperationError):
        IntDivide()(1, 0)

def test_percent():
    assert Percent()(50, 200) == 25.0
    with pytest.raises(OperationError):
        Percent()(1, 0)

def test_abs_diff():
    assert AbsDiff()(10, 3) == 7
    assert AbsDiff()(-3, 5) == 8
