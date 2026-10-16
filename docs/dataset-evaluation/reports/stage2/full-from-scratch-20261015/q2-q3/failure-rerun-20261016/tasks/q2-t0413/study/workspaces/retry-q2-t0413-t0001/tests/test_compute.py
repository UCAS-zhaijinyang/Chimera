"""Unit tests for compute(a, b) in src/main.py.

Run from the workspace root with either:
    /opt/anaconda3/bin/python -m unittest discover -s tests
    /opt/anaconda3/bin/python -m pytest tests/test_compute.py
"""

import os
import sys
import unittest

# Make the workspace root importable so "src.main" resolves regardless of
# the directory the test runner is invoked from.
WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if WORKSPACE_ROOT not in sys.path:
    sys.path.insert(0, WORKSPACE_ROOT)

from src.main import compute  # noqa: E402


class TestCompute(unittest.TestCase):
    """Behavioral checks for the arithmetic-mean feature."""

    def test_basic_mean(self):
        """Required check: compute(2, 3) must return 2.5."""
        self.assertEqual(compute(2, 3), 2.5)

    def test_zero_values(self):
        """Zero inputs are supported."""
        self.assertEqual(compute(0, 0), 0.0)
        self.assertEqual(compute(-4, 4), 0.0)

    def test_negative_values(self):
        """Negative inputs are supported."""
        self.assertEqual(compute(-2, -4), -3.0)
        self.assertEqual(compute(-10, 0), -5.0)

    def test_fractional_values(self):
        """Fractional inputs are supported."""
        self.assertEqual(compute(0.5, 0.25), 0.375)
        self.assertAlmostEqual(compute(1.5, 2.5), 2.0)

    def test_returns_float(self):
        """The result is always a float, even for int inputs."""
        self.assertIsInstance(compute(2, 3), float)
        self.assertIsInstance(compute(-1, 1), float)


if __name__ == "__main__":
    unittest.main()
