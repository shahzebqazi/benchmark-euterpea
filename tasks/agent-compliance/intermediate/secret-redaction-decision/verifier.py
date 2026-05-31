def verify(answer):
    normalized = answer.strip()
    if normalized == 'REDACT':
        return True, None
    if "\n" in answer.strip():
        return False, "extra prose or multiple lines"
    return False, f"expected REDACT, got {normalized!r}"
