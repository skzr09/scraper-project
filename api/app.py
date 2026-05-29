"""
API module for the scraper project
    This module provides a FastAPI interface to run the scraper and return results.
"""

import os

from fastapi import HTTPException
from fastapi import FastAPI

# for scraping and parsing
from scraper.logger import log
from scraper.loader import load_keywords
from scraper.scraper import scrape
from scraper.configs import get_config_from_url, load_configs

# for database interaction
from db.crud import save_articles
from db.db import SessionLocal
from db.models import Article

#------------------------------------------
# Settings
#------------------------------------------

# Pagination: Default limit for number of results to return from the scraper
N_LIMIT = 20

# Create a FastAPI application instance
app = FastAPI()

#------------------------------------------
# Define a GET endpoint at the root URL that returns a status message
@app.get("/")
def root():
    return {"message": "Scraper API running"}

#------------------------------------------
# Define a GET endpoint to debug configuration selection based on URL
@app.get("/debug-config")
def debug_config(url: str):
    config = get_config_from_url(url)
    return {"config": config}

#------------------------------------------
# Define a GET endpoint to retrieve all articles from the database, with optional filtering by source URL
@app.get("/get-data")
def get_data(source: str = "",
             keyword: str = "",
             limit: int = N_LIMIT):
    """
    Get all articles from the database and return them as a list of dictionaries.\n
    Args:\n
        source (str): Optional filter to return only articles from a specific source URL.\n
        keyword (str): Optional filter to return only articles containing a specific keyword.\n
    Returns:\n
        list: A list of dictionaries containing 'title', 'url', and 'source' keys for each article.\n
    """
    db = SessionLocal()
    query = db.query(Article)

    # apply 'source' filter if provided, otherwise return all articles
    if source:
        query = query.filter(Article.source.contains(source))

    # apply 'keyword' filter to title if provided
    if keyword:
        query = query.filter(Article.title.contains(keyword))

    # sort by created_at desc
    query = query.order_by(Article.created_at.desc())

    results = query.limit(limit).all()
    db.close()

    return [
        {
            "title": r.title,
            "url": r.url,
            "source": r.source,         
            "created_at": r.created_at,
            "updated_at": r.updated_at
        }
        for r in results
    ]

#------------------------------------------
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
            "config_name": "Unknown",
            "url": url
        }
    else:
        myconfigs = {
            "ready": True,
            "error": None,
            "config": config_path,
            "config_auto": config_auto,
            "config_name": load_configs(config_path).get("name"),
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

    # TODO: temporary, the format of fields in data is not consistent across configs,
    # we need to standardize it and make it more flexible to handle different field names and structures
    # For now, we will just return the raw data and let the client handle it

    # Save the scraped articles to the database
    save_articles(data, source=myconfigs["config_name"])  


    return {"message": "Scraper API test finished running",
            "target_url": url,
            "config_path": myconfigs["config"],
            "config_auto": myconfigs["config_auto"],
            "keyword_filename": kw_name,
            "nr_results": len(data),
            "results": data[:limit]}
