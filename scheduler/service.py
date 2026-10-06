from __future__ import annotations

import threading
import time
from datetime import datetime, timedelta
from typing import Callable


class SchedulerService:
    def __init__(self, db, callback: Callable[[str], None]):
        self.db = db
        self.callback = callback
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._loop, name="jarvis-scheduler", daemon=True)

    def start(self) -> None:
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()

    def add(self, text: str, run_at: datetime, repeat: str | None = None) -> int:
        return self.db.add_task(text, run_at.isoformat(timespec="seconds"), repeat)

    def _loop(self) -> None:
        while not self._stop.wait(5):
            for task in self.db.due_tasks():
                try:
                    self.callback(task["text"])
                    if task["repeat"] == "daily":
                        next_run = datetime.fromisoformat(task["run_at"]) + timedelta(days=1)
                        self.db.reschedule_task(task["id"], next_run.isoformat(timespec="seconds"))
                    elif task["repeat"] == "weekly":
                        next_run = datetime.fromisoformat(task["run_at"]) + timedelta(days=7)
                        self.db.reschedule_task(task["id"], next_run.isoformat(timespec="seconds"))
                    else:
                        self.db.complete_task(task["id"])
                except Exception:
                    self.db.complete_task(task["id"])
