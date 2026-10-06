from __future__ import annotations

import re
from datetime import datetime, timedelta

import psutil

from config import settings
from core.model_manager import ModelManager
from database.database import Database
from memory.store import MemoryStore
from scheduler.service import SchedulerService
from websearch.search import SearchError, search


class JarvisAgent:
    def __init__(self, db: Database):
        self.db = db
        self.models = ModelManager()
        self.memory = MemoryStore(db)
        self.notifications: list[str] = []
        self.scheduler = SchedulerService(db, self._notify)
        self.db.initialize()
        self.scheduler.start()

    def _notify(self, text: str) -> None:
        self.notifications.append(text)
        self.notifications[:] = self.notifications[-50:]

    def _schedule(self, message: str) -> dict | None:
        lower = message.lower()
        if not any(x in lower for x in ("remind me", "reminder", "alarm", "schedule")):
            return None

        now = datetime.now()
        run_at = None
        if "tomorrow" in lower:
            hour = 8
            m = re.search(r"(?:at\s+)?(\d{1,2})(?::(\d{2}))?\s*(am|pm)?", lower)
            if m:
                hour = int(m.group(1))
                minute = int(m.group(2) or 0)
                if m.group(3) == "pm" and hour < 12: hour += 12
                if m.group(3) == "am" and hour == 12: hour = 0
            else:
                minute = 0
            run_at = (now + timedelta(days=1)).replace(hour=hour, minute=minute, second=0, microsecond=0)
        elif "in " in lower:
            m = re.search(r"in\s+(\d+)\s+(minute|minutes|hour|hours|day|days)", lower)
            if m:
                n = int(m.group(1))
                unit = m.group(2)
                run_at = now + (timedelta(minutes=n) if "minute" in unit else timedelta(hours=n) if "hour" in unit else timedelta(days=n))

        if run_at is None:
            return None

        text = re.sub(r"remind me(?: to)?|reminder|alarm|schedule", "", message, flags=re.I).strip(" .")
        repeat = "daily" if "every day" in lower or "daily" in lower else "weekly" if "every week" in lower or "weekly" in lower else None
        task_id = self.scheduler.add(text or "Scheduled task", run_at, repeat)
        return {"reply": f"Scheduled task #{task_id} for {run_at.strftime('%Y-%m-%d %H:%M')}.", "model": "scheduler", "ok": True}

    def handle(self, message: str, confirmed: bool = False) -> dict:
        text = message.strip()
        lower = text.lower()

        try:
            scheduled = self._schedule(text)
            if scheduled:
                return scheduled

            if lower.startswith(("remember ", "remember that ")):
                value = re.sub(r"^remember(?: that)?\s+", "", text, flags=re.I)
                item = self.memory.remember(value)
                return {"reply": f"Memory saved as #{item['id']}.", "model": "memory", "ok": True}

            if lower.startswith(("recall ", "what do you remember about ")):
                query = re.sub(r"^(recall|what do you remember about)\s*", "", text, flags=re.I)
                rows = self.memory.recall(query)
                return {"reply": "\n".join(f"#{x['id']}: {x['text']}" for x in rows) or "No matching memory found.", "model": "memory", "ok": True}

            if lower.startswith("forget "):
                memory_id = int(re.search(r"\d+", text).group())
                return {"reply": "Memory forgotten." if self.memory.forget(memory_id) else "Memory ID not found.", "model": "memory", "ok": True}

            if lower.startswith(("search web ", "web search ")):
                query = re.sub(r"^(search web|web search)\s+", "", text, flags=re.I)
                results = search(query)
                return {"reply": "\n".join(f"{i+1}. {x['title']} — {x['url']}" for i,x in enumerate(results)), "sources": results, "model": "web-search", "ok": True}

            reply, model = self.models.generate(text)
            self.db.add_chat(text, reply, model)
            return {"reply": reply, "model": model, "ok": True}
        except SearchError as exc:
            return {"reply": f"WEB SEARCH ERROR: {exc}", "model": "web-search", "ok": False}
        except Exception as exc:
            return {
                "reply": f"JARVIS ERROR\nComponent: {type(exc).__name__}\nReason: {exc}",
                "model": self.models.active_model,
                "ok": False,
            }

    def status(self) -> dict:
        memory = psutil.virtual_memory()
        return {
            "ollama": {"ok": self.models.client.health()},
            "model": {"active": self.models.active_model, "general": settings.general_model, "coding": settings.coding_model},
            "system": {
                "cpu_percent": psutil.cpu_percent(interval=None),
                "ram_percent": round(memory.percent, 1),
                "ram_used_mb": round(memory.used / 1024 / 1024, 1),
                "ram_available_mb": round(memory.available / 1024 / 1024, 1),
                "process_ram_mb": round(psutil.Process().memory_info().rss / 1024 / 1024, 1),
            },
            "memory_count": len(self.memory.recall("", 100)),
            "tasks": self.db.list_tasks(),
            "notifications": self.notifications[-10:],
        }
