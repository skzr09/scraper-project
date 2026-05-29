"""
Scrapper Orchestrator
"""

from scraper.fetcher import fetch
from scraper.parser import parse_html
from scraper.configs import load_configs

def scrape(url: str, config_path: str) -> list:
    """
    Scrapes a web page from the given URL.
    Args:
        url (str): The URL of the web page to scrape.
        config_path (str): The path to the JSON configuration file.
    Returns:
        list: The parsed data from the web page.
    """
    # request the url content
    html = fetch(url)
    # get parsing rules from the config file
    rules = load_configs(config_path)
    # return the parsed data based on the HTML content and parsing rules
    return parse_html(html, rules)
