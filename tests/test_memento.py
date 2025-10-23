import pytest
from datetime import datetime
from app.history import History
from app.calculator_memento import Caretaker
from app.calculation import Calculation
from app.exceptions import HistoryError


def make_calc(i):
    return Calculation("add", i, i, i + i, datetime.now())


def test_undo_and_redo_basic():
    h = History(max_size=5)
    c = Caretaker()
    h.attach_caretaker(c)

    for i in range(3):
        h.add(make_calc(i))
        h.record_state()

    assert len(h.list()) == 3

    h.undo()
    assert len(h.list()) == 2

    h.redo()
    assert len(h.list()) == 3


def test_undo_without_caretaker_raises():
    h = History()
    with pytest.raises(HistoryError):
        h.undo()


def test_multiple_undo_redo_operations():
    h = History()
    c = Caretaker()
    h.attach_caretaker(c)

    for i in range(4):
        h.add(make_calc(i))
        h.record_state()

    h.undo()
    h.undo()
    assert len(h.list()) == 2
    h.redo()
    assert len(h.list()) == 3


def test_redo_after_new_operation_clears_redo_stack():
    h = History()
    c = Caretaker()
    h.attach_caretaker(c)

    for i in range(2):
        h.add(make_calc(i))
        h.record_state()

    h.undo()  # back to 1 calc
    assert len(h.list()) == 1

    # Add new calc after undo
    h.add(make_calc(99))
    h.record_state()

    # Now redo stack should be cleared
    with pytest.raises(HistoryError):
        h.redo()


def test_can_undo_redo_flags():
    c = Caretaker()
    h = History()
    h.attach_caretaker(c)
    assert not c.can_redo()
    assert c.can_undo()  # one initial state saved
