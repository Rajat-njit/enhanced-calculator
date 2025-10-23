"""Logging setup, observers, and CSV persistence (Phase 4.1)."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Iterable, List
from dataclasses import asdict
from datetime import datetime

import pandas as pd

from .calculation import Calculation
from .calculator_config import CalculatorConfig


# -----------------------------
# Base logging configuration
# -----------------------------
def configure_logger_from_config(cfg: CalculatorConfig) -> logging.Logger:
    Path(cfg.log_dir).mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("calculator")
    logger.setLevel(logging.INFO)
    # avoid duplicate handlers in repeated test runs
    if not any(isinstance(h, logging.FileHandler) for h in logger.handlers):
        fh = logging.FileHandler(cfg.log_path, encoding=cfg.default_encoding)
        fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        fh.setFormatter(fmt)
        logger.addHandler(fh)
    return logger


# -----------------------------
# CSV persistence helpers
# -----------------------------
def _calc_to_row(c: Calculation) -> dict:
    return {
        "timestamp": c.timestamp.isoformat(timespec="seconds"),
        "operation": c.operation,
        "a": c.a,
        "b": c.b,
        "result": c.result,
    }


def save_history_to_csv(history: Iterable[Calculation], csv_path: Path, encoding: str = "utf-8") -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    rows = [_calc_to_row(c) for c in history]
    df = pd.DataFrame(rows, columns=["timestamp", "operation", "a", "b", "result"])
    df.to_csv(csv_path, index=False, encoding=encoding)


def load_history_from_csv(csv_path: Path) -> List[Calculation]:
    if not csv_path.exists():
        return []
    df = pd.read_csv(csv_path)
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
# Observers
# -----------------------------
class LoggingObserver:
    """Observer that logs each calculation to app log."""

    def __init__(self, logger: logging.Logger):
        self._logger = logger

    def update(self, calculation: Calculation) -> None:
        self._logger.info(
            "calc: %s(%s, %s) = %s",
            calculation.operation,
            calculation.a,
            calculation.b,
            calculation.result,
        )


class AutoSaveObserver:
    """Observer that writes entire history to CSV after each calculation."""

    def __init__(self, cfg: CalculatorConfig):
        self._cfg = cfg

    def update(self, calculation: Calculation, history: Iterable[Calculation]) -> None:
        save_history_to_csv(
            history,
            self._cfg.history_path,
            encoding=self._cfg.default_encoding,
        )
