def verify(answer):
    normalized = answer.strip()
    if normalized == '1,2':
        return True, None
    if "\n" in answer.strip():
        return False, "extra prose or multiple lines"
    return False, f"expected 1,2, got {normalized!r}"
