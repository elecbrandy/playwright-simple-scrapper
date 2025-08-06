import pytest
from playwright_simple_scraper import scrape_list

def test_example_com_h1():
    result = scrape_list("https://example.com", "h1")
    assert "Example Domain" in result[0]
