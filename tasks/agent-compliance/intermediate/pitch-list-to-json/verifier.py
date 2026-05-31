import json

EXPECTED = {'pitches': ['C4', 'E4', 'G4']}

def verify(answer):
    raw = answer.strip()
    if raw.startswith("```") or raw.endswith("```"):
        return False, "markdown fence is not allowed"
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return False, "invalid JSON"
    if data != EXPECTED:
        return False, f"expected {{\"pitches\":[\"C4\",\"E4\",\"G4\"]}}, got {data!r}"
    if json.dumps(data, separators=(",", ":"), sort_keys=True) != raw:
        return False, "JSON must be minified with exact keys and values"
    return True, None
