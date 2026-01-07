def score_product(p: dict) -> int:
    score = 0

    if p["price"] <= 100:
        score += 3
    elif p["price"] <= 200:
        score += 1

    if p["seller_rating"] >= 4.5:
        score += 3
    elif p["seller_rating"] >= 4.0:
        score += 2

    if p["views"] >= 300:
        score += 2
    elif p["views"] >= 100:
        score += 1

    return min(score, 10)
