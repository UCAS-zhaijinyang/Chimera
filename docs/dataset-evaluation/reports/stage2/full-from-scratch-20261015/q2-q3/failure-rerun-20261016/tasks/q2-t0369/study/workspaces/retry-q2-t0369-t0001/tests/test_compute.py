"""Unit tests for ``compute`` in ``src/main.py``.

Run with: /opt/anaconda3/bin/python -m unittest discover -s tests -v
"""

import math
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from main import compute  # noqa: E402


class TestCompute(unittest.TestCase):
    """Behavioral tests for the arithmetic mean feature."""

    def test_basic_example(self):
        """The documented example: compute(2, 3) must return 2.5."""
        self.assertEqual(compute(2, 3), 2.5)

    def test_true_division_for_integers(self):
        """Integer inputs must use true division, not floor division."""
        self.assertIsInstance(compute(2, 3), float)
        self.assertEqual(compute(1, 2), 1.5)
        self.assertEqual(compute(4, 6), 5.0)

    def test_zero_values(self):
        """Zero must be supported as an input."""
        self.assertEqual(compute(0, 0), 0.0)
        self.assertEqual(compute(0, 10), 5.0)
        self.assertEqual(compute(0, -4), -2.0)

    def test_negative_values(self):
        """Negative values must be supported."""
        self.assertEqual(compute(-2, -4), -3.0)
        self.assertEqual(compute(-10, 10), 0.0)
        self.assertEqual(compute(-7, 0), -3.5)

    def test_fractional_values(self):
        """Fractional (float) values must be supported."""
        self.assertEqual(compute(-1.5, 2.5), 0.5)
        self.assertAlmostEqual(compute(0.1, 0.2), 0.15)
        self.assertEqual(compute(1.25, 3.75), 2.5)

    def test_symmetry(self):
        """The mean must be symmetric in its arguments."""
        self.assertEqual(compute(2, 3), compute(3, 2))
        self.assertEqual(compute(-1.5, 7.25), compute(7.25, -1.5))

    def test_rejects_non_numeric(self):
        """Non-numeric inputs must raise ValueError."""
        for bad in ("2", None, [2], {"a": 1}):
            with self.assertRaises(ValueError):
                compute(bad, 3)
            with self.assertRaises(ValueError):
                compute(2, bad)

    def test_rejects_non_finite(self):
        """NaN and infinity must raise ValueError."""
        for bad in (float("nan"), float("inf"), float("-inf")):
            with self.assertRaises(ValueError):
                compute(bad, 3)
            with self.assertRaises(ValueError):
                compute(2, bad)

    def test_helper_mean_values_used(self):
        """compute must delegate to helper.mean_values."""
        from helper import mean_values

        self.assertEqual(compute(2, 3), mean_values(2, 3))
        self.assertEqual(compute(-1.5, 2.5), mean_values(-1.5, 2.5))


if __name__ == "__main__":
    unittest.main()
