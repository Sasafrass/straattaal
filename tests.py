"""Testing module for global scope tests."""
import unittest


def reverse_string(test_str):
    """Return a reversed string.
    
    Args:
        test_str: The string to be reversed.
    """
    return "".join(reversed(test_str))

class BuildTestCase(unittest.TestCase):
    def test_mini(self):
        """Mock test for CI purposes asserting equality of a reversed string."""
        test_str = "testing"
        reversed_true = "gnitset"
        reversed_str = reverse_string(test_str)

        self.assertEqual(reversed_true, reversed_str)


if __name__ == "__main__":
    unittest.main(verbosity=2)