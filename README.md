# scraper-project
Project used to implement content scraper from the web. Can be scaled for as many sources as needed since each source has a dedicated parser. The information scraped is enriched with defined rules and stored in database. FastAPI is used to provide endpoint interface to the `scraper` function and `get-data` to access the information in the database.


## Structure
Summary of project structure

```python
project/
│
├── bin/
|   └── demo/DEMO.md        # Details on the demo
├── config/                 # Environment app configuations
│   └── configs.yaml
├── api/                    # FastAPI interface
│   └── app.py
├── db/                     # database models
│   └── db.py
│   └── models.py
|   ...
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

## Quick Demo
Check `bin\demo\DEMO.md`. Need to setup environment before demo (Includes setup of database, server and api interface).

```bash
$ python demo.py
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

## Development Plan+Logic

Check `\bin\Concept.md`