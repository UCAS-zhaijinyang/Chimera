"""Helper module providing the arithmetic mean of two finite numeric inputs."""


def mean_values(a, b):
    """Return the arithmetic mean of two finite numeric inputs.

    Supports zero, negative and fractional values.

    Args:
        a: First numeric value (int or float, must be finite).
        b: Second numeric value (int or float, must be finite).

    Returns:
        The arithmetic mean of ``a`` and ``b`` as a number.

    Raises:
        TypeError: If either input is not a real number (bool is rejected).
        ValueError: If either input is not finite (NaN or infinity).
    """
    for name, value in (("a", a), ("b", b)):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(
                "%s must be a finite numeric value, got %r" % (name, value)
            )
        if value != value or value in (float("inf"), float("-inf")):
            raise ValueError("%s must be finite, got %r" % (name, value))
    return (a + b) / 2
