import hello2
import unittest

class TestHello(unittest.TestCase):
    def test_sayHello_name(self):
        result = hello2.sayHello("Alex")
        self.assertEqual(result, "Hello, Alex")

    def test_sayHello_name_with_greeting(self):
        result = hello2.sayHello("Alex", "Happy testing")
        self.assertEqual(result, "Happy testing, Alex")

if __name__ == "__main__":
    unittest.main()
