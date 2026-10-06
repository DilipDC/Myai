from __future__ import annotations

import re
from urllib.parse import quote_plus

import requests


class SearchError(RuntimeError):
    pass


def search(query: str, limit: int = 5) -> list[dict]:
    url = "https://html.duckduckgo.com/html/?q=" + quote_plus(query)
    try:
        r = requests.get(url, headers={"User-Agent": "JARVIS/1.0"}, timeout=8)
        r.raise_for_status()
    except requests.RequestException as exc:
        raise SearchError(f"Online search unavailable: {exc}") from exc

    items = []
    for block in re.findall(r'<a rel="nofollow" class="result__a" href="(.*?)".*?>(.*?)</a>', r.text, re.S):
        href, title = block
        clean = re.sub("<.*?>", "", title)
        items.append({"title": clean.strip(), "url": href})
        if len(items) >= limit:
            break
    if not items:
        raise SearchError("Search returned no usable results.")
    return items
