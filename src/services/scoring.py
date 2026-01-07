def score_product(p):
    s = 0
    if p["price"] <= 100: s += 3
    if p.get("seller_rating", 0) >= 4.5: s += 3
    if p.get("views", 0) >= 200: s += 2
    return min(s, 10)
