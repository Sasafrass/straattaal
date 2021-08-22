"""Testing module for global scope tests."""
import unittest

from app import create_app, db
from app.models import User
from config import TestConfig


def reverse_string(test_str):
    """Return a reversed string.

    Args:
        test_str: The string to be reversed.
    """
    return "".join(reversed(test_str))


class BuildTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_mini(self):
        """Mock test for CI purposes asserting equality of a reversed string."""
        test_str = "testing"
        reversed_true = "gnitset"
        reversed_str = reverse_string(test_str)

        self.assertEqual(reversed_true, reversed_str)

    def test_password_hashing(self):
        u = User(username="test")
        u.set_password("cat")
        self.assertFalse(u.check_password("dog"))
        self.assertTrue(u.check_password("cat"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
