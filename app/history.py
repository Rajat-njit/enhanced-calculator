"""History management (Phase 3.1).

Stores and manages Calculation records with optional size limits.
"""

from __future__ import annotations
from typing import List
from dataclasses import dataclass
from .calculation import Calculation
from .exceptions import HistoryError


@dataclass
class History:
    """Container for storing past calculations."""
    max_size: int = 50

    def __post_init__(self):
        self._items: List[Calculation] = []
        self._pointer: int = -1  # used later for undo/redo (Phase 3.2)

    # -----------------
    # Core operations
    # -----------------

    def add(self, calc: Calculation) -> None:
        """Add a new calculation to history, respecting size limit."""
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
