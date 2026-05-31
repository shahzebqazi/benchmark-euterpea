def verify(answer):
    normalized = answer.strip()
    if normalized == 'D4':
        return True, None
    if "\n" in answer.strip():
        return False, "extra prose or multiple lines"
    return False, f"expected D4, got {normalized!r}"
