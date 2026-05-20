"""findata.symbol.get — single-symbol profile lookup."""
from .._shared import call_json


def call(symbol: str) -> dict | None:
    if not symbol:
        raise ValueError("symbol is required")
    try:
        return call_json("GET", f"/symbols/{symbol.upper()}")
    except Exception:
        # 404 → returns None as documented; let other errors propagate.
        from .._shared import FindataBadRequest
        raise
