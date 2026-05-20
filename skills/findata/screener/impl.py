"""findata.screener — server-side universe filtering."""
from typing import Optional

from skills._shared import call_json


def call(
    sector: Optional[str] = None,
    industry: Optional[str] = None,
    country: Optional[str] = None,
    exchange: Optional[str] = None,
    is_etf: Optional[bool] = None,
    is_fund: Optional[bool] = None,
    market_cap_min: Optional[float] = None,
    market_cap_max: Optional[float] = None,
    symbol_prefix: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
) -> dict:
    params = {}
    for k, v in [
        ("sector", sector), ("industry", industry),
        ("country", country), ("exchange", exchange),
        ("is_etf", is_etf), ("is_fund", is_fund),
        ("market_cap_min", market_cap_min),
        ("market_cap_max", market_cap_max),
        ("symbol_prefix", symbol_prefix),
        ("limit", max(1, min(int(limit), 1000))),
        ("offset", max(0, int(offset))),
    ]:
        if v is not None:
            params[k] = v
    return call_json("GET", "/screener", params=params)
