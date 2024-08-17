"""Method to validate kwargs of `from_parameters` methods in GMX V2 actions."""
from functools import wraps
from typing import Any, Callable


def validate_kwargs(
    required_keys: set[str],
) -> Callable[[Callable[[Any, Any], Any]], Callable[[Any, Any], Any]]:
    """Decorator to validate kwargs of `from_parameters` methods in GMX V2 actions."""

    def _decorator(func: Callable[[Any, Any], Any]) -> Callable[[Any, Any], Any]:
        @wraps(func)
        def wrapper(*args: list[Any], **kwargs: dict[str, Any]) -> Any:
            missing_keys = required_keys - kwargs.keys()
            if missing_keys:
                raise ValueError(f"Missing required keys: {missing_keys}")
            return func(*args, **kwargs)

        return wrapper

    return _decorator
