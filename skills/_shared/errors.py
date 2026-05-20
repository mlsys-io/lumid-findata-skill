"""Error taxonomy for the findata skill.

Mirrors the HTTP semantics the backend exposes so callers don't have to
inspect status codes by hand:

  401 → FindataAuthError       (no token, bad token, or upstream auth down)
  429 → FindataRateLimit       (carries Retry-After in .retry_after)
  4xx → FindataBadRequest      (everything else 400-class)
  5xx → FindataServerError     (transient — caller may retry)
  *   → FindataError           (network failures, decode errors)

Every exception preserves the original status code on `.status` and the
response body excerpt on `.detail`.
"""
from __future__ import annotations


class FindataError(Exception):
    """Base — network / transport / decode failures."""

    def __init__(self, message: str, *, status: int = 0, detail: str = ""):
        super().__init__(message)
        self.status = status
        self.detail = detail


class FindataAuthError(FindataError):
    """401 — token missing / invalid / lumid unreachable."""


class FindataRateLimit(FindataError):
    """429 — caller exceeded their rate-limit tier."""

    def __init__(self, message: str, *, status: int = 429,
                 detail: str = "", retry_after: int = 60):
        super().__init__(message, status=status, detail=detail)
        self.retry_after = retry_after


class FindataBadRequest(FindataError):
    """4xx other — malformed input, unknown symbol, etc."""


class FindataServerError(FindataError):
    """5xx — backend transient; caller may retry."""


def raise_for_status(status: int, detail: str, url: str) -> None:
    """Translate an HTTP status into the right exception. detail is the
    response body (already shortened to <= 500 chars by the caller)."""
    if 200 <= status < 300:
        return
    msg = f"{status} {detail[:180]} ({url})"
    if status == 401:
        raise FindataAuthError(msg, status=status, detail=detail)
    if status == 429:
        # Retry-After is parsed by the caller and passed in via kwargs
        # to the rate-limit exception specifically — fall through here.
        raise FindataRateLimit(msg, status=status, detail=detail)
    if 400 <= status < 500:
        raise FindataBadRequest(msg, status=status, detail=detail)
    raise FindataServerError(msg, status=status, detail=detail)
