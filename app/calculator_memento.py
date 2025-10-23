"""Memento Pattern for Calculator (Phase 3.2)."""

from __future__ import annotations
from dataclasses import dataclass, field
from copy import deepcopy
from typing import List, Optional
from .calculation import Calculation
from .exceptions import HistoryError


@dataclass(frozen=True)
class CalculatorMemento:
    """Immutable snapshot of calculator history state."""
    state: List[Calculation] = field(default_factory=list)

    @staticmethod
    def from_history(history: List[Calculation]) -> "CalculatorMemento":
        return CalculatorMemento(deepcopy(history))


class Caretaker:
    """Manages undo and redo operations via mementos."""

    def __init__(self):
        self._undo_stack: List[CalculatorMemento] = []
        self._redo_stack: List[CalculatorMemento] = []

    # ---------------------
    # Core operations
    # ---------------------

    def save(self, memento: CalculatorMemento) -> None:
        """Save current state to undo stack; clear redo stack."""
        self._undo_stack.append(memento)
        self._redo_stack.clear()

    def undo(self, current_state: List[Calculation]) -> Optional[List[Calculation]]:
        """Revert to the previous state."""
        if not self._undo_stack:
            raise HistoryError("Nothing to undo.")
        self._redo_stack.append(CalculatorMemento.from_history(current_state))
        previous = self._undo_stack.pop()
        return deepcopy(previous.state)

    def redo(self, current_state: List[Calculation]) -> Optional[List[Calculation]]:
        """Reapply a previously undone state."""
        if not self._redo_stack:
            raise HistoryError("Nothing to redo.")
        self._undo_stack.append(CalculatorMemento.from_history(current_state))
        next_state = self._redo_stack.pop()
        return deepcopy(next_state.state)

    def clear(self) -> None:
        """Clear all stacks."""
        self._undo_stack.clear()
        self._redo_stack.clear()

    def can_undo(self) -> bool:
        return bool(self._undo_stack)

    def can_redo(self) -> bool:
        return bool(self._redo_stack)
