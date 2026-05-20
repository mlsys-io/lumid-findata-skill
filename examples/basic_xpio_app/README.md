# basic_xpio_app

The smallest possible xpio app that consumes `lumid-findata-skill`. Run
it as the canonical "does the skill actually work end-to-end" check.

## What it does

One hourly loop: pulls stock-market + earnings news + last-known ticks
for a five-symbol watchlist, then writes a one-line summary memory back
to the agent bank. Total: ~10 lines of YAML, zero Python.

## Install + run

```bash
# 1. Install the skill onto your xpio runtime (LumidOS).
xp install lumid/lumid-findata-skill@0.1.0

# 2. Install this example app.
xp install lumid/lumid-findata-skill@0.1.0/examples/basic_xpio_app

# 3. Trigger one cycle manually (no waiting for the cron tick).
xp app run lumid-findata-example --loop watchlist_news_pull --once
```

You'll see one memory item land in
`~/.xp/kg/agents/lumid-findata-observer/bank.jsonl` with a
`market_snapshot` tag. Done.
