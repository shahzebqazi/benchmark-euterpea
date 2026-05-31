def verify(answer):
    normalized = answer.strip()
    if normalized == 'Ab,C,Eb,G':
        return True, None
    if "\n" in answer.strip():
        return False, "extra prose or multiple lines"
    return False, f"expected Ab,C,Eb,G, got {normalized!r}"
