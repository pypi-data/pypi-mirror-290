import git

import enum, binascii, os, shutil, sys, subprocess
from pathlib import Path


class SourceIdType(enum.Enum):
    """String prefix for source ID scheme"""

    SWH_CNT = "swh:1:cnt:"
    SWH_DIR = "swh:1:dir:"


class SourceId:
    def __init__(self, hexhash, src_id_type=None):
        if src_id_type is None:
            i = 1 + hexhash.rfind(":")
            src_id_type = SourceIdType(hexhash[:i])
            hexhash = hexhash[i:]
        self.hexhash = hexhash
        self.src_id_type = src_id_type
        assert isinstance(src_id_type, SourceIdType)

    @staticmethod
    def cnt(git_hash):
        return SourceId(git_hash, SourceIdType.SWH_CNT)

    @staticmethod
    def dir(git_hash):
        return SourceId(git_hash, SourceIdType.SWH_DIR)

    def is_dir(self):
        return (self.src_id_type == SourceIdType.SWH_DIR)

    def __eq__(self, other):
        if isinstance(other, SourceId):
            return self.__dict__ == other.__dict__
        return False

    def __repr__(self):
        return self.src_id_type.value + self.hexhash

    def __hash__(self):
        return hash(self.__dict__)


# git hash-object -t tree /dev/null
EMPTY_TREE = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"


class SourceCache:
    _CACHE_PATH = Path.home() / ".cache" / "epijats"

    def __init__(self, cache_dir):
        cache_dir = Path(cache_dir)
        try:
            self.repo = git.Repo(cache_dir)
        except git.exc.NoSuchPathError:
            self.repo = git.Repo.init(cache_dir)

    def put(self, src_path):
        src_path = Path(src_path)
        if not src_path.exists():
            raise FileNotFoundError
        if src_path.is_dir():
            g = git.Git(src_path) # src_path is working dir
            g.set_persistent_git_options(git_dir=self.repo.git_dir)
            temp_index = git.IndexFile.from_tree(self.repo, EMPTY_TREE)
            with g.custom_environment(GIT_INDEX_FILE=temp_index.path):
                g.add(".")
                git_hash = g.write_tree()
                return SourceId(git_hash, SourceIdType.SWH_DIR)
        else:
            git_hash = self.repo.git.hash_object("-w", "--", src_path)
            return SourceId(git_hash, SourceIdType.SWH_CNT)

    def get(self, src_id, dest_path):
        if src_id.is_dir():
            pass
        else:
            blob = git.Blob(self.repo, binascii.a2b_hex(src_id.hexhash))
            with open(dest_path, "wb") as file:
                blob.stream_data(file)
