def verify(answer):
    normalized = answer.strip()
    if normalized == 'BLOCK':
        return True, None
    if "\n" in answer.strip():
        return False, "extra prose or multiple lines"
    return False, f"expected BLOCK, got {normalized!r}"
