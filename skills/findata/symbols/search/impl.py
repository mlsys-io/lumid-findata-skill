"""findata.symbols.search — symbol/name substring search."""
from skills._shared import call_json


def call(q: str, limit: int = 20) -> list:
    if not q:
        raise ValueError("q is required")
    return call_json("GET", "/symbols/search",
                     params={"q": q, "limit": max(1, min(int(limit), 100))})
