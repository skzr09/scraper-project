from os import name

# scraping
from scraper.configs import get_config_from_url, load_configs
from scraper.parser import parse_html
from scraper.fetcher import fetch
from scraper.loader import load_keywords


# --- CONFIG PATH ---
CONFIG_PATH = "configs/config_file.json"

# --- TEST URL ---
URL = "http://localhost:8001/path/to/file/format.html"



# --- MAIN TEST ---
def main():
    print(f"[INFO] Fetching: {URL}")

    # Run the scraper with the provided URL and configuration
    # request the url content
    html = fetch(URL)

    # get parsing rules from the config file
    rules = load_configs(CONFIG_PATH)

    # return the parsed data based on the HTML content and parsing rules
    data = parse_html(html, rules)

    # load keywords from provided JSON file
    keyword_file = "bin\\keywords\\automotive.json"
    keywords, kw_name = load_keywords(keyword_file)

    print(keywords)
    print(kw_name)
    idx = 1

    for entry in data:
        title = entry.get("title", "")
        # NOTE:
        # TODO
        # this should check against inidividual keywords and return which ones matched for each title
        # not as substring
        #  'cti' in 'active' -> should not match ! FIXME
        #
        matching_keywords = [kw for kw in keywords if kw.lower() in title.lower()]
        if matching_keywords:
            print(f"[ {idx} ] Title: {title}")
            print(f"      Matching keywords: {matching_keywords}")
            print()
            idx += 1


if __name__ == "__main__":
    main()