import os
from typing import Tuple
from playwright.async_api import async_playwright, Browser, Playwright

async def launch_chromium(headless: bool = True, extra_args=None) -> Tuple[Playwright, Browser]:
    pw = await async_playwright().start()
    is_ci = os.getenv("CI") or os.getenv("GITHUB_ACTIONS")
    args = [
        "--no-sandbox",
        "--disable-setuid-sandbox",
        "--disable-dev-shm-usage",
        "--disable-blink-features=AutomationControlled",
    ]
    if extra_args:
        args += extra_args
    if is_ci:
        args += ["--single-process"]
    browser = await pw.chromium.launch(headless=headless, args=args)
    return pw, browser

async def launch_firefox(headless: bool = True):
    pw = await async_playwright().start()
    browser = await pw.firefox.launch(headless=headless, args=["--no-sandbox"])
    return pw, browser
