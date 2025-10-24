# pragma: no cover
"""Command-Line REPL interface for Enhanced Calculator (Decorator-based Help)."""

import sys
from colorama import Fore, Style, init
init(autoreset=True)

from app.calculator import Calculator
from app.history import History
from app.calculator_memento import Caretaker
from app.exceptions import ValidationError, OperationError, HistoryError
from app.logger import configure_logger_from_config, LoggingObserver, AutoSaveObserver

from app.help_menu import COMMAND_REGISTRY, print_help_menu
import app.commands  # <-- IMPORTANT: imports register all commands via decorators


def main():
    calc = Calculator(History(), Caretaker())

    # attach observers
    logger = configure_logger_from_config(calc.config)
    calc.register_observer(LoggingObserver(logger))
    if calc.config.auto_save:
        calc.register_observer(AutoSaveObserver(calc.config))

    print(Fore.CYAN + "\n=== 🧮 Enhanced Calculator ===" + Style.RESET_ALL)
    print(Fore.YELLOW + "Type 'help' to see available commands.")
    print("Type 'exit' to quit.\n" + Style.RESET_ALL)

    while True:
        try:
            raw = input(Fore.BLUE + ">>> " + Style.RESET_ALL).strip()
            if not raw:
                continue

            parts = raw.split()
            cmd, args = parts[0].lower(), parts[1:]

            # Dispatch via registry
            if cmd in COMMAND_REGISTRY:
                desc, handler = COMMAND_REGISTRY[cmd]
                handler(calc, args)
                continue

            print(Fore.RED + f"Unknown command: '{cmd}'. Type 'help' for a list of commands." + Style.RESET_ALL)

        except (ValidationError, OperationError, HistoryError) as e:
            print(Fore.RED + f"❌ Error: {e}" + Style.RESET_ALL)
        except KeyboardInterrupt:
            print(Fore.CYAN + "\n👋 Interrupted. Exiting gracefully." + Style.RESET_ALL)
            sys.exit(0)
        except EOFError:
            print(Fore.CYAN + "\n👋 Goodbye! (EOF received)" + Style.RESET_ALL)
            sys.exit(0)
        except Exception as e:
            print(Fore.RED + f"Unexpected error: {e}" + Style.RESET_ALL)


if __name__ == "__main__":
    main()