def verify(answer):
    normalized = answer.strip()
    if normalized == 'F#':
        return True, None
    if "\n" in answer.strip():
        return False, "extra prose or multiple lines"
    return False, f"expected F#, got {normalized!r}"
