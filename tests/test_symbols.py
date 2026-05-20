"""Round-trip tests for the symbols verb group."""
from skills.findata.symbol.get.impl import call as symbol_get
from skills.findata.symbols.search.impl import call as symbols_search
from skills.findata.universe.impl import call as universe
from skills.findata.screener.impl import call as screener


def test_symbol_get_aapl():
    row = symbol_get(symbol="AAPL")
    assert row is not None
    assert row["symbol"] == "AAPL"
    assert row["name"].lower().startswith("apple")
    assert "industry" in row


def test_symbol_get_btcusd():
    """Crypto symbol — falls back to the searchable catalog."""
    row = symbol_get(symbol="BTCUSD")
    assert row is not None
    assert row["symbol"] == "BTCUSD"
    assert row["industry"] == "cryptocurrency"


def test_symbols_search_qqq():
    hits = symbols_search(q="QQQ", limit=5)
    assert isinstance(hits, list)
    assert len(hits) >= 1
    assert any(h["symbol"] == "QQQ" for h in hits)


def test_universe_returns_thousands():
    rows = universe()
    assert isinstance(rows, list)
    assert len(rows) > 1000
    assert all("symbol" in r for r in rows[:10])


def test_screener_tech_megacaps():
    out = screener(sector="Technology", market_cap_min=1e12, limit=5)
    assert out["count"] >= 1
    assert out["returned"] >= 1
    for h in out["hits"]:
        assert h["sector"] == "Technology"
        assert (h.get("market_cap") or 0) >= 1e12
