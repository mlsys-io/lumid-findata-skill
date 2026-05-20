# Changelog

## 0.1.0 — initial release

Wraps the read surface of the Lumid finance data backend as 10 xpio verbs.
First-party imports: `httpx`, `pyyaml`, `pytest` (test-only).

Verbs:
- `findata.symbols.search`, `findata.symbol.get`, `findata.universe`,
  `findata.screener`
- `findata.ohlc.get`
- `findata.news.latest`, `findata.news.search`, `findata.news.by_symbol`,
  `findata.news.stats`
- `findata.quote.snapshot`

Shared infra: `skills/_shared/client.py` (one `httpx.Client` with retry +
Lumid PAT injection + tolerant error taxonomy).
