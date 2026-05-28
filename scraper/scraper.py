"""
Scrapper Orchestrator
"""

from scraper.fetcher import fetch
from scraper.parser import parse_html

def scrape(url: str) -> list:
    """
    Scrapes a web page from the given URL.
    Args:
        url (str): The URL of the web page to scrape.
    Returns:
        list: The parsed data from the web page.
    """
    html = fetch(url)
    return parse_html(html)
