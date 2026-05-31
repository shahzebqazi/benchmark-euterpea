"""Strict exact-output verifier."""
from __future__ import annotations

EXPECTED = '2'


def normalize(answer: str) -> str:
    return " ".join(answer.strip().split()).casefold()


def verify(answer: str) -> tuple[bool, str | None]:
    normalized = normalize(answer)
    if normalized == EXPECTED.casefold():
        return True, None
    if not normalized:
        return False, "empty answer; expected exactly 2"
    if len(normalized.split()) > len(EXPECTED.split()):
        return False, "extra prose or multiple tokens; expected exactly 2"
    return False, "Checks key-signature count rather than listing notes. Expected exactly 2."
