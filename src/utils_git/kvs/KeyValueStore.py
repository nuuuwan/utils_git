import os
import tempfile
from functools import cache

from utils_base import JSONFile, Log

from utils_git.core.Git import Git
from utils_git.kvs.Key import Key

log = Log('KeyValueStore')


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
        self.git.clone(self.temp_dir_repo)

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
