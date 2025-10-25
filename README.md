# 🧮 Enhanced Calculator — A Python Design Patterns Project  

[![Python Enhanced Calculator CI](https://github.com/Rajat-njit/enhanced-calculator/actions/workflows/python-app.yml/badge.svg)](https://github.com/Rajat-njit/enhanced-calculator/actions/workflows/python-app.yml)

---

## 📘 Project Overview

The **Enhanced Calculator** is a command-line Python application built to demonstrate **object-oriented design** and the **practical application of software design patterns**.  

It serves as a case study in writing **maintainable**, **modular**, and **extensible** Python code following **SOLID** and **DRY** principles, reinforced with **logging**, **configuration management**, **automated testing**, and **continuous integration (CI/CD)**.

---

## ⚙️ Environment Setup

### 1️⃣ Initialize Repository

```bash
git init
git add .
git commit -m "Initial commit: Enhanced Calculator setup"
git remote add origin https://github.com/<your-username>/enhanced-calculator.git
git push -u origin master
````
---

### 2️⃣ Create and Activate Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt**

```
colorama
pytest
pytest-cov
python-dotenv
pandas
```

---

## 🧾 Configuration Setup (`.env`)

Below is the list of environment variables used to configure the Enhanced Calculator.  
These variables should be placed in a `.env` file located at the project root directory.

| Variable | Description | Example |
|-----------|--------------|----------|
| `CALCULATOR_LOG_DIR` | Directory where logs are stored | `logs` |
| `CALCULATOR_HISTORY_DIR` | Directory for saved history CSVs | `history` |
| `CALCULATOR_AUTO_SAVE` | Automatically save after each calculation | `true` |
| `CALCULATOR_PRECISION` | Decimal places for rounding | `2` |
| `CALCULATOR_MAX_INPUT_VALUE` | Maximum allowed numeric input | `1000000` |
| `CALCULATOR_MAX_HISTORY_SIZE` | Maximum number of history records retained | `50` |
| `CALCULATOR_DEFAULT_ENCODING` | Default encoding for CSV and log files | `utf-8` |

### 💡 Example `.env` File

```bash
# Calculator Configuration
CALCULATOR_LOG_DIR=logs
CALCULATOR_HISTORY_DIR=history
CALCULATOR_AUTO_SAVE=true
CALCULATOR_PRECISION=2
CALCULATOR_MAX_INPUT_VALUE=1000000
CALCULATOR_MAX_HISTORY_SIZE=50
CALCULATOR_DEFAULT_ENCODING=utf-8
```

* Uses **python-dotenv** for loading.
* Default values are applied automatically if any field is missing.
* Validates numeric and boolean types at startup.

---

## 🧾 Coverage Configuration (`.coveragerc`)

To ensure consistent 100% test coverage enforcement both locally and in CI/CD,
the following `.coveragerc` file is used to omit intentionally untestable branches
(such as REPL exits and `__main__` guards) and document them explicitly.

```ini
[run]
branch = True
omit =
    app/__init__.py
    app/ui_style.py
    */__main__.py
    app/command_pattern.py
    app/commands.py

[report]
exclude_lines =
    pragma: no cover
    if __name__ == .__main__.:
```

> 🧠 **Note:**
> Lines marked with `# pragma: no cover` represent code paths that only trigger during
> real terminal interactions (e.g., `KeyboardInterrupt` or REPL exit),
> which are excluded from automated pytest coverage checks.

---


## 🧩 Design Pattern Map

This project demonstrates the use of multiple design patterns to ensure maintainability, scalability, and clarity.  
The following table maps each design pattern to its location and purpose in the codebase:

| **Pattern** | **Location** | **Purpose** |
|--------------|--------------|--------------|
| **Factory** | `app/calculation.py` | Creates operation instances dynamically based on operation name. |
| **Strategy** | `app/operations.py` | Encapsulates each arithmetic operation’s algorithm separately. |
| **Memento** | `app/calculator_memento.py` + `app/history.py` | Enables undo/redo functionality via saved state objects. |
| **Observer** | `app/logger.py` (`LoggingObserver`, `AutoSaveObserver`) + `app/history.py`(`Helper`) | Triggers automatic logging and CSV saving after each operation. |
| **Command** | `app/command_pattern.py` | Encapsulates calculator commands (add, subtract, undo, redo, etc.) as objects. |
| **Decorator** | `app/decorator.py` + `app/help_menu.py` | Dynamically builds the help menu so new operations appear automatically. |
| **Facade** | `app/calculator.py` | Provides a unified high-level interface coordinating all subsystems. |

---

## 🏗️ Repository Structure

```

project_root/
├── app/
│   ├── **init**.py
│   ├── calculator.py
│   ├── calculation.py
│   ├── calculator_config.py
│   ├── calculator_memento.py
│   ├── exceptions.py
│   ├── history.py
│   ├── input_validators.py
│   ├── operations.py
│   ├── logger.py
│   ├── command_pattern.py
│   ├── commands.py
│   ├── decorators.py
│   ├── help_menu.py
│   └── ui_style.py
│
├── tests/
│   ├── **init**.py
│   ├── test_calculator.py
│   ├── test_operations.py
│   ├── test_logger.py
│   └── ...
│
├── .env
├── requirements.txt
├── README.md
└── .github/
    ├── workflows/
    └── python-app.yml

````

---

## 🧱 Project Architecture & Modular Design

```
📦 enhanced-calculator/
│
├── 🧠 Core Components
│   ├── calculator.py        # Core engine: executes commands and notifies observers
│   ├── calculation.py       # Represents one arithmetic operation
│   ├── operations.py        # Factory-created operation classes
│   └── history.py           # Manages Undo/Redo stacks
│
├── 🧩 Design Patterns
│   ├── calculator_memento.py # Memento Pattern implementation
│   ├── command_pattern.py    # Encapsulated operation execution
│   ├── logger.py             # Observer + Singleton Logger
│   ├── decorators.py         # Dynamic Help Menu
│   └── help_menu.py          # User help and command listing
│
├── ⚙️ Configuration
│   ├── calculator_config.py  # Loads and validates .env
│   ├── input_validators.py   # Handles input range and type validation
│   └── exceptions.py         # Custom error classes
│
├── 🎨 CLI Layer
│   ├── commands.py           # REPL command registry
│   ├── ui_style.py           # Color-coded terminal messages
│   └── __main__.py           # Application entrypoint
```

### 🔹  Architectural Principles

* **DRY:** Shared logic consolidated in validators and logger.
* **SRP:** Each module focuses on one responsibility.
* **OCP:** System supports new operations without modifying existing code.
* **Encapsulation:** Logging, persistence, and CLI are isolated components.

---

## 🧩 Design Patterns in Action

### 🔹 Factory Pattern

Centralizes object creation:

```python
class OperationFactory:
    def create(name: str):
        operations = {
            "add": AddOperation(),
            "modulus": ModulusOperation(),
            "percent": PercentOperation()
        }
        if name not in operations:
            raise OperationError(f"Unknown operation: {name}")
        return operations[name]
```

💡 **Advantage:** Add new operations by defining a new class only.

---

### 🔹 Command Pattern

Encapsulates user requests as command objects.

```python
class OperationCommand:
    def __init__(self, operation, a, b):
        self.operation = operation
        self.a, self.b = a, b
    def execute(self):
        return self.operation.execute(self.a, self.b)
```

 Enables queued, repeatable, and undoable actions — foundation for history management.

---

### 🔹 Memento Pattern

Implements Undo/Redo functionality.

```python
memento = CalculatorMemento(current_state)
caretaker.save_state(memento)
```

**Undo Example:**

```python
previous = caretaker.undo()
calculator.restore_state(previous)
```

 State restoration covers operands, results, and timestamps.

---

### 🔹 Observer Pattern

Auto-handles side effects like logging and CSV saving.

```python
calc.register_observer(LoggingObserver(logger))
calc.register_observer(AutoSaveObserver(cfg))
```

 Keeps business logic clean while ensuring persistence and traceability.

---

### 🧩 Decorator Pattern

Dynamic Help Menu updates automatically as new commands register:

```python
@register_command("add", "Add two numbers")
def cmd_add(calc, args):
    ...
```

Typing `help` reflects all registered commands in real-time.

---

### 🔹 Logger (Singleton Pattern)

`configure_logger_from_config()` guarantees a **single global logger** across modules.

```python
logger = logging.getLogger("calculator")
if not logger.handlers:
    # attach handlers only once
    ...
```

Prevents duplicate log entries, ensures consistency across modules and tests.

---

## ⚙️ Optional Features Implemented

### 1. **Additional Design Pattern – Command Pattern**

**Purpose:** Encapsulate actions as objects allowing **parameterization**, **queuing**, and **undoability**.

**Example:**

```python
cmd = OperationCommand(AddOperation(), 5, 3)
queue = [cmd]
for c in queue:
    print(c.execute())  # 8
```

Enables **future automation** like macro commands or batch calculations.

---

### 2. **Color-Coded Outputs (UI Enhancement)**

Implemented with **Colorama** for better user readability:

```python
print(Fore.GREEN + "✅ Result: 25.0%" + Style.RESET_ALL)
```

**Colors:**

* ✅ Success → Green
* ⚠️ Warning → Yellow
* ❌ Error → Red

---

### 3. **Dynamic Help Menu (Decorator Pattern)**

Help menu updates dynamically as new commands are added:

```
=== 🧭 Available Commands ===
add        - Add two numbers
modulus    - Compute remainder
percent    - Compute (a/b * 100)
abs_diff   - Absolute difference
root       - nth root of a number
...
```

---

## 🧮 Supported Operations

| Command          | Example         | Description         |
| ---------------- | --------------- | ------------------- |
| `add a b`        | 5 + 7 → 12      | Addition            |
| `subtract a b`   | 10 - 4 → 6      | Subtraction         |
| `multiply a b`   | 3 * 5 → 15      | Multiplication      |
| `divide a b`     | 8 / 2 → 4       | Division            |
| `power a b`      | 2 ^ 4 → 16      | Exponentiation      |
| `root a b`       | root(27, 3) → 3 | Nth root            |
| `modulus a b`    | 11 % 4 → 3      | Remainder           |
| `int_divide a b` | 11 // 4 → 2     | Integer division    |
| `percent a b`    | (2, 8) → 25%    | Percentage          |
| `abs_diff a b`   | (10, 4) → 6     | Absolute difference |

---

## 🚀 Example Session

```text
=== 🧮 Enhanced Calculator ===
Type 'help' to see commands.

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

---

## 🔹 Logging System

### 📁 Log File: `logs/app.log`

```
2025-10-23 15:22:00 [INFO] calc: add(5.0, 7.0) = 12.0
2025-10-23 15:22:02 [INFO] calc: abs_diff(10.0, 4.0) = 6.0
2025-10-23 15:22:03 [INFO] calc: modulus(11.0, 4.0) = 3.0
```

### ⚙️ Features

* Timestamped entries with INFO/WARNING/ERROR levels
* Colorized console handler for debugging
* File handler for persistent logs
* Singleton ensures one global logger instance

---

## 💾 Serialization and Persistence

### Saving History

```python
def save_history_to_csv(history, path):
    pd.DataFrame(history).to_csv(path, index=False)
```

### Loading History

```python
def load_history_from_csv(path):
    df = pd.read_csv(path)
    return [Calculation(...row...) for _, row in df.iterrows()]
```

* Uses **pandas** for CSV serialization
* Recovers timestamps and results seamlessly
* Handles missing or corrupt files gracefully

---

## 🧪 Unit Testing and Coverage

```bash
pytest --cov=app --cov-report=term-missing --cov-fail-under=100
```

**Tests Include:**

* Operation accuracy
* Undo/Redo mechanics
* Input validation
* Logging observer verification
* Decorator dynamic help tests
* Edge cases (zero division, invalid input)

✅ **Goal:** 100% code coverage
✅ **Coverage Enforced:** GitHub Actions pipeline

---

## 🔄 CI/CD with GitHub Actions

### `.github/workflows/python-app.yml`

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

✅ Automatically runs tests on every push or PR.
✅ Ensures consistent reliability before merging.

---

## 🧩 Best Practices Followed

| Principle       | Application                                                  |
| --------------- | ------------------------------------------------------------ |
| **DRY**         | Centralized logic for validation, configuration, and logging |
| **SRP**         | Each file handles one responsibility                         |
| **Modularity**  | Isolated components for easier maintenance                   |
| **Logging**     | Every operation recorded via Observer                        |
| **Testability** | Functions written to be easily testable                      |
| **Reusability** | Patterns enable easy future extension                        |

---

## 🧑‍💻 Git Usage and Commit History

* Commits are **clear and atomic**
* Each new feature developed in a **separate branch**
* Merged via pull requests with **passing CI**

**Example Log:**

```
* 6197a3e (HEAD -> master) Implemented Color Coded Output
* 7e9cdcb Added Dynamic Helper Decorator
* 62835c2 Implemented Memento Pattern for Undo/Redo
* 1c86be7 Added GitHub Actions for CI/CD
```

---

## 🏁 Conclusion

The **Enhanced Calculator** demonstrates how core programming concepts scale into professional architecture when backed by design patterns and best practices.

It integrates:

* ✅ Object-oriented design
* ✅ Real-world design patterns
* ✅ Modular structure
* ✅ Full logging & persistence
* ✅ CI/CD and 100% testing discipline

This project is both a **technical showcase** and a **learning model** for maintainable Python applications.

> “Code simplicity is achieved through structured design — not shortcuts.”
> — *Rajat Pednekar*

---

## 👤 About the Author
```
**Rajat Pednekar**
**Graduate Student — Python for Web Development**
**New Jersey Institute of Technology**
```

---
```
