```markdown
# 🧮 Enhanced Calculator — A Python Design Patterns Project
**Author:** Rajat Pednekar | UCID: rp2348

---

## 📘 Project Overview

The **Enhanced Calculator** is a modular, object-oriented command-line calculator that demonstrates the practical application of **Software Design Patterns** in Python.

This project was developed as part of the *Python for Web Development* course to reinforce principles of software architecture, maintainability, and clean code design.

Unlike a basic calculator, this project integrates:

- ✅ **Factory Pattern** – for dynamic creation of arithmetic operations
- ✅ **Memento Pattern** – to implement undo/redo history management
- ✅ **Observer Pattern** – for real-time logging and auto-saving of history
- ✅ **Decorator Pattern** – for a dynamic, extensible help menu
- ✅ **Command Pattern** – to encapsulate each operation as an executable object
- ✅ **Color-Coded CLI** – for a professional and user-friendly terminal experience
- ✅ **Comprehensive Unit Testing & CI/CD Integration** – enforcing 100% test coverage

Together, these features transform a simple calculator into a **maintainable, extensible, and production-ready application**.

---

## 🧩 Core Features

| Feature | Description |
|----------|-------------|
| 🧠 **Factory Pattern** | Centralized creation of operations (`Add`, `Divide`, `Root`, etc.) ensuring extensibility. |
| 🕹️ **Command Pattern** | Each command (e.g., add, subtract) is an object encapsulating execution logic. |
| 💾 **Memento Pattern** | Enables `undo` and `redo` functionality by saving calculation states. |
| 🪶 **Observer Pattern** | `LoggingObserver` writes logs, and `AutoSaveObserver` persists history to CSV. |
| 🧰 **Decorator Pattern** | Dynamically builds the help menu based on registered commands — no manual updates needed. |
| 🎨 **Color Output (Colorama)** | Enhanced user interface with clear visual feedback in the terminal. |
| ⚙️ **Configuration via .env** | Customizes log paths, encoding, precision, and history limits. |
| 🧪 **CI/CD via GitHub Actions** | Automatic testing pipeline with enforced 100% coverage. |

---

## 🏗️ Project Architecture

```

enhanced-calculator/
├── app/
│ ├── init.py
│ ├── calculation.py \# Calculation entity
│ ├── calculator.py \# Core Calculator logic
│ ├── calculator\_config.py \# Loads configuration (.env)
│ ├── calculator\_memento.py \# Implements Memento Pattern
│ ├── command\_pattern.py \# Command Pattern classes
│ ├── commands.py \# REPL command implementations
│ ├── decorators.py \# Decorator for dynamic help
│ ├── exceptions.py \# Custom exception hierarchy
│ ├── help\_menu.py \# Prints dynamic command menu
│ ├── history.py \# Manages history stack
│ ├── input\_validators.py \# Input validation logic
│ ├── logger.py \# Logging & Observer pattern
│ ├── operations.py \# Factory-created operations
│ └── ui\_style.py \# Color-coded CLI styling
├── tests/ \# All pytest-based unit tests
├── .github/workflows/ \# GitHub Actions CI pipeline
├── requirements.txt
├── .env
└── README.md

````

This modular structure isolates functionality for **maximum testability, clarity, and reusability**.

---

## ⚙️ Installation & Setup Guide

### 1. Clone the Repository

```bash
git clone [https://github.com/](https://github.com/)<your-username>/enhanced-calculator.git
cd enhanced-calculator
````

### 2\. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3\. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 🧾 Configuration Setup (.env)

All runtime configuration is handled through an environment file `.env` located in the project root.

Example `.env` file:

```bash
# Base Directories
CALCULATOR_LOG_DIR=logs
CALCULATOR_HISTORY_DIR=history

# History Settings
CALCULATOR_MAX_HISTORY_SIZE=50
CALCULATOR_AUTO_SAVE=true

# Calculation Settings
CALCULATOR_PRECISION=2
CALCULATOR_MAX_INPUT_VALUE=1000000
CALCULATOR_DEFAULT_ENCODING=utf-8
```

These are automatically loaded by `calculator_config.py` using `python-dotenv`.
If variables are missing, the app applies safe defaults.

#### 🧠 Configuration Validation

During startup, the configuration module:

  - Creates directories if they don’t exist
  - Validates numerical ranges and boolean flags
  - Exposes an immutable `CalculatorConfig` object used across the app

### 🚀 Usage Guide (Command-Line Interface)

Run the calculator with:

```bash
python -m app
```

#### 🧮 Example Session

```text
=== 🧮 Enhanced Calculator ===
Type 'help' to see available commands.
Type 'exit' to quit.

>>> add 5 7
✅ Result: 12.0

>>> power 2 4
✅ Result: 16.0

>>> undo
⚠️  Undid last operation.

>>> redo
⚠️  Redid last operation.

>>> history
📜 Calculation History:
  1. add(5.0, 7.0) = 12.0
  2. power(2.0, 4.0) = 16.0

>>> save
💾 History saved to history/history.csv

>>> exit
👋 Goodbye! Thanks for using Enhanced Calculator.
```

### 💡 Available Commands

| Command | Description |
|----------|-------------|
| `add a b` | Add two numbers |
| `subtract a b` | Subtract b from a |
| `multiply a b` | Multiply two numbers |
| `divide a b` | Divide a by b |
| `power a b` | Compute a raised to b |
| `root a b` | Find the b-th root of a |
| `modulus a b` | Find remainder |
| `int_divide a b` | Integer division (truncated) |
| `percent a b` | (a/b) \* 100 |
| `abs_diff a b` | Absolute difference |
| `undo` / `redo` | Manage calculation history |
| `save` / `load` | Manual CSV persistence |
| `clear` | Clear all history |
| `help` | Display all available commands dynamically |
| `exit` | Exit gracefully |

-----

### 🧭 Dynamic Help Menu

The help menu uses the **Decorator Pattern**.
Every command registers itself using a decorator:

```python
@register_command("add", "Add two numbers")
def cmd_add(calc, args):
    ...
```

Adding a new command automatically updates the `help` menu — no manual edits required.

## 🧠 Design Patterns in Detail

### 🏭 Factory Pattern

Located in `operations.py`.
Each operation (Add, Root, Power, etc.) is created via a centralized factory method, allowing new operations to be plugged in easily.

### 🧩 Command Pattern

Each operation is represented by an `OperationCommand` class that encapsulates:

  - execution
  - undo/redo integration
  - operation metadata

This design separates user input from execution logic.

### 🧠 Memento Pattern

Implemented in `calculator_memento.py`.
The calculator saves each state to a stack, enabling `undo` and `redo` functionality — with state restoration for both operands and results.

### 🔔 Observer Pattern

Two observers (`LoggingObserver`, `AutoSaveObserver`) monitor the calculator:

  - **`LoggingObserver`** writes operation logs to `logs/app.log`.
  - **`AutoSaveObserver`** saves the current history to CSV after each operation.

### 🎁 Decorator Pattern

Implemented in `decorators.py` and `help_menu.py`.
It dynamically enhances the help menu without modifying base code.

-----

## 🖥️ Color Output (UI Enhancement)

Implemented via **Colorama** in `ui_style.py` to colorize output:

  - ✅ **Success (Green)**
  - ⚠️ **Warning (Yellow)**
  - ❌ **Error (Red)**
  - ℹ️ **Info (Blue)**

This improves readability and user engagement.

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

**Expected output:**

```bash
TOTAL 100% test coverage
161 tests passed successfully
```

Tests cover:

  - Edge cases (division by zero, negative roots, etc.)
  - Undo/Redo logic
  - CSV persistence
  - Logging observer validation
  - Input validation & exception handling
  - Decorator-based help menu registration

-----

## 🔄 Continuous Integration (CI/CD)

**GitHub Actions** is configured in `.github/workflows/python-app.yml` to automatically:

  - Check out the code
  - Install dependencies
  - Run all tests with `pytest`
  - Enforce 100% test coverage

### Workflow Summary

```yaml
name: Python Enhanced Calculator CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - run: pip install -r requirements.txt pytest pytest-cov
      - run: pytest --cov=app --cov-fail-under=100
```

### Adding a Badge

Add this badge to your `README.md`:

```markdown
![Build Status](https://github.com/<your-username>/enhanced-calculator/actions/workflows/python-app.yml/badge.svg)
```

-----

## 📊 Logging and History Files

### Logging (`logs/app.log`)

Each operation is logged in the following format:

```yaml
2025-10-23 12:00:00 [INFO] calc: add(2.0, 3.0) = 5.0
2025-10-23 12:00:01 [INFO] calc: multiply(3.0, 4.0) = 12.0
```

### CSV Persistence (`history/history.csv`)

Each saved history file contains:

```
timestamp,operation,a,b,result
2025-10-23T12:00:00,add,2.0,3.0,5.0
```

-----

## 🧑‍💻 Development Workflow & Git Usage

  - Git initialized locally with clear incremental commits
  - Branches created for each design pattern (`feature/memento`, `feature/observer`, etc.)
  - Merged with descriptive messages
  - CI/CD validated before merge
  - Final release tagged as `v1.0`

Example commands:

```bash
git branch feature/memento
git checkout feature/memento
git add .
git commit -m "feat: implement memento pattern for undo/redo"
git push origin feature/memento
```

-----

## 🧱 Design Philosophy

This project was designed to reflect clean architecture principles:

  - **DRY** (Don’t Repeat Yourself)
  - **SRP** (Single Responsibility Principle)
  - **OCP** (Open-Closed Principle)
  - **High Cohesion, Low Coupling**

The result is a codebase that’s scalable, readable, and extensible.

-----

## 🧭 Future Enhancements

  - Add REST API using FastAPI or Flask
  - Introduce GUI (Tkinter or PyQt)
  - Support complex numbers and matrices
  - Integrate database persistence (SQLite)
  - Extend logging to cloud storage (AWS S3 / MongoDB)

-----

## 🏁 Conclusion

The **Enhanced Calculator** project demonstrates how structured design, testing discipline, and automation can elevate a simple CLI tool into a robust, professional-grade application.

By leveraging multiple design patterns, enforcing CI/CD pipelines, and maintaining 100% coverage, this project reflects industry-level software engineering practices in Python.

> “Good architecture isn’t about more code — it’s about the right structure.”
> — Rajat Pednekar

```
```
