def verify(answer):
    normalized = answer.strip()
    if normalized == 'G4,E4,C4':
        return True, None
    if "\n" in answer.strip():
        return False, "extra prose or multiple lines"
    return False, f"expected G4,E4,C4, got {normalized!r}"
