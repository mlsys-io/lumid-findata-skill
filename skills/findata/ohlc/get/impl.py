"""findata.ohlc.get — OHLC bars (1min / 5min / 1d)."""
from typing import Optional

from skills._shared import call_json


def call(symbol: str, interval: str = "1d",
         start: Optional[str] = None, end: Optional[str] = None) -> dict:
    if not symbol:
        raise ValueError("symbol is required")
    if interval not in ("1min", "5min", "1d"):
        raise ValueError("interval must be one of 1min, 5min, 1d")
    params = {"interval": interval}
    if start: params["start"] = start
    if end:   params["end"]   = end
    return call_json("GET", f"/ohlc/{symbol.upper()}", params=params)
