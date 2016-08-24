import modes
import selinux
import unittest

class Test_mode_from_int(unittest.TestCase):
    def test_with_disabled(self):
        m = selinux.mode_from_int(modes.SELINUX_DISABLED)
        self.assertEqual(m, "disabled")

    def test_with_enforcing(self):
        m = selinux.mode_from_int(modes.SELINUX_ENFORCING)
        self.assertEqual(m, "enforcing")

    def test_with_permissive(self):
        m = selinux.mode_from_int(modes.SELINUX_PERMISSIVE)
        self.assertEqual(m, "permissive")


class TestCompletely(Test_mode_from_int):
    def test_with_values_outside_set(self):
        for mode in [-1, 9999]:
            m = selinux.mode_from_int(mode)
            self.assertEqual(m, "")

if __name__ == "__main__":
    unittest.main()
