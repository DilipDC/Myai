import pytest

from security.permissions import Risk, classify


def test_safe():
    assert classify("read file").risk == Risk.SAFE


def test_destructive_requires_confirmation():
    assert classify("delete file", destructive=True).risk == Risk.CONFIRM


def test_blocked():
    assert classify("rm -rf /").risk == Risk.BLOCKED


def test_secret_memory_blocked(tmp_path):
    from memory.store import MemoryStore
    from database.database import Database
    db = Database(tmp_path / "secret.db")
    db.initialize()
    with pytest.raises(ValueError):
        MemoryStore(db).remember("my api key is abc")
