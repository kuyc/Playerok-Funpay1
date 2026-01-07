from aiogram import Dispatcher, types
from config import ADMIN_IDS


def register_handlers(dp: Dispatcher):

    @dp.message_handler(commands=["start"])
    async def start(msg: types.Message):
        await msg.answer(
            "🤖 <b>Playerok Scanner</b>\n\n"
            "Я ищу выгодные сделки на Playerok.\n"
            "Уведомляю автоматически."
        )

    @dp.message_handler(commands=["ping"])
    async def ping(msg: types.Message):
        await msg.answer("✅ Бот жив")

    @dp.message_handler(commands=["test"])
    async def test(msg: types.Message):
        if msg.from_user.id not in ADMIN_IDS:
            return
        await msg.answer("🔧 Админ-доступ подтверждён")
