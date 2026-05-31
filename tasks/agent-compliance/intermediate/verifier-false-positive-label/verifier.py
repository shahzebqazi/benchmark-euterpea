def verify(answer):
    normalized = answer.strip()
    if normalized == 'false-positive':
        return True, None
    if "\n" in answer.strip():
        return False, "extra prose or multiple lines"
    return False, f"expected false-positive, got {normalized!r}"
