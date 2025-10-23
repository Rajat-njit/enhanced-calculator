import pytest
from app.calculator import Calculator
from app.history import History
from app.calculator_memento import Caretaker
from app.exceptions import HistoryError, ValidationError


def make_calculator():
    return Calculator(History(), Caretaker())


def test_basic_operation_and_history():
    calc = make_calculator()
    result = calc.perform_operation("add", 2, 3)
    assert result == 5.0
    history = calc.get_history()
    assert len(history) == 1
    assert "add(2.0, 3.0)" in history[0]


def test_multiple_operations_and_undo_redo():
    calc = make_calculator()
    calc.perform_operation("add", 1, 1)
    calc.perform_operation("multiply", 2, 3)
    calc.perform_operation("subtract", 10, 4)

    assert len(calc.history.list()) == 3
    calc.undo()
    assert len(calc.history.list()) == 2
    calc.redo()
    assert len(calc.history.list()) == 3


def test_clear_history_resets_all():
    calc = make_calculator()
    calc.perform_operation("add", 1, 2)
    calc.perform_operation("power", 2, 3)
    calc.clear_history()
    assert len(calc.history.list()) == 0
    assert not calc.caretaker.can_redo()
    assert calc.caretaker.can_undo()


def test_invalid_operation_raises():
    calc = make_calculator()
    with pytest.raises(ValidationError):
        calc.perform_operation("add", "a", 3)


def test_undo_redo_without_history_raises():
    calc = make_calculator()
    with pytest.raises(HistoryError):
        calc.undo()
    with pytest.raises(HistoryError):
        calc.redo()
