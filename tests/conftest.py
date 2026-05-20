"""Shared pytest config for the findata skill round-trip tests.

Each test hits the real backend (default `https://kv.run:5000`). To run
locally without burning quota, point at a staging URL:

    FINDATA_BASE_URL=http://localhost:5010 pytest

To use an authed PAT (raises the rate-limit ceiling), set:

    XPIO_LUMID_PAT="lm_pat_live_..." pytest
"""
import os
import sys
from pathlib import Path

import pytest


# Make `skills.*` imports work from the tests/ directory.
REPO = Path(__file__).parent.parent
sys.path.insert(0, str(REPO))


@pytest.fixture(scope="session")
def base_url() -> str:
    return os.environ.get("FINDATA_BASE_URL", "https://kv.run:5000")


@pytest.fixture(scope="session", autouse=True)
def _hint_no_pat():
    """One-time stderr warning if the test session has no PAT set."""
    if not os.environ.get("XPIO_LUMID_PAT"):
        print(
            "\n  [findata-skill tests] XPIO_LUMID_PAT not set — exercising "
            "anonymous tier (60 req/min). Set the env var to test the authed "
            "path against your own identity.\n",
            file=sys.stderr,
        )
