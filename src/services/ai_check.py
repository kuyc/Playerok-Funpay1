def ai_risk_check(p, market):
    return "⚠️ Слишком дёшево — проверь продавца" if p["price"] < market*0.5 else "✅ Цена адекватная"
