# 🧮 Enhanced Calculator — A Python Design Patterns Project  
**Author:** Rajat Pednekar | UCID: rp2348  
**Course:** Python for Web Development  
**Instructor:** [Your Professor’s Name]  

---

## 📘 Project Overview

The **Enhanced Calculator** is a command-line Python application designed to demonstrate **object-oriented programming** and **software design patterns** in real-world software architecture.  

This project moves beyond simple arithmetic — it integrates **modularity**, **maintainability**, and **professional development practices** such as **logging**, **configuration management**, **CI/CD**, and **unit testing** with **100% coverage enforcement**.

The calculator supports a **fully interactive REPL (Read-Eval-Print Loop)** interface, dynamic help menus, automatic history management, and persistent storage using CSV and logging observers.

### 🎯 Objectives
- Implement key **software design patterns** for real-world scalability.  
- Demonstrate **professional software engineering practices** — CI/CD, logging, testing, configuration.  
- Reinforce concepts of **OOP**, **SOLID**, and **DRY** principles.  
- Provide a **clear commit history**, **modular code**, and **well-documented architecture**.  

---

## 🧩 Key Design Patterns Implemented

| Design Pattern | Purpose | Module |
|----------------|----------|---------|
| **Factory** | Centralizes creation of operation objects dynamically | `operations.py` |
| **Command** | Encapsulates requests (operations) as objects | `command_pattern.py` |
| **Memento** | Enables undo/redo by storing calculator states | `calculator_memento.py` |
| **Observer** | Logs and auto-saves results automatically | `logger.py` |
| **Decorator** | Dynamically generates help menu | `decorators.py` |
| **Singleton/Config Loader** | Loads and validates environment configs | `calculator_config.py` |

---

## 🏗️ Repository Setup

### 📁 Directory Structure

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
│   ├── help_menu.py
│   ├── decorators.py
│   └── ui_style.py
│
├── tests/
│   ├── **init**.py
│   ├── test_calculator.py
│   ├── test_calculation.py
│   ├── test_operations.py
│   ├── test_logger.py
│   └── ...
│
├── .env
├── requirements.txt
├── README.md
└── .github/
└── workflows/
└── python-app.yml

````

### 🧠 Purpose of Key Folders
- `app/`: Core logic, operations, and patterns implementation  
- `tests/`: Pytest-based automated tests for all modules  
- `.github/workflows/`: CI/CD configuration using GitHub Actions  
- `.env`: Configuration variables for logging, precision, and limits  

---

## ⚙️ Environment Setup

### 1️⃣ Initialize a Git Repository
```bash
git init
git add .
git commit -m "Initial commit: setup enhanced calculator structure"
git remote add origin https://github.com/<your-username>/enhanced-calculator.git
git push -u origin master
````

> 💡 **Commit regularly** — descriptive commit messages are mandatory for grading.
> Projects without a clear commit history will be flagged under academic integrity.

---

### 2️⃣ Create and Activate Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies

Ensure all dependencies are in `requirements.txt`:

```text
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

---

## 🧾 Configuration Setup (`.env`)

The calculator uses `.env` for flexible configuration.

```bash
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

Loaded automatically by `calculator_config.py` using `python-dotenv`.

---

## 🧱 Project Architecture and Modular Design

```
📦 enhanced-calculator/
│
├── 🧠 Core Logic
│   ├── calculator.py          # Orchestrates operations, manages observers
│   ├── calculation.py         # Represents an atomic calculation
│   ├── operations.py          # Arithmetic operation factory
│   └── history.py             # Manages history stack
│
├── 🧩 Design Patterns
│   ├── calculator_memento.py  # Memento for undo/redo
│   ├── command_pattern.py     # Encapsulated operation commands
│   ├── logger.py              # Observer Pattern (logging + autosave)
│   ├── decorators.py          # Decorator Pattern for dynamic help
│   └── help_menu.py           # Uses decorators to generate help dynamically
│
├── ⚙️ Configuration & Validation
│   ├── calculator_config.py   # Loads .env configs, validates
│   ├── input_validators.py    # Validates user input
│   └── exceptions.py          # Custom error handling
│
├── 🎨 CLI & UI Layer
│   ├── commands.py            # User REPL commands
│   ├── ui_style.py            # Color-coded messages (Colorama)
│   └── main (__main__.py)     # CLI entry point
```

### 🧩 Best Practices

* **DRY Principle:** Reused methods and validation checks avoid duplication.
* **Single Responsibility:** Each module has one defined purpose.
* **Open/Closed Principle:** Operations can be extended without changing base code.
* **Encapsulation:** Logging, validation, and persistence are decoupled from calculator logic.

---

## 🧮 Supported Operations

### Mandatory Operations

| Operation        | Example       | Description                  |   |                     |
| ---------------- | ------------- | ---------------------------- | - | ------------------- |
| `add a b`        | 5 + 7 → 12    | Addition                     |   |                     |
| `subtract a b`   | 10 - 4 → 6    | Subtraction                  |   |                     |
| `multiply a b`   | 3 * 6 → 18    | Multiplication               |   |                     |
| `divide a b`     | 8 / 2 → 4     | Division with error handling |   |                     |
| `power a b`      | 2^4 → 16      | Exponentiation               |   |                     |
| `root a b`       | √a (nth root) | b-th root of a               |   |                     |
| `modulus a b`    | 10 % 4 → 2    | Remainder                    |   |                     |
| `int_divide a b` | 11 // 4 → 2   | Integer division             |   |                     |
| `percent a b`    | (a/b) * 100   | Percentage                   |   |                     |
| `abs_diff a b`   |               | a−b                          |   | Absolute difference |

---

## 🧠 Design Patterns Explained with Examples

### 🏭 Factory Pattern — `operations.py`

Creates operation objects dynamically:

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

💡 **Why:** Simplifies adding new operations — just define a new class and register it.

---

### 🕹️ Command Pattern — `command_pattern.py`

Encapsulates user actions as objects, enabling queuing, reuse, and undo.

```python
class OperationCommand:
    def __init__(self, operation, a, b):
        self.operation = operation
        self.a = a
        self.b = b

    def execute(self):
        return self.operation.execute(self.a, self.b)
```

**Benefit:**

* Each command can be logged, saved, or reversed.
* Makes the system more flexible and testable.

---

### 🧠 Memento Pattern — `calculator_memento.py`

Stores calculator states for undo/redo.

```python
memento = CalculatorMemento(current_state)
caretaker.save_state(memento)
```

When `undo` is invoked:

```python
previous = caretaker.undo()
calculator.restore_state(previous)
```

**Outcome:**
Undo/Redo restores both operands and results exactly.

---

### 🔔 Observer Pattern — `logger.py`

Observers get notified automatically when a new calculation occurs.

```python
calc.register_observer(LoggingObserver(logger))
calc.register_observer(AutoSaveObserver(cfg))
```

When an operation executes:

* LoggingObserver → logs to `logs/app.log`
* AutoSaveObserver → saves to `history/history.csv`

**Benefit:**
Side effects are decoupled — core logic remains clean.

---

### 🧩 Decorator Pattern — `decorators.py`

Used for the **Dynamic Help Menu**:

```python
@register_command("add", "Add two numbers")
def cmd_add(calc, args):
    ...
```

When `help` is typed, all registered commands appear automatically.

---

### 🎨 Color-Coded Output — `ui_style.py`

Implements color feedback with **Colorama**:

```python
print(Fore.GREEN + "✅ Result: 12.0" + Style.RESET_ALL)
```

Output:

```text
✅ Result: 12.0
⚠️  Invalid input
❌  Division by zero error
```

---

## 🧮 Example Session

```text
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

---

## 🪵 Logging System

All logs are managed through a **centralized logger** configured in `logger.py`.

### 📂 Example Log (`logs/app.log`)

```
2025-10-23 15:22:00 [INFO] calc: add(5.0, 7.0) = 12.0
2025-10-23 15:22:02 [INFO] calc: abs_diff(10.0, 4.0) = 6.0
2025-10-23 15:22:03 [INFO] calc: modulus(11.0, 4.0) = 3.0
```

### 🔍 Features

* Uses `logging.FileHandler` and optional `StreamHandler` for pytest
* Color-coded logs for console debugging
* Logs creation and setup handled via `.env` config
* Follows INFO/WARNING/ERROR levels

---

## 💾 Serialization and Persistence

### ✅ Saving History

Automatically saves every calculation using pandas:

```python
def save_history_to_csv(history, path):
    pd.DataFrame(history).to_csv(path, index=False)
```

### ✅ Loading History

Reads saved CSV and reconstructs Calculation objects:

```python
def load_history_from_csv(path):
    df = pd.read_csv(path)
    return [Calculation(...row...) for _, row in df.iterrows()]
```

**Handles:** missing files, malformed CSVs, encoding errors.

---

## 🧪 Unit Testing and Coverage

Run all tests:

```bash
pytest
```

Enforce coverage:

```bash
pytest --cov=app --cov-report=term-missing --cov-fail-under=100
```

### 🔍 Test Highlights

* Arithmetic operation validation
* Undo/Redo flow
* Logger output verification
* Input validation and error handling
* Dynamic help decorator tests

---

## ⚙️ CI/CD with GitHub Actions

The pipeline (`.github/workflows/python-app.yml`) ensures:

* Automatic testing on push and pull requests
* Dependency installation
* 100% coverage enforcement

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

A build badge can be added to your README:

```markdown
![Build Status](https://github.com/<username>/enhanced-calculator/actions/workflows/python-app.yml/badge.svg)
```

---

## ⚙️ Optional Features Implemented

### 🌟 1. Dynamic Help Menu (Decorator Pattern)

Automatically updates when new commands are added.
No manual editing required.

**Example Output:**

```
=== 🧭 Available Commands ===
add        - Add two numbers
percent    - Calculate percentage
modulus    - Find remainder
root       - Find nth root
undo       - Undo last operation
```

---

### 💾 2. Auto-Save Feature (Observer Pattern)

The `AutoSaveObserver` watches calculator state and writes to CSV automatically after every operation.

**Output Example:**

```text
💾 Auto-save: add(5.0, 7.0) persisted to history/history.csv
```

---

### 🎨 3. Color-Coded Outputs (UI Enhancement)

Using `Colorama`, results and errors are highlighted visually:

* ✅ Success (Green)
* ⚠️ Warning (Yellow)
* ❌ Error (Red)

---

### 🕹️ 4. Additional Design Pattern: Command Pattern

**Purpose:**
Encapsulate operations as objects — allowing queuing, scheduling, and parameterization.

**Example:**

```python
cmd = OperationCommand(AddOperation(), 5, 3)
queue = [cmd]
for c in queue:
    print(c.execute())  # 8
```

**Benefit:**
Future extensibility — e.g., batch processing or macro commands.

---

## 🧩 Best Practices Followed

### 🧱 Modular Design

Code is divided into cohesive, testable modules.
Each file handles a single responsibility.

### 🔁 DRY Principle

Repeated validation, formatting, and persistence logic is centralized — no duplication.

### 🪵 Comprehensive Logging

All calculations and errors are recorded using the `Logger` class.
No silent failures — every event leaves a trace.

### 🧪 Continuous Testing

Every module has direct and integration tests ensuring robust error handling.

---

## 🧑‍💻 Git Usage and Commit History

* Clear, descriptive commit messages:

  ```
  feat: add observer pattern for auto-save
  fix: handle divide by zero in operations.py
  refactor: improve command registration decorator
  ```
* Feature branches used for modular development:

  ```
  git checkout -b feature/logger
  git push origin feature/logger
  ```
* Commits reflect actual progress — ensuring full academic integrity.

---

## 🏁 Conclusion

The **Enhanced Calculator** project integrates multiple design patterns, follows DRY and modular best practices, and includes robust logging, configuration, and automated testing.

It represents a **production-ready architecture** emphasizing:

* Extensibility
* Maintainability
* Test coverage
* Continuous integration

> *“Code is only as good as its structure — and structure comes from design.”*
> — Rajat Pednekar

---

## 🏗️ Future Enhancements

* REST API interface using **FastAPI**
* GUI interface using **Tkinter** or **PyQt**
* Batch command support (using Command Pattern queue)
* Cloud logging or database persistence
* Advanced mathematical expression parsing

```

---

Would you like me to now generate a **short 400-word GitHub summary (repository front-page version)** optimized for recruiters and professors (concise but impactful)?
```
