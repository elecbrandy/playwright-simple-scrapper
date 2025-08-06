import asyncio
import importlib
import random
from typing import List, Optional
from .exceptions import ScrapeError

_STRATEGY_PATHS = [
    "playwright_simple_scraper.strategies.stealth",
    "playwright_simple_scraper.strategies.human_like",
    "playwright_simple_scraper.strategies.diff_browser",
    "playwright_simple_scraper.strategies.mobile",
    "playwright_simple_scraper.strategies.proxy",
]

async def _run_strategies(url: str, selector: str, attribute: Optional[str], headless: bool) -> List[str]:
    last_err: Exception | None = None

    # Try each strategy in order
    for i, mod_path in enumerate(_STRATEGY_PATHS):
        strat = importlib.import_module(mod_path)
        try:
            return await strat.run(url, selector, headless, attribute)
        except Exception as e:
            last_err = e
            await asyncio.sleep((i + 1) * 2 + random.uniform(1, 3))
    raise RuntimeError(f"All strategies failed: {last_err}")

def _run_sync(url: str, selector: str,attribute: Optional[str]) -> List[str]:
    try:
        # Check if we are already in an event loop
        loop = asyncio.get_running_loop()
        import nest_asyncio; nest_asyncio.apply()
        return loop.run_until_complete(_run_strategies(url, selector, attribute, True))
    except RuntimeError:
        # If not, create a new event loop
        return asyncio.run(_run_strategies(url, selector, attribute, True))

def _validate_inputs(url: str, selector: str) -> None:
    if not isinstance(url, str):
        raise TypeError("URL must be a string")
    if not url:
        raise ValueError("URL must not be empty")
    if not isinstance(selector, str):
        raise TypeError("Selector must be a string")
    if not selector:
        raise ValueError("Selector must not be empty")

def scrape_list(url: str, selector: str) -> List[str]:
    """Return the text of all elements that match a CSS selector.

    Uses Playwright to open the page, tries a few safe methods,
    and collects each element’s inner text (trimmed).

    Args:
      url: Page URL.
      selector: CSS selector to match.

    Returns:
      List of texts (empty if nothing matches).
    """
    _validate_inputs(url, selector)
    return _run_sync(url, selector, None)


def scrape_href(url: str, selector: str) -> List[str]:
    """Return the href attributes of all elements that match a CSS selector.

    Uses Playwright to open the page, tries a few safe methods,
    and collects each element’s href attribute.

    Args:
      url: Page URL.
      selector: CSS selector to match.

    Returns:
      List of hrefs (empty if nothing matches).
    """
    _validate_inputs(url, selector)
    return _run_sync(url, selector, "href")
