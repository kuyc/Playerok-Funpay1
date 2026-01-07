import asyncio, re
from playwright.async_api import async_playwright

BASE = "https://playerok.com"

async def scan_playerok(limit=15):
    res = []
    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True)
        page = await b.new_page()
        await page.goto(BASE + "/category/cs2")
        for _ in range(2):
            await page.mouse.wheel(0, 2500)
            await asyncio.sleep(1)

        cards = await page.query_selector_all("a[href*='/product/']")
        for c in cards[:limit]:
            t = await c.inner_text()
            url = await c.get_attribute("href")
            price = extract_price(t)
            if price <= 0: continue
            res.append({
                "name": t.split("\n")[0][:100],
                "price": price,
                "url": BASE + url,
                "seller_rating": extract_rating(t),
                "views": extract_views(t),
                "source": "playerok"
            })
        await b.close()
    return res

def extract_price(t):
    m = re.search(r"(\d+)\s*₽", t)
    return int(m.group(1)) if m else 0

def extract_rating(t):
    m = re.search(r"(\d\.\d)", t)
    return float(m.group(1)) if m else 0

def extract_views(t):
    m = re.search(r"(\d+)\s*просмотр", t.lower())
    return int(m.group(1)) if m else 0
