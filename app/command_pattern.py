# Author: Rajat Pednekar | UCID: rp2348

"""
command_pattern.py
-------------------
Implements the Command Design Pattern for the Enhanced Calculator.

Each operation (Add, Subtract, etc.) is encapsulated as a Command object,
allowing structured execution, extensibility, and easy integration with
undo/redo mechanisms or operation queues in the future.

Design Pattern:
    - **Command Pattern**: Encapsulates requests as objects,
      enabling parameterization and command chaining.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol, TYPE_CHECKING
from app.exceptions import OperationError

if TYPE_CHECKING:
    from app.calculator import Calculator


class Command(Protocol):
    """
    Base Command class representing a calculator action.
    Each concrete command will store an operation (function) and its arguments.
    """

    def execute(self) -> float: ...
    def undo(self) -> None: ...


@dataclass
class OperationCommand:
    """Concrete Command encapsulating a calculator operation request.

    Each OperationCommand object stores:
    - the target calculator instance
    - the operation name (e.g., 'add', 'divide')
    - the input operands (a, b)

    It supports execute() and undo() methods, enabling
    queueing, replaying, and integration with Memento history.
    """

    calculator: Calculator
    operation_name: str
    a: float
    b: float

    def execute(self) -> float:
        """Execute the encapsulated operation."""
        try:
            return self.calculator.perform_operation(self.operation_name, self.a, self.b)
        except Exception as e:
            raise OperationError(f"Failed to execute {self.operation_name}: {e}")

    def undo(self) -> None:
        """Undo the last operation through the calculator."""
        try:
            self.calculator.undo()
        except Exception as e:
            raise OperationError(f"Cannot undo {self.operation_name}: {e}")
