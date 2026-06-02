"""
API module for the scraper project
    This module provides a FastAPI interface to run the scraper and return results.
"""

from operator import concat
import os
import json

from datetime import datetime
from fastapi import HTTPException
from fastapi import FastAPI

# for scraping and parsing
from scraper.keywords import load_keywords_library, keyword_match, load_keywords
from scraper.logger import log
from scraper.scraper import scrape
from scraper.sources import get_sources_from_url, load_from_json


# for database interaction
from db.crud import save_articles
from db.db import SessionLocal
from db.models import Article

#------------------------------------------
# Settings
#------------------------------------------

# Pagination: Default limit for number of results to return from the scraper
N_LIMIT = 20

# Path to the folder with all the keywords
PATH_KEYWORDS = "bin\\keywords"

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
    config = get_sources_from_url(url)
    return {"config": config}

#------------------------------------------
# Define a GET endpoint to retrieve all articles from the database, with optional filtering by source URL
@app.get("/get-data")
def get_data(source: str = "",
             keyword: str = "",
             tags: str = "",
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

    # apply 'keyword' filter to title if provided **TODO: include summary?
    if keyword:
        query = query.filter(Article.title.contains(keyword))

    # apply 'tag' filter to tags if provided
    if tags:
        tag_list = [t.strip() for t in tags.split(",")] # allows multi tagging, e.g. tag=tag1,tag2
        for tg in tag_list:
            query = query.filter(Article.tags.contains(tg))

    # sort by created_at desc
    query = query.order_by(Article.created_at.desc())

    results = query.limit(limit).all()
    db.close()

    return [
        {
            "title": r.title,
            "url": r.url,
            "source": r.source,
            "tags": r.tags,
            "author": r.author,
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
                limit: int = N_LIMIT):
    """
    Run the scraper on the provided URL and return results.\n
    Args:\n
        url (str): The URL to scrape.\n
        config_path (str): The path to the JSON configuration file for the scraper.\n
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
        config_path = get_sources_from_url(url)
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
            "config_name": load_from_json(config_path).get("name"),
            "url": url
        }

    log.info("URL received: %s", url)
    log.info("Configuration status: %s", myconfigs)

    if myconfigs["error"]:
        raise HTTPException(status_code=400, detail=myconfigs["error"])

    #
    # TODO: Sections below need clearning..
    #

    #---- Scrape --------

    # Run the scraper with the provided URL and configuration
    data = scrape(url, myconfigs["config"])
    keywords = []
    kw_name  = ""
    loop_ctr = 0

    #---- Enrichment --------

    # get list of all tags and associated keywords into dict ['tag']:[kw1, kw2, ...]
    tags_dict = load_keywords_library(PATH_KEYWORDS)
    log.info("Loaded keywords library with tags: %s", list(tags_dict.keys()))

    # TODO: The following parsing of scraped data should be moved to a dedicated function

    for entry in data:
        text_content = ""
        tags_selected = []
        tag_scores = {}

        # from the scraped data get the title and summary if available
        if "title" in entry:
            text_content += entry.get("title", "")

        if "summary" in entry:
            text_content += " <summary> " + entry.get("summary", "")

        # check each tag in the keyword library and see if any keywords match
        for tag, keywords in tags_dict.items():
            matching_keywords = keyword_match(text_content, keywords)
            if matching_keywords:
                tags_selected.append(concat("#", tag))
                tag_scores[tag] = len(matching_keywords)

        # add the matched tags to the entry and the tag scores
        if tags_selected:
            entry["tags"] = ",".join(tags_selected)
            log.debug("Entry: %s... Matched tags: %s", entry.get("title", "")[:10], tags_selected)
        else:
            entry["tags"] = ""

        if tag_scores:
            entry["tag_scores"] = json.dumps(tag_scores) # convert dict to JSON string for storage
            log.debug("Scores: %s... Tag scores: %s", entry.get("title", "")[:10], tag_scores)
        else:
            entry["tag_scores"] = json.dumps({}) # empty dict as JSON string

        if "author" not in entry:
            entry["author"] = ""

        if ("date" not in entry) or (not entry["date"]):
            entry["date"] = None
        else:
            # try to parse date into standard datetime format, then overwrite date field
            parsed_date = datetime.strptime(entry["date"], "%b %d, %Y")
            entry["date"] = parsed_date

        if "source" not in entry:
            entry["source"] = ""
        else:
            entry["source"] = myconfigs["config_name"]

        loop_ctr += 1
        log.debug("%d Processed with tags/scores: %s", loop_ctr, entry["tag_scores"])


    # TODO: temporary, the format of fields in data is not consistent across configs,
    # we need to standardize it and make it more flexible to handle different field names and structures
    # For now, we will just return the raw data and let the client handle it

    log.info("Processed entries in total: %d", loop_ctr)

    # Save the scraped articles to the database
    save_articles(data)

    return {"message": "Scraper API test finished running",
            "target_url": url,
            "config_path": myconfigs["config"],
            "config_auto": myconfigs["config_auto"],
            "keyword_filename": kw_name,
            "nr_results": len(data),
            "results": data[:limit]}
