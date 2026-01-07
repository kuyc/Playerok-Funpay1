from collections import defaultdict, deque
_h = defaultdict(lambda: deque(maxlen=30))
def add_price(n,p): _h[n.lower()].append(p)
def get_avg_price(n):
    v=_h.get(n.lower()); return int(sum(v)/len(v)) if v else 0
