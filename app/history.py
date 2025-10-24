# Author: Rajat Pednekar | UCID: rp2348

"""
history.py
-----------
Implements the History class responsible for storing and managing past calculations.
Supports undo/redo functionality via the Memento Design Pattern.

Design Pattern:
    - Memento Pattern: For state restoration via Caretaker and CalculatorMemento.
"""

from __future__ import annotations
from typing import List
from dataclasses import dataclass
import pandas as pd
from .calculation import Calculation
from .exceptions import HistoryError
from .calculator_memento import Caretaker, CalculatorMemento


@dataclass
class History:
   
    """
    Manages a list of past calculations with undo/redo functionality.

    Attributes:
        _items (list): Stored Calculation instances.
        _pointer (int): Current index pointer in history.
        max_size (int): Maximum allowed history entries.
    """

    max_size: int = 50

    def __post_init__(self):
        self._items: List[Calculation] = []
        self._pointer: int = -1  # used later for undo/redo (Phase 3.2)

    # -----------------
    # Core operations
    # -----------------

    def add(self, calc: Calculation) -> None:
        
        """
        Adds a new calculation to the history and enforces maximum size.

        Args:
            calc (Calculation): The calculation to store.

        Raises:
            HistoryError: If the provided object is not a Calculation.
        """

        if not isinstance(calc, Calculation):
            raise HistoryError("Only Calculation instances can be added to history.")

        # If we later support undo/redo, drop any "redo" entries past the pointer
        if self._pointer < len(self._items) - 1:
            self._items = self._items[: self._pointer + 1]

        self._items.append(calc)
        self._pointer = len(self._items) - 1

        # Enforce maximum size
        if len(self._items) > self.max_size:
            overflow = len(self._items) - self.max_size
            self._items = self._items[overflow:]
            self._pointer = len(self._items) - 1

    def list(self) -> List[Calculation]:
        """Return a copy of all stored calculations."""
        return list(self._items)

    def last(self) -> Calculation | None:
        """Return the last calculation if present."""
        if not self._items:
            return None
        return self._items[-1]

    def clear(self) -> None:
        """Remove all stored calculations."""
        self._items.clear()
        self._pointer = -1

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self):
        yield from self._items

    def attach_caretaker(self, caretaker: Caretaker) -> None:
        """Link a caretaker to save/restore history states."""
        self._caretaker = caretaker
        # capture initial empty state
        caretaker.save(CalculatorMemento.from_history(self._items))

    def record_state(self) -> None:
        """Store the current state snapshot in caretaker."""
        if hasattr(self, "_caretaker"):
            self._caretaker.save(CalculatorMemento.from_history(self._items))

    def undo(self) -> None:
        """Revert to previous state."""
        if not hasattr(self, "_caretaker"):
            raise HistoryError("Caretaker not attached.")
        new_state = self._caretaker.undo(self._items)
        self._items = new_state or []
        self._pointer = len(self._items) - 1

    def redo(self) -> None:
        """Reapply an undone state."""
        if not hasattr(self, "_caretaker"):
            raise HistoryError("Caretaker not attached.")
        new_state = self._caretaker.redo(self._items)
        self._items = new_state or []
        self._pointer = len(self._items) - 1

    # --------------------------------------------
    # Persistence methods
    # --------------------------------------------
    def save_to_csv(self, file_path: str, encoding: str = "utf-8") -> None:
        """Save all calculations to a CSV file."""
        try:
            rows = [
                {
                    "timestamp": c.timestamp.isoformat(timespec="seconds"),
                    "operation": c.operation,
                    "a": c.a,
                    "b": c.b,
                    "result": c.result,
                }
                for c in self._items
            ]
            df = pd.DataFrame(rows)
            df.to_csv(file_path, index=False, encoding=encoding)
        except Exception as e:
            raise HistoryError(f"Failed to save history: {e}")

    def load_from_csv(self, file_path: str, encoding: str = "utf-8") -> None:
        """Load calculations from a CSV file and replace current history."""
        try:
            df = pd.read_csv(file_path, encoding=encoding)
            new_items = []
            for _, row in df.iterrows():
                new_items.append(
                    Calculation(
                        operation=str(row["operation"]),
                        a=float(row["a"]),
                        b=float(row["b"]),
                        result=float(row["result"]),
                        timestamp=pd.to_datetime(row["timestamp"]).to_pydatetime(),
                    )
                )
            self._items = new_items
            # refresh caretaker state if present
            if hasattr(self, "_caretaker") and self._caretaker:
                self._caretaker.clear()
                self.record_state()

        except FileNotFoundError:
            raise HistoryError(f"History file '{file_path}' not found.")
        except Exception as e:
            raise HistoryError(f"Failed to load history: {e}")