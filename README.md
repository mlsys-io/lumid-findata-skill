# lumid-findata-skill

Unified data-access skill for Lumid xpio apps. One import; all the reads.

Wraps the public read surface of the Lumid finance data backend as a set of
xpio verbs an app declares in `xpcloud.yaml` via `skill_imports:`. Authed
via the caller's Lumid PAT (`XPIO_LUMID_PAT` env var, injected by the
LumidOS runner). Anonymous calls work for the public read paths too, at a
lower rate-limit tier.

## Verbs (v0.1.0)

| Verb | Returns |
|---|---|
| `findata.symbols.search` | Substring ticker / name search across the universe |
| `findata.symbol.get` | One symbol's profile (sector / industry / market cap / …) |
| `findata.universe` | The 7,851-symbol US-equity universe |
| `findata.screener` | Filter the universe by sector / industry / market cap / instrument type |
| `findata.ohlc.get` | OHLC bars (1min / 5min / 1d) for one symbol |
| `findata.news.latest` | Global news firehose with optional category filter |
| `findata.news.search` | Full-text search across all news |
| `findata.news.by_symbol` | Articles for one symbol, deduped across providers |
| `findata.news.stats` | Per-category row counts + freshness |
| `findata.quote.snapshot` | Last-known tick per symbol (cache snapshot, up to 100) |

Planned for v0.2.0: `findata.kols.*`, `findata.fundamentals.*`,
`findata.holders.*`, `findata.estimates.*`, `findata.iceberg.run`.

## Install

In an xpio app's `xpcloud.yaml`:

```yaml
skill_imports:
  - lumid/lumid-findata-skill@>=0.1.0
```

Or, in a one-off script:

```bash
xp install lumid/lumid-findata-skill@0.1.0
xp run 'findata.symbol.get(symbol="AAPL")'
```

## Auth

The skill reads `XPIO_LUMID_PAT` from the environment. The LumidOS runner
populates this with the caller's PAT before invoking any verb. For local
testing:

```bash
export XPIO_LUMID_PAT="lm_pat_live_..."
python -c "from skills.findata.symbol_get.impl import call; print(call(symbol='AAPL'))"
```

Anonymous calls also work (the backing service permits anonymous reads at
60 req/min); just set `XPIO_LUMID_PAT=""` or leave it unset.

## Configuration

| env | default | what |
|---|---|---|
| `XPIO_LUMID_PAT` | (none) | Lumid PAT injected by the runner |
| `FINDATA_BASE_URL` | `https://kv.run:5000` | API base URL — override for testing |
| `FINDATA_TIMEOUT_S` | `15` | per-request timeout |
| `FINDATA_RETRIES` | `2` | retry count for 5xx / network errors |

## Conventions

- Times are UTC ISO-8601. Dates are `YYYY-MM-DD`.
- Symbols are upper-cased by the backend.
- Verb outputs are JSON-shaped dicts / lists — pass them straight to other
  skills or persist to memory.
- Errors raise `FindataError` (taxonomy in `skills/_shared/errors.py`)
  with the HTTP status preserved at `.status`.

## Layout

```
skills/
├── _shared/
│   ├── __init__.py
│   ├── client.py     # one httpx.Client (sync) + retry + PAT injection
│   └── errors.py     # FindataError, FindataAuthError, FindataRateLimit
├── findata.symbol.get/
│   ├── skill.yaml
│   └── impl.py
├── findata.symbols.search/
│   ├── skill.yaml
│   └── impl.py
├── findata.universe/
├── findata.screener/
├── findata.ohlc.get/
├── findata.news.latest/
├── findata.news.search/
├── findata.news.by_symbol/
├── findata.news.stats/
└── findata.quote.snapshot/

tests/      one round-trip test per verb against kv.run:5000
            (skipped if FINDATA_BASE_URL or PAT not set)
examples/   a runnable xpio app demonstrating the skill
```

## Versioning

`0.1.0` — initial 10 verbs (symbols + ohlc + news + quote). Synchronous-only.
Future versions will add ownership / fundamentals / KOL tweets / Iceberg
job submission. Streaming verbs (WS / SSE wrappers) are deferred to v0.3+.

## License

Internal — Lumid ecosystem.
