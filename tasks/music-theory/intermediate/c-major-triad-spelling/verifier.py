"""Strict exact-output verifier."""
from __future__ import annotations

EXPECTED = 'C,E,G'


def normalize(answer: str) -> str:
    return " ".join(answer.strip().split()).casefold()


def verify(answer: str) -> tuple[bool, str | None]:
    normalized = normalize(answer)
    if normalized == EXPECTED.casefold():
        return True, None
    if not normalized:
        return False, "empty answer; expected exactly C,E,G"
    if len(normalized.split()) > len(EXPECTED.split()):
        return False, "extra prose or multiple tokens; expected exactly C,E,G"
    return False, "Checks chord spelling and output delimiter compliance. Expected exactly C,E,G."
