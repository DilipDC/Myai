#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

if [ ! -x ".venv/bin/python" ]; then
  python3 -m venv .venv
fi

source .venv/bin/activate
python -m pip install -r requirements.txt

if curl -fsS http://127.0.0.1:11434/api/version >/dev/null 2>&1; then
  echo "[OK] Ollama is reachable."
else
  echo "[WARN] Ollama is not running. Start Ollama before sending AI requests."
fi

( sleep 2; xdg-open "http://127.0.0.1:8000" >/dev/null 2>&1 || true ) &
python app.py
