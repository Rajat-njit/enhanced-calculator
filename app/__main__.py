# pragma: no cover
"""Command-Line REPL interface for Enhanced Calculator (Dynamic Help + Color UI)."""

import sys
from colorama import init
init(autoreset=True)

from app.ui_style import UI
from app.calculator import Calculator
from app.history import History
from app.calculator_memento import Caretaker
from app.logger import configure_logger_from_config, LoggingObserver, AutoSaveObserver
from app.exceptions import ValidationError, OperationError, HistoryError

from app.help_menu import COMMAND_REGISTRY, print_help_menu
import app.commands  # <-- Import triggers registration of all @register_command functions


def main():
    """Main REPL loop for the Enhanced Calculator."""
    calc = Calculator(History(), Caretaker())

    # Attach Observers
    logger = configure_logger_from_config(calc.config)
    calc.register_observer(LoggingObserver(logger))
    if calc.config.auto_save:
        calc.register_observer(AutoSaveObserver(calc.config))

    # Welcome Banner
    print(UI.HEADER + f"\n=== {UI.ICONS['calc']} Enhanced Calculator ===" + UI.RESET)
    print(UI.WARNING + "Type 'help' to see available commands." + UI.RESET)
    print("Type 'exit' to quit.\n")

    while True:
        try:
            raw = input(UI.PROMPT + ">>> " + UI.RESET).strip()
            if not raw:
                continue

            parts = raw.split()
            cmd, args = parts[0].lower(), parts[1:]

            if cmd in COMMAND_REGISTRY:
                _, handler = COMMAND_REGISTRY[cmd]
                handler(calc, args)
                continue

            print(UI.ERROR + f"{UI.ICONS['error']} Unknown command: '{cmd}'. Type 'help' for a list of commands." + UI.RESET)

        except (ValidationError, OperationError, HistoryError) as e:
            print(UI.ERROR + f"{UI.ICONS['error']} {e}" + UI.RESET)
        except KeyboardInterrupt:
            print(UI.HEADER + f"\n{UI.ICONS['exit']} Interrupted. Exiting gracefully." + UI.RESET)
            sys.exit(0)
        except EOFError:
            print(UI.HEADER + f"\n{UI.ICONS['exit']} Goodbye! (EOF received)" + UI.RESET)
            sys.exit(0)
        except Exception as e:
            print(UI.ERROR + f"{UI.ICONS['error']} Unexpected error: {e}" + UI.RESET)


if __name__ == "__main__":
    main()
