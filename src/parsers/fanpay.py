import asyncio, re
from playwright.async_api import async_playwright

BASE = "https://funpay.com"

async def scan_fanpay(limit=15):
    res = []
    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True)
        page = await b.new_page()
        await page.goto(BASE)
        await asyncio.sleep(2)

        cards = await page.query_selector_all("a[href*='/lot/']")
        for c in cards[:limit]:
            t = await c.inner_text()
            url = await c.get_attribute("href")
            price = extract_price(t)
            if price <= 0: continue
            res.append({
                "name": t.split("\n")[0][:100],
                "price": price,
                "url": BASE + url,
                "seller_rating": 0.0,
                "views": 0,
                "source": "fanpay"
            })
        await b.close()
    return res

def extract_price(t):
    m = re.search(r"(\d+)\s*[₽р]", t)
    return int(m.group(1)) if m else 0
