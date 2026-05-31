def verify(answer):
    normalized = answer.strip()
    if normalized == 'ready':
        return True, None
    if normalized.casefold() == 'ready':
        return False, "case mismatch"
    return False, f"expected ready, got {normalized!r}"
