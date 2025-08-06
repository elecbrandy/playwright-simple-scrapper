from playwright_simple_scraper import scrape_list, scrape_href

if __name__ == "__main__":
    titles = scrape_list("https://news.ycombinator.com", ".athing .titleline")
    links = scrape_href("https://news.ycombinator.com", ".athing .titleline > a")
    print("Top 5 titles:", titles[:5])
    print("Top 5 links: ", links[:5])
