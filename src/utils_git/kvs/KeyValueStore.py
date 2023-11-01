import os
import tempfile
from functools import cache, cached_property

from utils_base import JSONFile, Log, hashx

from utils_git.core.Git import Git

LEN_HASH = 16
LEN_BRANCH_ID = 8

log = Log('KeyValueStore')


class KeyValueStore:
    @staticmethod
    def get_hash(key: str) -> str:
        return hashx.md5(key)[:LEN_HASH]

    @staticmethod
    def get_branch_name(key: str) -> str:
        branch_id = KeyValueStore.get_hash(key)[:LEN_BRANCH_ID]
        return 'kvs-' + branch_id

    def get_json_file_name(key: str) -> str:
        return KeyValueStore.get_hash(key) + ".json"

    @cached_property
    def temp_dir_repo(self) -> str:
        return tempfile.TemporaryDirectory().name

    @cache
    def get_data_file_path(self, key: str) -> str:
        return os.path.join(
            self.temp_dir_repo, KeyValueStore.get_json_file_name(key)
        )

    def get_data_file(self, key: str) -> JSONFile:
        return JSONFile(self.get_data_file_path(key))

    def __init__(self, user_name: str, repo_name: str):
        self.user_name = user_name
        self.repo_name = repo_name
        self.git = Git.from_github(user_name, repo_name)

        self.git.clone(self.temp_dir_repo)

    def branch_and_checkout(self, key: str):
        branch_name = KeyValueStore.get_branch_name(key)
        log.debug(f'{branch_name=}')
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
