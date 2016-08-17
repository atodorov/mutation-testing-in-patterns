import sandwich.control
import unittest

class TestControl(unittest.TestCase):
    def test_loading_via_importlib(self):
        ham_in_fridge = sandwich.control.ham_class()
        self.assertEqual(ham_in_fridge.pieces, 10)


if __name__ == "__main__":
    unittest.main()
