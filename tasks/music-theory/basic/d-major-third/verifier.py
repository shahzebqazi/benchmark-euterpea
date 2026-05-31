"""Strict exact-output verifier."""
from __future__ import annotations

EXPECTED = 'F#'


def normalize(answer: str) -> str:
    return " ".join(answer.strip().split()).casefold()


def verify(answer: str) -> tuple[bool, str | None]:
    normalized = normalize(answer)
    if normalized == EXPECTED.casefold():
        return True, None
    if not normalized:
        return False, "empty answer; expected exactly F#"
    if len(normalized.split()) > len(EXPECTED.split()):
        return False, "extra prose or multiple tokens; expected exactly F#"
    return False, "Distinguishes major-scale spelling from white-key counting. Expected exactly F#."
