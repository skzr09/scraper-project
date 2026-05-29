"""
HTML content parser module
   This module provides functionality to parse Hacker News HTML content
   and extract story information.
"""

from html import unescape
from bs4 import BeautifulSoup

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

    for it in items:
        entry = {}

        for field, cfg in rules["fields"].items():
            element = it.select_one(cfg["selector"])
            entry[field] = element.text.strip() if element else ""
            
            if not element:
                if cfg.get("optional"):
                    entry[field] = None
                    continue
                else:
                    continue

            if cfg["type"] == "text":
                entry[field] = element.text.strip()

            elif cfg["type"] == "attribute":
                entry[field] = element.get(cfg["name"], "")

        results.append(entry)

    return results

"""

    for t in soup.select(".titleline a"):
        #title = t.text
        title = unescape(t.text) # clearner output without HTML entities
        link = t.get("href", "")

        data.append({
            "title": title,
            "url": link
        })
"""