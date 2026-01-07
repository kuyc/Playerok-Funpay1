_seen = set()
def is_new(k):
    if k in _seen: return False
    _seen.add(k); return True
