"""findata.symbol.get — single-symbol profile lookup."""
from skills._shared import call_json, FindataBadRequest


def call(symbol: str) -> dict | None:
    if not symbol:
        raise ValueError("symbol is required")
    try:
        return call_json("GET", f"/symbols/{symbol.upper()}")
    except FindataBadRequest as e:
        # 404 → returns None as documented; let other errors propagate.
        if e.status == 404:
            return None
        raise
