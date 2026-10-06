from __future__ import annotations

import os
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

from config import settings
from core.agent import JarvisAgent
from database.database import Database

BASE_DIR = Path(__file__).resolve().parent

app = Flask(__name__, static_folder=".", static_url_path="")
db = Database(settings.database_path)
agent = JarvisAgent(db=db)


@app.get("/")
def index():
    return send_from_directory(BASE_DIR, "index.html")


@app.post("/chat")
def chat():
    payload = request.get_json(silent=True) or {}
    message = str(payload.get("message", "")).strip()

    if not message:
        return jsonify({"error": "message is required"}), 400

    result = agent.handle(message)
    return jsonify(result)


@app.get("/status")
def status():
    return jsonify(agent.status())


@app.get("/history")
def history():
    return jsonify(db.get_recent_chats(limit=30))


def initialize() -> None:
    db.initialize()


if __name__ == "__main__":
    initialize()
    print("=" * 36)
    print("        JARVIS")
    print("    BUILT BY DILIP")
    print("=" * 36)
    print(f"[OK] Database: {settings.database_path}")
    print(f"[OK] Ollama: {settings.ollama_base_url}")
    print(f"[OK] General model: {settings.general_model}")
    print(f"[OK] Web: http://{settings.host}:{settings.port}")
    print("JARVIS ONLINE")
    app.run(host=settings.host, port=settings.port, debug=False)
