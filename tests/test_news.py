"""Round-trip tests for the news verb group."""
from skills.findata.news.latest.impl import call as news_latest
from skills.findata.news.search.impl import call as news_search
from skills.findata.news.by_symbol.impl import call as news_by_symbol
from skills.findata.news.stats.impl import call as news_stats


def test_news_latest_general():
    rows = news_latest(category="general", limit=5)
    assert isinstance(rows, list)
    assert len(rows) >= 1
    for r in rows:
        assert "published_at" in r
        assert "headline" in r


def test_news_search_fed():
    rows = news_search(q="Fed", limit=5)
    assert isinstance(rows, list)
    # Allow zero hits in case backfill is paused — only assert shape.
    for r in rows:
        assert "headline" in r


def test_news_by_symbol_aapl():
    rows = news_by_symbol(symbol="AAPL", limit=5)
    assert isinstance(rows, list)
    for r in rows:
        assert "headline" in r


def test_news_stats_shape():
    out = news_stats()
    assert "categories" in out
    assert isinstance(out["categories"], list)
    for c in out["categories"]:
        for k in ("rows_last_7d", "rows_last_30d", "latest_in_60d"):
            assert k in c
