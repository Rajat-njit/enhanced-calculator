"""
exceptions.py
--------------
Defines all custom exception types used throughout the calculator application.

These exceptions improve error handling clarity and ensure user-friendly messages.
"""

class CalculatorError(Exception): ...

class OperationError(CalculatorError): ...
"""Raised when an invalid or unsafe operation is attempted."""

class ValidationError(CalculatorError): ...
"""Raised when input validation fails."""

class ConfigError(CalculatorError): ...

class HistoryError(CalculatorError): ...
"""Raised when undo/redo operations fail or invalid state access occurs."""

class PersistenceError(CalculatorError): ...
