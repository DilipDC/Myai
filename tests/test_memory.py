from database.database import Database
from memory.store import MemoryStore


def test_memory_roundtrip(tmp_path):
    db = Database(tmp_path / "test.db")
    db.initialize()
    store = MemoryStore(db)
    item = store.remember("Dilip likes Python", "preference")
    assert item["id"] > 0
    assert store.recall("Python")[0]["text"] == "Dilip likes Python"
    assert store.update(item["id"], "Dilip uses Python", "preference")
    assert store.forget(item["id"])
    assert store.recall("Python") == []
