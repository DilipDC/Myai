from __future__ import annotations

import re
from typing import Any

from database.database import Database


SECRET = re.compile(r"(api[_ -]?key|token|password|secret|private[_ -]?key|authorization)", re.I)


class MemoryStore:
    def __init__(self, db: Database):
        self.db = db

    def remember(self, text: str, category: str = "general") -> dict[str, Any]:
        if SECRET.search(text):
            raise ValueError("Secrets and credentials are not stored as ordinary memories.")
        memory_id = self.db.add_memory(text.strip(), category)
        return {"id": memory_id, "text": text.strip(), "category": category}

    def recall(self, query: str = "", limit: int = 20) -> list[dict[str, Any]]:
        return self.db.search_memories(query.strip(), limit)

    def forget(self, memory_id: int) -> bool:
        return self.db.delete_memory(memory_id)

    def update(self, memory_id: int, text: str, category: str = "general") -> bool:
        if SECRET.search(text):
            raise ValueError("Secrets and credentials are not stored as ordinary memories.")
        return self.db.update_memory(memory_id, text.strip(), category)
