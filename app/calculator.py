# Author: Rajat Pednekar | UCID: rp2348

"""
calculator.py
--------------
Defines the core Calculator class that orchestrates operations, history management,
state restoration, and observer notifications.

Design Patterns:
    - Factory Pattern: For creating operations dynamically.
    - Memento Pattern: For undo/redo via History and Caretaker.
    - Observer Pattern: For logging and auto-save triggers.
"""

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
   
    """
    Core Calculator class that performs operations, manages history,
    and coordinates observers.

    Attributes:
        config (CalculatorConfig): Loaded application configuration.
        history (History): Manages calculation records and undo/redo.
        caretaker (Caretaker): Handles saved states for undo/redo.
        _observers (list): Registered observer instances.
    """

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
        """Registers an observer that reacts to calculation updates."""
        self.observers.append(observer)

    def _notify_observers(self, calc: Calculation) -> None:
        """Notifies all observers after a calculation is completed."""
        for obs in self.observers:
            try:
                # Prefer (calculation, history) signature
                obs.update(calc, self.history.list())
            except TypeError:
                # Fallback to (calculation) signature
                obs.update(calc)

    # -------------------------
    # Core Operation Execution
    # -------------------------

    def perform_operation(self, operation_name: str, a, b) -> float:
        """
        Executes an arithmetic operation and records it in history.

        Args:
            name (str): Name of the operation (e.g., "add", "divide").
            a (float): First operand.
            b (float): Second operand.

        Returns:
            float: Computed result rounded to configured precision.

        Raises:
            OperationError: If the operation is invalid or fails.
        """
        try:
            calc = Calculation.create(operation_name, a, b, self.config)
            self.history.add(calc)
            self.history.record_state()
            # Notify observers only after success
            self._notify_observers(calc)
            return calc.result
        except (OperationError, ValidationError) as e:
            log = self._get_logger()
            if log:
                log.error("❌ Operation failed: %s(%r, %r) | %s", # pragma: no cover
                        operation_name, a, b, e)
            raise

    # -------------------------
    # History Manipulation
    # -------------------------

    def get_history(self) -> List[str]:
        """Returns the full calculation history."""
        entries = []
        for c in self.history.list():
            entries.append(f"{c.operation}({c.a}, {c.b}) = {c.result}")
        return entries

    def clear_history(self):
        """Clears all calculation records and caretaker states."""
        self.history.clear()
        self.caretaker.clear()
        self.history.attach_caretaker(self.caretaker)
        log = self._get_logger()
        if log:
            log.info("🧹 History cleared by user.") # pragma: no cover
    # -------------------------
    # Undo/Redo Commands
    # -------------------------

    def undo(self):
        """Restores the previous calculation state."""
        try:
            self.history.undo()
            log = self._get_logger()
            if log:
                log.info("↩️  Undo applied.") # pragma: no cover
        except HistoryError as e:
            log = self._get_logger()
            if log:
                log.warning("⚠️  Undo failed: %s", e)
            raise HistoryError(f"Undo failed: {e}")

    def redo(self):
        """Restores the next calculation state."""
        try:
            self.history.redo()
            log = self._get_logger()
            if log:
                log.info("↪️  Redo applied.") # pragma: no cover
        except HistoryError as e:
            log = self._get_logger()
            if log:
                log.warning("⚠️  Redo failed: %s", e)
            raise HistoryError(f"Redo failed: {e}")

    def _get_logger(self):
        """Return the LoggingObserver's logger if present, else None."""
        for obs in self.observers:
            if hasattr(obs, "_logger"):
                return obs._logger
        return None
