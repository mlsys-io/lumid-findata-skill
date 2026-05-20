"""findata.quote.snapshot — realtime cache snapshot."""
from skills._shared import call_json


def call(symbols: list) -> list:
    if not symbols:
        raise ValueError("symbols is required")
    if not all(isinstance(s, str) and s for s in symbols):
        raise ValueError("symbols must be a list of non-empty strings")
    if len(symbols) > 100:
        raise ValueError("max 100 symbols per call")
    csv = ",".join(s.upper() for s in symbols)
    return call_json("GET", "/quotes", params={"symbols": csv})
