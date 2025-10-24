# Author: Rajat Pednekar

"""
calculation.py
--------------
Defines the `Calculation` class, which encapsulates a single arithmetic operation.
This class is designed to be immutable and used as a data record for calculations.
It provides a factory method to create validated operations safely.

Design Pattern:
    - Factory Pattern: Used indirectly via OperationFactory to create operation instances.
"""

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
    
    """
    Represents a single arithmetic calculation.

    Attributes:
        operation (str): Name of the operation (e.g., 'add', 'divide').
        a (float): First operand.
        b (float): Second operand.
        result (float): Computed result.
        timestamp (datetime): Time when calculation was created.
    """

    operation: str
    a: float
    b: float
    result: float
    timestamp: datetime

    @staticmethod
    def create(operation_name: str, a, b, config: CalculatorConfig) -> "Calculation":
        
        """
        Factory method to safely create a Calculation instance.

        Args:
            operation (str): Operation name.
            a (float): First operand.
            b (float): Second operand.
            cfg: Calculator configuration object for precision.

        Returns:
            Calculation: The completed calculation record.

        Raises:
            OperationError: If the operation creation or execution fails.
        """
        
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
