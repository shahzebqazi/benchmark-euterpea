def verify(answer):
    normalized = answer.strip()
    if normalized == 'READY-204':
        return True, None
    if "\n" in answer.strip():
        return False, "extra prose or multiple lines"
    return False, f"expected READY-204, got {normalized!r}"
