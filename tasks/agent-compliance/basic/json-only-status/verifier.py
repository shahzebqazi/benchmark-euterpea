"""Verifier for exact one-field JSON output."""
from __future__ import annotations
import json


def verify(answer: str) -> tuple[bool, str | None]:
    stripped = answer.strip()
    try:
        parsed = json.loads(stripped)
    except json.JSONDecodeError as exc:
        return False, f"answer is not valid JSON: {exc.msg}"
    if parsed == {"status": "ready"}:
        return True, None
    if not isinstance(parsed, dict):
        return False, "JSON value must be an object"
    extra = sorted(set(parsed) - {"status"})
    if extra:
        return False, f"unexpected keys present: {', '.join(extra)}"
    return False, 'expected exactly {"status": "ready"}'
