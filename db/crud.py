"""
CRUD Database Operations
"""

from db.db import SessionLocal
from db.models import Article

def save_articles(data, source):
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
        exists = db.query(Article).filter_by(url=item["url"]).first()
        if not exists:
            db.add(Article(
                title=item["title"],
                url=item["url"],
                source=source
            ))

    db.commit()
    db.close()
