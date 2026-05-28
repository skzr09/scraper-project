"""
API module for the scraper project
    This module provides a FastAPI interface to run the scraper and return results.
"""

from fastapi import FastAPI
from scraper.scraper import scrape

# Create a FastAPI application instance
app = FastAPI()

# Define a GET endpoint at the root URL that returns a status message
@app.get("/")
def root():
    return {"message": "Scraper API running"}


# Define a GET endpoint that accepts a URL parameter and runs the scraper
@app.get("/scrape")
def run_scraper(url: str):
    data = scrape(url)
    return {"results": data,
            "message": "Scraper API test finished running"}