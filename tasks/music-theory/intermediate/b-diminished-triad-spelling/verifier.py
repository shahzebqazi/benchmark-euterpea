def verify(answer):
    normalized = answer.strip()
    if normalized == 'B,D,F':
        return True, None
    if "\n" in answer.strip():
        return False, "extra prose or multiple lines"
    return False, f"expected B,D,F, got {normalized!r}"
