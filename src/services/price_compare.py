from statistics import median
def get_market_price(items):
    p = [i["price"] for i in items]
    return int(median(p)) if p else 0
def is_undervalued(price, market):
    return market and price < market * 0.7
