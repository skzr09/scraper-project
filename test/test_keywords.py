""" Test loading keywords library and printing it in a readable format. """

import json
from scraper.configs import load_keywords_library

KEYWORD_PATH = "bin\\keywords"

# load the keyword library, which is a dictionary of tags and their associated keywords
tag_kw = load_keywords_library(KEYWORD_PATH)

print(json.dumps(tag_kw, indent=2))
