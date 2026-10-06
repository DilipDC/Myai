from __future__ import annotations

import platform


class PlatformBase:
    @property
    def name(self) -> str:
        return platform.system()
