"""findata.news.latest — global news firehose with category filter."""
from typing import Optional

from .._shared import call_json


def call(category: Optional[str] = None,
         since: Optional[str] = None,
         limit: int = 50) -> list:
    params = {"limit": max(1, min(int(limit), 200))}
    if category: params["category"] = category
    if since:    params["since"]    = since
    return call_json("GET", "/news/latest", params=params)
