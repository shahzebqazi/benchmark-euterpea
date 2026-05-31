"""Strict exact-output verifier."""
from __future__ import annotations

EXPECTED = '4'


def normalize(answer: str) -> str:
    return " ".join(answer.strip().split()).casefold()


def verify(answer: str) -> tuple[bool, str | None]:
    normalized = normalize(answer)
    if normalized == EXPECTED.casefold():
        return True, None
    if not normalized:
        return False, "empty answer; expected exactly 4"
    if len(normalized.split()) > len(EXPECTED.split()):
        return False, "extra prose or multiple tokens; expected exactly 4"
    return False, "Two quarter notes plus one half note equals four quarter-note units. Expected exactly 4."
