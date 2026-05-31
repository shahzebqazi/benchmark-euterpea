def verify(answer):
    normalized = answer.strip()
    if normalized == '3':
        return True, None
    if "\n" in answer.strip():
        return False, "extra prose or multiple lines"
    return False, f"expected 3, got {normalized!r}"
