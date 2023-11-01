from functools import cached_property
from utils_base import hashx

LEN_HASH = 16
LEN_BRANCH_ID = 8


class Key:
    def __init__(self, key_str: str):
        self.key_str = key_str

    @cached_property
    def hash(self) -> str:
        return hashx.md5(self.key_str)[:LEN_HASH]

    @cached_property
    def branch_name(self) -> str:
        branch_id = self.hash[:LEN_BRANCH_ID]
        return 'kvs-' + branch_id

    @cached_property
    def data_file_name(self) -> str:
        return self.hash + ".json"
