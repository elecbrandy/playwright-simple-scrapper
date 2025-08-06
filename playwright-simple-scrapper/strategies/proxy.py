# ──────────────────────────────────────────
# playwright-simple-scraper/playwright_simple_scraper/strategies/proxy.py
# ──────────────────────────────────────────
import random
from typing import List, Optional
from ..browser import launch_chromium
from ..utils import UA_POOL, realistic_headers, extract_elements, simulate_human

async def run(url: str, selector: str, headless: bool,
              attribute: Optional[str]) -> List[str]:
    pw, browser = await launch_chromium(headless)
    try:
        headers = {
            **realistic_headers(),
            "X-Forwarded-For": ".".join(str(random.randint(1, 255)) for _ in range(4)),
            "X-Real-IP": ".".join(str(random.randint(1, 255)) for _ in range(4)),
            "Via": "1.1 proxy-server",
        }
        ctx = await browser.new_context(
            user_agent=random.choice(UA_POOL),
            viewport={"width": 1440, "height": 900},
            extra_http_headers=headers,
        )
        page = await ctx.new_page()
        await page.goto(url, wait_until="load", timeout=30000)
        await simulate_human(page)
        await page.wait_for_selector(selector, state="visible", timeout=15000)
        return await extract_elements(page, selector, attribute)
    finally:
        await browser.close(); await pw.stop()
