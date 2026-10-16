"""Public entry point exposing :func:`compute`.

``compute(a, b)`` returns the arithmetic mean of two finite numeric
inputs. The core logic lives in :func:`helper.mean_values` and is
imported and reused here so the behavior is defined in one place.
"""

from helper import mean_values

__all__ = ["compute"]


def compute(a, b):
    """Return the arithmetic mean of two finite numeric inputs.

    Examples:
        >>> compute(2, 3)
        2.5
        >>> compute(0, -4)
        -2.0
        >>> compute(-1.5, 2.5)
        0.5

    Zero, negative and fractional values are supported. Non-numeric or
    non-finite inputs (e.g. ``NaN`` or ``inf``) raise ``ValueError``.
    """
    return mean_values(a, b)
