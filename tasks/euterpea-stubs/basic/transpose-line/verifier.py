"""Strict exact-output verifier."""
from __future__ import annotations

EXPECTED = 'D4,F#4,A4'


def normalize(answer: str) -> str:
    return " ".join(answer.strip().split()).casefold()


def verify(answer: str) -> tuple[bool, str | None]:
    normalized = normalize(answer)
    if normalized == EXPECTED.casefold():
        return True, None
    if not normalized:
        return False, "empty answer; expected exactly D4,F#4,A4"
    if len(normalized.split()) > len(EXPECTED.split()):
        return False, "extra prose or multiple tokens; expected exactly D4,F#4,A4"
    return False, "Symbolic transposition should preserve spelling and octaves. Expected exactly D4,F#4,A4."
