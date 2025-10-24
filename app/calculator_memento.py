# Author: Rajat Pednekar | UCID: rp2348

"""
calculator_memento.py
---------------------
Implements the Memento Design Pattern for calculator state management.

The Memento pattern captures and restores an object’s internal state without
violating encapsulation, enabling undo/redo functionality.

Classes:
    CalculatorMemento: Immutable snapshot of history state.
    Caretaker: Manages stack of mementos to provide undo/redo.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from copy import deepcopy
from typing import List, Optional
from .calculation import Calculation
from .exceptions import HistoryError


@dataclass(frozen=True)
class CalculatorMemento:

    """
    Represents an immutable snapshot of the calculator's history.

    Attributes:
        items (List[Calculation]): A deep copy of the current calculation list.
    """

    state: List[Calculation] = field(default_factory=list)

    @staticmethod
    def from_history(history: List[Calculation]) -> "CalculatorMemento":
        """Creates a deep-copied memento from the current history list."""
        return CalculatorMemento(deepcopy(history))


class Caretaker:

    """
    Maintains undo and redo stacks for calculator state management.

    Methods:
        save(memento): Saves a new state snapshot.
        undo(): Reverts to the previous state.
        redo(): Restores the next state if available.
    """

    def __init__(self):
        self._undo_stack: List[CalculatorMemento] = []
        self._redo_stack: List[CalculatorMemento] = []

    def save(self, memento: CalculatorMemento) -> None:
        """
        Pushes the current state to the undo stack and clears redo history.

        Args:
            memento (CalculatorMemento): The state snapshot to save.
        """
        self._undo_stack.append(memento)
        self._redo_stack.clear()

    def undo(self, current_state: List[Calculation]) -> Optional[List[Calculation]]:
        """
        Pops the last state from the undo stack and pushes it to redo.

        Returns:
            CalculatorMemento: The previous state snapshot.

        Raises:
            HistoryError: If there is no state to undo.
        """
        if len(self._undo_stack) <= 1:
            raise HistoryError("Nothing to undo.")

        # Current state → redo stack
        self._redo_stack.append(CalculatorMemento.from_history(current_state))

        # Remove the most recent snapshot (current state)
        self._undo_stack.pop()

        # Restore the previous one
        previous = self._undo_stack[-1]
        return deepcopy(previous.state)

    def redo(self, current_state: List[Calculation]) -> Optional[List[Calculation]]:
        """
        Restores the most recently undone state.

        Returns:
            CalculatorMemento: The next available redo state.

        Raises:
            HistoryError: If there is no state to redo.
        """
        if not self._redo_stack:
            raise HistoryError("Nothing to redo.")

        # Save current to undo stack
        self._undo_stack.append(CalculatorMemento.from_history(current_state))

        # Restore next state
        next_state = self._redo_stack.pop()
        return deepcopy(next_state.state)

    def clear(self) -> None:
        """Completely clears both undo and redo stacks."""
        self._undo_stack.clear()
        self._redo_stack.clear()

    def can_undo(self) -> bool:
        """Checks if undo is available."""
        return len(self._undo_stack)

    def can_redo(self) -> bool:
        """Checks if redo is available."""
        return bool(self._redo_stack)
