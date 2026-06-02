"""
Configuration management for the scraper project.
    This module provides functionality to load and manage configurations for the scraper.
"""

import json
import os

from pathlib import Path
from scraper.logger import log

# TODO: 'hardcoded', fix later
SOURCES_NAME = "sources"
BASE_DIR = Path(__file__).resolve().parent.parent

def get_sources_path():
    """ Get the path to the sources directory. """
    return BASE_DIR / SOURCES_NAME

def load_from_json(path: str):
    """ Load configuration from a JSON file at the given path. """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_sources_from_url(url: str):
    """ Get configuration based on the URL. """

    # Extract the domain from the URL to determine which configuration to use
    # Get matching directly from the config file defined URLs to prevent conflicts

    path_src = get_sources_path()
    src_files = os.listdir(path_src)

    for src in src_files:
        src_rule_path = os.path.join(path_src, src) # get full path to the source rule file
        # log.info(f"Checking: {cfg_path}")

        with open(src_rule_path, "r", encoding="utf-8") as f:
            cfg_data = json.load(f)
            log.debug("Base URL(s): %s", cfg_data.get("base_urls"))

            if "base_urls" in cfg_data:
                for base in cfg_data["base_urls"]:
                    if base in url:
                        log.debug("Match found: %s", src_rule_path)
                        return src_rule_path
    log.warning("No matching config found for URL: %s", url)
    return None


