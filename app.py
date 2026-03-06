
from flask import Flask, request, jsonify, send_from_directory
import sqlite3, os
from ai import ask_ai

app = Flask(__name__)
DB = "chat.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS chats(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_message TEXT,
        ai_response TEXT
    )''')
    conn.commit()
    conn.close()

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    msg = data.get("message","")

    reply = ask_ai(msg)

    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO chats(user_message, ai_response) VALUES(?,?)",(msg,reply))
    conn.commit()
    conn.close()

    return jsonify({"reply":reply})

@app.route("/history")
def history():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT user_message, ai_response FROM chats ORDER BY id DESC LIMIT 30")
    rows = c.fetchall()
    conn.close()
    return jsonify(rows)

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0", port=port)
