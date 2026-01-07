import asyncio
import re
from typing import List, Dict
from playwright.async_api import async_playwright

BASE_URL = "https://playerok.com"


async def scan_playerok(limit: int = 20) -> List[Dict]:
    results = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )

        context = await browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        )

        page = await context.new_page()
        await page.goto(BASE_URL + "/category/cs2", timeout=60000)

        for _ in range(3):
            await page.mouse.wheel(0, 3000)
            await asyncio.sleep(1)

        cards = await page.query_selector_all("a[href*='/product/']")

        for card in cards[:limit]:
            text = await card.inner_text()
            url = await card.get_attribute("href")

            price = extract_price(text)
            if price <= 0:
                continue

            results.append({
                "name": text.split("\n")[0][:100],
                "price": price,
                "seller_rating": extract_rating(text),
                "views": extract_views(text),
                "url": BASE_URL + url
            })

        await browser.close()

    return results


def extract_price(text: str) -> int:
    m = re.search(r"(\d{1,6})\s*₽", text)
    return int(m.group(1)) if m else 0


def extract_rating(text: str) -> float:
    m = re.search(r"(\d\.\d)", text)
    return float(m.group(1)) if m else 0.0


def extract_views(text: str) -> int:
    m = re.search(r"(\d+)\s*просмотр", text.lower())
    return int(m.group(1)) if m else 0
