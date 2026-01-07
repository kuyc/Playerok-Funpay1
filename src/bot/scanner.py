import asyncio
from config import ADMIN_IDS, SCAN_INTERVAL, WHITELIST_KEYWORDS
from parsers.playerok import scan_playerok
from parsers.fanpay import scan_fanpay
from services.scoring import score_product
from services.dedup import is_new
from services.price_compare import get_market_price, is_undervalued
from services.ai_check import ai_risk_check
from services.price_history import add_price, get_avg_price
from services.stats import inc_found, inc_sent

def start_scanner(bot):
    asyncio.get_event_loop().create_task(scanner_loop(bot))

def allowed(name: str) -> bool:
    name = name.lower()
    return any(k in name for k in WHITELIST_KEYWORDS)

async def scanner_loop(bot):
    while True:
        items = await asyncio.gather(scan_playerok(), scan_fanpay())
        items = items[0] + items[1]

        market_price = get_market_price(items)

        for p in items:
            if not allowed(p["name"]):
                continue
            if not is_new(p["url"]):
                continue

            add_price(p["name"], p["price"])
            avg_price = get_avg_price(p["name"])

            if avg_price and p["price"] > avg_price * 0.9:
                continue

            score = score_product(p)
            if score < 7:
                continue

            if not is_undervalued(p["price"], market_price):
                continue

            inc_found()
            ai_note = ai_risk_check(p, market_price)

            text = (
                f"🔥 <b>АРБИТРАЖ</b>\n\n"
                f"📦 {p['name']}\n"
                f"💰 {p['price']} ₽ | рынок ~{market_price} ₽\n"
                f"⭐ {p.get('seller_rating', 0)} | 👁 {p.get('views', 0)}\n\n"
                f"🤖 SCORE: {score}/10\n"
                f"{ai_note}\n\n"
                f"<a href='{p['url']}'>Открыть</a>"
            )

            for admin in ADMIN_IDS:
                await bot.send_message(admin, text)
                inc_sent()

        await asyncio.sleep(SCAN_INTERVAL)
