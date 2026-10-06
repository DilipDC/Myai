@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
  python -m venv .venv
)

call ".venv\Scripts\activate.bat"
python -m pip install -r requirements.txt

curl -fsS http://127.0.0.1:11434/api/version >nul 2>&1
if errorlevel 1 (
  echo [WARN] Ollama is not running. Start Ollama before sending AI requests.
) else (
  echo [OK] Ollama is reachable.
)

start "" cmd /c "timeout /t 2 >nul & start http://127.0.0.1:8000"
python app.py
