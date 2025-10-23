"""Main Calculator core (Phase 3.3 + Phase 4.1 observers)."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Any

from .calculation import Calculation
from .history import History
from .calculator_memento import Caretaker
from .calculator_config import load_config, CalculatorConfig
from .exceptions import OperationError, ValidationError, HistoryError


@dataclass
class Calculator:
    """Central Calculator orchestrating all components."""

    history: History
    caretaker: Caretaker
    config: Optional[CalculatorConfig] = None
    observers: List[Any] = field(default_factory=list)

    def __post_init__(self):
        if self.config is None:
            self.config = load_config()
        self.history.attach_caretaker(self.caretaker)

    # Observer registration
    def register_observer(self, observer: Any) -> None:
        self.observers.append(observer)

    def _notify_observers(self, calc: Calculation) -> None:
        # Call observer.update with best-effort signatures
        for obs in self.observers:
            try:
                # Prefer (calculation, history) signature
                obs.update(calc, self.history.list())
            except TypeError:
                # Fallback to (calculation) signature
                obs.update(calc)

    # Core operation execution
    def perform_operation(self, operation_name: str, a, b) -> float:
        try:
            calc = Calculation.create(operation_name, a, b, self.config)
            self.history.add(calc)
            self.history.record_state()
            # Notify observers only after success
            self._notify_observers(calc)
            return calc.result
        except (OperationError, ValidationError) as e:
            raise e

    # History and Memento controls
    def get_history(self) -> List[str]:
        entries = []
        for c in self.history.list():
            entries.append(f"{c.operation}({c.a}, {c.b}) = {c.result}")
        return entries

    def clear_history(self):
        self.history.clear()
        self.caretaker.clear()
        self.history.attach_caretaker(self.caretaker)

    def undo(self):
        try:
            self.history.undo()
        except HistoryError as e:
            raise HistoryError(f"Undo failed: {e}")

    def redo(self):
        try:
            self.history.redo()
        except HistoryError as e:
            raise HistoryError(f"Redo failed: {e}")
