import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

ADMIN_IDS = [
    int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip().isdigit()
]

SCAN_INTERVAL = 40

WHITELIST_KEYWORDS = [
    "cs", "cs2", "prime",
    "steam", "account", "аккаунт",
    "key", "ключ",
    "subscription", "подписка",
    "spotify", "netflix", "nitro",
]
