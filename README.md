# JARVIS — BUILT BY DILIP

Local-first personal AI command center for Windows and Linux using Ollama.

## Features

- Qwen3 0.6B general model
- Qwen2.5-Coder 1.5B coding model
- Persistent SQLite chat history and memory
- Remember / recall / update / forget memory APIs
- Persistent one-time, daily and weekly reminders
- Real online DuckDuckGo search with returned URLs
- Controlled file tools
- Allowlisted terminal execution
- CPU, RAM, disk, network and process telemetry
- Confirmed shutdown/restart
- Coding-agent inspection, planning and test execution
- Lightweight futuristic command-center UI
- Browser microphone/STT when supported
- Browser TTS and optional Python TTS
- CLI fallback
- Windows and Linux startup scripts
- SAFE / CONFIRM / BLOCKED permission model

## Architecture

Browser or CLI -> Flask -> JarvisAgent -> model router / memory / scheduler / tools

Model router -> Ollama -> Qwen3 0.6B or Qwen2.5-Coder 1.5B

SQLite stores chats, memories and scheduled tasks.

## Requirements

Python 3.10+, Ollama, Windows 10/11 or Linux, and a low-resource target of 4 GB RAM.

Install models:

    ollama pull qwen3:0.6b
    ollama pull qwen2.5-coder:1.5b

JARVIS checks that models exist and does not silently download them.

## Windows

Run:

    start_jarvis.bat

Or:

    python -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt
    python app.py

Open http://127.0.0.1:8000

## Linux

    chmod +x start_jarvis.sh
    ./start_jarvis.sh

## CLI

    python cli.py "what is Python?"

## Memory

Examples:

    remember that I use Python
    recall Python
    forget 1

Memory survives restarts. API keys, passwords, tokens and similar secrets are rejected by the ordinary memory interface.

## Scheduler

Examples:

    remind me tomorrow at 8 AM to study
    remind me in 20 minutes to check the build

Tasks are persisted in SQLite and survive restart.

## Web search

Use:

    search web latest Python release

JARVIS performs a real HTTP search. If the network is unavailable, it reports the failure instead of inventing sources.

## System and coding tools

The application exposes CPU/RAM/disk/network telemetry, process inspection, controlled file operations, an approved terminal allowlist, coding inspection/planning/testing, and power actions requiring confirmation.

Permissions are SAFE, CONFIRM, or BLOCKED.

JARVIS does not implement credential theft, malware, hidden persistence, unauthorized surveillance, destructive behavior, or unauthorized access.

## Voice

Browser SpeechRecognition is used when supported. Browser speech synthesis provides TTS. Text remains a fallback. Optional Python voice support uses SpeechRecognition and pyttsx3 and depends on the local audio backend.

## RAM optimization

The default configuration is deliberately small:

    GENERAL_MODEL=qwen3:0.6b
    CODING_MODEL=qwen2.5-coder:1.5b
    OLLAMA_KEEP_ALIVE=0
    MAX_CONTEXT_TOKENS=2048
    MAX_OUTPUT_TOKENS=512

The coding model is selected only for coding-oriented prompts and Ollama keep-alive is disabled by default.

The project does not claim a universal 1 GB model footprint. Actual memory depends on quantization, context size, Ollama, operating system and other processes and must be measured on the target machine.

## Configuration

Copy .env.example to .env.

Important settings include GENERAL_MODEL, CODING_MODEL, OLLAMA_BASE_URL, MAX_CONTEXT_TOKENS, MAX_OUTPUT_TOKENS, RAM_TARGET_MB, OLLAMA_KEEP_ALIVE, DATABASE_PATH, HOST and PORT.

Never commit .env, credentials, virtual environments, model files or caches.

## API

GET /status
GET /system
GET /processes
GET /history
GET /memory?q=...
GET /tasks

POST /chat
POST /file/read
POST /file/write
POST /coding/inspect
POST /coding/plan
POST /coding/test
POST /power

## Testing

Run:

    pytest -q

Core tests cover memory persistence, secret-memory rejection, permission classification and terminal allowlisting.

Full Ollama, browser microphone, OS power and live web-search verification requires those services to be available on the target machine.

## Project structure

    app.py
    cli.py
    config.py
    index.html
    requirements.txt
    start_jarvis.bat
    start_jarvis.sh
    core/
    models/
    database/
    memory/
    scheduler/
    security/
    tools/
    websearch/
    voice/
    coding/
    system_platform/
    tests/

system_platform is used instead of a top-level package named platform because Python already has a standard-library module named platform.

## Troubleshooting

Ollama offline: start Ollama and check http://127.0.0.1:11434/api/version.

Model missing: run ollama list and pull the configured model.

Voice unavailable: use text input; browser and audio backends are platform-dependent.

Web search unavailable: check internet connectivity.

RAM higher than expected: inspect the JARVIS process and Ollama process separately.

## Security

JARVIS binds to localhost by default. Do not expose Flask or Ollama to an untrusted network without authentication and hardening.

## License

No license has been selected yet. Until a license file is added, normal copyright restrictions apply.
