"""Input validators (Phase 0 stub)."""
def is_number(x) -> bool:
    try:
        float(x)
        return True
    except (TypeError, ValueError):
        return False
