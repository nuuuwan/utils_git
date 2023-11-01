import os
import tempfile
from functools import cache

from utils_base import JSONFile, Log

from utils_git.core.Git import Git
from utils_git.kvs.Key import Key

log = Log('KeyValueStore')
TEMP_DIR_REPO = tempfile.TemporaryDirectory().name


class KeyValueStore:
    @cache
    def get_data_file_path(self, key: str) -> str:
        return os.path.join(TEMP_DIR_REPO, Key(key).data_file_name)

    def get_data_file(self, key: str) -> JSONFile:
        return JSONFile(self.get_data_file_path(key))

    def __init__(self, user_name: str, repo_name: str):
        self.user_name = user_name
        self.repo_name = repo_name
        self.git = Git.from_github(user_name, repo_name)
        self.git.clone(TEMP_DIR_REPO)

    def branch_and_checkout(self, key: str):
        branch_name = Key(key).branch_name
        self.git.checkout('empty')
        self.git.branch(branch_name)
        self.git.checkout(branch_name)
        self.git.pull()

    def __setitem__(self, key: str, value):
        self.branch_and_checkout(key)
        self.get_data_file(key).write(value)
        log.debug(f'Wrote "{key}" to file.')
        self.git.add()
        self.git.commit(f'Updated key "{key}"')
        self.git.push()
        return value

    def __getitem__(self, key: str):
        self.branch_and_checkout(key)
        try:
            return self.get_data_file(key).read()
        except FileNotFoundError:
            raise KeyError(key)
