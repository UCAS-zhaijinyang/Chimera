"""Unit tests for compute(a, b) in src/main.py."""

import os
import sys
import unittest

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src")
)

from main import compute  # noqa: E402


class TestCompute(unittest.TestCase):
    def test_mean_of_two_and_three(self):
        """Required check: compute(2, 3) must equal 2.5."""
        self.assertEqual(compute(2, 3), 2.5)

    def test_zero_values(self):
        self.assertEqual(compute(0, 0), 0)
        self.assertEqual(compute(0, 4), 2.0)

    def test_negative_values(self):
        self.assertEqual(compute(-2, -4), -3.0)
        self.assertEqual(compute(-1, 1), 0.0)

    def test_fractional_values(self):
        self.assertEqual(compute(1.5, 2.5), 2.0)
        self.assertAlmostEqual(compute(0.1, 0.2), 0.15)

    def test_symmetry(self):
        self.assertEqual(compute(7, 3), compute(3, 7))


if __name__ == "__main__":
    unittest.main()
