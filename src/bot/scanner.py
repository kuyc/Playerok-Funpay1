import asyncio
import logging

from parsers.playerok import scan_playerok
from services.scoring import score_product
from config import ADMIN_IDS, SCAN_INTERVAL

logger = logging.getLogger("scanner")


def start_scanner(bot):
    asyncio.get_event_loop().create_task(scanner_loop(bot))


async def scanner_loop(bot):
    while True:
        try:
            products = await scan_playerok()

            for p in products:
                score = score_product(p)

                if score >= 7:
                    text = format_alert(p, score)
                    for admin in ADMIN_IDS:
                        await bot.send_message(admin, text)

        except Exception as e:
            logger.exception(e)

        await asyncio.sleep(SCAN_INTERVAL)


def format_alert(p, score):
    return (
        "🔥 <b>ВОЗМОЖНАЯ СДЕЛКА</b>\n\n"
        f"📦 {p['name']}\n"
        f"💰 {p['price']} ₽\n"
        f"⭐ {p['seller_rating']} | 👁 {p['views']}\n\n"
        f"🤖 SCORE: <b>{score}/10</b>\n"
        f"<a href='{p['url']}'>Открыть</a>"
    )
