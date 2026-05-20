"""findata.news.search — full-text news search."""
from typing import Optional

from skills._shared import call_json


def call(q: str,
         category: Optional[str] = None,
         since: Optional[str] = None,
         limit: int = 50) -> list:
    if not q:
        raise ValueError("q is required")
    params = {"q": q, "limit": max(1, min(int(limit), 200))}
    if category: params["category"] = category
    if since:    params["since"]    = since
    return call_json("GET", "/news/search", params=params)
