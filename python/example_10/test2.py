import boolops2 as boolops
import unittest

class TestBoolOps(unittest.TestCase):
    def test_xnor_raise_a_empty_b_empty(self):
        with self.assertRaises(Exception):
            boolops.xnor_raise([], [])

    def test_xnor_raise_a_not_empty_b_not_empty(self):
        with self.assertRaises(Exception):
            boolops.xnor_raise([1], [2])

    def test_xnor_raise_a_empty_b_not_empty(self):
        # doesn'r raise exception
        boolops.xnor_raise([], [2])

    def test_xnor_raise_a_not_empty_b_empty(self):
        # doesn't raise exception
        boolops.xnor_raise([1], [])


if __name__ == "__main__":
    unittest.main()
