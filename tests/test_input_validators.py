import pytest
from app.input_validators import (
    validate_numeric,
    validate_range,
    validate_division,
    validate_root,
    validate_inputs,
)
from app.exceptions import ValidationError, OperationError


def test_validate_numeric_accepts_numbers():
    validate_numeric(1, 2)
    validate_numeric(1.5, 2.7)


@pytest.mark.parametrize("a,b", [("x", 2), (1, "y")])
def test_validate_numeric_rejects_non_numbers(a, b):
    with pytest.raises(ValidationError):
        validate_numeric(a, b)


def test_validate_range_within_limits():
    validate_range(100, -200, 1e6)


@pytest.mark.parametrize("a,b", [(1e7, 1), (1, -1e7)])
def test_validate_range_exceeds_limit(a, b):
    with pytest.raises(ValidationError):
        validate_range(a, b, 1e6)


def test_validate_division_zero_raises():
    with pytest.raises(OperationError):
        validate_division(0)


def test_validate_root_zero_degree():
    with pytest.raises(OperationError):
        validate_root(9, 0)


def test_validate_root_even_negative():
    with pytest.raises(OperationError):
        validate_root(-9, 2)


def test_validate_root_odd_negative_allowed():
    # cube root of -8 -> valid
    validate_root(-8, 3)


@pytest.mark.parametrize(
    "op,a,b,expect_error",
    [
        ("divide", 1, 0, OperationError),
        ("modulus", 1, 0, OperationError),
        ("int_divide", 1, 0, OperationError),
        ("percent", 1, 0, OperationError),
        ("root", -8, 3, None),  # allowed
        ("add", 1, 2, None),
    ],
)
def test_validate_inputs_dispatches_correctly(op, a, b, expect_error):
    if expect_error:
        with pytest.raises(expect_error):
            validate_inputs(op, a, b, 1e6)
    else:
        validate_inputs(op, a, b, 1e6)

