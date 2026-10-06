from __future__ import annotations

import psutil

from config import settings
from core.model_manager import ModelManager
from database.database import Database


class JarvisAgent:
    def __init__(self, db: Database):
        self.db = db
        self.models = ModelManager()
        self.db.initialize()

    def handle(self, message: str) -> dict:
        try:
            reply, model = self.models.generate(message)
            self.db.add_chat(message, reply, model)
            return {"reply": reply, "model": model, "ok": True}
        except Exception as exc:
            return {
                "reply": (
                    "JARVIS ERROR\n"
                    f"Component: {type(exc).__name__}\n"
                    f"Reason: {exc}\n"
                    "Suggested action: verify Ollama and the configured model."
                ),
                "model": self.models.active_model,
                "ok": False,
            }

    def status(self) -> dict:
        memory = psutil.virtual_memory()
        return {
            "ollama": {"ok": self.models.client.health()},
            "model": {
                "active": self.models.active_model,
                "general": settings.general_model,
                "coding": settings.coding_model,
            },
            "system": {
                "cpu_percent": psutil.cpu_percent(interval=None),
                "ram_percent": round(memory.percent, 1),
                "ram_used_mb": round(memory.used / 1024 / 1024, 1),
                "ram_available_mb": round(memory.available / 1024 / 1024, 1),
                "ram_target_mb": settings.ram_target_mb,
                "process_ram_mb": round(
                    psutil.Process().memory_info().rss / 1024 / 1024, 1
                ),
            },
        }
