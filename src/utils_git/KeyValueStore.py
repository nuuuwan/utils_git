import os
import tempfile

from utils_base import JSONFile, Log, hashx

from utils_git.Git import Git

LEN_HASH = 16
LEN_BRANCH_ID = 8

log = Log('KeyValueStore')


class KeyValueStore:
    def __init__(self, user_name, repo_name):
        self.git = Git.from_github(user_name, repo_name)

    @staticmethod
    def get_hash(key):
        return hashx.md5(key)[:LEN_HASH]

    @staticmethod
    def get_branch_name(key):
        branch_id = KeyValueStore.get_hash(key)[:LEN_BRANCH_ID]
        return 'kvs-' + branch_id

    def get_json_file_name(key):
        return KeyValueStore.get_hash(key) + ".json"

    def __setitem__(self, key, value):
        branch_name = KeyValueStore.get_branch_name(key)
        file_name = KeyValueStore.get_json_file_name(key)

        dummy_dir_path = os.path.join(tempfile.gettempdir(), branch_name)
        dummy_file_path = os.path.join(dummy_dir_path, file_name)
        if not os.path.exists(dummy_dir_path):
            os.makedirs(dummy_dir_path)
            log.info(f'Created {dummy_dir_path}')
        JSONFile(dummy_file_path).write(value)
        log.debug(f'Wrote {dummy_file_path}')

        return value

    def __getitem__(self, key):
        branch_name = KeyValueStore.get_branch_name(key)
        file_name = KeyValueStore.get_json_file_name(key)

        dummy_dir_path = os.path.join(tempfile.gettempdir(), branch_name)
        dummy_file_path = os.path.join(dummy_dir_path, file_name)

        if not os.path.exists(dummy_file_path):
            raise KeyError(key)

        return JSONFile(dummy_file_path).read()
