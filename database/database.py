from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any


class Database:
    def __init__(self, path: Path):
        self.path = Path(path)

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.path, timeout=10)
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
                "SELECT user_message, ai_response, model, created_at FROM chats ORDER BY id DESC LIMIT ?",
                (max(1, min(limit, 100)),),
            ).fetchall()
        return [dict(row) for row in rows]

    def add_memory(self, text: str, category: str = "general") -> int:
        with self._connect() as conn:
            cur = conn.execute("INSERT INTO memories(text, category) VALUES(?, ?)", (text, category))
            return int(cur.lastrowid)

    def search_memories(self, query: str, limit: int = 20) -> list[dict[str, Any]]:
        with self._connect() as conn:
            if query:
                rows = conn.execute(
                    "SELECT id,text,category,created_at,updated_at FROM memories WHERE text LIKE ? ORDER BY updated_at DESC LIMIT ?",
                    (f"%{query}%", max(1, min(limit, 100))),
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT id,text,category,created_at,updated_at FROM memories ORDER BY updated_at DESC LIMIT ?",
                    (max(1, min(limit, 100)),),
                ).fetchall()
        return [dict(row) for row in rows]

    def update_memory(self, memory_id: int, text: str, category: str) -> bool:
        with self._connect() as conn:
            cur = conn.execute(
                "UPDATE memories SET text=?, category=?, updated_at=CURRENT_TIMESTAMP WHERE id=?",
                (text, category, memory_id),
            )
            return cur.rowcount == 1

    def delete_memory(self, memory_id: int) -> bool:
        with self._connect() as conn:
            cur = conn.execute("DELETE FROM memories WHERE id=?", (memory_id,))
            return cur.rowcount == 1

    def add_task(self, text: str, run_at: str, repeat: str | None = None) -> int:
        with self._connect() as conn:
            cur = conn.execute("INSERT INTO tasks(text,run_at,repeat) VALUES(?,?,?)", (text,run_at,repeat))
            return int(cur.lastrowid)

    def due_tasks(self) -> list[dict[str, Any]]:
        from datetime import datetime
        now = datetime.now().isoformat(timespec="seconds")
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT id,text,run_at,repeat FROM tasks WHERE completed=0 AND run_at<=? ORDER BY run_at",
                (now,),
            ).fetchall()
        return [dict(row) for row in rows]

    def complete_task(self, task_id: int) -> None:
        with self._connect() as conn:
            conn.execute("UPDATE tasks SET completed=1 WHERE id=?", (task_id,))

    def reschedule_task(self, task_id: int, run_at: str) -> None:
        with self._connect() as conn:
            conn.execute("UPDATE tasks SET run_at=? WHERE id=?", (run_at, task_id))

    def list_tasks(self, include_completed: bool = False) -> list[dict[str, Any]]:
        with self._connect() as conn:
            if include_completed:
                rows = conn.execute("SELECT * FROM tasks ORDER BY run_at").fetchall()
            else:
                rows = conn.execute("SELECT * FROM tasks WHERE completed=0 ORDER BY run_at").fetchall()
        return [dict(row) for row in rows]
