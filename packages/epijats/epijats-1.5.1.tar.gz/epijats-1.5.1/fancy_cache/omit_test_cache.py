import pytest

import filecmp
from pathlib import Path

from epijats.util import SourceCache, SourceId, SourceIdType


TESTS_DIR = Path(__file__).parent


def test_cache_file(tmp_path):
    cache = SourceCache(tmp_path / "cache")
    expect = TESTS_DIR / "cases" / "hello" / "hello.txt"
    sid = cache.put(expect)
    assert not sid.is_dir()
    assert sid == SourceId.cnt("e965047ad7c57865823c7d992b1d046ea66edf78")
    got = tmp_path / "got"
    cache.get(sid, got)
    assert filecmp.cmp(got, expect, shallow=False)


def test_cache_dir(tmp_path):
    cache = SourceCache(tmp_path / "cache")
    expect = TESTS_DIR / "cases" / "hello"
    sid = cache.put(expect)
    assert sid.is_dir()
    assert sid == SourceId.dir("8c3c7fbcd903744b20fd7567a1fcefa99133b5bc")
    got = tmp_path / "got"
    cache.get(sid, got)
    assert filecmp.cmp(got / "hello.txt", expect / "hello.txt", shallow=False)


def test_cache_id():
    hasha = "e965047ad7c57865823c7d992b1d046ea66edf78"
    swhid = "swh:1:cnt:" + hasha
    sid = SourceId(swhid)
    assert str(sid) == swhid
    assert sid == SourceId.cnt(hasha)
    assert sid != SourceId.dir(hasha)
