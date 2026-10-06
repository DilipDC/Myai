from __future__ import annotations

from config import settings
from models.ollama_client import OllamaClient, OllamaError


class ModelManager:
    def __init__(self):
        self.client = OllamaClient(settings.ollama_base_url)
        self.active_model: str | None = None

    def choose_model(self, prompt: str) -> str:
        lower = prompt.lower()
        coding_markers = (
            "write code", "create code", "python", "javascript", "typescript",
            "fastapi", "flask", "debug", "bug", "error", "program", "script",
            "function", "class", "api", "sql",
        )
        return settings.coding_model if any(m in lower for m in coding_markers) else settings.general_model

    def installed_models(self) -> list[str]:
        return self.client.installed_models()

    def generate(self, prompt: str) -> tuple[str, str]:
        model = self.choose_model(prompt)
        self.active_model = model

        if not self.client.health():
            raise OllamaError(
                "Ollama is not running. Start Ollama, then retry the request."
            )

        installed = self.installed_models()
        if model not in installed:
            raise OllamaError(
                f"Configured model '{model}' is not installed in Ollama. "
                f"Install it with: ollama pull {model}"
            )

        system = (
            "You are JARVIS, a truthful local-first assistant. "
            "Do not claim that an action happened unless a tool actually performed it. "
            "Keep answers concise and practical."
        )
        answer = self.client.chat(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            num_ctx=settings.max_context_tokens,
            num_predict=settings.max_output_tokens,
            keep_alive=settings.ollama_keep_alive,
        )
        return answer, model
