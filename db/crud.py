"""
CRUD Database Operations
"""
from db.db import SessionLocal
from db.models import Article

from scraper.logger import log

def save_articles(data):
    """
    Save a list of articles to the database. Each article is a dict with keys "title" and "url".
    Args:
        data (list): A list of dictionaries, each containing "title" and "url" of an article.
        source (str): The source of the articles (e.g., "news_site").
    Returns:
        None
    """
    db = SessionLocal()

    for item in data:
        # check if the article already exists to prevent duplicates (checks URL hash)
        exists = db.query(Article).filter_by(url_hash=item["url_hash"]).first()

        if not exists:
           log.debug(f"Adding to table (hash): {item['url_hash']}")

           db.add(Article(
                title       = item["title"],
                url         = item["url"],
                url_hash    = item["url_hash"],
                tags        = item["tags"],
                tag_scores  = item["tag_scores"],
                source      = item["source"],
                author      = item["author"],
                published_date=item["date"]
                # TODO: add more fields as needed
            ))

    db.commit()
    db.close()

