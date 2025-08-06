import random
from typing import List, Optional
from ..browser import launch_chromium
from ..utils import UA_POOL, STEALTH_SCRIPT, realistic_headers, simulate_human, extract_elements

async def run(url: str, selector: str, headless: bool,
              attribute: Optional[str]) -> List[str]:
    pw, browser = await launch_chromium(headless, extra_args=[
        "--disable-features=TranslateUI", "--mute-audio"
    ])
    try:
        ctx = await browser.new_context(
            user_agent=random.choice(UA_POOL),
            locale="en-US",
            extra_http_headers=realistic_headers(),
            viewport={"width": 1440, "height": 900},
            java_script_enabled=True,
        )
        await ctx.add_init_script(STEALTH_SCRIPT)
        page = await ctx.new_page()
        await page.route("**/*.{png,jpg,jpeg,gif,svg,css,woff,woff2}", lambda r: r.abort())
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        await simulate_human(page)
        await page.wait_for_selector(selector, state="visible", timeout=20000)
        return await extract_elements(page, selector, attribute)
    finally:
        await browser.close(); await pw.stop()
