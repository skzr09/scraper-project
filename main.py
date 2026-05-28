"""
Main entry point for the web scraper application.
"""

from scraper.scraper import scrape
import json


def main():
    """ main function to run the scraper """

    url = input("Enter URL or file path: ")
    data = scrape(url)

    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
