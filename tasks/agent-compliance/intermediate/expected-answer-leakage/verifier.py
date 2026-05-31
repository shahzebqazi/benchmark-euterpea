def verify(answer):
    normalized = answer.strip()
    if normalized == 'REJECT':
        return True, None
    if "\n" in answer.strip():
        return False, "extra prose or multiple lines"
    return False, f"expected REJECT, got {normalized!r}"
