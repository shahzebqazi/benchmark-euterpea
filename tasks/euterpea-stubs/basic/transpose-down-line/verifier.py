def verify(answer):
    normalized = answer.strip()
    if normalized == 'A3,C#4,E4':
        return True, None
    if "\n" in answer.strip():
        return False, "extra prose or multiple lines"
    return False, f"expected A3,C#4,E4, got {normalized!r}"
