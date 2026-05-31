"""Strict exact-output verifier."""
from __future__ import annotations

EXPECTED = 'Fx'


def normalize(answer: str) -> str:
    return " ".join(answer.strip().split()).casefold()


def verify(answer: str) -> tuple[bool, str | None]:
    normalized = normalize(answer)
    if normalized == EXPECTED.casefold():
        return True, None
    if not normalized:
        return False, "empty answer; expected exactly Fx"
    if len(normalized.split()) > len(EXPECTED.split()):
        return False, "extra prose or multiple tokens; expected exactly Fx"
    return False, "Requires double-sharp spelling, not the easier enharmonic G. Expected exactly Fx."
