"""Operations + Factory (Phase 0 stub)."""
from typing import Protocol

class Operation(Protocol):
    def __call__(self, a: float, b: float) -> float: ...

class OperationFactory:
    @staticmethod
    def create(name: str) -> Operation:
        raise NotImplementedError  # implemented in Phase 1
