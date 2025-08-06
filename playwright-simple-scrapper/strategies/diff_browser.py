from typing import List, Optional
from ..browser import launch_firefox
from ..utils import extract_elements

async def run(url: str, selector: str, headless: bool,
              attribute: Optional[str]) -> List[str]:
    pw, browser = await launch_firefox(headless)
    try:
        ctx = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
            viewport={"width": 1280, "height": 720},
        )
        page = await ctx.new_page()
        await page.goto(url, wait_until="load", timeout=30000)
        await page.wait_for_selector(selector, state="visible", timeout=15000)
        return await extract_elements(page, selector, attribute)
    finally:
        await browser.close(); await pw.stop()
