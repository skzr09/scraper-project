# scraper-project
Scraper project

## Structure
Summary of project structure

```python
project/
│
├── bin/
├── api/
│   └── app.py
├── configs/            # source parsing configs
│   └── hackernews.py
│       ...
├── data/               # empty by default (download data content)
├── scraper/            # main module
│   └── fetcher.py
│       parser.py
│       scraper.py
├── scripts/
├── models/
├── main.py             # entry point
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

## API Setup
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

# Development Plan+Logic

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
>> Added `configs.py` to the scraper\ to manage the config mapping
>> Added auto-selection of configs based on the URL selection
* In `configs`, added support for:
    * hackernews
    * todo
    * todo


