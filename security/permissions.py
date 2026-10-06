from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Risk(str, Enum):
    SAFE = "SAFE"
    CONFIRM = "CONFIRM"
    BLOCKED = "BLOCKED"


BLOCKED_PATTERNS = (
    "rm -rf /", "rm -rf ~", "format c:", "del /f /s /q c:\",
    "credential dump", "keylogger", "steal password", "ransomware",
    "disable antivirus", "reverse shell", "meterpreter", "persistence",
)


@dataclass(frozen=True)
class Permission:
    risk: Risk
    reason: str


def classify(action: str, destructive: bool = False) -> Permission:
    text = action.lower()
    if any(pattern in text for pattern in BLOCKED_PATTERNS):
        return Permission(Risk.BLOCKED, "Potentially destructive, credential-theft, malware, or persistence behavior.")
    if destructive:
        return Permission(Risk.CONFIRM, "The requested action can modify or destroy user data or system state.")
    return Permission(Risk.SAFE, "Low-risk local operation.")


def require_confirmation(confirmed: bool, action: str) -> None:
    permission = classify(action, destructive=True)
    if permission.risk == Risk.BLOCKED:
        raise PermissionError(permission.reason)
    if permission.risk == Risk.CONFIRM and not confirmed:
        raise PermissionError(f"CONFIRMATION_REQUIRED: {permission.reason}")
