"""Round-trip test for findata.quote.snapshot."""
from skills.findata.quote.snapshot.impl import call as quote_snapshot


def test_quote_snapshot_mixed_assets():
    rows = quote_snapshot(symbols=["AAPL", "BTCUSD", "EURUSD"])
    assert len(rows) == 3
    by_sym = {r["symbol"]: r for r in rows}
    for sym in ("AAPL", "BTCUSD", "EURUSD"):
        assert sym in by_sym
        # ts may be None when the asset hasn't been seen in the cache
        # window; the shape still must include the field.
        assert "ts" in by_sym[sym]
        assert "source" in by_sym[sym]


def test_quote_snapshot_caps_at_100():
    import pytest
    with pytest.raises(ValueError):
        quote_snapshot(symbols=[f"SYM{i}" for i in range(101)])
