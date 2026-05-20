"""findata.universe — list the canonical US-equity universe."""
from .._shared import call_json


def call() -> list:
    return call_json("GET", "/universe")
