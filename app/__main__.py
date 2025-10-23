"""Command-Line REPL interface for Enhanced Calculator (Phase 3.4)."""

import sys
from app.calculator import Calculator
from app.history import History
from app.calculator_memento import Caretaker
from app.exceptions import ValidationError, OperationError, HistoryError


COMMANDS = {
    "add": "Add two numbers",
    "subtract": "Subtract two numbers",
    "multiply": "Multiply two numbers",
    "divide": "Divide two numbers",
    "power": "Raise one number to the power of another",
    "root": "Find the nth root of a number",
    "modulus": "Find remainder of division",
    "int_divide": "Integer division (truncate)",
    "percent": "Percentage (a/b * 100)",
    "abs_diff": "Absolute difference between numbers",
    "undo": "Undo the last operation",
    "redo": "Redo a previously undone operation",
    "history": "Display all past calculations",
    "clear": "Clear the history and reset",
    "help": "Show available commands",
    "exit": "Exit the calculator",
}


def show_help():
    print("\nAvailable Commands:")
    for cmd, desc in COMMANDS.items():
        print(f"  {cmd:<12} - {desc}")
    print()


def parse_numbers(args):
    """Convert user input args into floats if possible."""
    if len(args) != 2:
        raise ValidationError("This command requires exactly two numbers.")
    try:
        return float(args[0]), float(args[1])
    except ValueError:
        raise ValidationError("Both operands must be numbers.")


def main():
    calc = Calculator(History(), Caretaker())

    print("\n=== 🧮 Enhanced Calculator ===")
    print("Type 'help' to see available commands.")
    print("Type 'exit' to quit.\n")

    while True:
        try:
            raw = input(">>> ").strip()
            if not raw:
                continue

            parts = raw.split()
            cmd = parts[0].lower()
            args = parts[1:]

            # --- Exit / Help commands ---
            if cmd == "exit":
                print("Goodbye! 👋")
                sys.exit(0)
            elif cmd == "help":
                show_help()
                continue

            # --- History commands ---
            elif cmd == "history":
                hist = calc.get_history()
                if not hist:
                    print("(no history yet)")
                else:
                    for i, entry in enumerate(hist, 1):
                        print(f"{i}. {entry}")
                continue
            elif cmd == "clear":
                calc.clear_history()
                print("History cleared.")
                continue
            elif cmd == "undo":
                try:
                    calc.undo()
                    print("Undid last operation.")
                except HistoryError as e:
                    print(f"⚠️  {e}")
                continue
            elif cmd == "redo":
                try:
                    calc.redo()
                    print("Redid last operation.")
                except HistoryError as e:
                    print(f"⚠️  {e}")
                continue

            # --- Arithmetic commands ---
            elif cmd in COMMANDS and cmd not in {"help", "exit", "history", "undo", "redo", "clear"}:
                a, b = parse_numbers(args)
                result = calc.perform_operation(cmd, a, b)
                print(f"Result: {result}")
                continue

            else:
                print(f"Unknown command: '{cmd}'. Type 'help' for a list of commands.")

        except (ValidationError, OperationError) as e:
            print(f"❌ Error: {e}")
        except KeyboardInterrupt:
            print("\nInterrupted. Exiting gracefully.")
            sys.exit(0)
        except EOFError:
            print("\nGoodbye! 👋")
            sys.exit(0)
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
