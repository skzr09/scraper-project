""" Module for handling keyword-related operations. """

import re
import json

from pathlib import Path
from scraper.logger import log


def load_keywords_library(keywords_folder: str):
    """
    Load keywords from all JSON files in a folder and return a dictionary.
    Args:
        keywords_folder: Path to the folder containing keyword JSON files
    Returns:
        Dictionary where key = config[tag] and value = list of config[keywords]
    """
    keywords_dict = {}
    keywords_path = Path(keywords_folder)

    if not keywords_path.exists():
        log.warning("Keywords folder not found: %s", keywords_folder)
        return keywords_dict

    for file in keywords_path.glob("*.json"):
        try:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
                if "tag" in data and "keywords" in data:
                    tag = data["tag"]
                    keywords_dict[tag] = data["keywords"]
        except (json.JSONDecodeError, IOError) as e:
            log.error("Error loading keywords from %s: %s", file, e)

    return keywords_dict


def keyword_match(entry: str, keywords: list[str]) -> list[str]:
    """
    Check if any of the keywords are present in the entry string and
    return a list of matched keywords.
    Args:
        entry: The string to check for keyword matches
        keywords: A list of keywords to match against the entry
    Returns:
        A list of keywords that were found in the entry string.
    """
    matched = []
    for kw in keywords:
        if re.search(rf"\b{re.escape(kw)}\b", entry, re.IGNORECASE):
            matched.append(kw)
    return matched


# TODO: consider removing (only being used in test module)
def load_keywords(path: str):
    """ Load keywords from a JSON file at the given path. """
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data["keywords"], data["name"]
