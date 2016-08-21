import hello
import unittest

class TestHello(unittest.TestCase):
    def test_sayHello_without_title(self):
        result = hello.sayHello("Senko")
        self.assertEqual(result, "Hello Mr. Senko")

    def test_sayHello_with_title(self):
        result = hello.sayHello("Senko", title="The Misterious")
        self.assertEqual(result, "Hello The Misterious Senko")


if __name__ == "__main__":
    unittest.main()
