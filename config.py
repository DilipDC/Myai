from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


def _int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except ValueError:
        return default


@dataclass(frozen=True)
class Settings:
    general_model: str = os.getenv("GENERAL_MODEL", "qwen3:0.6b")
    coding_model: str = os.getenv("CODING_MODEL", "qwen2.5-coder:1.5b")
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434").rstrip("/")
    host: str = os.getenv("HOST", "127.0.0.1")
    port: int = _int("PORT", 8000)
    max_context_tokens: int = _int("MAX_CONTEXT_TOKENS", 2048)
    max_output_tokens: int = _int("MAX_OUTPUT_TOKENS", 512)
    ram_target_mb: int = _int("RAM_TARGET_MB", 1024)
    ollama_keep_alive: str = os.getenv("OLLAMA_KEEP_ALIVE", "0")
    database_path: Path = BASE_DIR / os.getenv("DATABASE_PATH", "data/jarvis.db")


settings = Settings()
settings.database_path.parent.mkdir(parents=True, exist_ok=True)
