def verify(answer):
    normalized = answer.strip()
    if normalized == '1':
        return True, None
    if "\n" in answer.strip():
        return False, "extra prose or multiple lines"
    return False, f"expected 1, got {normalized!r}"
