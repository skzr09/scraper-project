"""
HTML content fetcher module
   This module provides a simple interface to fetch content from both remote HTTP(S)
   URLs and local filesystem paths.
"""

import requests
from requests.exceptions import HTTPError
from scraper.logger import log

def fetch(url: str) -> str:
    """
    Fetches content from a given URL or local file path.
    Args:
        url (str): The URL or local file path to fetch content from.
    Returns:
        str: The content retrieved from the URL or local file.
    """
    res = None

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:

        if url.startswith("http://") or url.startswith("https://"):
            res = requests.get(url, headers=headers, timeout=20) #timeout=20)

            if res.status_code == 403:
                print("❌ Access blocked (403) for %s", url)
                log.warning("❌ Access blocked (403) for %s", url)
                return "Error: Access blocked (403)"

            res.raise_for_status() # Raise an exception for HTTP errors
            log.info("Fetched URL: %s with status code %s", url, res.status_code)
            return res.text

        else:
            # treat as local file
            with open(url, "r", encoding="utf-8") as f:
                content = f.read()
                log.info("Fetched local file: %s", url)
                return content

    except Exception as e:
        print("[Err ] Failed to fetch %s: \n[MSG] %s", url, e)
        log.error("Unexpected error while fetching %s: %s", url, e)
        return ""
