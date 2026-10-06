from __future__ import annotations

import subprocess

from system_platform.base import PlatformBase


class WindowsPlatform(PlatformBase):
    def open_application(self, command: str) -> None:
        subprocess.Popen(command, shell=True)
