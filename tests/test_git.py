import os
import tempfile
import unittest

from utils_base import TIME_FORMAT_TIME_ID, File, Time

from utils_git.Git import Git

TEST_REPO_URL = 'https://github.com/nuuuwan/utils_git'
TEST_DIR_REPO = tempfile.TemporaryDirectory().name
TEST_BRACH_NAME = 'main'

TEST_GIT = Git(TEST_REPO_URL)


class TestGit(unittest.TestCase):
    def test_lifecycle(self):
        git = TEST_GIT
        git = Git(TEST_REPO_URL)
        git.clone(TEST_DIR_REPO, TEST_BRACH_NAME)

        git.status()
        git.diff()

        test_file = os.path.join(TEST_DIR_REPO, 'tests', 'test.txt')
        File(test_file).write(TIME_FORMAT_TIME_ID.stringify(Time.now()))

        git.add()
        git.commit('Test Commit')

        git.pull()
        git.push()

        git.checkout(TEST_BRACH_NAME)


if __name__ == '__main__':
    unittest.main()
