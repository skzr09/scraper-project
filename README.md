# scraper-project
Scraper project

## Structure
```
project/
│
├── bin/
├── scraper/
│   └── hackernews.py
├── models/
├── main.py
├── requirements.txt
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
