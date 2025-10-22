"""Calculation entity (Phase 0 stub)."""
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Calculation:
    operation: str
    a: float
    b: float
    result: float
    timestamp: datetime
