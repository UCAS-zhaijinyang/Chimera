"""Public compute(a, b) feature: product of two finite numeric inputs.

Implements the requirement from issue f2c5fc2cd26d:
- compute(2, 3) returns 6
- supports zero, negative and fractional values
- rejects non-numeric and non-finite inputs
"""

import math
import numbers

__all__ = ["compute"]


def _validate(value, name):
    """Validate that *value* is a finite real number.

    Raises:
        TypeError: if value is not a real number (bool is rejected).
        ValueError: if value is NaN or +/- infinity.
    """
    if isinstance(value, bool) or not isinstance(value, numbers.Real):
        raise TypeError(
            f"{name} must be a finite number, got {type(value).__name__}"
        )
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            raise ValueError(f"{name} must be a finite number, got {value!r}")
    return value


def compute(a, b):
    """Return the product of two finite numeric inputs.

    Examples:
        >>> compute(2, 3)
        6
        >>> compute(0, 5)
        0
        >>> compute(-2, 3)
        -6
        >>> compute(2.5, 4)
        10.0
    """
    _validate(a, "a")
    _validate(b, "b")
    return a * b
