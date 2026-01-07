_seen = set()
def is_new(pid):
    if pid in _seen: return False
    _seen.add(pid); return True
