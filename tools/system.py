from __future__ import annotations

import os
import platform
import socket
import subprocess

import psutil

from security.permissions import require_confirmation


def status() -> dict:
    vm = psutil.virtual_memory()
    disk = psutil.disk_usage(os.path.abspath(os.sep))
    return {
        "os": platform.platform(),
        "cpu_percent": psutil.cpu_percent(interval=None),
        "ram_percent": vm.percent,
        "ram_used_mb": round(vm.used / 1024 / 1024, 1),
        "ram_available_mb": round(vm.available / 1024 / 1024, 1),
        "disk_percent": disk.percent,
        "hostname": socket.gethostname(),
        "network": [{"name": n, "addresses": [a.address for a in addrs]} for n, addrs in psutil.net_if_addrs().items()],
    }


def processes(limit: int = 30) -> list[dict]:
    rows = []
    for p in psutil.process_iter(["pid", "name", "memory_percent", "cpu_percent"]):
        try:
            rows.append(p.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return sorted(rows, key=lambda x: x.get("memory_percent") or 0, reverse=True)[:limit]


def open_app(command: str) -> None:
    if os.name == "nt":
        subprocess.Popen(command, shell=True)
    else:
        subprocess.Popen(command, shell=True)


def power(action: str, confirmed: bool = False) -> None:
    require_confirmation(confirmed, action)
    if os.name == "nt":
        subprocess.run(["shutdown", "/r" if action == "restart" else "/s", "/t", "0"], check=True)
    else:
        subprocess.run(["systemctl", action], check=True)
