"""Strict exact-output verifier."""
from __future__ import annotations

EXPECTED = 'COMPLY-739'


def normalize(answer: str) -> str:
    return " ".join(answer.strip().split()).casefold()


def verify(answer: str) -> tuple[bool, str | None]:
    normalized = normalize(answer)
    if normalized == EXPECTED.casefold():
        return True, None
    if not normalized:
        return False, "empty answer; expected exactly COMPLY-739"
    if len(normalized.split()) > len(EXPECTED.split()):
        return False, "extra prose or multiple tokens; expected exactly COMPLY-739"
    return False, "Output-only constraints are graded as exact behavior. Expected exactly COMPLY-739."
