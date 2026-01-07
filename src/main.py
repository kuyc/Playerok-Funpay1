import logging
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import BOT_TOKEN
from bot.handlers import register_handlers
from bot.scanner import start_scanner
from web import start_web

logging.basicConfig(level=logging.INFO)

def main():
    bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
    dp = Dispatcher(bot, storage=MemoryStorage())

    register_handlers(dp)
    start_scanner(bot)
    start_web()

    executor.start_polling(dp, skip_updates=True)

if __name__ == "__main__":
    main()
