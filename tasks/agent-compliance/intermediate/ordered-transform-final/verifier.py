def verify(answer):
    normalized = answer.strip()
    if normalized == 'ACE':
        return True, None
    if "\n" in answer.strip():
        return False, "extra prose or multiple lines"
    return False, f"expected ACE, got {normalized!r}"
