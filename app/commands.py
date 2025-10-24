# Author: Rajat Pednekar | UCID: rp2348
"""
commands.py
------------
Implements the command-line REPL for the Enhanced Calculator.

Features:
    - Dynamic help menu (Decorator Pattern)
    - Color-coded outputs using Colorama (via UI class)
    - Undo/Redo, History, and Persistence (Memento Pattern)
    - Observers for logging and autosave
    - Command Pattern for encapsulating operations
    - Integrated logger for session-level actions
"""

from __future__ import annotations
from app.help_menu import register_command, print_help_menu
from app.ui_style import UI
from app.exceptions import ValidationError, OperationError, HistoryError
from app.command_pattern import OperationCommand
from app.logger import configure_logger_from_config


# Initialize shared logger (via calculator config)
# This ensures all commands can log session actions.
from app.calculator_config import CalculatorConfig
logger = configure_logger_from_config(CalculatorConfig())


# ---------------------------
# Utility for Parsing
# ---------------------------

def _parse_two_numbers(args):
    """Ensure two numeric arguments are provided."""
    if len(args) != 2:
        raise ValidationError("This command requires exactly two numbers.")
    try:
        return float(args[0]), float(args[1])
    except ValueError:
        raise ValidationError("Both operands must be numbers.")


# ---------------------------
# Arithmetic Commands (Command Pattern)
# ---------------------------

@register_command("add", "Add two numbers")
def cmd_add(calc, args):
    a, b = _parse_two_numbers(args)
    cmd = OperationCommand(calc, "add", a, b)
    result = cmd.execute()
    print(UI.SUCCESS + f"{UI.ICONS['success']} Result: {result}" + UI.RESET)
    logger.info("Operation: add(%s, %s) = %s", a, b, result)


@register_command("subtract", "Subtract two numbers")
def cmd_subtract(calc, args):
    a, b = _parse_two_numbers(args)
    cmd = OperationCommand(calc, "subtract", a, b)
    result = cmd.execute()
    print(UI.SUCCESS + f"{UI.ICONS['success']} Result: {result}" + UI.RESET)
    logger.info("Operation: subtract(%s, %s) = %s", a, b, result)


@register_command("multiply", "Multiply two numbers")
def cmd_multiply(calc, args):
    a, b = _parse_two_numbers(args)
    cmd = OperationCommand(calc, "multiply", a, b)
    result = cmd.execute()
    print(UI.SUCCESS + f"{UI.ICONS['success']} Result: {result}" + UI.RESET)
    logger.info("Operation: multiply(%s, %s) = %s", a, b, result)


@register_command("divide", "Divide two numbers")
def cmd_divide(calc, args):
    a, b = _parse_two_numbers(args)
    cmd = OperationCommand(calc, "divide", a, b)
    result = cmd.execute()
    print(UI.SUCCESS + f"{UI.ICONS['success']} Result: {result}" + UI.RESET)
    logger.info("Operation: divide(%s, %s) = %s", a, b, result)


@register_command("power", "Raise one number to the power of another")
def cmd_power(calc, args):
    a, b = _parse_two_numbers(args)
    cmd = OperationCommand(calc, "power", a, b)
    result = cmd.execute()
    print(UI.SUCCESS + f"{UI.ICONS['success']} Result: {result}" + UI.RESET)
    logger.info("Operation: power(%s, %s) = %s", a, b, result)


@register_command("root", "Find the nth root of a number")
def cmd_root(calc, args):
    a, b = _parse_two_numbers(args)
    cmd = OperationCommand(calc, "root", a, b)
    result = cmd.execute()
    print(UI.SUCCESS + f"{UI.ICONS['success']} Result: {result}" + UI.RESET)
    logger.info("Operation: root(%s, %s) = %s", a, b, result)


@register_command("modulus", "Find remainder of division")
def cmd_modulus(calc, args):
    a, b = _parse_two_numbers(args)
    cmd = OperationCommand(calc, "modulus", a, b)
    result = cmd.execute()
    print(UI.SUCCESS + f"{UI.ICONS['success']} Result: {result}" + UI.RESET)
    logger.info("Operation: modulus(%s, %s) = %s", a, b, result)


@register_command("int_divide", "Integer division (truncate)")
def cmd_int_divide(calc, args):
    a, b = _parse_two_numbers(args)
    cmd = OperationCommand(calc, "int_divide", a, b)
    result = cmd.execute()
    print(UI.SUCCESS + f"{UI.ICONS['success']} Result: {result}" + UI.RESET)
    logger.info("Operation: int_divide(%s, %s) = %s", a, b, result)


@register_command("percent", "Percentage (a/b * 100)")
def cmd_percent(calc, args):
    a, b = _parse_two_numbers(args)
    cmd = OperationCommand(calc, "percent", a, b)
    result = cmd.execute()
    print(UI.SUCCESS + f"{UI.ICONS['success']} Result: {result}%" + UI.RESET)
    logger.info("Operation: percent(%s, %s) = %s%%", a, b, result)


@register_command("abs_diff", "Absolute difference between numbers")
def cmd_abs_diff(calc, args):
    a, b = _parse_two_numbers(args)
    cmd = OperationCommand(calc, "abs_diff", a, b)
    result = cmd.execute()
    print(UI.SUCCESS + f"{UI.ICONS['success']} Result: {result}" + UI.RESET)
    logger.info("Operation: abs_diff(%s, %s) = %s", a, b, result)


# ---------------------------
# History & Utility Commands
# ---------------------------

@register_command("history", "Display calculation history")
def cmd_history(calc, args):
    hist = calc.get_history()
    if not hist:
        print(UI.WARNING + f"{UI.ICONS['warn']} (no history yet)" + UI.RESET)
        logger.info("User checked history — empty.")
        return
    print(UI.INFO + f"\n{UI.ICONS['history']} Calculation History:" + UI.RESET)
    for i, entry in enumerate(hist, 1):
        print(UI.PROMPT + f"  {i}. {entry}" + UI.RESET)
    logger.info("Displayed %d history entries.", len(hist))


@register_command("clear", "Clear the history and reset")
def cmd_clear(calc, args):
    calc.clear_history()
    print(UI.INFO + f"{UI.ICONS['clear']} History cleared." + UI.RESET)
    logger.info("User cleared calculator history.")


@register_command("undo", "Undo the last operation")
def cmd_undo(calc, args):
    try:
        calc.undo()
        print(UI.WARNING + f"{UI.ICONS['undo']} Undid last operation." + UI.RESET)
        logger.info("Undo executed successfully.")
    except HistoryError as e:
        print(UI.ERROR + f"{UI.ICONS['error']} {e}" + UI.RESET)
        logger.warning("Undo failed: %s", e)


@register_command("redo", "Redo a previously undone operation")
def cmd_redo(calc, args):
    try:
        calc.redo()
        print(UI.WARNING + f"{UI.ICONS['redo']} Redid last operation." + UI.RESET)
        logger.info("Redo executed successfully.")
    except HistoryError as e:
        print(UI.ERROR + f"{UI.ICONS['error']} {e}" + UI.RESET)
        logger.warning("Redo failed: %s", e)


@register_command("save", "Manually save calculation history to CSV")
def cmd_save(calc, args):
    calc.history.save_to_csv(calc.config.history_path, calc.config.default_encoding)
    print(UI.INFO + f"{UI.ICONS['save']} History saved to {calc.config.history_path}" + UI.RESET)
    logger.info("History manually saved to %s", calc.config.history_path)


@register_command("load", "Load calculation history from CSV")
def cmd_load(calc, args):
    calc.history.load_from_csv(calc.config.history_path, calc.config.default_encoding)
    print(UI.INFO + f"{UI.ICONS['load']} History loaded from {calc.config.history_path}" + UI.RESET)
    logger.info("History manually loaded from %s", calc.config.history_path)


@register_command("help", "Show available commands")
def cmd_help(calc, args):
    print_help_menu()
    logger.info("User requested help menu.")


@register_command("exit", "Exit the calculator gracefully")
def cmd_exit(calc, args):
    from sys import exit
    print(UI.HEADER + f"\n{UI.ICONS['exit']} Goodbye! Thanks for using Enhanced Calculator." + UI.RESET)
    logger.info("👋 User exited the calculator gracefully.")
    logger.info("=== Session Ended ===")
    exit(0)
