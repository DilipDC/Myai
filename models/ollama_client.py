from __future__ import annotations

from typing import Any

import requests


class OllamaError(RuntimeError):
    pass


class OllamaClient:
    def __init__(self, base_url: str, timeout: float = 60.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

    def health(self) -> bool:
        try:
            response = self.session.get(f"{self.base_url}/api/version", timeout=3)
            return response.ok
        except requests.RequestException:
            return False

    def installed_models(self) -> list[str]:
        response = self.session.get(f"{self.base_url}/api/tags", timeout=5)
        if not response.ok:
            raise OllamaError(f"Ollama /api/tags returned HTTP {response.status_code}")
        data = response.json()
        return [m.get("name", "") for m in data.get("models", []) if m.get("name")]

    def chat(
        self,
        model: str,
        messages: list[dict[str, str]],
        num_ctx: int,
        num_predict: int,
        keep_alive: str,
    ) -> str:
        payload: dict[str, Any] = {
            "model": model,
            "messages": messages,
            "stream": False,
            "keep_alive": keep_alive,
            "options": {
                "num_ctx": num_ctx,
                "num_predict": num_predict,
            },
        }
        try:
            response = self.session.post(
                f"{self.base_url}/api/chat",
                json=payload,
                timeout=self.timeout,
            )
        except requests.RequestException as exc:
            raise OllamaError(f"Cannot reach Ollama: {exc}") from exc

        if not response.ok:
            raise OllamaError(
                f"Ollama /api/chat returned HTTP {response.status_code}: "
                f"{response.text[:300]}"
            )

        data = response.json()
        content = data.get("message", {}).get("content")
        if not isinstance(content, str):
            raise OllamaError("Ollama returned no text response")
        return content.strip()
