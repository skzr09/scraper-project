""" Test the config selection logic for the scraper. """

# test_config.py
from scraper.configs import get_config_from_url

url = "http://localhost:8001/0.... website.html"

result = get_config_from_url(url)

print(result)
