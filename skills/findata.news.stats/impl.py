"""findata.news.stats — per-category counts + freshness."""
from .._shared import call_json


def call() -> dict:
    return call_json("GET", "/news/stats")
