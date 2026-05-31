def verify(answer):
    normalized = answer.strip()
    if normalized == 'false-negative':
        return True, None
    if "\n" in answer.strip():
        return False, "extra prose or multiple lines"
    return False, f"expected false-negative, got {normalized!r}"
