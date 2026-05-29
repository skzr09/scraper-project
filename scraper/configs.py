"""
Configuration management for the scraper project.
    This module provides functionality to load and manage configurations for the scraper.
"""

import json
import os

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# --REMOVED-- no info loaded directly from json files
#CONFIG_MAP ={
#    "hackernews"    : "configs/hackernews.json",
#    "thehackernews" : "configs/thehackernews.json"
#}

def get_configs_path():
    """ Get the path to the configs directory. """
    return BASE_DIR / "configs"


def get_config_from_url(url: str):
    """ Get configuration based on the URL. """

    # Extract the domain from the URL to determine which configuration to use
    # Get matching directly from the config file defined URLs to prevent conflicts

    path_configs = get_configs_path()
    print(get_configs_path())

    config_files = os.listdir(path_configs)

    for cfg in config_files:
        cfg_path = os.path.join(path_configs, cfg) # get full path to the config file

        print(f"Checking: {cfg_path}")

        with open(cfg_path, "r", encoding="utf-8") as f:
            cfg_data = json.load(f)
            print(f"Base URL(s): {cfg_data.get('base_urls')}")

            if "base_urls" in cfg_data:
                for base in cfg_data["base_urls"]:
                    if base in url:
                        print(f"✅ Match found: {cfg_path}")
                        return cfg_path
    print("❌ No matching config found for URL:", url)
    return None

def load_configs(path: str):
    """ Load configuration from a JSON file at the given path. """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

