"""Helper module providing the arithmetic mean of two values.

This module holds the core computation used by ``src/main.py``:
:func:`mean_values` returns the arithmetic mean of two finite numeric
inputs and supports zero, negative and fractional values.
"""

import math
import numbers

__all__ = ["mean_values"]


def _validate_finite_number(value, name):
    """Raise ``ValueError`` unless *value* is a finite real number.

    ``bool`` is explicitly rejected even though it subclasses ``int``,
    because it does not carry numeric meaning for this API.
    """
    if isinstance(value, bool) or not isinstance(value, numbers.Real):
        raise ValueError(
            "%s must be a finite number, got %s"
            % (name, type(value).__name__)
        )
    # Only floats can be NaN/inf; ``math.isfinite`` on very large ints
    # would raise OverflowError, so restrict the finiteness check.
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError("%s must be a finite number, got %r" % (name, value))


def mean_values(a, b):
    """Return the arithmetic mean of two finite numeric values.

    The mean is computed with true division, so integer inputs produce a
    float result (``mean_values(2, 3) == 2.5``). Zero, negative and
    fractional values are all supported.

    Raises:
        ValueError: if ``a`` or ``b`` is not a finite real number.
    """
    _validate_finite_number(a, "a")
    _validate_finite_number(b, "b")
    return (a + b) / 2
