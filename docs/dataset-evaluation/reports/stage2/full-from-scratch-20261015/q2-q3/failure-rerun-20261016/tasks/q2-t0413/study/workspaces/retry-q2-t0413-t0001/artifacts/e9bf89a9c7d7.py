"""Public entry point for the arithmetic-mean feature.

compute(a, b) returns the arithmetic mean of two finite numeric inputs,
e.g. compute(2, 3) == 2.5. The actual math is implemented by mean_values()
in src/helper.py and imported/used here.
"""

try:  # Package-style import (src is a package / imported as src.main).
    from .helper import mean_values
except ImportError:  # Fallback: src itself is on sys.path (checks/tests).
    from helper import mean_values

__all__ = ["compute"]


def compute(a, b):
    """Return the arithmetic mean of two finite numeric inputs.

    Delegates to mean_values() from src/helper.py. Supports zero, negative
    and fractional values; the result is always a float, so compute(2, 3)
    returns 2.5.

    Raises:
        TypeError: if a or b is not an int/float (bool is rejected too).
        ValueError: if a or b is NaN or +/- infinity.
    """
    return mean_values(a, b)
