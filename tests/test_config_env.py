import os
from app.calculator_config import load_config, CalculatorConfig
from app.exceptions import ConfigError

def test_default_config_loads_when_env_missing(monkeypatch, tmp_path):
    # Clear env vars
    for key in list(os.environ.keys()):
        if key.startswith("CALCULATOR_"):
            monkeypatch.delenv(key, raising=False)

    cfg = load_config()
    assert isinstance(cfg, CalculatorConfig)
    assert cfg.log_dir == "logs"
    assert cfg.precision == 2
    assert cfg.auto_save is True


def test_env_overrides(monkeypatch, tmp_path):
    monkeypatch.setenv("CALCULATOR_PRECISION", "5")
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "false")
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path))

    cfg = load_config()
    assert cfg.precision == 5
    assert cfg.auto_save is False
    assert cfg.log_dir == str(tmp_path)


def test_invalid_values_raise(monkeypatch):
    monkeypatch.setenv("CALCULATOR_PRECISION", "-1")
    try:
        load_config()
    except ConfigError as e:
        assert "PRECISION" in str(e)
