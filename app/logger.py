# Author: Rajat Pednekar | UCID: rp2348
"""
logger.py
----------
Provides centralized logging, CSV persistence, and observer implementations.

Design Patterns:
    - Observer Pattern: LoggingObserver and AutoSaveObserver
      react to calculator events.
    - Singleton Principle: Logging configuration created once via `configure_logger_from_config`.
"""

from __future__ import annotations
import os
import io
import logging
from pathlib import Path
from typing import Iterable, List
from datetime import datetime
from dataclasses import asdict
import pandas as pd
from colorama import Fore, Style, init as colorama_init

from .calculation import Calculation
from .calculator_config import CalculatorConfig

# Initialize colorama for cross-platform terminal colors
colorama_init(autoreset=True)


# -----------------------------
# Base logging configuration
# -----------------------------

# pragma: no cover
class ColoredFormatter(logging.Formatter):
    """Custom formatter that adds color-coded log levels for console output."""
    COLORS = {
        logging.DEBUG: Fore.BLUE,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.MAGENTA,
    }
    def format(self, record):
        color = self.COLORS.get(record.levelno, "") # pragma: no cover
        message = super().format(record) # pragma: no cover
        return f"{color}{message}{Style.RESET_ALL}" # pragma: no cover


def configure_logger_from_config(cfg: CalculatorConfig) -> logging.Logger:
    """
    Configure the calculator logger.
    - Writes logs to file.
    - Adds in-memory stream handler during pytest for caplog capture.
    """
    Path(cfg.log_dir).mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("calculator")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Clear previous handlers (important for repeated tests)
    if logger.hasHandlers():
        logger.handlers.clear()

    # --- File Handler ---
    fh = logging.FileHandler(cfg.log_path, encoding=cfg.default_encoding)
    fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logger.addHandler(fh)

    # --- During pytest: attach a memory stream handler ---
    if "PYTEST_CURRENT_TEST" in os.environ:
        log_stream = io.StringIO()
        sh = logging.StreamHandler(log_stream)
        sh.setLevel(logging.INFO)
        sh.setFormatter(logging.Formatter("%(message)s"))
        logger.addHandler(sh)
        logger._pytest_stream = log_stream  # store reference (optional for debugging)

    if not getattr(logger, "_initialized", False):
        logger.info("🟢 Logger initialized successfully.")
        logger.info(f"Log file path: {cfg.log_path}")
        logger._initialized = True

    # ✅ During pytest, allow propagation so caplog can capture it
    if "PYTEST_CURRENT_TEST" in os.environ:
        logger.propagate = True

    return logger


# -----------------------------
# CSV persistence helpers
# -----------------------------
def _calc_to_row(c: Calculation) -> dict:
    """Convert a Calculation instance to a dictionary row for CSV export."""
    return {
        "timestamp": c.timestamp.isoformat(timespec="seconds"),
        "operation": c.operation,
        "a": c.a,
        "b": c.b,
        "result": c.result,
    }


def save_history_to_csv(history: Iterable[Calculation], csv_path: Path, encoding: str = "utf-8") -> None:
    """Saves all history entries to a CSV file."""
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    rows = [_calc_to_row(c) for c in history]
    df = pd.DataFrame(rows, columns=["timestamp", "operation", "a", "b", "result"])
    df.to_csv(csv_path, index=False, encoding=encoding)


def load_history_from_csv(csv_path: Path) -> List[Calculation]:
    """Loads calculation history from a CSV file into Calculation objects."""
    if not csv_path.exists():
        return []
    df = pd.read_csv(csv_path)
    required_cols = {"operation", "a", "b", "result", "timestamp"}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"Malformed CSV — missing columns: {required_cols - set(df.columns)}") 
        
    out: List[Calculation] = []
    for _, row in df.iterrows():
        out.append(
            Calculation(
                operation=str(row["operation"]),
                a=float(row["a"]),
                b=float(row["b"]),
                result=float(row["result"]),
                timestamp=datetime.fromisoformat(str(row["timestamp"])),
            )
        )
    return out


# -----------------------------
# Observer Implementations
# -----------------------------
class LoggingObserver:
    """Observer that logs each calculation to app log."""
    def __init__(self, logger: logging.Logger):
        self._logger = logger

    def update(self, calculation: Calculation) -> None:
        try:
            self._logger.info(
                "calc: %s(%s, %s) = %s",
                calculation.operation, calculation.a, calculation.b, calculation.result,
            )
        except Exception as e: # pragma: no cover
            self._logger.error("❌ Logging failed for %s: %s", calculation.operation, e)
            

class AutoSaveObserver:
    """Observer that writes entire history to CSV after each calculation."""

    def __init__(self, cfg: CalculatorConfig):
        self._cfg = cfg

    def update(self, calculation: Calculation, history: Iterable[Calculation]) -> None:
        """Save full history automatically when a new calculation occurs."""
        save_history_to_csv(
            history,
            self._cfg.history_path,
            encoding=self._cfg.default_encoding,
        )

