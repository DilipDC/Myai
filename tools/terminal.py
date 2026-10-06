from __future__ import annotations

import os
import shlex
import subprocess
from pathlib import Path

from security.permissions import classify, require_confirmation


ALLOWED = {
    "python", "python3", "pip", "pip3", "git", "pytest", "npm", "node",
    "cargo", "go", "java", "javac", "gcc", "g++", "ollama",
}


def run(command: str, cwd: str | None = None, confirmed: bool = False, timeout: int = 30) -> dict:
    permission = classify(command, destructive=False)
    if permission.risk.value == "BLOCKED":
        raise PermissionError(permission.reason)

    parts = shlex.split(command, posix=os.name != "nt")
    if not parts or Path(parts[0]).name.lower() not in ALLOWED:
        raise PermissionError("Terminal command is not on the approved executable allowlist.")

    if any(x in command.lower() for x in ("&&", "||", ";", "|", ">", "<", " rm ", " del ")):
        require_confirmation(confirmed, command)

    proc = subprocess.run(
        command, shell=True, cwd=cwd, capture_output=True, text=True, timeout=timeout
    )
    return {"returncode": proc.returncode, "stdout": proc.stdout[-8000:], "stderr": proc.stderr[-8000:]}
