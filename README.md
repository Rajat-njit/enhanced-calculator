# 🧮 Enhanced Calculator — A Python Design Patterns Project
**Author:** Rajat Pednekar | UCID: rp2348

---

## 📘 Project Overview

The **Enhanced Calculator** is an object-oriented, command-line calculator application. Its primary purpose is not just to perform arithmetic, but to serve as a practical demonstration of how fundamental **Software Design Patterns** are applied to build a robust, maintainable, and extensible application in Python.

This project moves beyond a simple script by focusing on core software engineering principles. It emphasizes a clean, modular architecture where components are decoupled and testable. The design enforces **SOLID principles**, particularly the **Single Responsibility Principle (SRP)** and the **Open-Closed Principle (OCP)**, demonstrating how to create software that is easy to maintain and extend over time.

---

## 🎯 Learning Goals & Objectives

This project was designed to bridge the gap between basic scripting and professional software engineering. The key learning objectives achieved include:

* **Practical Application of Design Patterns:** Moving beyond theory to implement five distinct design patterns (Factory, Command, Memento, Observer, Decorator) to solve specific, real-world structural and behavioral problems.
* **Architecting for Extensibility:** Understanding how to design a system (like the **Factory** and **Command** patterns) where new functionality (e.g., new operations like `log` or `sqrt`) can be added with minimal changes to existing, stable code.
* **Decoupling Components:** Mastering techniques (like the **Observer** pattern) to allow components to communicate without creating hard dependencies, making the system more modular and easier to test in isolation.
* **Engineering Discipline:** Implementing a complete development lifecycle, including configuration management (`.env`), comprehensive logging, a full suite of unit tests with `pytest` (achieving 100% coverage), and automated testing via a **CI/CD pipeline** with GitHub Actions.

---

## 🧩 Implemented Design Patterns in Detail

This project is built upon a foundation of five key design patterns that work together to create a flexible and maintainable system.

### 1. 🏭 Factory Pattern
* **Purpose:** To centralize and abstract the creation of operation objects (e.g., `AddOperation`, `DivideOperation`).
* **Location:** `app/operations.py`
* **Explanation:** Instead of having a large `if/elif/else` block within the main calculator logic to decide which operation to perform, the calculator delegates this responsibility to an `OperationFactory`. The calculator simply asks the factory for an operation object matching a given name (e.g., "add").
* **Benefit:** This **decouples** the calculator's core logic from the concrete implementation of the operations. To add a new operation (e.g., "power"), we only need to create a new `PowerOperation` class and update the factory. The `Calculator` class itself remains completely unchanged, perfectly adhering to the **Open-Closed Principle**.

```python
class OperationFactory:
    @staticmethod
    def create(operation: str):
        if operation == "add":
            return AddOperation()
        elif operation == "divide":
            return DivideOperation()
        # New operations can be added here
        ...
````

### 2\. 🕹️ Command Pattern

  * **Purpose:** To encapsulate a request (an operation) as an object, thereby letting you parameterize clients with different requests, queue or log requests, and support undoable operations.
  * **Location:** `app/command_pattern.py`
  * **Explanation:** When a user types `add 5 7`, we don't just execute the addition immediately. We create an `OperationCommand` object that "wraps" the `AddOperation` and the arguments (`5`, `7`). This command object has a single `execute()` method. The calculator's history manager simply stores these command objects.
  * **Benefit:** This pattern is the key to enabling **undo/redo** functionality. The `History` class maintains a stack of executed commands. To "undo," it can simply pop the last command. It also separates the *issuer* of the request (the CLI input) from the *executor* (the operation object).

<!-- end list -->

```python
class OperationCommand:
    def __init__(self, operation, a, b):
        self.operation = operation
        self.a = a
        self.b = b

    def execute(self):
        # The command encapsulates the logic
        return self.operation.execute(self.a, self.b)
```

### 3\. 🧠 Memento Pattern

  * **Purpose:** To capture and externalize an object's internal state so that the object can be restored to this state later, without violating encapsulation.
  * **Location:** `app/calculator_memento.py`
  * **Explanation:** This pattern works hand-in-hand with the Command pattern to manage the undo/redo stacks. The `Calculator` (the *Originator*) can create a `CalculatorMemento` object, which is a lightweight snapshot of its current state (e.g., the current history of calculations). This memento is given to the `History` class (the *Caretaker*), which stores it.
  * **Benefit:** When a user performs an "undo," the `History` class provides the *previous* memento back to the `Calculator`, which then restores its state from that snapshot. This allows for complex state management (like undoing an entire `clear` operation) without exposing the `Calculator`'s internal structure to the `History` class.

### 4\. 🔔 Observer Pattern

  * **Purpose:** To define a one-to-many dependency between objects so that when one object (the "subject") changes state, all its dependents ("observers") are notified and updated automatically.
  * **Location:** `app/logger.py`
  * **Explanation:** The `Calculator` acts as the **Subject**. We can register multiple **Observers** with it, such as a `LoggingObserver` and an `AutoSaveObserver`. When the `Calculator` performs an operation (a state change), it "notifies" all its registered observers by calling their `update()` method, passing along data about the calculation.
  * **Benefit:** The `Calculator` has no knowledge of what the observers do. It doesn't know or care about logging or auto-saving to CSV. This is a powerful decoupling mechanism. We can add new observers (e.g., one that sends an email, one that updates a GUI) without *any* modification to the `Calculator` class.

<!-- end list -->

```python
# The Calculator notifies observers after an operation
calc.register_observer(LoggingObserver(logger))
calc.register_observer(AutoSaveObserver(cfg))

# This line will automatically trigger both logging and auto-saving
calc.perform_operation("add", 2, 3)
```

### 5\. 🧱 Decorator Pattern

  * **Purpose:** To attach additional responsibilities to an object dynamically. Decorators provide a flexible alternative to subclassing for extending functionality.
  * **Location:** `app/decorators.py`
  * **Explanation:** This pattern is used to create the dynamic `help` menu. Each function that implements a CLI command (like `cmd_add`) is "decorated" with `@register_command`. This decorator is a function that *wraps* the `cmd_add` function. When the file is loaded, the decorator executes, adding the command's name ("add") and its description ("Add two numbers") to a global registry.
  * **Benefit:** The `help` command simply iterates over this registry and prints its contents. This means adding a new command *automatically* adds it to the help menu. We never need to manually edit a `help_menu.py` file, which prevents the help text from becoming outdated.

<!-- end list -->

```python
# This decorator automatically adds the command to the help registry
@register_command("add", "Add two numbers")
def cmd_add(calc, args):
    # ... command logic ...
```

-----

## 🧱 Project Architecture

The project is organized into a clean, modular structure that separates concerns.

```bash
enhanced-calculator/
├── app/
│ ├── __init__.py
│ ├── calculation.py # Calculation data entity
│ ├── calculator.py # Core Calculator logic (Subject)
│ ├── calculator_config.py # Loads configuration (.env)
│ ├── calculator_memento.py # Implements Memento Pattern
│ ├── command_pattern.py # Command Pattern classes
│ ├── commands.py # REPL command implementations
│ ├── decorators.py # Decorator for dynamic help
│ ├── exceptions.py # Custom exception hierarchy
│ ├── help_menu.py # Prints dynamic command menu
│ ├── history.py # Manages history stack (Caretaker)
│ ├── input_validators.py # Input validation logic
│ ├── logger.py # Logging & Observer pattern
│ ├── operations.py # Factory-created operations
│ └── ui_style.py # Color-coded CLI styling
├── tests/ # All pytest-based unit tests
├── .github/workflows/ # GitHub Actions CI pipeline
├── requirements.txt
├── .env
└── README.md
```

-----

## 🖥️ Additional Features

### Color-Coded CLI

  * **Purpose:** To provide a clear, professional, and user-friendly terminal experience.
  * **Location:** `app/ui_style.py`
  * **Implementation:** Using the `colorama` library, terminal output is color-coded based on context:
      * **Success (Green):** For successful results (e.g., `✅ Result: 12.0`).
      * **Warning (Yellow):** For non-terminal issues or undo/redo actions (e.g., `⚠️ Undid last operation.`).
      * **Error (Red):** For critical failures or invalid input (e.g., `❌ Error: Division by zero.`).
      * **Info (Blue):** For general information and prompts.

### 🪵 Logging and Persistence

  * **Logging:** All operations are logged to `logs/app.log` via the `LoggingObserver`. This provides a complete, timestamped audit trail of every calculation performed.
    ```text
    2025-10-23 14:03:22 [INFO] calc: add(5.0, 7.0) = 12.0
    2025-10-23 14:03:24 [INFO] calc: abs_diff(10.0, 4.0) = 6.0
    ```
  * **CSV Auto-Save:** The `AutoSaveObserver` automatically persists the entire calculation history to `history/history.csv` after each successful operation, ensuring no data is lost between sessions.

-----

### 🧾 Configuration Setup (.env)

The application is configured using environment variables stored in a `.env` file, which is loaded on startup. This separates configuration (which changes between environments) from code.

**Example `.env`:**

```bash
# Paths for generated files
CALCULATOR_LOG_DIR=logs
CALCULATOR_HISTORY_DIR=history

# Toggles and Limits
CALCULATOR_AUTO_SAVE=true
CALCULATOR_PRECISION=2
CALCULATOR_MAX_INPUT_VALUE=1000000
CALCULATOR_DEFAULT_ENCODING=utf-8
```

-----

### 🚀 Example Session

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

>>> undo
⚠️  Undid last operation.

>>> history
📜 Calculation History:
  1. add(5.0, 7.0) = 12.0
  2. abs_diff(10.0, 4.0) = 6.0

>>> save
💾 History saved to history/history.csv

>>> exit
👋 Goodbye! Thanks for using Enhanced Calculator.
```

-----

## 🧪 Testing and Coverage

The project enforces a 100% test coverage policy, validated by `pytest` and `pytest-cov`.

### Running Tests

```bash
pytest
```

### Checking Coverage

```bash
pytest --cov=app --cov-report=term-missing
```

This test suite covers all logic, including all operations, edge cases (like division by zero), exception handling, and the correct behavior of all design patterns (e.g., memento restoration, observer notifications).

-----

## 🔄 Continuous Integration (CI/CD)

A GitHub Actions workflow is configured in `.github/workflows/python-app.yml` to automatically run the entire test suite on every `push` and `pull_request`.

This CI pipeline:

1.  Checks out the code.
2.  Sets up a clean Python environment.
3.  Installs all dependencies from `requirements.txt`.
4.  Runs `pytest` and **fails the build** if test coverage drops below 100%.

This automation ensures that no code that breaks existing functionality or lacks tests can be merged into the main branch.

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

-----

## 🧑‍💻 Git Workflow

Development followed a professional Git branching model:

  * Features (e.g., `feature/memento`, `feature/logger`) were developed in isolated branches.
  * Code was merged into `master` via Pull Requests.
  * Each merge was contingent on the CI pipeline passing all tests.

-----

## 🏁 Conclusion

This **Enhanced Calculator** project successfully demonstrates how to architect a simple application using professional engineering practices. By implementing core design patterns, the calculator is transformed from a simple script into a robust, maintainable, and extensible system. The focus on decoupling, testability, and automation (CI/CD) reflects a modern approach to software development in Python.

> “Clean code and modular design are not the end — they’re the beginning of scalable innovation.”
> — Rajat Pednekar

-----

## 🏗️ Future Enhancements

  * **API Layer:** Introduce a REST API using FastAPI or Flask to expose the calculator logic as a web service.
  * **GUI:** Build a graphical user interface (GUI) using Tkinter or PyQt that consumes the core calculator logic.
  * **Database:** Replace CSV persistence with a more robust database solution like SQLite or PostgreSQL.
  * **Expression Parser:** Implement a math expression parser to handle complex, chained inputs like `(5 + 10) / 3`.

<!-- end list -->

```
```
