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
