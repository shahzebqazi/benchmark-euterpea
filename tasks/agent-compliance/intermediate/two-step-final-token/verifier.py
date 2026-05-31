def verify(answer):
    normalized = answer.strip()
    if normalized == 'bbb':
        return True, None
    if "\n" in answer.strip():
        return False, "extra prose or multiple lines"
    return False, f"expected bbb, got {normalized!r}"
