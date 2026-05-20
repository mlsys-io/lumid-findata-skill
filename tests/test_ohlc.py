"""Round-trip tests for OHLC."""
from skills.findata.ohlc.get.impl import call as ohlc_get


def test_ohlc_aapl_daily_default_window():
    out = ohlc_get(symbol="AAPL", interval="1d")
    assert out["symbol"] == "AAPL"
    assert out["interval"] == "1d"
    assert out["count"] >= 100  # ~250 trading days/year by default
    bar = out["bars"][0]
    for k in ("ts", "open", "high", "low", "close", "volume"):
        assert k in bar


def test_ohlc_qqq_daily_rollup():
    """ETF daily isn't natively stored — it's rolled up from 1-min."""
    out = ohlc_get(symbol="QQQ", interval="1d")
    assert out["count"] >= 1


def test_ohlc_btcusd_daily_rollup():
    out = ohlc_get(symbol="BTCUSD", interval="1d")
    assert out["count"] >= 1
