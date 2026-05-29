# scraper-project
Scraper project

## Structure
Summary of project structure

```python
project/
│
├── bin/
├── api/                    # FastAPI
│   └── app.py
├── db/                     # database
│   └── db.py
│   └── models.py
|
├── configs/                # parsing rules
│   └── hackernews.json
│   └── bleepingcomputer.py
│       ...
├── data/                   # data samples (download data content)
├── scraper/                # main module
│   └── fetcher.py
│   └── parser.py
│   └── scraper.py
|       ...
├── scripts/
│   └── init_db.py          # initialize database
│   └── server.py           # initialize server localhost
|
├── test/                   # validation
├── main.py                 # entry point
├── README.md
├── requirements.txt
```

## Install

Clone the repository
```bash
git clone <repository-url>
cd scraper-project
```

Setup virtual environment (optionally use `virtualenv`)
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate       # Windows
```

Install dependencies using the requirements file
```bash
pip install -r requirements.txt
```

Verify installation:
```bash
python main.py
```

## Database

### Create database
To instantiate the database (local) used to store data, use init script. Output in `\db\`

```bash
@ python -m scripts.init_db
```

### Delete database

```bash
$ del .\db\scraper.db
```



## Testing

### Live mode - localhost server
Get data from online sources, such 'thehackernews' and download the html page.
This allows testing the models in a setup where the html is depo

**Download file CLI**
```bash
curl https://news.ycombinator.com > index.html
```
**Proposed structure**
```bash
# example
 data/
 └── index.html

 # setup
 $ python -m http.server 8000

 # check
 http://localhost:8000
```

Optionally use the script `server.py`
```bash
$ python server.py
```

### API Setup
Setup of [FastAPI](https://fastapi.tiangolo.com/) to connect to backend.

### Install and run

```bash
# install
$ pip install fastapi uvicorn

# start server (from project root)
uvicorn api.app:app --reload --port 8000

# open
http://localhost:8000/docs
```

## Adding sources

### Select the source

1. Select URL = "https://websiteXYZ.com"
2. (for offline testing) Go to the page and 'SAVE AS' (.html)
3. Create a config file and add in `configs/` (use template)

### Create the config file
Create the configuration files with the parsing rules. Within new config file make sure that the url have both options *.html (for offline testing) and *.com. See example. Finish the configuration of the new file with the selected fields for carving data from website.
```json
# Example of config for 'websitexyz'
{
  "name": "websiteXYZ",
  "base_urls": [
    "websiteXYZ.com",
    "websiteXYZ.html"
  ],
  "item_selector": "...",
  "fields": {
    ...
  }
}
```

### Testing
For testing that the config data is correctly being loaded use the testing scripts (see `test\`).
```bash
$ python -m test.test_config_selection
```

# Development Plan+Logic

## Features

* Core scraping engine
* Supports live online and live offline (local) URLs
* Supports multiple sources
* Uses generic parser json configuration files for parsing rules


## Development

### 1. Setup basic environemnt

Need to setup basic environment for testing of scrapping. This can be done fully 'online' mode but we will likely ran into issues with website 'rate limits'. Thus options include:

1. Have 'offline' mode (page is read from a stored local file) -> issue: no HTTP layer (no realistic)
2. Have 'live local' mode (page is served locally using localhost:8001)
    * *better for overall testing - 8001 is being used for FastAPI server*

### 2. Scrapper

* Setup the basic scrapper
* Make sure the content is moduralized from the begginning
    * contains `fetcher.py`, `parser.py` and `scraper` files
* Added `beautifulsoup4`, `requests`

### 3. API Backend (FastAPI)

* Connect API to backend (Client → FastAPI → Scraper → HTML → Parsed → JSON ✅)
* Added: `fastapi`, `uvicorn`

### 4. Expanded config-based sources

* Defined a rule-based generic parser to handle different formats - each with specific parsing rules.
* Added `configs.py` to the scraper\ to manage the config mapping
* Added auto-selection of configs based on the URL selection
* In `configs`, added support for (examples):
    * *new.ycombinaytor hackernews*
    * *thehackernews*
    * *bleepingcomputer*

### 5. Logging

* Added basic support for `logging` accross the module.

### 6. Storage

* Added support for DB (save results, query stored data and avoid duplications)
* Setup `sqlalchemy` for strage (SQL abstraction rather than direct SQL communication).
* Added `db/` folder with the models and DB interface.
* Added option in main `app` to get data from the existing database (basic filter).

```
Notes:
* Used 'sqlalchemy' to avoid exposure to raw DB commands.
* The DB is simple and only local for now.
* The get-data has very basic filtering by 'source' field.
```

### 7. Enrichment and Filtering

* Add filterting and enrichment features
* Add tags and other fields in DB
* TODO :)