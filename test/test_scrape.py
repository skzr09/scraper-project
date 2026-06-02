"""
This is a test script to validate the scraping is working 
Usage:
    python -m test.test_scrape
"""

# scraping
from scraper.sources import load_from_json
from scraper.parser import parse_html
from scraper.fetcher import fetch

# --- SOURCES RULE PATH ---
URL_RULE_PATH = "sources/config_file.json"
URL_RULE_PATH = "sources/bleepingcomputer.json"

# --- TEST URL ---
URL = "http://localhost:8001/path/to/file/format.html"
URL = "http://localhost:8001/04_bleepingcomputer/bleepingcomputer.html"
URL = "https://www.bleepingcomputer.com/"


def main():
    print(f"[INFO] Fetching: {URL}")

    # Run the scraper with the provided URL and configuration
    # request the url content
    html = fetch(URL)

    # check 'html' for error text
    if "Error" in html or "Not Found" in html:
        print(f"[ERR ] Failed to fetch content from {URL}. Response: {html[:200]}...")
        return

    # get parsing rules from the config file
    rules = load_from_json(URL_RULE_PATH)

    # return the parsed data based on the HTML content and parsing rules
    data = parse_html(html, rules)
    
    #print pretty the data
    print(f"Scraped data: {data}")

if __name__ == "__main__":
    main()