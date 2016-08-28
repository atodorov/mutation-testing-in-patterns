import example1 as example
import unittest

class TestReversePassword(unittest.TestCase):
    def test_non_empty_password(self):
        revpass = example.reverse_password('secret')
        self.assertEqual(revpass, 'terces')

    def test_empty_password(self):
        revpass = example.reverse_password('')
        self.assertEqual(revpass, '')

    def test_no_password_provided(self):
        revpass = example.reverse_password()
        self.assertEqual(revpass, '')

if __name__ == "__main__":
    unittest.main()
