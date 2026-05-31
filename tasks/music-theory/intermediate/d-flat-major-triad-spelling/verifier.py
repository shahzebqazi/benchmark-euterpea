def verify(answer):
    normalized = answer.strip()
    if normalized == 'Db,F,Ab':
        return True, None
    if "\n" in answer.strip():
        return False, "extra prose or multiple lines"
    return False, f"expected Db,F,Ab, got {normalized!r}"
