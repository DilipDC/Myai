from __future__ import annotations

from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

from coding.agent import CodingAgent
from config import settings
from core.agent import JarvisAgent
from database.database import Database
from tools import files as file_tools
from tools import system

BASE_DIR = Path(__file__).resolve().parent
app = Flask(__name__, static_folder=".", static_url_path="")
db = Database(settings.database_path)
agent = JarvisAgent(db)
coding = CodingAgent(agent.models)


@app.get("/")
def index():
    return send_from_directory(BASE_DIR, "index.html")


@app.post("/chat")
def chat():
    payload = request.get_json(silent=True) or {}
    message = str(payload.get("message", "")).strip()
    if not message:
        return jsonify({"error": "message is required"}), 400
    return jsonify(agent.handle(message, confirmed=bool(payload.get("confirmed", False))))


@app.get("/status")
def status():
    return jsonify(agent.status())


@app.get("/system")
def system_status():
    return jsonify(system.status())


@app.get("/processes")
def process_list():
    return jsonify(system.processes())


@app.get("/history")
def history():
    return jsonify(db.get_recent_chats(limit=50))


@app.get("/memory")
def memories():
    return jsonify(agent.memory.recall(request.args.get("q", ""), 100))


@app.get("/tasks")
def tasks():
    return jsonify(db.list_tasks())


@app.post("/file/read")
def file_read():
    payload = request.get_json(silent=True) or {}
    return jsonify({"content": file_tools.read_file(str(payload["path"]))})


@app.post("/file/write")
def file_write():
    payload = request.get_json(silent=True) or {}
    return jsonify({"path": file_tools.write_file(str(payload["path"]), str(payload.get("content", "")), bool(payload.get("confirmed", False)))})


@app.post("/coding/inspect")
def coding_inspect():
    payload = request.get_json(silent=True) or {}
    return jsonify(coding.inspect(str(payload["path"])))


@app.post("/coding/plan")
def coding_plan():
    payload = request.get_json(silent=True) or {}
    return jsonify({"answer": coding.ask_model(str(payload.get("requirement", "")), str(payload.get("context", "")))})


@app.post("/coding/test")
def coding_test():
    payload = request.get_json(silent=True) or {}
    return jsonify(coding.test(str(payload["path"])))


@app.post("/power")
def power():
    payload = request.get_json(silent=True) or {}
    system.power(str(payload["action"]), bool(payload.get("confirmed", False)))
    return jsonify({"ok": True})


if __name__ == "__main__":
    print("=" * 38)
    print("       JARVIS — BUILT BY DILIP")
    print("=" * 38)
    print(f"Web: http://{settings.host}:{settings.port}")
    app.run(host=settings.host, port=settings.port, debug=False)
