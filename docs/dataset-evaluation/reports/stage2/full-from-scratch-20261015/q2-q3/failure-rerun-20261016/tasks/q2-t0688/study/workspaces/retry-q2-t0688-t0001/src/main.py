"""Arithmetic helper module.

Provides :func:`compute`, which returns the product of two finite
numeric inputs. Zero, negative, and fractional values are supported.
"""


def compute(a, b):
    """Return the product of the two given finite numeric inputs.

    Examples
    --------
    >>> compute(2, 3)
    6
    >>> compute(0, 5)
    0
    >>> compute(-2, 3)
    -6
    >>> compute(2.5, 4)
    10.0
    """
    return a * b
