"""Public API: product of two finite numeric inputs."""

import math
import numbers

__all__ = ["compute"]


def compute(a, b):
    """Return the product of two finite numeric inputs.

    Supports zero, negative and fractional values, e.g.:

    >>> compute(2, 3)
    6
    >>> compute(0, 5)
    0
    >>> compute(-2, 3)
    -6
    >>> compute(2.5, 4)
    10.0

    Raises:
        TypeError: if either input is not a real number.
        ValueError: if either input is not finite (NaN or infinity).
    """
    for name, value in (("a", a), ("b", b)):
        if not isinstance(value, numbers.Real):
            raise TypeError(
                "%s must be a finite numeric input, got %s"
                % (name, type(value).__name__)
            )
        if isinstance(value, float) and not math.isfinite(value):
            raise ValueError("%s must be finite, got %r" % (name, value))
    return a * b
