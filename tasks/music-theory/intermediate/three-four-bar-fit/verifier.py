def verify(answer):
    normalized = answer.strip()
    if normalized == 'yes':
        return True, None
    if normalized.casefold() == 'yes':
        return False, "case mismatch"
    return False, f"expected yes, got {normalized!r}"
