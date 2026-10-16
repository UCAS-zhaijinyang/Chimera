"""Main module exposing compute(a, b): the arithmetic mean of two finite numbers."""

try:  # Package-style import (src is a package or imported as one).
    from .helper import mean_values
except ImportError:  # Fallback: src directory itself on sys.path.
    from helper import mean_values


def compute(a, b):
    """Return the arithmetic mean of two finite numeric inputs.

    Example:
        compute(2, 3) -> 2.5

    Zero, negative and fractional values are supported. Validation and the
    mean calculation are delegated to helper.mean_values.
    """
    return mean_values(a, b)


if __name__ == "__main__":
    print(compute(2, 3))
