"""
Keyword loader module
   This module provides functionality to load information from files.
"""

# scraper/keywords_loader.py
import json

def load_keywords(path: str):
    """ Load keywords from a JSON file at the given path. """

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data["keywords"], data["name"]
