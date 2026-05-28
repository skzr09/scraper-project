# scraper-project
Scraper project

## Structure
Summary of project structure

```python
project/
│
├── bin/
├── data/               # empty by default (need to download data content)
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

Clone the repository:
```bash
git clone <repository-url>
cd scraper-project
```

Install dependencies using the requirements file:
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


# Logic

### 1. Setup basic environemnt

Need to setup basic environment for testing of scrapping. This can be done fully 'online' mode but we will likely ran into issues with website 'rate limits'. Thus options include:

1. Have 'offline' mode (page is read from a stored local file) -> issue: no HTTP layer (no realistic)
2. Have 'live local' mode (page is served locally using localhost:8000) -> better for overall testing.

### 2. Scrapper

1. Setup the basic scrapper
2. Make sure the content is moduralized from the begginning
    * contains `fetcher.py`, `parser.py` and `scraper` files

###