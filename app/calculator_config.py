# Author: Rajat Pednekar | UCID: rp2348

"""
calculator_config.py
--------------------
Handles all configuration management for the calculator application.
Loads environment variables via `python-dotenv` and provides validation.

Design Pattern:
    - Singleton-like behavior (configuration loaded once and reused).
"""

from dataclasses import dataclass
from pathlib import Path
import os
from dotenv import load_dotenv
from .exceptions import ConfigError


@dataclass(frozen=True)
class CalculatorConfig:

    """
    Holds all calculator configuration parameters loaded from environment variables.

    Attributes:
        log_dir (str): Directory for logs.
        history_dir (str): Directory for history CSVs.
        precision (int): Decimal precision for results.
        max_input_value (float): Max allowed absolute input value.
        max_history_size (int): Max number of history entries.
        auto_save (bool): Whether auto-save is enabled.
        default_encoding (str): Encoding for file I/O.
    """

    log_dir: str = "logs"
    history_dir: str = "history"
    log_file: str = "app.log"
    history_file: str = "history.csv"
    max_history_size: int = 50
    auto_save: bool = True
    precision: int = 2
    max_input_value: float = 1_000_000.0
    default_encoding: str = "utf-8"

    @property
    def log_path(self) -> Path:
        """Returns the full path for the log file."""
        return Path(self.log_dir) / self.log_file

    @property
    def history_path(self) -> Path:
        """Returns the full path for the history CSV file."""
        return Path(self.history_dir) / self.history_file

def _to_bool(val: str) -> bool:
    return str(val).strip().lower() in {"1", "true", "yes", "y", "on"}

def load_config(env_path: str = ".env") -> CalculatorConfig:
    
    """
    Loads configuration from environment variables with validation and defaults.

    Returns:
        CalculatorConfig: Loaded and validated configuration instance.

    Raises:
        ConfigError: If any configuration value is invalid.
    """

    load_dotenv(env_path, override=False)

    try:
        log_dir = os.getenv("CALCULATOR_LOG_DIR", "logs")
        history_dir = os.getenv("CALCULATOR_HISTORY_DIR", "history")
        log_file = os.getenv("CALCULATOR_LOG_FILE", "app.log")
        history_file = os.getenv("CALCULATOR_HISTORY_FILE", "history.csv")

        max_history_size = int(os.getenv("CALCULATOR_MAX_HISTORY_SIZE", "50"))
        auto_save = _to_bool(os.getenv("CALCULATOR_AUTO_SAVE", "true"))
        precision = int(os.getenv("CALCULATOR_PRECISION", "2"))
        max_input_value = float(os.getenv("CALCULATOR_MAX_INPUT_VALUE", "1000000"))
        default_encoding = os.getenv("CALCULATOR_DEFAULT_ENCODING", "utf-8")

        # basic validation
        if precision < 0 or precision > 12:
            raise ConfigError("CALCULATOR_PRECISION must be between 0 and 12")
        if max_history_size < 0:
            raise ConfigError("CALCULATOR_MAX_HISTORY_SIZE must be >= 0")
        if max_input_value <= 0:
            raise ConfigError("CALCULATOR_MAX_INPUT_VALUE must be > 0")

        Path(log_dir).mkdir(parents=True, exist_ok=True)
        Path(history_dir).mkdir(parents=True, exist_ok=True)

        return CalculatorConfig(
            log_dir=log_dir,
            history_dir=history_dir,
            log_file=log_file,
            history_file=history_file,
            max_history_size=max_history_size,
            auto_save=auto_save,
            precision=precision,
            max_input_value=max_input_value,
            default_encoding=default_encoding,
        )
    except ValueError as e:
        raise ConfigError(f"Invalid numeric configuration: {e}") from e
