import pytest
from app.calculator import Calculator
from app.history import History
from app.calculator_memento import Caretaker
from app.calculator_config import load_config
from app.logger import configure_logger_from_config, LoggingObserver


def test_placeholder_calculator_imports():
    from app.calculator import Calculator
    assert hasattr(Calculator, "__doc__")

import pytest
from app.calculator import Calculator
from app.history import History
from app.calculator_memento import Caretaker
from app.logger import configure_logger_from_config, LoggingObserver
from app.calculator_config import load_config

def test_calculator_undo_redo_logging(tmp_path, caplog):
    cfg = load_config()
    logger = configure_logger_from_config(cfg)
    calc = Calculator(History(), Caretaker(), config=cfg)
    calc.register_observer(LoggingObserver(logger))

    # Perform an operation so undo has something to revert
    calc.perform_operation("add", 2, 3)
    with caplog.at_level("INFO"):
        calc.undo()
        calc.redo()
    assert any("Undo" in r.message for r in caplog.records)
    assert any("Redo" in r.message for r in caplog.records)

def test_calculator_clear_history_logging(tmp_path):
    cfg = load_config()
    logger = configure_logger_from_config(cfg)
    calc = Calculator(History(), Caretaker(), config=cfg)
    calc.register_observer(LoggingObserver(logger))

    # Ensure clear_history logs once
    calc.clear_history()
    with open(cfg.log_path) as f:
        log_text = f.read()
    assert "History cleared" in log_text

def test_operation_failure_logging(tmp_path, caplog):
    cfg = load_config()
    logger = configure_logger_from_config(cfg)
    calc = Calculator(History(), Caretaker(), config=cfg)
    calc.register_observer(LoggingObserver(logger))

    with caplog.at_level("ERROR"):
        with pytest.raises(Exception):
            calc.perform_operation("divide", 5, 0)
    assert any("Operation failed" in r.message for r in caplog.records)
