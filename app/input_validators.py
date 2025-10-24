"""Comprehensive input validation utilities (Phase 2.1).

All validation rules are centralized here. The goal is to ensure
that every operation receives only safe, finite, and reasonable
inputs before execution.
"""

import math
from .exceptions import ValidationError, OperationError


def is_number(value) -> bool:
    """Check if value is a valid number (int or float)."""
    try:
        float(value)
        return True
    except (TypeError, ValueError):
        return False


def validate_numeric(a, b):
    """Ensure both a and b are numeric and finite."""
    if not (is_number(a) and is_number(b)):
        raise ValidationError(f"Inputs must be numeric. Got: {a!r}, {b!r}")
    if not (math.isfinite(float(a)) and math.isfinite(float(b))):
        raise ValidationError("Inputs must be finite numbers.")


def validate_range(a, b, max_value: float):
    """Ensure both values are within the allowed numeric range."""
    for v in (a, b):
        if abs(float(v)) > max_value:
            raise ValidationError(
                f"Input value {v} exceeds allowed limit ({max_value})."
            )


def validate_division(b):
    """Ensure denominator is not zero."""
    if float(b) == 0.0:
        raise OperationError("Division or modulus by zero is undefined.")


def validate_root(a, b):
    """Ensure valid root parameters."""
    if float(b) == 0.0:
        raise OperationError("Root with zero degree is undefined.")

    # Check for even root of a negative number
    if float(a) < 0 and float(b).is_integer() and int(abs(b)) % 2 == 0:
        raise OperationError("Even root of negative number is not real.")


'''
def validate_inputs(operation_name: str, a, b, max_value: float):
    """Composite validation entrypoint for any operation."""
    name = operation_name.lower().strip()
    validate_numeric(a, b)
    validate_range(a, b, max_value)

    if name in {"divide", "modulus", "int_divide", "percent"}:
        validate_division(b)

    if name == "root":
        validate_root(a, b)
'''
def to_float(value) -> float:
    """Convert safely to float; raise ValidationError if impossible."""
    try:
        val = float(value)
    except (TypeError, ValueError):
        raise ValidationError(f"Input {value!r} is not a number.")
    if not math.isfinite(val):
        raise ValidationError(f"Input {value!r} is not finite.")
    return val


def sanitize_inputs(a, b):
    """Return numeric (float) equivalents after validating finite."""
    return to_float(a), to_float(b)


def validate_inputs(operation_name: str, a, b, max_value: float):
    """Composite validation entrypoint (enhanced Phase 2.3)."""
    name = operation_name.lower().strip()
    a, b = sanitize_inputs(a, b)
    validate_range(a, b, max_value)

    if name in {"divide", "modulus", "int_divide", "percent"}:
        validate_division(b)

    if name == "root":
        validate_root(a, b)

    return a, b  # useful for clean numeric results