"""Helper module providing the arithmetic-mean primitive.

The core math for the compute() feature lives here so that src/main.py can
import and reuse it (single source of truth for the mean calculation).
"""

import math

__all__ = ["mean_values"]


def _validate_finite_number(value, name):
    """Raise TypeError/ValueError unless *value* is a finite real number."""
    # bool is a subclass of int but is not a meaningful numeric input here.
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(
            "%s must be a finite number (int or float), got %s"
            % (name, type(value).__name__)
        )
    if not math.isfinite(value):
        raise ValueError("%s must be finite, got %r" % (name, value))


def mean_values(a, b):
    """Return the arithmetic mean of two finite numeric inputs.

    Supports zero, negative and fractional values. The result is always a
    float, so integer inputs still yield fractional means (e.g. (2 + 3) / 2
    == 2.5).

    Raises:
        TypeError: if a or b is not an int/float (bool is rejected too).
        ValueError: if a or b is NaN or +/- infinity.
    """
    _validate_finite_number(a, "a")
    _validate_finite_number(b, "b")
    return (a + b) / 2.0
