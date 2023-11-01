import unittest

from tests.test_git import REPO_NAME, USER_NAME
from utils_git import KeyValueStore


class TestCase(unittest.TestCase):
    def test_lifecycle(self):
        kvs = KeyValueStore(USER_NAME, REPO_NAME)
        self.assertIsNotNone(kvs)

        kvs['name'] = 'Nuwan'
        self.assertEqual(kvs['name'], 'Nuwan')

        with self.assertRaises(KeyError):
            kvs['name2']
