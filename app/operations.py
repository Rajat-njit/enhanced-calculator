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
