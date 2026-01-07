from aiogram import Dispatcher, types
from services.stats import STATS, uptime
from services.subscribers import add_user, remove_user
from services.top import get_top
from services.price_history import get_avg_price
from parsers.playerok import scan_playerok
from parsers.fanpay import scan_fanpay

def register_handlers(dp: Dispatcher):

    @dp.message_handler(commands=["start"])
    async def start(msg: types.Message):
        add_user(msg.from_user.id)
        await msg.answer("🤖 Бот запущен\n🔔 Уведомления включены")

    @dp.message_handler(commands=["on"])
    async def on(msg):
        add_user(msg.from_user.id)
        await msg.answer("🔔 Уведомления включены")

    @dp.message_handler(commands=["off"])
    async def off(msg):
        remove_user(msg.from_user.id)
        await msg.answer("🔕 Уведомления выключены")

    @dp.message_handler(commands=["stats"])
    async def stats(msg):
        await msg.answer(
            f"📊 Статистика\n"
            f"🔍 Найдено: {STATS['found']}\n"
            f"📨 Отправлено: {STATS['sent']}\n"
            f"⏱ Аптайм: {uptime()} сек"
        )

    @dp.message_handler(commands=["find"])
    async def find(msg):
        await msg.answer("🔍 Ищу сделки...")
        items = (await scan_playerok()) + (await scan_fanpay())
        best = sorted(items, key=lambda x: x["price"])[:3]
        if not best:
            await msg.answer("❌ Ничего не найдено")
            return
        text = "🔥 Лучшие сделки:\n\n"
        for p in best:
            text += f"• {p['name']} — {p['price']} ₽\n"
        await msg.answer(text)

    @dp.message_handler(commands=["top"])
    async def top(msg):
        deals = get_top()
        if not deals:
            await msg.answer("❌ Пока нет сделок")
            return
        text = "🏆 ТОП сделок:\n\n"
        for p in deals:
            text += f"• {p['name']} — {p['price']} ₽\n"
        await msg.answer(text)

    @dp.message_handler(commands=["price"])
    async def price(msg):
        q = msg.get_args()
        if not q:
            await msg.answer("❌ Пример: /price cs2")
            return
        avg = get_avg_price(q)
        if not avg:
            await msg.answer("❌ Нет данных")
            return
        await msg.answer(f"📊 Средняя цена `{q}`: {avg} ₽")
