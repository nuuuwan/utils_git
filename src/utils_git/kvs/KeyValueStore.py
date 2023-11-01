import os
import tempfile
from functools import cache

from utils_base import JSONFile, Log

from utils_git.core.Git import Git
from utils_git.kvs.Key import Key

log = Log('KeyValueStore')
BRANCH_EMPTY = 'empty'


class KeyValueStore:
    @cache
    def get_data_file_path(self, key: str) -> str:
        return os.path.join(self.temp_dir_repo, Key(key).data_file_name)

    def get_data_file(self, key: str) -> JSONFile:
        return JSONFile(self.get_data_file_path(key))

    def __init__(self, user_name: str, repo_name: str):
        self.user_name = user_name
        self.repo_name = repo_name
        self.git = Git.from_github(user_name, repo_name)
        self.temp_dir_repo = tempfile.TemporaryDirectory().name
        self.git.clone(self.temp_dir_repo, BRANCH_EMPTY)

    def enter_branch(self, key: str):
        branch_name = Key(key).branch_name
        self.git.checkout(BRANCH_EMPTY)
        self.git.branch(branch_name)
        self.git.checkout(branch_name)
        self.git.pull()

    def exit_branch(self):
        self.git.checkout(BRANCH_EMPTY)

    def __setitem__(self, key: str, value):
        self.enter_branch(key)
        self.get_data_file(key).write(value)
        log.debug(f'Wrote "{key}" to file.')
        self.git.add()
        self.git.commit(f'Updated key "{key}"')
        self.git.push()
        self.exit_branch()
        return value

    def __getitem__(self, key: str):
        self.enter_branch(key)
        try:
            value = self.get_data_file(key).read()
        except FileNotFoundError:
            raise KeyError(key)
        self.exit_branch()
        return value
