import hello
import unittest

class TestHello(unittest.TestCase):
    def test_sayHello_to_one_person(self):
        result = hello.sayHello("Alex")
        self.assertEqual(result, "Hello, Alex")

class TestHelloProperly(TestHello):
    def test_sayHello_to_nobody(self):
        with self.assertRaises(Exception):
            hello.sayHello("")

    def test_sayHello_to_many_people(self):
        with self.assertRaises(Exception):
            hello.sayHello("Alex,Krasi")

if __name__ == "__main__":
    unittest.main()
