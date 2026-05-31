"""Strict exact-output verifier."""
from __future__ import annotations

EXPECTED = 'Bb'


def normalize(answer: str) -> str:
    return " ".join(answer.strip().split()).casefold()


def verify(answer: str) -> tuple[bool, str | None]:
    normalized = normalize(answer)
    if normalized == EXPECTED.casefold():
        return True, None
    if not normalized:
        return False, "empty answer; expected exactly Bb"
    if len(normalized.split()) > len(EXPECTED.split()):
        return False, "extra prose or multiple tokens; expected exactly Bb"
    return False, "Checks flat-key signature recall and exact spelling. Expected exactly Bb."
