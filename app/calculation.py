"""Calculation entity and creation logic (Phase 2.2)."""

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime

from .operations import OperationFactory
from .input_validators import validate_inputs
from .exceptions import ValidationError, OperationError
from .calculator_config import CalculatorConfig


@staticmethod
def create(operation_name: str, a, b, config: CalculatorConfig) -> "Calculation":
    try:
        # Run validations (returns numeric floats)
        a_num, b_num = validate_inputs(operation_name, a, b, config.max_input_value)

        operation_instance = OperationFactory.create(operation_name)
        result = operation_instance(a_num, b_num)

        if math.isfinite(result):
            result = round(result, config.precision)
        else:
            raise ValidationError(f"Result of {operation_name} is not finite.")

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

