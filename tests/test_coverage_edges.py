import os
import math
import pytest
from datetime import datetime
from app.calculation import Calculation
from app.calculator_config import load_config, ConfigError
from app.history import History
from app.calculator_memento import Caretaker
from app.logger import configure_logger_from_config
from app.calculator_config import load_config
from app.input_validators import validate_inputs
from app.operations import OperationFactory
from app.exceptions import OperationError, ValidationError
from app.exceptions import HistoryError


def make_calc(i=1):
    """Utility to quickly create a Calculation object for tests."""
    return Calculation(
        operation="add",
        a=float(i),
        b=float(i + 1),
        result=float(i + (i + 1)),
        timestamp=datetime.now(),
    )
# ---- Calculation Fallbacks ----
def test_calculation_fallback(monkeypatch):
    def bad_create(_): raise Exception("Boom")
    monkeypatch.setattr(OperationFactory, "create", staticmethod(lambda op: bad_create))
    cfg = load_config()
    with pytest.raises(OperationError):
        Calculation.create("add", 1, 2, cfg)

# ---- Config Errors ----
def test_invalid_precision(monkeypatch):
    monkeypatch.setenv("CALCULATOR_PRECISION", "-2")
    with pytest.raises(ConfigError):
        load_config()

def test_invalid_max_value(monkeypatch):
    monkeypatch.setenv("CALCULATOR_MAX_INPUT_VALUE", "0")
    with pytest.raises(ConfigError):
        load_config()

def test_invalid_history_size(monkeypatch):
    monkeypatch.setenv("CALCULATOR_MAX_HISTORY_SIZE", "-1")
    with pytest.raises(ConfigError):
        load_config()

# ---- History Edge Cases ----
def test_history_save_load_exceptions(tmp_path):
    h = History()
    bad_path = tmp_path / "no_dir" / "file.csv"
    with pytest.raises(Exception):
        h.save_to_csv(bad_path)

    # Load with missing file
    with pytest.raises(Exception):
        h.load_from_csv(tmp_path / "missing.csv")

def test_history_with_no_caretaker():
    h = History()
    h._items = []  # no caretaker attached
    h.record_state()
    with pytest.raises(HistoryError):
        h.undo()

# ---- Input Validator Edge Cases ----
def test_validator_invalid_numeric():
    with pytest.raises(ValidationError):
        validate_inputs("add", "abc", 3, 100)

def test_validator_nan_and_inf():
    with pytest.raises(ValidationError):
        validate_inputs("divide", float("nan"), 1, 100)
    with pytest.raises(ValidationError):
        validate_inputs("divide", float("inf"), 1, 100)

def test_validator_out_of_range():
    with pytest.raises(ValidationError):
        validate_inputs("add", 1_000_001, 2, 1_000_000)

def test_validator_invalid_root_inputs():
    with pytest.raises(OperationError):
        validate_inputs("root", 4, 0, 1_000_000)

def test_logger_reuse():
    cfg = load_config()
    log1 = configure_logger_from_config(cfg)
    log2 = configure_logger_from_config(cfg)
    assert log1 is log2  # logger is cached by name in logging module


# ---- Operation Edge Cases ----
def test_operation_factory_invalid():
    with pytest.raises(OperationError):
        OperationFactory.create("invalid_op")

def test_divide_by_zero():
    op = OperationFactory.create("divide")
    with pytest.raises(OperationError):
        op(5, 0)

def test_history_save_fails(monkeypatch, tmp_path):
    """Force History.save_to_csv to hit generic exception block."""
    h = History()
    bad_path = tmp_path / "bad.csv"
    # Monkeypatch pandas.DataFrame to throw an exception
    import pandas as pd
    monkeypatch.setattr(pd, "DataFrame", lambda *a, **kw: (_ for _ in ()).throw(Exception("boom")))
    with pytest.raises(HistoryError):
        h.save_to_csv(bad_path)

def test_history_load_fails(monkeypatch, tmp_path):
    """Force History.load_from_csv to hit generic exception block."""
    h = History()
    import pandas as pd
    monkeypatch.setattr(pd, "read_csv", lambda *a, **kw: (_ for _ in ()).throw(Exception("boom")))
    with pytest.raises(HistoryError):
        h.load_from_csv(tmp_path / "fake.csv")

def test_invalid_config_valueerror(monkeypatch):
    """Force ValueError in load_config."""
    monkeypatch.setenv("CALCULATOR_PRECISION", "abc")
    from app.calculator_config import load_config, ConfigError
    with pytest.raises(ConfigError):
        load_config()

def test_validator_invalid_type():
    """Trigger ValidationError by passing non-numeric strings."""
    from app.input_validators import validate_inputs
    with pytest.raises(ValidationError):
        validate_inputs("add", "x", "y", 100)

def test_validator_division_by_zero():
    """Force OperationError by dividing by zero."""
    from app.input_validators import validate_inputs
    with pytest.raises(OperationError):
        validate_inputs("divide", 10, 0, 1000)

def test_calculation_unexpected_error(monkeypatch):
    """Force Calculation.create() to hit generic exception path."""
    cfg = load_config()

    # Patch OperationFactory.create to raise unexpected exception
    def bad_factory(_): raise RuntimeError("weird math fail")
    monkeypatch.setattr(OperationFactory, "create", staticmethod(bad_factory))

    with pytest.raises(OperationError) as exc:
        Calculation.create("add", 1, 2, cfg)
    assert "weird math fail" in str(exc.value)


def test_history_undo_redo_empty_and_errors():
    """Trigger undo/redo fallback lines."""
    h = History()
    # no caretaker attached → direct HistoryError
    with pytest.raises(HistoryError):
        h.undo()
    with pytest.raises(HistoryError):
        h.redo()


def test_history_record_state_and_clear(tmp_path):
    """Force History record_state & caretaker reset branches."""
    h = History()
    c = Caretaker()
    h.attach_caretaker(c)
    h.add(make_calc(1))
    h.record_state()
    c.clear()
    assert not c.can_undo()
    assert not c.can_redo()


def test_history_load_generic_exception(monkeypatch, tmp_path):
    """Force generic exception in History.load_from_csv."""
    h = History()
    import pandas as pd
    monkeypatch.setattr(pd, "read_csv", lambda *a, **kw: (_ for _ in ()).throw(Exception("read fail")))
    with pytest.raises(HistoryError):
        h.load_from_csv(tmp_path / "fake.csv")


def test_validator_edge_cases(monkeypatch):
    """Cover final guard clauses in input_validators."""
    from app.input_validators import validate_inputs

    # 1. negative root with even degree (invalid)
    with pytest.raises(OperationError):
        validate_inputs("root", -16, 2, 10000)

    # 2. out-of-bound high value for percentage
    with pytest.raises(ValidationError):
        validate_inputs("percent", 999999999, 10, 1_000_000)

    # 3. invalid modulus with zero divisor
    with pytest.raises(OperationError):
        validate_inputs("modulus", 10, 0, 1000)


def test_logger_duplicate_handler(monkeypatch, tmp_path):
    """Force logger duplicate handler path (line 55)."""
    cfg = load_config()
    logger1 = configure_logger_from_config(cfg)
    # Call again to trigger "duplicate handler" skip branch
    logger2 = configure_logger_from_config(cfg)
    assert logger1 is logger2


def test_operations_invalid_division(monkeypatch):
    """Force division by zero in operation itself."""
    div_op = OperationFactory.create("divide")
    with pytest.raises(OperationError):
        div_op(10, 0)


def test_operations_unknown(monkeypatch):
    """Force unknown operation in OperationFactory."""
    monkeypatch.setattr(OperationFactory, "_registry", {})
    with pytest.raises(OperationError):
        OperationFactory.create("not_a_real_op")

def test_calculation_generic_exception(monkeypatch):
    """Covers unexpected exception branch in Calculation.create()."""
    from app.calculation import Calculation
    from app.calculator_config import load_config
    from app.operations import OperationFactory
    from app.exceptions import OperationError

    cfg = load_config()

    def broken_factory(_):
        raise RuntimeError("boom")

    monkeypatch.setattr(OperationFactory, "create", staticmethod(broken_factory))

    with pytest.raises(OperationError):
        Calculation.create("add", 1, 2, cfg)


def test_history_undo_redo_and_load(monkeypatch, tmp_path):
    """Cover fallback and refresh branches in History."""
    from app.history import History
    from app.calculator_memento import Caretaker
    from app.exceptions import HistoryError
    import pandas as pd
    from datetime import datetime
    from app.calculation import Calculation

    h = History()
    # undo/redo without caretaker
    with pytest.raises(HistoryError):
        h.undo()
    with pytest.raises(HistoryError):
        h.redo()

    # simulate proper caretaker and state reset
    c = Caretaker()
    h.attach_caretaker(c)
    h._items = [
        Calculation("add", 1, 2, 3, datetime.now()),
        Calculation("sub", 5, 2, 3, datetime.now()),
    ]
    h.record_state()
    c.clear()  # triggers clear state
    h.record_state()

    # force load_from_csv generic refresh branch
    df = pd.DataFrame([
        {"timestamp": datetime.now().isoformat(timespec="seconds"),
         "operation": "add", "a": 1, "b": 2, "result": 3}
    ])
    csv_path = tmp_path / "hist.csv"
    df.to_csv(csv_path, index=False)
    h.load_from_csv(csv_path)


def test_history_undo_redo_and_load(monkeypatch, tmp_path):
    """Cover fallback and refresh branches in History."""
    from app.history import History
    from app.calculator_memento import Caretaker
    from app.exceptions import HistoryError
    import pandas as pd
    from datetime import datetime
    from app.calculation import Calculation

    h = History()
    # undo/redo without caretaker
    with pytest.raises(HistoryError):
        h.undo()
    with pytest.raises(HistoryError):
        h.redo()

    # simulate proper caretaker and state reset
    c = Caretaker()
    h.attach_caretaker(c)
    h._items = [
        Calculation("add", 1, 2, 3, datetime.now()),
        Calculation("sub", 5, 2, 3, datetime.now()),
    ]
    h.record_state()
    c.clear()  # triggers clear state
    h.record_state()

    # force load_from_csv generic refresh branch
    df = pd.DataFrame([
        {"timestamp": datetime.now().isoformat(timespec="seconds"),
         "operation": "add", "a": 1, "b": 2, "result": 3}
    ])
    csv_path = tmp_path / "hist.csv"
    df.to_csv(csv_path, index=False)
    h.load_from_csv(csv_path)

def test_input_validators_uncovered():
    """Hit every validation guard branch."""
    from app.input_validators import validate_inputs
    from app.exceptions import ValidationError, OperationError

    # invalid modulus divisor
    with pytest.raises(OperationError):
        validate_inputs("modulus", 10, 0, 1000)

    # negative root even degree
    with pytest.raises(OperationError):
        validate_inputs("root", -4, 2, 10000)

    # overflow beyond max_input_value
    with pytest.raises(ValidationError):
        validate_inputs("add", 1_000_001, 5, 1_000_000)

def test_logger_duplicate_handler(tmp_path):
    """Cover duplicate FileHandler guard branch."""
    from app.logger import configure_logger_from_config
    from app.calculator_config import load_config

    cfg = load_config()
    logger1 = configure_logger_from_config(cfg)
    # call again — ensures no duplicate handlers added
    logger2 = configure_logger_from_config(cfg)
    assert logger1 is logger2

def test_operations_invalid_cases():
    """Covers OperationFactory invalid op and division by zero."""
    from app.operations import OperationFactory
    from app.exceptions import OperationError

    # unknown op
    with pytest.raises(OperationError):
        OperationFactory.create("not_real_op")

    # divide by zero
    divide = OperationFactory.create("divide")
    with pytest.raises(OperationError):
        divide(5, 0)

def test_calculation_infinite_result(monkeypatch):
    """Force Calculation.create to hit ValidationError for non-finite result."""
    from app.calculation import Calculation
    from app.operations import OperationFactory
    from app.exceptions import ValidationError
    cfg = load_config()

    class FakeOp:
        def __call__(self, a, b):
            return float('inf')

    monkeypatch.setattr(OperationFactory, "create", staticmethod(lambda _: FakeOp()))
    with pytest.raises(ValidationError):
        Calculation.create("add", 1, 2, cfg)

def test_history_record_state_no_caretaker():
    """Explicitly call record_state with no caretaker to hit silent branch."""
    h = History()
    h.add(make_calc(1))
    # should not raise, just no caretaker
    h.record_state()

def test_input_validator_cast_failure():
    """Covers ValueError raised during float conversion."""
    with pytest.raises(ValidationError):
        validate_inputs("add", "NaNish", "oops", 1000)

def test_logger_duplicate_guard_persistent(tmp_path):
    """Ensures duplicate FileHandler skip branch executes."""
    cfg = load_config()
    logger = configure_logger_from_config(cfg)
    # Force-add a FileHandler manually, then reconfigure
    import logging
    logger.addHandler(logging.FileHandler(cfg.log_path))
    logger2 = configure_logger_from_config(cfg)
    assert logger2 is logger

def test_history_no_caretaker_branches():
    """Covers undo/redo/record_state when no caretaker is attached."""
    from app.history import History
    from app.exceptions import HistoryError
    from datetime import datetime
    from app.calculation import Calculation

    h = History()
    h.add(Calculation("add", 1, 2, 3, datetime.now()))

    # record_state() should silently return
    h.record_state()

    # undo/redo should raise HistoryError
    with pytest.raises(HistoryError):
        h.undo()
    with pytest.raises(HistoryError):
        h.redo()

def test_input_validators_all_guards():
    """Trigger all remaining validation guard branches."""
    from app.input_validators import validate_inputs
    from app.exceptions import ValidationError, OperationError

    # Non-numeric strings → float() ValueError → ValidationError
    with pytest.raises(ValidationError):
        validate_inputs("add", "abc", "xyz", 1000)

    # Root: negative base with even degree
    with pytest.raises(OperationError):
        validate_inputs("root", -9, 2, 1_000_000)

    # Root: zero degree
    with pytest.raises(OperationError):
        validate_inputs("root", 9, 0, 1_000_000)

    # Modulus: zero divisor
    with pytest.raises(OperationError):
        validate_inputs("modulus", 10, 0, 1_000_000)

    # Overflow beyond max_input_value
    with pytest.raises(ValidationError):
        validate_inputs("add", 1_000_001, 1, 1_000_000)

def test_logger_duplicate_filehandler_guard(tmp_path):
    """Cover the FileHandler duplication guard branch."""
    from app.logger import configure_logger_from_config
    from app.calculator_config import load_config
    import logging

    cfg = load_config()
    logger = configure_logger_from_config(cfg)
    # Manually add a FileHandler to trigger guard skip
    logger.addHandler(logging.FileHandler(cfg.log_path))
    logger2 = configure_logger_from_config(cfg)
    assert logger2 is logger

def test_operations_final_guards():
    """Cover unknown operation and divide-by-zero branches."""
    from app.operations import OperationFactory
    from app.exceptions import OperationError

    with pytest.raises(OperationError):
        OperationFactory.create("not_real_operation")

    divide = OperationFactory.create("divide")
    with pytest.raises(OperationError):
        divide(10, 0)

def test_history_no_caretaker_paths():
    """Hit undo/redo/record_state when no caretaker is attached."""
    from app.history import History
    from app.exceptions import HistoryError
    from datetime import datetime
    from app.calculation import Calculation

    h = History()
    h.add(Calculation("add", 1, 2, 3, datetime.now()))

    # record_state() should silently pass
    h.record_state()

    # undo and redo should raise
    with pytest.raises(HistoryError):
        h.undo()
    with pytest.raises(HistoryError):
        h.redo()

def test_input_validators_full_guard_suite():
    """Trigger every uncovered guard branch in input_validators."""
    from app.input_validators import validate_inputs
    from app.exceptions import ValidationError, OperationError

    # Bad type conversion
    with pytest.raises(ValidationError):
        validate_inputs("add", "foo", "bar", 1000)

    # Negative root even degree
    with pytest.raises(OperationError):
        validate_inputs("root", -16, 2, 1_000_000)

    # Zero-degree root
    with pytest.raises(OperationError):
        validate_inputs("root", 9, 0, 1_000_000)

    # Zero divisor modulus
    with pytest.raises(OperationError):
        validate_inputs("modulus", 9, 0, 1_000_000)

    # Overflow beyond max limit
    with pytest.raises(ValidationError):
        validate_inputs("add", 1_000_001, 5, 1_000_000)

def test_logger_duplicate_guard_persistent(tmp_path):
    """Cover duplicate FileHandler guard branch (logger.py:55)."""
    from app.logger import configure_logger_from_config
    from app.calculator_config import load_config
    import logging

    cfg = load_config()
    logger = configure_logger_from_config(cfg)
    # Manually attach FileHandler → ensures skip path executes
    logger.addHandler(logging.FileHandler(cfg.log_path))
    logger2 = configure_logger_from_config(cfg)
    assert logger2 is logger


def test_operations_remaining_guards():
    """Cover unknown op and divide-by-zero branches."""
    from app.operations import OperationFactory
    from app.exceptions import OperationError

    # Unknown operation
    with pytest.raises(OperationError):
        OperationFactory.create("imaginary_op")

    # Divide-by-zero inside operation
    divide = OperationFactory.create("divide")
    with pytest.raises(OperationError):
        divide(42, 0)

def test_history_size_limit_and_empty_last():
    """Covers size-limit trim and last() early return in History."""
    from app.history import History
    from app.calculation import Calculation
    from datetime import datetime

    h = History(max_size=3)
    # Fill beyond limit → triggers overflow trim (line 37)
    for i in range(5):
        h.add(Calculation("add", i, i + 1, i + (i + 1), datetime.now()))
    assert len(h.list()) == 3  # should have trimmed to max_size

    # Empty the history → covers last() early return (line 55)
    h.clear()
    assert h.last() is None

def test_history_record_state_no_caretaker():
    """Covers record_state() branch when no caretaker is attached (line 67)."""
    from app.history import History
    from datetime import datetime
    from app.calculation import Calculation

    h = History()
    h.add(Calculation("add", 1, 2, 3, datetime.now()))
    # No caretaker attached → skip branch executes
    h.record_state()

def test_validate_numeric_and_root_guards():
    """Covers NaN/Inf branch in validate_numeric and all root guard errors."""
    import math
    from app.input_validators import validate_numeric, validate_root
    from app.exceptions import ValidationError, OperationError

    # NaN and Inf → ValidationError (line 26)
    with pytest.raises(ValidationError):
        validate_numeric(math.nan, 5)
    with pytest.raises(ValidationError):
        validate_numeric(5, math.inf)

    # Zero-degree root → OperationError (line 56)
    with pytest.raises(OperationError):
        validate_root(4, 0)

    # Even root of negative number → OperationError (line 60)
    with pytest.raises(OperationError):
        validate_root(-16, 2)

    # Odd root of negative number → should **not** raise
    validate_root(-27, 3)

def test_check_numbers_invalid_finite_values():
    """Covers _check_numbers branch where a or b is not finite (operations.py:22)."""
    from app.operations import _check_numbers
    from app.exceptions import OperationError
    import math

    # NaN input
    with pytest.raises(OperationError):
        _check_numbers(math.nan, 2.0)

    # Infinite input
    with pytest.raises(OperationError):
        _check_numbers(1.0, math.inf)


def test_root_even_negative_branch():
    """Covers Root even-negative-number branch (operations.py:78)."""
    from app.operations import Root
    from app.exceptions import OperationError

    r = Root()

    # Even root of negative number should raise
    with pytest.raises(OperationError):
        r(-16, 2)

    # Odd root of negative number should succeed
    assert pytest.approx(r(-27, 3)) == -3

def test_history_overflow_and_record_state_no_caretaker():
    """Cover history overflow trim (line 37) and record_state() w/o caretaker (line 67)."""
    from app.history import History
    from app.calculation import Calculation
    from datetime import datetime

    # Overflow beyond max_size → triggers trim
    h = History(max_size=2)
    for i in range(4):
        h.add(Calculation("add", i, i + 1, i + (i + 1), datetime.now()))
    assert len(h.list()) == 2

    # record_state() when caretaker not attached (skips branch)
    h.record_state()

def test_validate_root_full_branch():
    """Covers all validate_root() conditions (lines 56–64)."""
    from app.input_validators import validate_root
    from app.exceptions import OperationError

    # Zero-degree root
    with pytest.raises(OperationError):
        validate_root(4, 0)

    # Even root of negative number
    with pytest.raises(OperationError):
        validate_root(-16, 2)

    # Odd root of negative number — should pass
    validate_root(-27, 3)


def test_logger_duplicate_handler_branch():
    """Covers duplicate FileHandler guard (logger.py:55)."""
    from app.logger import configure_logger_from_config
    from app.calculator_config import load_config

    cfg = load_config()
    logger1 = configure_logger_from_config(cfg)
    # Call again — duplicate handler should be skipped
    logger2 = configure_logger_from_config(cfg)
    assert logger1 is logger2

def test_root_even_negative_number():
    """Covers even root of negative number in Root.__call__ (operations.py:78)."""
    from app.operations import Root
    from app.exceptions import OperationError

    r = Root()
    with pytest.raises(OperationError):
        r(-9, 2)


def test_history_overflow_and_record_state_without_caretaker():
    """Hit overflow trim (37) and record_state without caretaker (67)."""
    from app.history import History
    from app.calculation import Calculation
    from datetime import datetime

    h = History(max_size=2)
    # overflow: add 3 items into size-2 history → trims oldest
    for i in range(3):
        h.add(Calculation("add", i, i + 1, i + (i + 1), datetime.now()))
    assert len(h.list()) == 2

    # record_state with no caretaker attached → skip branch
    h.record_state()

def test_validate_root_all_branches():
    """Cover zero-degree, even-negative, and odd-negative root cases (56-64)."""
    from app.input_validators import validate_root
    from app.exceptions import OperationError

    # Zero-degree root
    with pytest.raises(OperationError):
        validate_root(4, 0)

    # Even root of negative
    with pytest.raises(OperationError):
        validate_root(-9, 2)

    # Odd root of negative (valid path)
    validate_root(-27, 3)

def test_root_even_negative_branch_operations():
    """Hit even-root-of-negative branch in Root.__call__ (78)."""
    from app.operations import Root
    from app.exceptions import OperationError

    r = Root()
    with pytest.raises(OperationError):
        r(-16, 2)

def test_history_force_overflow_and_no_caretaker_branch(monkeypatch):
    """Explicitly trigger overflow trim and record_state false branch."""
    from app.history import History
    from app.calculation import Calculation
    from datetime import datetime

    h = History(max_size=1)
    # Force overflow trim
    for i in range(3):
        h.add(Calculation("add", i, i + 1, i + i + 1, datetime.now()))
    assert len(h) == 1  # triggers line 37

    # record_state when caretaker missing → skip hasattr() true path
    if hasattr(h, "_caretaker"):
        delattr(h, "_caretaker")
    h.record_state()  # triggers line 67

def test_validate_root_all_edge_paths():
    """Force every branch of validate_root (56–64)."""
    from app.input_validators import validate_root
    from app.exceptions import OperationError

    # Zero-degree
    with pytest.raises(OperationError):
        validate_root(5, 0)

    # Even root of negative
    with pytest.raises(OperationError):
        validate_root(-8, 2)

    # Odd root (valid)
    validate_root(-27, 3)


def test_logger_duplicate_handler_guard_branch():
    """Trigger duplicate FileHandler guard (line 55)."""
    from app.logger import configure_logger_from_config
    from app.calculator_config import load_config

    cfg = load_config()
    log1 = configure_logger_from_config(cfg)
    # Calling again should skip creating new handler
    log2 = configure_logger_from_config(cfg)
    assert log1 is log2

def test_root_even_negative_branch_operations_final():
    """Covers even-root-of-negative-number branch (line 78)."""
    from app.operations import Root
    from app.exceptions import OperationError

    root_op = Root()
    with pytest.raises(OperationError):
        root_op(-16, 2)

def test_history_overflow_and_record_state_without_caretaker():
    """Covers history.py:37 (overflow trim) and :67 (record_state no caretaker)."""
    from app.history import History
    from app.calculation import Calculation
    from datetime import datetime

    # Force overflow: max_size=1, add 3 → trims to 1 (executes line 37)
    h = History(max_size=1)
    for i in range(3):
        h.add(Calculation("add", i, i + 1, i + i + 1, datetime.now()))
    assert len(h.list()) == 1

    # Ensure no caretaker is attached so hasattr(...) is False
    if hasattr(h, "_caretaker"):
        delattr(h, "_caretaker")

    # Should execute the guarded line (67) and do nothing
    h.record_state()


def test_validate_root_all_three_paths():
    """Covers input_validators.py:56–64 (root guards)."""
    from app.input_validators import validate_root
    from app.exceptions import OperationError

    # Zero degree → OperationError
    with pytest.raises(OperationError):
        validate_root(4, 0)

    # Even root of negative → OperationError
    with pytest.raises(OperationError):
        validate_root(-16, 2)

    # Odd root of negative → allowed (no exception)
    validate_root(-27, 3)


def test_logger_duplicate_handler_guard_line():
    """Covers logger.py:55 (duplicate FileHandler guard)."""
    from app.logger import configure_logger_from_config
    from app.calculator_config import load_config

    cfg = load_config()
    # First call adds a FileHandler
    logger1 = configure_logger_from_config(cfg)
    # Second call executes the guard and skips adding another handler
    logger2 = configure_logger_from_config(cfg)
    assert logger1 is logger2


def test_operations_even_negative_root_branch():
    """Covers operations.py:78 (even root of negative → OperationError)."""
    from app.operations import Root
    from app.exceptions import OperationError

    root = Root()
    with pytest.raises(OperationError):
        root(-9, 2)

def test_history_drops_redo_tail_on_add():
    """Covers history.py:37 by simulating a redo tail and adding a new calc."""
    from app.history import History
    from app.calculation import Calculation
    from datetime import datetime

    h = History(max_size=10)

    c0 = Calculation("add", 1, 1, 2, datetime.now())
    c1 = Calculation("add", 2, 2, 4, datetime.now())
    c2 = Calculation("add", 3, 3, 6, datetime.now())

    # Add three items; pointer ends at index 2
    h.add(c0)
    h.add(c1)
    h.add(c2)

    # Simulate an undo: move pointer back to 1 (leaving a "redo" entry at index 2)
    h._pointer = 1

    # Adding a new calc must drop any redo entries beyond the pointer (executes line 37)
    c3 = Calculation("add", 4, 4, 8, datetime.now())
    h.add(c3)

    # After drop-and-add, the history should be [c0, c1, c3]; c2 must be gone
    items = h.list()
    assert items == [c0, c1, c3]
    # Pointer should now point to the new last item
    assert h._pointer == len(items) - 1


def test_history_iter_yield_from():
    """Covers history.py:67 by iterating over History (yield from self._items)."""
    from app.history import History
    from app.calculation import Calculation
    from datetime import datetime

    h = History()
    c0 = Calculation("add", 1, 2, 3, datetime.now())
    c1 = Calculation("add", 2, 3, 5, datetime.now())
    h.add(c0)
    h.add(c1)

    # Iterating the history invokes __iter__ → 'yield from self._items' (line 67)
    iterated = list(h)
    assert iterated == [c0, c1]

def test_validate_root_full_branch_coverage():
    """Covers input_validators.py lines 56–64 (root validation guards)."""
    from app.input_validators import validate_root
    from app.exceptions import OperationError

    # 1️⃣ Zero-degree root — should raise
    with pytest.raises(OperationError):
        validate_root(5, 0)

    # 2️⃣ Even root of negative — should raise
    with pytest.raises(OperationError):
        validate_root(-16, 2)

    # 3️⃣ Odd root of negative — should pass successfully
    validate_root(-27, 3)

def test_validate_inputs_all_branches():
    """Covers input_validators.py lines 56–64: all operation type branches."""
    from app.input_validators import validate_inputs
    from app.exceptions import OperationError

    # 1️⃣ Division operation — triggers name in {"divide", ...} and calls validate_division
    with pytest.raises(OperationError):
        validate_inputs("divide", 5, 0, 1000)  # b=0 hits validate_division path

    # 2️⃣ Root operation — triggers the 'if name == "root"' branch
    with pytest.raises(OperationError):
        validate_inputs("root", 4, 0, 1000)  # b=0 hits validate_root path

    # 3️⃣ Normal add operation — passes both conditions
    validate_inputs("add", 5, 5, 1000)

def test_validate_inputs_branch_coverage_clean_paths():
    """Fully cover input_validators.py lines 56–64 without early ValidationError."""
    from app.input_validators import validate_inputs
    from app.exceptions import OperationError

    # 1️⃣ Safe numeric inputs for divide (no ValidationError from range/numeric)
    # but b=0 should trigger OperationError in validate_division()
    with pytest.raises(OperationError):
        validate_inputs("divide", 10, 0, 10000)

    # 2️⃣ Safe numeric inputs for root (no ValidationError from range/numeric)
    # b=0 triggers OperationError in validate_root()
    with pytest.raises(OperationError):
        validate_inputs("root", 10, 0, 10000)

    # 3️⃣ Non-branch operation (add) to ensure the function returns normally
    validate_inputs("add", 1, 2, 10000)

def test_validate_inputs_dispatch_paths_reload():
    """Force coverage of input_validators.py:56–64 (divide & root dispatch)."""
    import importlib
    import app.input_validators as iv
    iv = importlib.reload(iv)
    from app.exceptions import OperationError

    # Ensure numeric/range validations pass; then hit the 'divide' branch → validate_division
    with pytest.raises(OperationError):
        iv.validate_inputs("divide", 10, 0, 10000)  # b=0 triggers OperationError in validate_division

    # Hit the 'root' branch → validate_root
    with pytest.raises(OperationError):
        iv.validate_inputs("root", 9, 0, 10000)  # b=0 triggers OperationError in validate_root

    # Normal non-branch operation to complete the function cleanly
    iv.validate_inputs("add", 1, 2, 10000)

def test_logger_duplicate_filehandler_guard_strict(tmp_path):
    """Cover logger.py:55 by ensuring a FileHandler already exists before calling configure again."""
    from app.logger import configure_logger_from_config
    from app.calculator_config import load_config
    import logging

    cfg = load_config()
    logger = configure_logger_from_config(cfg)

    # Manually add a FileHandler so the guard condition becomes False on next call
    handler = logging.FileHandler(cfg.log_path)
    logger.addHandler(handler)

    # Now call again; the guard should skip adding another handler (executes condition line)
    logger2 = configure_logger_from_config(cfg)
    assert logger2 is logger

def test_root_even_negative_strict():
    """Cover operations.py:78 (even root of negative should raise)."""
    from app.operations import Root
    from app.exceptions import OperationError

    r = Root()
    with pytest.raises(OperationError):
        r(-16, 2)

def test_logger_load_history_from_csv_nonexistent(tmp_path):
    """Cover logger.py line 55: csv_path.exists() is False."""
    from app.logger import load_history_from_csv
    from pathlib import Path

    fake_path = tmp_path / "does_not_exist.csv"
    # No file created — ensures csv_path.exists() returns False
    result = load_history_from_csv(fake_path)
    assert result == []  # should return an empty list

def test_root_zero_degree_guard():
    """Cover operations.py line 78: root with zero degree should raise OperationError."""
    from app.operations import Root
    from app.exceptions import OperationError

    r = Root()
    with pytest.raises(OperationError):
        r(9, 0)  # b = 0 triggers "Root with zero degree is undefined."
