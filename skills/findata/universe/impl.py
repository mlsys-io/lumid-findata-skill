"""findata.universe — list the canonical US-equity universe."""
from skills._shared import call_json


def call() -> list:
    return call_json("GET", "/universe")
