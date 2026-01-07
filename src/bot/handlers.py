from aiogram import Dispatcher, types
from services.stats import STATS, uptime

def register_handlers(dp: Dispatcher):

    @dp.message_handler(commands=["start"])
    async def start(msg: types.Message):
        await msg.answer("🤖 Арбитражный бот запущен")

    @dp.message_handler(commands=["ping"])
    async def ping(msg: types.Message):
        await msg.answer("✅ Бот жив")

    @dp.message_handler(commands=["stats"])
    async def stats(msg: types.Message):
        await msg.answer(
            f"📊 Статистика\n"
            f"🔍 Найдено: {STATS['found']}\n"
            f"📨 Отправлено: {STATS['sent']}\n"
            f"⏱ Аптайм: {uptime()} сек"
        )
