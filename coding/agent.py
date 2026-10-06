from __future__ import annotations

from pathlib import Path

from core.model_manager import ModelManager
from tools.terminal import run


class CodingAgent:
    def __init__(self, models: ModelManager):
        self.models = models

    def inspect(self, root: str) -> dict:
        base = Path(root).expanduser().resolve()
        if not base.exists():
            raise FileNotFoundError(root)
        files = [str(p.relative_to(base)) for p in base.rglob("*") if p.is_file() and ".git" not in p.parts and ".venv" not in p.parts]
        return {"root": str(base), "files": files[:300]}

    def ask_model(self, requirement: str, context: str = "") -> str:
        prompt = (
            "You are JARVIS coding agent. Analyze the requirement and give an exact implementation plan "
            "or code. Never claim files were changed unless a tool changed them.\n\n"
            f"Requirement:\n{requirement}\n\nContext:\n{context[:12000]}"
        )
        answer, _ = self.models.generate(prompt)
        return answer

    def test(self, cwd: str) -> dict:
        return run("pytest -q", cwd=cwd, confirmed=False, timeout=60)
