import percent
import unittest

class TestPercent(unittest.TestCase):
    def test_value_in_range(self):
        result = percent.validate_percent(50)
        self.assertEqual(result, 50)

    def test_value_not_in_range(self):
        with self.assertRaises(Exception):
            percent.validate_percent(500)

        with self.assertRaises(Exception):
            percent.validate_percent(-10)

if __name__ == "__main__":
    unittest.main()
