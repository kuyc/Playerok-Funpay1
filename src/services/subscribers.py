SUBSCRIBERS=set()
def add_user(uid): SUBSCRIBERS.add(uid)
def remove_user(uid): SUBSCRIBERS.discard(uid)
def get_all(): return list(SUBSCRIBERS)
