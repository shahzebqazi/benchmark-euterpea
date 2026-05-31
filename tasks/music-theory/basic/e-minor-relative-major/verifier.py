def verify(answer):
    normalized = answer.strip()
    if normalized == 'G major':
        return True, None
    if "\n" in answer.strip():
        return False, "extra prose or multiple lines"
    return False, f"expected G major, got {normalized!r}"
