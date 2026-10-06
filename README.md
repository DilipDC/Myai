# JARVIS — BUILT BY DILIP

Local-first personal AI agent optimized for low-resource Windows and Linux systems.

## Phase 1

Current Phase 1 provides:

- Flask local web UI at `127.0.0.1:8000`
- Ollama integration
- Configurable Qwen3 0.6B general model
- SQLite chat persistence
- Lightweight CPU/RAM status
- Truthful startup/status reporting
- Cross-platform startup scripts

The master build specification is in the supplied project prompt.

## Requirements

- Python 3.10+
- Ollama installed locally
- Qwen3 0.6B available in Ollama
- Windows 10/11 or Linux

## Install

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

Then open:

```
http://127.0.0.1:8000
```

## Ollama

Verify Ollama is running:

```text
http://127.0.0.1:11434
```

Install the configured model yourself before running JARVIS. JARVIS will not silently download multi-gigabyte models.

## Configuration

Copy `.env.example` to `.env`.

Important settings include:

- `GENERAL_MODEL`
- `CODING_MODEL`
- `OLLAMA_BASE_URL`
- `MAX_CONTEXT_TOKENS`
- `MAX_OUTPUT_TOKENS`
- `RAM_TARGET_MB`

## Architecture

Phase 1 keeps the system intentionally small:

```text
Browser
  ↓
Flask API
  ↓
JarvisAgent
  ↓
ModelManager
  ↓
Ollama
  ↓
Qwen3 0.6B

SQLite stores chat history.
psutil reports local system usage.
```

Later phases add memory, permissions, scheduler, system tools, web search, voice, coding agent, and model switching.

## Security

JARVIS binds to `127.0.0.1` by default. No public network exposure is enabled by default.
