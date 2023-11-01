import unittest

from utils_base import TIME_FORMAT_TIME_ID, Time

from tests.test_git import REPO_NAME, USER_NAME
from utils_git import KeyValueStore


class TestCase(unittest.TestCase):
    def test_lifecycle(self):
        kvs = KeyValueStore(USER_NAME, REPO_NAME)
        self.assertIsNotNone(kvs)

        time_id = TIME_FORMAT_TIME_ID.stringify(Time.now())
        key = f'key-{time_id}'
        value = f'value-{time_id}'
        kvs[key] = value
        self.assertEqual(kvs[key], value)

        for i in range(0, 3):
            key = f'key-{time_id}-{i}'
            value = f'value-{time_id}-{i}'
            kvs[key] = value
            self.assertEqual(kvs[key], value)
