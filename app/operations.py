"""Operations and Factory (Phase 1.1–1.4).

Each operation implements a callable interface:
    result = Operation()(a: float, b: float) -> float
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol, Dict, Callable
from math import isfinite
from .exceptions import OperationError


class Operation(Protocol):
    """Callable arithmetic operation over two floats."""
    def __call__(self, a: float, b: float) -> float: ...


def _check_numbers(a: float, b: float) -> None:
    """Basic sanity checks (Phase 1 minimal). Detailed validation in Phase 2."""
    if not (isfinite(a) and isfinite(b)):
        raise OperationError("Inputs must be finite numbers.")

# ---------------------
# Core operations
# ---------------------

@dataclass(frozen=True)
class Add:
    def __call__(self, a: float, b: float) -> float:
        _check_numbers(a, b)
        return a + b


@dataclass(frozen=True)
class Subtract:
    def __call__(self, a: float, b: float) -> float:
        _check_numbers(a, b)
        return a - b


@dataclass(frozen=True)
class Multiply:
    def __call__(self, a: float, b: float) -> float:
        _check_numbers(a, b)
        return a * b


@dataclass(frozen=True)
class Divide:
    def __call__(self, a: float, b: float) -> float:
        _check_numbers(a, b)
        if b == 0:
            raise OperationError("Division by zero.")
        return a / b

# ---------------------
# Advanced operations
# ---------------------

@dataclass(frozen=True)
class Power:
    def __call__(self, a: float, b: float) -> float:
        _check_numbers(a, b)
        return a ** b


@dataclass(frozen=True)
class Root:
    """Compute the b-th root of a: root(a, b) = a ** (1/b).
    Phase 1 minimal rules:
      - b == 0 -> error
      - negative a with even integer b -> error (Phase 2 will formalize)
    """
    def __call__(self, a: float, b: float) -> float:
        _check_numbers(a, b)
        if b == 0:
            raise OperationError("Root with zero degree is undefined.")
        # If b is an integer and even, disallow negative radicand
        if a < 0 and float(b).is_integer() and int(abs(b)) % 2 == 0:
            raise OperationError("Even root of a negative number is not real.")
        return a ** (1.0 / b)


@dataclass(frozen=True)
class Modulus:
    def __call__(self, a: float, b: float) -> float:
        _check_numbers(a, b)
        if b == 0:
            raise OperationError("Modulus by zero.")
        return a % b


@dataclass(frozen=True)
class IntDivide:
    """Integer division that discards fractional part (truncates toward zero)."""
    def __call__(self, a: float, b: float) -> float:
        _check_numbers(a, b)
        if b == 0:
            raise OperationError("Integer division by zero.")
        return float(int(a / b))  # truncation toward zero


@dataclass(frozen=True)
class Percent:
    """Compute (a / b) * 100."""
    def __call__(self, a: float, b: float) -> float:
        _check_numbers(a, b)
        if b == 0:
            raise OperationError("Percentage denominator cannot be zero.")
        return (a / b) * 100.0


@dataclass(frozen=True)
class AbsDiff:
    def __call__(self, a: float, b: float) -> float:
        _check_numbers(a, b)
        return abs(a - b)
