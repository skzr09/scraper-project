"""
HTML content parser module
   This module provides functionality to parse Hacker News HTML content
   and extract story information.
"""

# import select
from bs4 import BeautifulSoup
from scraper.logger import log


def parse_html(html: str, rules: dict) -> list:
    """
    Parse HTML and extract story titles and URLs.
    Args:
        html (str): The HTML content to parse.
        rules (dict): The parsing rules from the configuration file.
    Returns:
        list: A list of dictionaries containing 'title' and 'url' keys
    """
    # "html.parser" = built‑in Python parser for html
    soup = BeautifulSoup(html, "html.parser")
    items = soup.select(rules["item_selector"])
    results = []

    log.info("Parsing HTML with %d items found using selector: %s",
             len(items), rules["item_selector"])

    for it in items:
        entry = {}

        for field, cfg in rules["fields"].items():
            # element = it.select_one(cfg["selector"])

            if cfg["selector"] == "":
                element = it
            else:
                element = it.select_one(cfg["selector"])

            log.debug("Processing field: %s, Selector: %s, Element found: %s",
                      field, cfg["selector"], bool(element))

            # updated to deal with cases
            #   URL is on the root <a> element / No need to re-select

            entry[field] = element.text.strip() if element else ""

            if not element:
                if cfg.get("optional"):
                    entry[field] = None
                    continue

            if cfg["type"] == "text":
                entry[field] = element.text.strip()

            elif cfg["type"] == "attribute":
                entry[field] = element.get(cfg["name"], "")

        results.append(entry)

    return results
