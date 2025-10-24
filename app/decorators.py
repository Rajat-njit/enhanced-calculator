# app/decorators.py
from typing import Callable, Dict, Any

operation_registry: Dict[str, Dict[str, Any]] = {}

def register_operation(name: str, desc: str):
    """Decorator that registers an operation class with metadata."""
    def decorator(cls_or_func: Callable):
        operation_registry[name.lower()] = {
            "name": name.lower(),
            "desc": desc.strip(),
            "ref": cls_or_func,
        }
        return cls_or_func
    return decorator
