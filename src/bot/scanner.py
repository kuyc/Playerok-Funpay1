import asyncio
from config import SCAN_INTERVAL, WHITELIST_KEYWORDS
from parsers.playerok import scan_playerok
from parsers.fanpay import scan_fanpay
from services.scoring import score_product
from services.dedup import is_new
from services.price_compare import get_market_price, is_undervalued
from services.price_history import add_price, get_avg_price
from services.stats import inc_found, inc_sent
from services.subscribers import get_all
from services.top import add_deal

def start_scanner(bot):
    asyncio.get_event_loop().create_task(loop(bot))

def allowed(name):
    name = name.lower()
    return any(k in name for k in WHITELIST_KEYWORDS)

async def loop(bot):
    while True:
        items = (await scan_playerok()) + (await scan_fanpay())
        market = get_market_price(items)

        for p in items:
            if not allowed(p["name"]): continue
            if not is_new(p["url"]): continue

            add_price(p["name"], p["price"])
            avg = get_avg_price(p["name"])
            if avg and p["price"] > avg * 0.9: continue

            score = score_product(p)
            if score < 7: continue
            if not is_undervalued(p["price"], market): continue

            inc_found()
            add_deal(p)

            text = (
                f"🔥 <b>АРБИТРАЖ</b>\n\n"
                f"{p['name']}\n"
                f"💰 {p['price']} ₽ | рынок ~{market} ₽\n"
                f"🤖 SCORE: {score}/10\n"
                f"<a href='{p['url']}'>Открыть</a>"
            )

            for uid in get_all():
                await bot.send_message(uid, text)
                inc_sent()

        await asyncio.sleep(SCAN_INTERVAL)
