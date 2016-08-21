import hello
import unittest

class TestHello(unittest.TestCase):
    def test_sayHello_without_friends(self):
        result = hello.sayHello("Alex", [])
        self.assertEqual(result, "Hello, Alex")

    def test_sayHello_with_friends(self):
        with self.assertRaises(Exception):
            hello.sayHello("Alex", ["Krasi"])


if __name__ == "__main__":
    unittest.main()
