"""
HTML content parser module
   This module provides functionality to parse Hacker News HTML content
   and extract story information.
"""

from bs4 import BeautifulSoup

def parse_html(html: str) -> list:
    """
    Parse HTML and extract story titles and URLs.
    Args:
        html (str): The HTML content to parse.
    Returns:
        list: A list of dictionaries containing 'title' and 'url' keys
    """
    # "html.parser" = built‑in Python parser for html
    soup = BeautifulSoup(html, "html.parser")
    data = []

    for t in soup.select(".titleline a"):
        title = t.text
        link = t.get("href", "")

        data.append({
            "title": title,
            "url": link
        })

    return data