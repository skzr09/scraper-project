"""
API module for the scraper project
    This module provides a FastAPI interface to run the scraper and return results.
"""

import os

from fastapi import HTTPException
from fastapi import FastAPI

from scraper.logger import log
from scraper.loader import load_keywords
from scraper.scraper import scrape
from scraper.configs import get_config_from_url

N_LIMIT = 10 # Default limit for number of results to return from the scraper

# Create a FastAPI application instance
app = FastAPI()

# Define a GET endpoint at the root URL that returns a status message
@app.get("/")
def root():
    return {"message": "Scraper API running"}

# Define a GET endpoint to debug configuration selection based on URL
@app.get("/debug-config")
def debug_config(url: str):
    config = get_config_from_url(url)
    return {"config": config}


# Define a GET endpoint that accepts a URL parameter and runs the scraper
@app.get("/scrape")
def run_scraper(url: str,
                config_path: str = "",
                keyword_file: str = "",
                limit: int = N_LIMIT):
    """
    Run the scraper on the provided URL and return results.\n
    Args:\n
        url (str): The URL to scrape.\n
        config_path (str): The path to the JSON configuration file for the scraper.\n
        keyword_file (str): Optional path to a JSON file containing keywords to filter results.\n
        limit (int): The maximum number of results to return (default is N_LIMIT).\n
    Returns:\n
        dict: A dictionary containing the scraper results and a message.\n
    """
    myconfigs = {}

    #---- Validation --------

    # Validate URL, prevents bad HTTP requests without a URL parameter
    if not url:
        raise HTTPException(status_code=400, detail="URL required")

    # Auto-pick config if not provided
    if not config_path:
        config_path = get_config_from_url(url)
        config_auto = True
    else:
        config_path = f"{config_path}"
        config_auto = False

    if not os.path.exists(config_path):
        myconfigs = {
            "ready": False,
            "error": "Config not found",
            "config": config_path,
            "config_auto": config_auto,
            "url": url
        }
    else:
        myconfigs = {
            "ready": True,
            "error": None,
            "config": config_path,
            "config_auto": config_auto,
            "url": url
        }
    log.info(f"URL received: {url}")
    log.info(f"Configuration status: {myconfigs}")

    if myconfigs["error"]:
        raise HTTPException(status_code=400, detail=myconfigs["error"])

    #---- Scrape --------

    # Run the scraper with the provided URL and configuration
    data = scrape(url, myconfigs["config"])
    keywords = []
    kw_name  = ""

    if keyword_file:
        print("Loading keywords from file:", keyword_file)

        # load keywords from provided JSON file
        keywords, kw_name = load_keywords(keyword_file)

        # filter results based on keywords
        data = [d for d in data if any(k in d["title"] for k in keywords)]

    return {"message": "Scraper API test finished running",
            "target_url": url,
            "config_path": myconfigs["config"],
            "config_auto": myconfigs["config_auto"],
            "keyword_filename": kw_name,
            "nr_results": len(data),
            "results": data[:limit]}
