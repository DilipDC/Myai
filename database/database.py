from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any


class Database:
    def __init__(self, path: Path):
        self.path = Path(path)

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        return conn

    def initialize(self) -> None:
        schema = Path(__file__).with_name("schema.sql").read_text(encoding="utf-8")
        with self._connect() as conn:
            conn.executescript(schema)

    def add_chat(self, user_message: str, ai_response: str, model: str) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO chats(user_message, ai_response, model) VALUES(?, ?, ?)",
                (user_message, ai_response, model),
            )

    def get_recent_chats(self, limit: int = 30) -> list[dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT user_message, ai_response, model, created_at
                FROM chats
                ORDER BY id DESC
                LIMIT ?
                """,
                (max(1, min(limit, 100)),),
            ).fetchall()
        return [dict(row) for row in rows]
