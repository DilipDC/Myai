from __future__ import annotations

import sys


class PlatformBase:
    @property
    def name(self) -> str:
        return sys.platform
