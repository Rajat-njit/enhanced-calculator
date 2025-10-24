# app/help_menu.py
from __future__ import annotations
from typing import Callable, Dict, Tuple, List
from colorama import Fore, Style

# name -> (description, handler)
COMMAND_REGISTRY: Dict[str, Tuple[str, Callable]] = {}

def register_command(name: str, description: str):
    """Decorator to register a CLI command dynamically."""
    def decorator(func: Callable):
        COMMAND_REGISTRY[name] = (description, func)
        return func
    return decorator

def list_commands() -> List[tuple[str, str]]:
    """(name, description) sorted for help menu."""
    return sorted((name, meta[0]) for name, meta in COMMAND_REGISTRY.items())

def print_help_menu():
    print(Fore.CYAN + "\n=== 🧭 Available Commands ===" + Style.RESET_ALL)
    for name, desc in list_commands():
        print(f"  {Fore.BLUE}{name:<12}{Style.RESET_ALL} - {desc}")
    print()
