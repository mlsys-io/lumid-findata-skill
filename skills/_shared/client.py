"""Thin httpx wrapper used by every findata verb.

Single point of truth for:
  - Where the API lives                  (`FINDATA_BASE_URL`, default `https://kv.run:5000`)
  - How long we wait                     (`FINDATA_TIMEOUT_S`, default 15s)
  - How many times we retry transients   (`FINDATA_RETRIES`, default 2)
  - How we send the caller's identity    (`Authorization: Bearer $XPIO_LUMID_PAT`)
  - How non-2xx responses become Python  (`errors.raise_for_status`)

Verbs build their request via `call_json(method, path, params=…, json_body=…)`
and never touch httpx directly. That keeps the surface tiny when we swap
the underlying transport (e.g. to a connection pool, or to MCP) later.

Sync-only on purpose: xpio verbs run inside the LumidOS runner which is
synchronous; we don't want to drag asyncio into every call site. The
backend is fast enough that a 15s sync timeout covers every realistic
read path.
"""
from __future__ import annotations

import logging
import os
import random
import time
from typing import Any, Optional

import httpx

from .errors import (
    FindataError,
    FindataRateLimit,
    FindataServerError,
    raise_for_status,
)

log = logging.getLogger("lumid-findata-skill")

_DEFAULT_BASE = "https://kv.run:5000"
_DEFAULT_TIMEOUT_S = 15.0
_DEFAULT_RETRIES = 2


def _env_or(default: str, name: str) -> str:
    v = os.environ.get(name)
    return v if v else default


def _env_float(name: str, default: float) -> float:
    try:
        return float(os.environ.get(name) or default)
    except (TypeError, ValueError):
        return default


def _env_int(name: str, default: int) -> int:
    try:
        return int(os.environ.get(name) or default)
    except (TypeError, ValueError):
        return default


def _auth_header() -> dict:
    pat = os.environ.get("XPIO_LUMID_PAT", "").strip()
    return {"Authorization": f"Bearer {pat}"} if pat else {}


class FindataClient:
    """Per-process HTTP client. Reused across verbs in one xpio run."""

    def __init__(self, base_url: Optional[str] = None, timeout_s: Optional[float] = None):
        self.base_url = (base_url or _env_or(_DEFAULT_BASE, "FINDATA_BASE_URL")).rstrip("/")
        self.timeout_s = timeout_s if timeout_s is not None else _env_float(
            "FINDATA_TIMEOUT_S", _DEFAULT_TIMEOUT_S)
        self._client = httpx.Client(
            base_url=self.base_url,
            timeout=httpx.Timeout(self.timeout_s, connect=5.0),
            headers={"Accept": "application/json"},
            http2=False,
        )

    def close(self) -> None:
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()

    def get(self, path: str, params: Optional[dict] = None) -> Any:
        return self._request("GET", path, params=params)

    def post(self, path: str, json_body: Optional[dict] = None,
             params: Optional[dict] = None) -> Any:
        return self._request("POST", path, params=params, json_body=json_body)

    def _request(self, method: str, path: str, *,
                 params: Optional[dict] = None,
                 json_body: Optional[dict] = None) -> Any:
        retries = _env_int("FINDATA_RETRIES", _DEFAULT_RETRIES)
        last_exc: Optional[Exception] = None
        for attempt in range(retries + 1):
            try:
                r = self._client.request(
                    method, path,
                    params=params, json=json_body,
                    headers=_auth_header(),
                )
            except (httpx.TimeoutException, httpx.HTTPError) as e:
                last_exc = FindataError(
                    f"network error: {e}", status=0, detail=str(e))
                if attempt < retries:
                    time.sleep(0.2 * (2 ** attempt) + random.random() * 0.1)
                    continue
                raise last_exc

            body = r.text[:500]
            try:
                raise_for_status(r.status_code, body, str(r.url))
            except FindataRateLimit as e:
                # 429 with Retry-After header — re-raise with parsed value.
                ra = r.headers.get("retry-after") or r.headers.get("Retry-After")
                try:
                    e.retry_after = int(ra) if ra else 60
                except (TypeError, ValueError):
                    e.retry_after = 60
                if attempt < retries:
                    time.sleep(min(e.retry_after, 5))
                    continue
                raise
            except FindataServerError as e:
                if attempt < retries:
                    time.sleep(0.2 * (2 ** attempt) + random.random() * 0.1)
                    continue
                raise

            try:
                return r.json()
            except ValueError:
                # Some endpoints return text/html (e.g. /status); fall
                # through and return the raw body for the caller to handle.
                return body
        # unreachable; satisfies type checker
        assert last_exc is not None
        raise last_exc


# Module-level convenience — most verbs only need one call per invocation,
# so they don't need to own a client instance.

_singleton: Optional[FindataClient] = None


def _client() -> FindataClient:
    global _singleton
    if _singleton is None:
        _singleton = FindataClient()
    return _singleton


def call_json(method: str, path: str, *,
              params: Optional[dict] = None,
              json_body: Optional[dict] = None) -> Any:
    """One-shot JSON call. Re-uses a process-wide client."""
    c = _client()
    if method.upper() == "GET":
        return c.get(path, params=params)
    if method.upper() == "POST":
        return c.post(path, json_body=json_body, params=params)
    raise ValueError(f"unsupported method: {method}")
