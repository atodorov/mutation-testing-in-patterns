import flaky
import unittest
from unittest import mock

class TestFlaky(unittest.TestCase):
    def test_sayHello(self):
        flaky.sayHello()
        try:
            f = open('./test.txt')
            lines = f.readlines()
            self.assertEqual(len(lines), 2)
        finally:
            f.close()

class TestFlakyWithMock(unittest.TestCase):
    @mock.patch('flaky.log_to_file')
    def test_sayHello(self, _log_to_file):
        calls = [mock.call('Hello World\n'), mock.call('Hello World\n')]
        flaky.sayHello()
        # called twice with lower case string
        self.assertEqual(_log_to_file.call_count, 2)
        _log_to_file.assert_has_calls(calls)


if __name__ == "__main__":
    unittest.main()
