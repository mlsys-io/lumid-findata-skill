"""findata.news.by_symbol — per-symbol articles."""
from typing import Optional

from skills._shared import call_json


def call(symbol: str,
         since: Optional[str] = None,
         limit: int = 50) -> list:
    if not symbol:
        raise ValueError("symbol is required")
    params = {"limit": max(1, min(int(limit), 200))}
    if since: params["since"] = since
    return call_json("GET", f"/news/{symbol.upper()}", params=params)
