# 🧮 Enhanced Calculator — A Python Design Patterns Project
**Author:** Rajat Pednekar | UCID: rp2348
**Course:** Python for Web Development
**Instructor:** [Your Professor’s Name]

---

## 🔹 Project Overview

The **Enhanced Calculator** is a command-line Python application designed to demonstrate **object-oriented programming** and **software design patterns** in real-world software architecture.

This project moves beyond simple arithmetic — it integrates **modularity**, **maintainability**, and **professional development practices** such as **logging**, **configuration management**, **CI/CD**, and **unit testing** with **100% coverage enforcement**.

The calculator supports a **fully interactive REPL (Read-Eval-Print Loop)** interface, dynamic help menus, automatic history management, and persistent storage using CSV and logging observers.

### » Objectives
- Implement key **software design patterns** for real-world scalability.
- Demonstrate **professional software engineering practices** — CI/CD, logging, testing, configuration.
- Reinforce concepts of **OOP**, **SOLID**, and **DRY** principles.
- Provide a **clear commit history**, **modular code**, and **well-documented architecture**.

---

## 🔹 Repository Setup

### » Directory Structure
```

project\_root/
├── app/
│   ├── **init**.py
│   ├── calculator.py
│   ├── calculation.py
│   ├── calculator\_config.py
│   ├── calculator\_memento.py
│   ├── exceptions.py
│   ├── history.py
│   ├── input\_validators.py
│   ├── operations.py
│   ├── logger.py
│   ├── command\_pattern.py
│   ├── commands.py
│   ├── help\_menu.py
│   ├── decorators.py
│   └── ui\_style.py
│
├── tests/
│   ├── **init**.py
│   ├── test\_calculator.py
│   ├── test\_calculation.py
│   ├── test\_operations.py
│   ├── test\_logger.py
│   └── ...
│
├── .env
├── requirements.txt
├── README.md
└── .github/
└── workflows/
└── python-app.yml

````

### » Purpose of Key Folders
- `app/`: Core logic, operations, and patterns implementation
- `tests/`: Pytest-based automated tests for all modules
- `.github/workflows/`: CI/CD configuration using GitHub Actions
- `.env`: Configuration variables for logging, precision, and limits

---

## 🔹 Environment Setup

### » 1. Initialize a Git Repository
```bash
git init
git add .
git commit -m "Initial commit: setup enhanced calculator structure"
git remote add origin [https://github.com/](https://github.com/)<your-username>/enhanced-calculator.git
git push -u origin master
````

**Note:** Commit regularly — descriptive commit messages are mandatory for grading. Projects without a clear commit history will be flagged under academic integrity.

### » 2. Create and Activate Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### » 3. Install Dependencies

Ensure all dependencies are in `requirements.txt`:

```
colorama
pytest
pytest-cov
python-dotenv
pandas
```

Then install:

```bash
pip install -r requirements.txt
```

### » 4. Configuration Setup (.env)

The calculator uses `.env` for flexible configuration.

```
# Directories
CALCULATOR_LOG_DIR=logs
CALCULATOR_HISTORY_DIR=history

# History and Behavior
CALCULATOR_MAX_HISTORY_SIZE=50
CALCULATOR_AUTO_SAVE=true

# Calculations
CALCULATOR_PRECISION=2
CALCULATOR_MAX_INPUT_VALUE=1000000
CALCULATOR_DEFAULT_ENCODING=utf-8
```

This file is loaded automatically by `calculator_config.py` using `python-dotenv`.

-----

## 🔹 Supported Operations

| Operation | Example | Description |
|---|---|---|
| `add a b` | 5 + 7 → 12 | Addition |
| `subtract a b` | 10 - 4 → 6 | Subtraction |
| `multiply a b`| 3 \* 6 → 18 | Multiplication |
| `divide a b` | 8 / 2 → 4 | Division with error handling |
| `power a b` | 2^4 → 16 | Exponentiation |
| `root a b` | √a (nth root) | b-th root of a |
| `modulus a b` | 10 % 4 → 2 | Remainder |
| `int_divide a b`| 11 // 4 → 2 | Integer division |
| `percent a b` | (a/b) \* 100 | Percentage |
| `abs_diff a b` | |a−b| | Absolute difference |

-----

## 🔹 Core Features and Design Patterns Explained

This project is structured around key design patterns to ensure modularity and extensibility.

### » Factory Pattern — `operations.py`

**Purpose:** Centralizes the creation of operation objects. The calculator asks the factory for an operation (e.g., "add") instead of creating the `AddOperation` object itself.

**Benefit:** Simplifies adding new operations. To add "logarithm," we only need to create a `LogOperation` class and register it with the factory. The core calculator code remains unchanged, adhering to the **Open-Closed Principle**.

```python
class OperationFactory:
    def create(op_name: str):
        ops = {
            "add": AddOperation(),
            "divide": DivideOperation(),
            "modulus": ModulusOperation(),
        }
        if op_name not in ops:
            raise OperationError(f"Unknown operation: {op_name}")
        return ops[op_name]
```

### » Command Pattern — `command_pattern.py`

**Purpose:** Encapsulates a user's request (e.g., "add 5 7") as an object. This object contains everything needed to execute the request.

**Benefit:** This encapsulation allows us to easily queue commands, log them, and most importantly, support **undo/redo** operations. The history stack stores these command objects, not just the results.

```python
class OperationCommand:
    def __init__(self, operation, a, b):
        self.operation = operation
        self.a = a
        self.b = b

    def execute(self):
        return self.operation.execute(self.a, self.b)
```

### » Memento Pattern — `calculator_memento.py`

**Purpose:** Stores a "snapshot" of the calculator's state (e.g., its entire history) without exposing its internal implementation.

**Benefit:** This pattern provides the mechanism for the Command Pattern's undo/redo. When an operation is performed, a *memento* (snapshot) of the *previous* state is saved. When `undo` is called, the calculator's state is restored from the last saved memento.

```python
# Create a snapshot
memento = CalculatorMemento(current_state)
# Save snapshot to the history stack
caretaker.save_state(memento)

# On undo
previous_state = caretaker.undo()
calculator.restore_state(previous_state)
```

### » Observer Pattern — `logger.py`

**Purpose:** Allows objects (Observers) to "subscribe" to events from another object (the Subject). When the Subject's state changes, it automatically notifies all its Observers.

**Benefit:** This decouples side-effects from core logic. The `Calculator` (Subject) simply performs calculations. The `LoggingObserver` and `AutoSaveObserver` (Observers) listen for these calculations and react by writing to a log file or saving to a CSV, respectively. The calculator doesn't need to know anything about logging or saving.

```python
# Register observers with the calculator
calc.register_observer(LoggingObserver(logger))
calc.register_observer(AutoSaveObserver(cfg))

# When an operation executes, both observers are notified automatically
```

### » Decorator Pattern — `decorators.py`

**Purpose:** Used to create the **Dynamic Help Menu**. A decorator (`@register_command`) wraps each command function.

**Benefit:** When the application loads, the decorator "registers" the command's name and description in a central list. The `help` command then just prints this list. This means adding a new command *automatically* adds it to the help menu with no extra work.

```python
@register_command("add", "Add two numbers")
def cmd_add(calc, args):
    ...
```

**Example Output:**

```
=== 🧭 Available Commands ===
add        - Add two numbers
percent    - Calculate percentage
modulus    - Find remainder
root       - Find nth root
undo       - Undo last operation
```

### » Color-Coded Output — `ui_style.py`

**Purpose:** Uses the `Colorama` library to provide clear, visual feedback to the user.

**Benefit:** Improves user experience by making outputs unambiguous.

  - ✅ **Success (Green):** Indicates a successful calculation.
  - ⚠️ **Warning (Yellow):** Used for non-critical messages like `undo`.
  - ❌ **Error (Red):** Clearly highlights errors like "Division by zero."

<!-- end list -->

```python
print(Fore.GREEN + "✅ Result: 12.0" + Style.RESET_ALL)
```

-----

## 🔹 Example Session

```
=== 🧮 Enhanced Calculator ===
Type 'help' for commands, 'exit' to quit.

>>> add 5 7
✅ Result: 12.0

>>> abs_diff 10 4
✅ Result: 6.0

>>> modulus 11 4
✅ Result: 3.0

>>> percent 2 8
✅ Result: 25.0%

>>> undo
⚠️  Undid last operation.

>>> redo
⚠️  Redid last operation.

>>> history
📜 Calculation History:
  1. add(5.0, 7.0) = 12.0
  2. abs_diff(10.0, 4.0) = 6.0
  3. modulus(11.0, 4.0) = 3.0
  4. percent(2.0, 8.0) = 25.0%

>>> save
💾 History saved to history/history.csv
```

-----

## 🔹 Logging and Persistence

### » Example Log (`logs/app.log`)

All operations are logged via the `LoggingObserver`.

```
2025-10-23 15:22:00 [INFO] calc: add(5.0, 7.0) = 12.0
2025-10-23 15:22:02 [INFO] calc: abs_diff(10.0, 4.0) = 6.0
2025-10-23 15:22:03 [INFO] calc: modulus(11.0, 4.0) = 3.0
```

### » Logging Features

  - Uses `logging.FileHandler` for persistent logs and `StreamHandler` for `pytest` output.
  - Log creation and paths are configured via the `.env` file.
  - Follows standard `INFO`, `WARNING`, and `ERROR` levels.

### » Serialization and Persistence

**Saving History:**
The `AutoSaveObserver` automatically saves the full history to a CSV file after every operation using `pandas`.

```python
def save_history_to_csv(history, path):
    pd.DataFrame(history).to_csv(path, index=False)
```

**Loading History:**
On startup, the calculator can reload its state from the saved CSV.

```python
def load_history_from_csv(path):
    df = pd.read_csv(path)
    return [Calculation(...row...) for _, row in df.iterrows()]
```

The system includes error handling for missing files, malformed CSVs, and encoding errors.

-----

## 🔹 Unit Testing and Coverage

The project enforces 100% test coverage.

**Run all tests:**

```bash
pytest
```

**Enforce coverage:**

```bash
pytest --cov=app --cov-report=term-missing --cov-fail-under=100
```

### » Test Highlights

  - Arithmetic operation validation (including edge cases like division by zero).
  - Correct `undo`/`redo` flow using the Memento pattern.
  - Verification of logger output.
  - Input validation and custom exception handling.
  - Tests for the dynamic help decorator.

-----

## 🔹 CI/CD with GitHub Actions

The pipeline (`.github/workflows/python-app.yml`) ensures code quality by:

  - Automatically running all tests on every `push` and `pull_request`.
  - Installing all dependencies in a clean environment.
  - **Failing the build** if test coverage drops below 100%.

<!-- end list -->

```yaml
name: Python Enhanced Calculator CI
on:
  push:
    branches: [ master ]
  pull_request:
    branches: [ master ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov
      - run: pytest --cov=app --cov-fail-under=100
```

Add this build badge to your `README.md` (replace `<username>`):

```markdown
![Build Status](https://github.com/<username>/enhanced-calculator/actions/workflows/python-app.yml/badge.svg)
```

-----

## 🔹 Best Practices Followed

### » Modular Design

Code is divided into cohesive, testable modules. Each file handles a single, clear responsibility (e.g., `operations.py` only handles operations, `logger.py` only handles logging).

### » DRY Principle (Don't Repeat Yourself)

Repeated logic (like validation, formatting, and persistence) is centralized into reusable functions and classes to avoid duplication.

### » Comprehensive Logging

All calculations, errors, and significant events are recorded. There are no "silent failures" — every event leaves a trace.

### » Continuous Testing

Every module has corresponding unit and integration tests, ensuring that new features don't break existing ones and that all error handling is robust.

-----

## 🔹 Git Usage and Commit History

Development followed a professional workflow with clear, descriptive commit messages.

```
feat: add observer pattern for auto-save
fix: handle divide by zero in operations.py
refactor: improve command registration decorator
```

Feature branches were used for modular development and merged after CI passed:

```bash
git checkout -b feature/logger
git push origin feature/logger
```

Commits reflect actual progress, ensuring full academic integrity.

-----

## 🔹 Conclusion

The Enhanced Calculator project integrates multiple design patterns, follows DRY and modular best practices, and includes robust logging, configuration, and automated testing. It represents a production-ready architecture emphasizing:

  - **Extensibility**
  - **Maintainability**
  - **Test Coverage**
  - **Continuous Integration**

> “Code is only as good as its structure — and structure comes from design.”
>
> — Rajat Pednekar

-----

## 🔹 Future Enhancements

  - REST API interface using FastAPI
  - GUI interface using Tkinter or PyQt
  - Batch command support (using the Command Pattern queue)
  - Cloud logging or database persistence (e.g., SQLite, PostgreSQL)
  - Advanced mathematical expression parsing (e.g., `(5 + 3) * 2`)
```
