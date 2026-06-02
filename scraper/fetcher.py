"""
HTML content fetcher module
   This module provides a simple interface to fetch content from both remote HTTP(S)
   URLs and local filesystem paths.
"""

import requests

from scraper.logger import log

def fetch(url: str) -> str:
    """
    Fetches content from a given URL or local file path.
    Args:
        url (str): The URL or local file path to fetch content from.
    Returns:
        str: The content retrieved from the URL or local file.
    """

    if url.startswith("http://") or url.startswith("https://"):
        res = requests.get(url) #, timeout=20)
        res.raise_for_status() # Raise an exception for HTTP errors
        log.info("Fetched URL: %s with status code %s", url, res.status_code)
        return res.text
    else:
        # treat as local file
        with open(url, "r", encoding="utf-8") as f:
            content = f.read()
            log.info("Fetched local file: %s", url)
            return content
