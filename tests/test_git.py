import os
import tempfile
import unittest

from utils_base import TIME_FORMAT_TIME_ID, File, Time

from utils_git import Git

USER_NAME = 'nuuuwan'
REPO_NAME = 'utils_git'
TEST_BRACH_NAME = 'main'


class TestCase(unittest.TestCase):
    @unittest.skip('While testing others')
    def test_lifecycle(self):
        git = Git.from_github(USER_NAME, REPO_NAME)

        dir_repo = tempfile.TemporaryDirectory().name
        git.clone(dir_repo, TEST_BRACH_NAME)

        git.status()
        git.diff()

        time_id = TIME_FORMAT_TIME_ID.stringify(Time.now())
        test_file = os.path.join(dir_repo, 'tests', 'test.txt')
        File(test_file).write('TestGit wrote ' + time_id)

        git.add()
        git.commit('Test Commit')

        git.pull()
        git.push()

        git.checkout(TEST_BRACH_NAME)
        new_branch_name = 'test_branch-' + time_id
        git.branch(new_branch_name)
        test_file = os.path.join(dir_repo, 'tests', 'branch-test.txt')
        File(test_file).write('TestGit (new branch) wrote ' + time_id)
        git.add()
        git.commit('Test Commit - in new branch')
        git.push()
