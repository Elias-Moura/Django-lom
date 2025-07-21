from typing import Any


def is_positive_number(value: Any) -> bool:
    try:
        number = float(value)
    except ValueError:
        return False
    return number > 0