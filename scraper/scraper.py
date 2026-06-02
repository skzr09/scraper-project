"""
Scrapper Orchestrator
"""

import hashlib

from scraper.fetcher import fetch
from scraper.parser import parse_html
from scraper.sources import load_from_json


def hash_string(text: str):
    """ Generate a SHA-256 hash of the given text. """
    return hashlib.sha256(text.encode()).hexdigest()


def scrape(url: str, source_path: str) -> list:
    """
    Scrapes a web page from the given URL.
    Args:
        url (str): The URL of the web page to scrape.
        source_path (str): The path to the source JSON configuration file.
    Returns:
        list: The parsed data from the web page.
    """
    # request the url content
    html = fetch(url)
    # get parsing rules from the config file
    rules = load_from_json(source_path)
    # return the parsed data based on the HTML content and parsing rules
    parsed_html = parse_html(html, rules)
    # for each entry in parsed_html, compute hash(url)
    for entry in parsed_html:
        entry["url_hash"] = hash_string(entry["url"])
    return parsed_html
