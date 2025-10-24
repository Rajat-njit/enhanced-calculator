# 🧮 Enhanced Calculator — A Python Design Patterns Project
**Author:** Rajat Pednekar | UCID: rp2348

---

## 📘 Project Overview

The **Enhanced Calculator** is a modular, object-oriented **command-line calculator** built to demonstrate the real-world application of **Software Design Patterns** in Python.

Unlike traditional calculators, this project focuses on:
- Robust **software architecture**
- **Reusability**, **extensibility**, and **testability**
- Clean, modular code that enforces **SOLID principles**
- Real-world engineering practices like **CI/CD**, **logging**, and **config-driven behavior**

---

## 🎯 Learning Goals

The project was designed to demonstrate:
- The power of **Design Patterns** in scalable software design
- The importance of **logging**, **configuration management**, and **testing discipline**
- How to create a **cleanly architected CLI application** using professional-grade Python practices

---

## 🧩 Implemented Design Patterns (With Examples)

### 🏭 Factory Pattern
**Purpose:** Centralize creation of operation objects (`Add`, `Subtract`, `Power`, etc.) to simplify extensibility.

**Where:** `app/operations.py`

**Example:**
```python
class OperationFactory:
    @staticmethod
    def create(operation: str):
        if operation == "add":
            return AddOperation()
        elif operation == "divide":
            return DivideOperation()
        ...
````

**How it helps:**

  - New operations (e.g., `SquareRoot`, `Logarithm`) can be added without touching core calculator logic.
  - Enforces **Open-Closed Principle** — open for extension, closed for modification.

### 🕹️ Command Pattern

**Purpose:** Encapsulate each calculator operation as an independent command that can be executed, undone, or redone.

**Where:** `app/command_pattern.py`

**Example:**

```python
class OperationCommand:
    def __init__(self, operation, a, b):
        self.operation = operation
        self.a = a
        self.b = b

    def execute(self):
        return self.operation.execute(self.a, self.b)
```

**Usage:**

```python
cmd = OperationCommand(AddOperation(), 5, 3)
result = cmd.execute()  # 8
```

This separation makes it trivial to:

  - Add new commands dynamically
  - Record operations for Undo/Redo functionality
  - Trigger side effects like logging through observers

### 🧠 Memento Pattern

**Purpose:** Allow the calculator to revert or redo previous states.

**Where:** `app/calculator_memento.py`

**Concept:**
The calculator state (operands, result, timestamp) is wrapped in a `Memento` object.
Two stacks — `undo` and `redo` — manage historical states.

**Example:**

```python
memento = CalculatorMemento(current_state)
caretaker.save_state(memento)
```

When `undo` is called:

```python
previous_state = caretaker.undo()
calculator.restore_state(previous_state)
```

This pattern ensures operations are non-destructive and reversible — mimicking professional-grade version control for calculations.

### 🔔 Observer Pattern

**Purpose:** Automatically trigger log saving and CSV persistence when new operations occur.

**Where:** `app/logger.py`

**Observers:**

  - `LoggingObserver`: logs every operation in `logs/app.log`
  - `AutoSaveObserver`: saves calculation history to CSV (`history/history.csv`)

**Example:**

```python
calc.register_observer(LoggingObserver(logger))
calc.register_observer(AutoSaveObserver(cfg))
```

When `calc.perform_operation("add", 2, 3)` runs, both observers react without direct coupling.
This pattern decouples core logic from side effects (logging and persistence).

### 🧱 Decorator Pattern

**Purpose:** Dynamically build and display the help menu.

**Where:** `app/decorators.py`

Each command registers itself:

```python
@register_command("add", "Add two numbers")
def cmd_add(calc, args):
    ...
```

When the user types `help`, all decorated commands are dynamically listed:

```sql
=== 🧭 Available Commands ===
add - Add two numbers
subtract - Subtract one number from another
...
```

No manual edits are needed when new commands are added — fully automatic.

-----

### 🎨 UI Enhancement: Colorized Output

**Purpose:** Provide clear, visually distinct output for different message types.

**Where:** `app/ui_style.py`

  - ✅ Success → **Green**
  - ⚠️ Warning → **Yellow**
  - ❌ Error → **Red**
  - ℹ️ Info → **Blue**

This improves user interaction and mimics modern terminal UX.

-----

### 🪵 Logging and Observability

**Module:** `app/logger.py`

The logging system uses both `FileHandler` and `StreamHandler` (for testing under `pytest`).
It follows a single-entry configuration pattern via `configure_logger_from_config()`.

**📁 File Output:** `logs/app.log`

```text
2025-10-23 14:03:22 [INFO] calc: add(5.0, 7.0) = 12.0
2025-10-23 14:03:24 [INFO] calc: abs_diff(10.0, 4.0) = 6.0
2025-10-23 14:03:25 [INFO] calc: modulus(11.0, 4.0) = 3.0
```

#### 🧠 Key Logging Features

  - Timestamped entries in `YYYY-MM-DD HH:MM:SS` format
  - Rotating handlers prevented to avoid duplicates
  - Configurable log path via `.env`
  - `Pytest` stream handler ensures coverage testing captures log events

-----

## 🧱 Project Architecture (Clean Layered Design)

```bash
📂 enhanced-calculator/
│
├── app/
│   ├── core/
│   │   ├── calculator.py         # Core business logic (orchestrates everything)
│   │   ├── calculation.py        # Calculation entity
│   │   ├── operations.py         # Arithmetic operations factory
│   │   └── history.py            # Manages history stack
│   │
│   ├── patterns/
│   │   ├── calculator_memento.py # Undo/Redo (Memento)
│   │   ├── command_pattern.py    # Encapsulated operation execution
│   │   ├── decorators.py         # Help menu registration
│   │   └── logger.py             # Observer pattern implementation
│   │
│   ├── cli/
│   │   ├── commands.py           # REPL commands
│   │   ├── help_menu.py          # Dynamic help
│   │   └── ui_style.py           # Color-coded terminal styling
│   │
│   └── config/
│       ├── calculator_config.py  # Loads and validates .env settings
│       └── exceptions.py         # Centralized error handling
│
├── tests/                      # 100% pytest coverage
├── .github/workflows/          # CI/CD pipeline configuration
├── .env
├── requirements.txt
└── README.md
```

#### 🧩 Architectural Goals

  - **Low Coupling:** Each module serves one purpose
  - **High Cohesion:** Related functions stay within the same logical group
  - **Dependency Injection:** Configs and loggers are passed, not hardcoded
  - **Extensibility:** New commands can be added in one file without altering core logic

-----

### 🧾 Configuration Setup (.env)

**Example `.env`:**

```bash
CALCULATOR_LOG_DIR=logs
CALCULATOR_HISTORY_DIR=history
CALCULATOR_AUTO_SAVE=true
CALCULATOR_PRECISION=2
CALCULATOR_MAX_INPUT_VALUE=1000000
CALCULATOR_DEFAULT_ENCODING=utf-8
```

Automatically loaded via `dotenv`.
If missing, defaults are applied safely.

-----

### 🚀 Example Session (Expanded)

```text
=== 🧮 Enhanced Calculator ===
Type 'help' to see available commands.
Type 'exit' to quit.

>>> add 5 7
✅ Result: 12.0

>>> abs_diff 10 4
✅ Result: 6.0

>>> modulus 11 4
✅ Result: 3.0

>>> percent 2 8
✅ Result: 25.0%

>>> divide 10 2
✅ Result: 5.0

>>> undo
⚠️  Undid last operation.

>>> redo
⚠️  Redid last operation.

>>> history
📜 Calculation History:
  1. add(5.0, 7.0) = 12.0
  2. abs_diff(10.0, 4.0) = 6.0
  3. modulus(11.0, 4.0) = 3.0
  4. percent(2.0, 8.0) = 25.0

>>> save
💾 History saved to history/history.csv

>>> exit
👋 Goodbye! Thanks for using Enhanced Calculator.
```

-----

## 🧪 Testing and Coverage

### Running Tests

```bash
pytest
```

### Checking Coverage

```bash
pytest --cov=app --cov-report=term-missing
```

✅ **Goal: 100% coverage** — all modules, all branches, all exceptions.

-----

## 🔄 Continuous Integration (CI/CD)

GitHub Actions workflow `.github/workflows/python-app.yml` automatically:

  - Installs dependencies
  - Runs `pytest`
  - Enforces 100% coverage

### Workflow Example

```yaml
name: Python Enhanced Calculator CI
on:
  push:
    branches: [ master ]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt pytest pytest-cov
      - run: pytest --cov=app --cov-fail-under=100
```

✅ The badge in the README updates automatically when tests pass.

-----

## ⚙️ Optional Features Implemented

### 1️⃣ Dynamic Help Menu (Decorator Pattern)

**Goal:** Automatically reflect all available commands in the help menu.

**Implementation:**

  - Each command registers with `@register_command(name, description)`
  - The decorator stores entries in a global registry.
  - When `help` is invoked, all commands display dynamically.

**Example Output:**

```text
=== 🧭 Available Commands ===
add         - Add two numbers
subtract    - Subtract one number from another
abs_diff    - Absolute difference between two numbers
percent     - Percentage (a/b * 100)
...
```

**Advantage:**
Adding new commands requires **zero updates** to the help menu.

### 2️⃣ Auto CSV Save (Observer Pattern)

**Goal:** Automatically persist calculation history after each operation.

**Implementation:**
`AutoSaveObserver` listens to calculator events:

```python
def update(self, calculation: Calculation):
    save_history_to_csv(self.history, self.cfg.history_path)
```

**Output:**

```text
💾 Auto-saving: History updated with add(5.0, 7.0) = 12.0
```

**CSV Example:**

```
timestamp,operation,a,b,result
2025-10-23T14:00:00,add,5.0,7.0,12.0
```

### 3️⃣ Color-Coded Logging & Console Output

**Goal:** Improve user interaction with color-coded messages.

**Implementation:**

```python
Fore.GREEN + "✅ Result: 12.0" + Style.RESET_ALL
```

**Effect:**

  - Success messages → **Green**
  - Warnings → **Yellow**
  - Errors → **Red**

**Output Example:**

```text
✅ Result: 25.0%
⚠️  Invalid input, please retry.
```

-----

## 🧑‍💻 Git and Collaboration

  - Clear, descriptive commit messages (`feat:`, `fix:`, `refactor:`)
  - Branch-based development (`feature/memento`, `feature/logger`, etc.)
  - Merging handled via Pull Requests after CI passes

**Sample Git Log:**

```bash
* 6197a3e (HEAD -> master) Implemented Color Coded Output Successfully
* 7e9cdcb Implemented Dynamic Helper Option
* 3132e12 Integrated dynamic help menu into CLI REPL
* 43ab7b0 Added LoggingObserver and AutoSaveObserver
* 62835c2 Implemented Memento pattern with undo/redo
```

-----

## 🏁 Conclusion

This **Enhanced Calculator** project reflects an end-to-end understanding of real-world software design, combining:

  - Design patterns
  - Clean architecture
  - Continuous integration
  - Logging and persistence
  - Extensible CLI interface

With **100% code coverage** and **CI/CD integration**, it represents a professional-quality Python application demonstrating true mastery of modular design and maintainability.

> “Clean code and modular design are not the end — they’re the beginning of scalable innovation.”
> — Rajat Pednekar

-----

## 🏗️ Future Enhancements

  - GUI interface using PyQt or Tkinter
  - REST API integration with FastAPI
  - Database persistence (SQLite/PostgreSQL)
  - Voice or speech command input
  - Math expression parser for multi-operation chaining

<!-- end list -->

```
```
