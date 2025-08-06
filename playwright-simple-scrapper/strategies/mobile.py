import asyncio
from typing import List, Optional
from ..browser import launch_chromium
from ..utils import realistic_headers, extract_elements

MOBILE_UA = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1"

async def run(url: str, selector: str, headless: bool,
              attribute: Optional[str]) -> List[str]:
    pw, browser = await launch_chromium(headless)
    try:
        ctx = await browser.new_context(
            user_agent=MOBILE_UA,
            viewport={"width": 375, "height": 667},
            device_scale_factor=2,
            is_mobile=True,
            has_touch=True,
            extra_http_headers=realistic_headers(),
        )
        page = await ctx.new_page()
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        await page.touch_screen.tap(200, 300)
        for _ in range(3):
            await page.evaluate("window.scrollBy(0, 200)")
            await asyncio.sleep(0.8)
        await page.wait_for_selector(selector, state="visible", timeout=15000)
        return await extract_elements(page, selector, attribute)
    finally:
        await browser.close(); await pw.stop()
