import logging
from pathlib import Path

from app.calculator import Calculator
from app.calculator_config import CalculatorConfig
from app.calculator_memento import Caretaker
from app.history import History
from app.logger import (
    configure_logger_from_config,
    LoggingObserver,
    AutoSaveObserver,
)
from app.logger import load_history_from_csv


def make_cfg(tmp_path: Path) -> CalculatorConfig:
    return CalculatorConfig(
        log_dir=str(tmp_path / "logs"),
        history_dir=str(tmp_path / "history"),
        log_file="app.log",
        history_file="history.csv",
        max_history_size=50,
        auto_save=True,
        precision=2,
        max_input_value=1_000_000.0,
        default_encoding="utf-8",
    )


def test_logging_observer_writes_log(tmp_path, caplog):
    cfg = make_cfg(tmp_path)
    logger = configure_logger_from_config(cfg)

    calc = Calculator(History(), Caretaker(), config=cfg)
    calc.register_observer(LoggingObserver(logger))

    with caplog.at_level("INFO"):
        calc.perform_operation("add", 2, 3)

    # ✅ Verify log record was actually emitted
    messages = [rec.message for rec in caplog.records]
    assert any("add" in msg and "5.0" in msg for msg in messages)


def test_autosave_observer_writes_csv(tmp_path):
    cfg = make_cfg(tmp_path)
    logger = configure_logger_from_config(cfg)

    calc = Calculator(History(), Caretaker(), config=cfg)
    calc.register_observer(LoggingObserver(logger))
    calc.register_observer(AutoSaveObserver(cfg))

    calc.perform_operation("multiply", 3, 4)  # 12
    csv_path = Path(cfg.history_dir) / cfg.history_file
    assert csv_path.exists()

    # Load back and check
    rows = load_history_from_csv(csv_path)
    assert len(rows) == 1
    row = rows[0]
    assert row.operation == "multiply"
    assert row.result == 12.0
