"""
Configuration management for the scraper project.
    This module provides functionality to load and manage configurations for the scraper.
"""

import json


CONFIG_MAP ={
    "hackernews": "configs/hackernews.json"
}

def get_config_from_url(url: str):
    """ Get configuration based on the URL. """
    for key, path in CONFIG_MAP.items():
        if key in url:
            return path
    return "configs/generic.json"


def load_configs(path: str):
    """ Load configuration from a JSON file at the given path. """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

