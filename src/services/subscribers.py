SUBSCRIBERS = set()

def add_user(user_id: int):
    SUBSCRIBERS.add(user_id)

def remove_user(user_id: int):
    SUBSCRIBERS.discard(user_id)

def get_all():
    return list(SUBSCRIBERS)
