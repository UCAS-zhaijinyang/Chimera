"""Public API: compute(a, b) returns the maximum of two finite numeric inputs."""

import math
import numbers


def compute(a, b):
    """Return the maximum of two finite numeric inputs.

    Supports zero, negative, and fractional values (int and float).

    Examples:
        compute(2, 3) -> 3
        compute(-1, 0) -> 0
        compute(2.5, 2.4) -> 2.5
        compute(-3.5, -2.5) -> -2.5

    Raises:
        TypeError: if either argument is not a real number.
        ValueError: if either argument is not finite (NaN or infinity).
    """
    for name, value in (("a", a), ("b", b)):
        if isinstance(value, bool) or not isinstance(value, numbers.Real):
            raise TypeError(
                f"{name} must be a finite real number, got {type(value).__name__}"
            )
        if not math.isfinite(value):
            raise ValueError(f"{name} must be finite, got {value!r}")
    return b if b > a else a
