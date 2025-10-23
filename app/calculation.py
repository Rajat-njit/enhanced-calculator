"""Calculation entity and creation logic (Phase 2.2–2.3)."""

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
import math

from .operations import OperationFactory
from .input_validators import validate_inputs
from .exceptions import ValidationError, OperationError
from .calculator_config import CalculatorConfig


@dataclass(frozen=True)
class Calculation:
    """Immutable record of a single calculator operation."""
    operation: str
    a: float
    b: float
    result: float
    timestamp: datetime

    @staticmethod
    def create(operation_name: str, a, b, config: CalculatorConfig) -> "Calculation":
        """Validate inputs, execute operation via factory, and return a Calculation."""
        try:
            # Run validations (returns numeric floats)
            a_num, b_num = validate_inputs(operation_name, a, b, config.max_input_value)

            # Execute operation
            operation_instance = OperationFactory.create(operation_name)
            result = operation_instance(a_num, b_num)

            # Ensure finite result
            if math.isfinite(result):
                result = round(result, config.precision)
            else:
                raise ValidationError(f"Result of {operation_name} is not finite.")

            # Build final immutable record
            return Calculation(
                operation=operation_name.lower().strip(),
                a=a_num,
                b=b_num,
                result=result,
                timestamp=datetime.now(),
            )

        except (ValidationError, OperationError):
            raise
        except Exception as e:
            raise OperationError(f"Unexpected error executing '{operation_name}': {e}")
