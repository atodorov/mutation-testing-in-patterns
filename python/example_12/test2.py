import percent
import unittest

class TestPercent(unittest.TestCase):
    def test_lower_boundary(self):
        result = percent.validate_percent(0)
        self.assertEqual(result, 0)

    def test_upper_boundary(self):
        result = percent.validate_percent(100)
        self.assertEqual(result, 100)

    def test_below_lower_boundary(self):
        with self.assertRaises(Exception):
            percent.validate_percent(-1)

    def test_above_upper_boundary(self):
        with self.assertRaises(Exception):
            percent.validate_percent(101)

if __name__ == "__main__":
    unittest.main()
