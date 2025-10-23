"""Calculation entity and creation logic (Phase 2.2)."""

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime

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
        """Validate, execute, and build a Calculation instance."""
        try:
            # Run composite validation (Phase 2.1 rules)
            validate_inputs(operation_name, a, b, config.max_input_value)

            # Execute operation using the factory
            operation_instance = OperationFactory.create(operation_name)
            result = operation_instance(float(a), float(b))

            # Apply precision rounding from config
            if config.precision is not None:
                result = round(result, config.precision)

            return Calculation(
                operation=operation_name.lower().strip(),
                a=float(a),
                b=float(b),
                result=result,
                timestamp=datetime.now(),
            )

        except (ValidationError, OperationError):
            # Re-raise known, expected calculator errors unchanged
            raise
        except Exception as e:
            # Wrap any other error type
            raise OperationError(f"Unexpected error executing operation '{operation_name}': {e}")
