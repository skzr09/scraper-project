# DEMO

Included in this project there is a simple demo which allows to try using the `scraping engine` out-of-the-box. This directory contains details and examples of how to run the engine and outputs.

**[ Demo for testing functions only ]**


## 📦 Demo Package

### Setup Environment

⚠️ Tested on Windows (should also work on Linux/macOS - fingers cross)

1. **Create Virtual Environment**
   ```bash
   $ python -m venv .venv
   ```
   Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`

2. **Install Required Packages**
   ```bash
   $ pip install -r requirements.txt
   ```

### Configs

The application uses a centralized configuration file. Validation through `pydantic`.
```
\config\config.yaml
```

## ▶️ Usage

### Run demo script

Run the main provided script with the demo file (from `root` directory). This will initialize the database, content server and the application.

```
$ python demo.py
```

**Example**
```bash
(.venv) \scraper-project> python demo2.py
==================[ SCRAPER DEMO ]==================
[INFO] Initializing demo environment...
[WARN] Database already exists!
[INFO] ✅ DB Path: data/scraper.db
[INFO] Starting server...
[INFO] Starting API...
[INFO] ✅ Server running (PID: 20752) See http://localhost:8001
[INFO] ✅ API running    (PID: 35768) See http://localhost:8000
====================================================
INFO:     Will watch for changes in these directories: ['\\scraper-project']
[INFO] Serving at http://localhost:8001
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [14784] using StatReload
INFO:     Started server process [17928]
INFO:     Waiting for application startup.
INFO:     Application startup complete.

// (CTRL + C) to end
```

### Components

The demo sets up and initializes the following components (see table below).

| Component | Description |
|-----------|-------------|
| Content Server | Serves static HTML pages (mock sources) (Port 8001) |
| API Server | FastAPI application exposing endpoints (Port 8000) |
| Scraper Engine | Extracts and processes data |
| Database | Stores enriched results locally |


### Get data

Sample data is not provided since -*I do not own it*-, as such, to test the application, better download some data and test it in 'offline mode'.

For the demo, go to [BleepingComputer](https://www.bleepingcomputer.com/), right click on the page and "Save as" (CTRL + S). Make sure to save the data inside a folder, suggestion.

#### Example
```
root\
| data
|   |__mydata\bleepingComputerpage.html
|   |__mydata\bleepingComputerpage_files\
```

#### Check Content
Once running, check in the browser localhost:port, you should be able to see the contents.

```python
[ Local Server content ] http://localhost:8001
```

### Using Application
Once running, check the link (ports might vary based on `config.yaml`). Inside local application `APP` the following endpoints should be available.

```python
[ Local Application (FastAPI) ] http://localhost:8000/docs
```

#### /get-data

Provides interface to query the database. Check the parameters available (use 'Execute'). Will return entries from the database which match. Make sure to run scraper first in order to populate the database.

![fastapi_getdata](..\pics\02_fastapi_getdata.png)


#### /run-scraper

Scraper application. Pass as input the path url for the targeted `http` url.

![fastapi_getdata](..\pics\03_fastapi_runscraper.png)

