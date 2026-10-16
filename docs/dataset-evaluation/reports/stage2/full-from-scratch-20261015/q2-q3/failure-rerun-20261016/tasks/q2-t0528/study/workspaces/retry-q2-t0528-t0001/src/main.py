"""Minimal-value utility.

Provides :func:`compute`, which returns the minimum of two finite numeric
inputs (integers, floats, zero, negative and fractional values are all
supported).
"""

import math
import numbers


def compute(a, b):
    """Return the minimum of two finite numeric inputs.

    Examples:
        compute(2, 3) -> 2
        compute(-1.5, 0) -> -1.5
        compute(0, -7) -> -7

    Raises:
        TypeError: if either input is not a real number.
        ValueError: if either input is not finite (NaN or infinity).
    """
    for name, value in (("a", a), ("b", b)):
        if isinstance(value, bool) or not isinstance(value, numbers.Real):
            raise TypeError(
                "compute() expects finite numeric inputs; "
                "%s=%r is not a real number" % (name, value)
            )
        if not math.isfinite(value):
            raise ValueError(
                "compute() expects finite numeric inputs; "
                "%s=%r is not finite" % (name, value)
            )
    return min(a, b)
