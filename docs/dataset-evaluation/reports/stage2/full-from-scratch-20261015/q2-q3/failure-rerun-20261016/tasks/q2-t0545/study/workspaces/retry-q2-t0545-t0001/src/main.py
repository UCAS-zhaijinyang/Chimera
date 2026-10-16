"""Compute the difference of two finite numeric inputs."""

import math


def compute(a, b):
    """Return the difference ``a - b`` of two finite numeric inputs.

    Supports zero, negative and fractional values, e.g. ``compute(2, 3)``
    returns ``-1``. Non-numeric inputs raise ``TypeError`` and non-finite
    values (NaN, +/-inf) raise ``ValueError``.
    """
    for name, value in (("a", a), ("b", b)):
        if not isinstance(value, (int, float)):
            raise TypeError(
                "%s must be a finite number, got %s" % (name, type(value).__name__)
            )
        if not math.isfinite(value):
            raise ValueError("%s must be a finite number, got %r" % (name, value))
    return a - b
