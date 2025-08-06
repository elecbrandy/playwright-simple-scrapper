import random, asyncio
from typing import List, Optional
from ..browser import launch_chromium
from ..utils import UA_POOL, realistic_headers, simulate_human, extract_elements

async def run(url: str, selector: str, headless: bool,
              attribute: Optional[str]) -> List[str]:
    pw, browser = await launch_chromium(headless)
    try:
        ctx = await browser.new_context(
            user_agent=random.choice(UA_POOL),
            viewport={"width": 1366, "height": 768},
            extra_http_headers=realistic_headers(),
        )
        page = await ctx.new_page()
        await page.goto(url, wait_until="networkidle", timeout=45000)
        await asyncio.sleep(random.uniform(3, 7))
        await simulate_human(page)
        await page.wait_for_selector(selector, state="visible", timeout=20000)
        return await extract_elements(page, selector, attribute)
    finally:
        await browser.close(); await pw.stop()
