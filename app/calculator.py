"""Main Calculator core (Phase 3.3).

Integrates all components: Calculation, History, and Caretaker (Memento pattern).
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List

from .calculation import Calculation
from .history import History
from .calculator_memento import Caretaker
from .calculator_config import load_config
from .exceptions import OperationError, ValidationError, HistoryError


@dataclass
class Calculator:
    """Central Calculator orchestrating all components."""

    history: History
    caretaker: Caretaker
    config: Optional[object] = None

    def __post_init__(self):
        if self.config is None:
            self.config = load_config()

        # Connect caretaker and capture initial snapshot
        self.history.attach_caretaker(self.caretaker)

    # ----------------------------
    # Core operation execution
    # ----------------------------

    def perform_operation(self, operation_name: str, a, b) -> float:
        """Perform an operation, validate inputs, save result to history, and return result."""
        try:
            calc = Calculation.create(operation_name, a, b, self.config)
            self.history.add(calc)
            self.history.record_state()
            return calc.result
        except (OperationError, ValidationError) as e:
            raise e

    # ----------------------------
    # History and Memento controls
    # ----------------------------

    def get_history(self) -> List[str]:
        """Return formatted strings of all history entries."""
        entries = []
        for c in self.history.list():
            entries.append(f"{c.operation}({c.a}, {c.b}) = {c.result}")
        return entries

    def clear_history(self):
        """Clear the history and caretaker stacks."""
        self.history.clear()
        self.caretaker.clear()
        # Reattach caretaker to reset snapshot
        self.history.attach_caretaker(self.caretaker)

    def undo(self):
        """Undo last operation."""
        try:
            self.history.undo()
        except HistoryError as e:
            raise HistoryError(f"Undo failed: {e}")

    def redo(self):
        """Redo a previously undone operation."""
        try:
            self.history.redo()
        except HistoryError as e:
            raise HistoryError(f"Redo failed: {e}")
