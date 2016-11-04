import modes
import selinux_str
import unittest

class Test_mode_from_str(unittest.TestCase):
    def test_with_disabled(self):
        m = selinux_str.mode_from_str("disabled")
        self.assertEqual(m, modes.SELINUX_DISABLED)

    def test_with_enforcing(self):
        m = selinux_str.mode_from_str("enforcing")
        self.assertEqual(m, modes.SELINUX_ENFORCING)

    def test_with_permissive(self):
        m = selinux_str.mode_from_str("permissive")
        self.assertEqual(m, modes.SELINUX_PERMISSIVE)


class TestCompletely(Test_mode_from_str):
    def test_with_values_outside_set(self):
        for mode in ['aaaaa', 'zzzzz']:
            m = selinux_str.mode_from_str(mode)
            self.assertEqual(m, None)

if __name__ == "__main__":
    unittest.main()
