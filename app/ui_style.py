# app/ui_style.py
from colorama import Fore, Style

class UI:
    """Reusable color and symbol constants for the CLI."""
    # Headings & banners
    HEADER = Fore.CYAN + Style.BRIGHT
    PROMPT = Fore.BLUE + Style.BRIGHT

    # Message types
    SUCCESS = Fore.GREEN + Style.BRIGHT
    WARNING = Fore.YELLOW + Style.BRIGHT
    ERROR = Fore.RED + Style.BRIGHT
    INFO = Fore.MAGENTA + Style.BRIGHT

    # Symbols
    ICONS = {
        "success": "✅",
        "error": "❌",
        "warn": "⚠️",
        "info": "ℹ️",
        "calc": "🧮",
        "save": "💾",
        "load": "📂",
        "undo": "↩️",
        "redo": "↪️",
        "clear": "🧹",
        "exit": "👋",
        "history": "📜",
    }

    RESET = Style.RESET_ALL
