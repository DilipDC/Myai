from __future__ import annotations

import shutil
from pathlib import Path

from security.permissions import require_confirmation


def _safe(path: str, root: Path | None = None) -> Path:
    p = Path(path).expanduser().resolve()
    if root is not None and root.resolve() not in p.parents and p != root.resolve():
        raise PermissionError("Path is outside the configured workspace.")
    return p


def read_file(path: str) -> str:
    return _safe(path).read_text(encoding="utf-8")


def write_file(path: str, content: str, confirmed: bool = False) -> str:
    p = _safe(path)
    require_confirmation(confirmed, f"write file {p}")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return str(p)


def copy_file(src: str, dst: str, confirmed: bool = False) -> str:
    require_confirmation(confirmed, f"copy {src} to {dst}")
    target = _safe(dst)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(_safe(src), target)
    return str(target)


def move_file(src: str, dst: str, confirmed: bool = False) -> str:
    require_confirmation(confirmed, f"move {src} to {dst}")
    target = _safe(dst)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(_safe(src)), str(target))
    return str(target)
