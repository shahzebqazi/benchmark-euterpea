def verify(answer):
    normalized = answer.strip()
    if normalized == 'C,E,G':
        return True, None
    if "\n" in answer.strip():
        return False, "extra prose or multiple lines"
    return False, f"expected C,E,G, got {normalized!r}"
