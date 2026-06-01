"""
Scrapper Orchestrator
"""

from scraper.fetcher import fetch
from scraper.parser import parse_html
from scraper.configs import load_configs

import hashlib

def hash_string(text: str):
    """ Generate a SHA-256 hash of the given text. """
    return hashlib.sha256(text.encode()).hexdigest()


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
    parsed_html = parse_html(html, rules)
    # for each entry in parsed_html, compute hash(url)
    for entry in parsed_html:
        entry["url_hash"] = hash_string(entry["url"])
    return parsed_html


# TODO: REMOVE FUNCTGION, not necessary, just use the parser directly in the test
def filter_entry_by_keywords(entry: str, keywords: list) -> list:
    """
    Filter the scraped data based on the provided keywords.
    Args:
        entry (str): The scraped data entry to filter.
        keywords (list): The list of keywords to filter by.
    Returns:
        list: A list of filtered data entries that match the keywords.
    """
    filtered = []
    for kw in keywords:
        if kw.lower() in entry.lower():
            filtered.append(kw)
            break
    return filtered
