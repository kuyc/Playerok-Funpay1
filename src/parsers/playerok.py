import asyncio, re
from playwright.async_api import async_playwright

BASE_URL = "https://playerok.com"

async def scan_playerok(limit=20):
    res = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(BASE_URL + "/category/cs2")
        for _ in range(2):
            await page.mouse.wheel(0, 2500)
            await asyncio.sleep(1)

        cards = await page.query_selector_all("a[href*='/product/']")
        for c in cards[:limit]:
            text = await c.inner_text()
            url = await c.get_attribute("href")
            price = extract_price(text)
            if price <= 0:
                continue
            res.append({
                "name": text.split("\n")[0][:100],
                "price": price,
                "url": BASE_URL + url,
                "seller_rating": extract_rating(text),
                "views": extract_views(text),
                "source": "playerok"
            })
        await browser.close()
    return res

def extract_price(t): 
    m = re.search(r"(\d+)\s*₽", t)
    return int(m.group(1)) if m else 0

def extract_rating(t):
    m = re.search(r"(\d\.\d)", t)
    return float(m.group(1)) if m else 0.0

def extract_views(t):
    m = re.search(r"(\d+)\s*просмотр", t.lower())
    return int(m.group(1)) if m else 0
