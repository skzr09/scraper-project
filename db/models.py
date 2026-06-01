"""
Database Models (tables)
    This module defines the database models for storing scraped data and configurations.
    It uses SQLAlchemy to define the models and their relationships.
"""

#from traceback import StackSummary
#from turtle import pu
#from typing import Text

from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from datetime import datetime
from db.db import Base


class Article(Base):
    """ SQLAlchemy model for the 'articles' table in the database. """
    __tablename__ = "articles"

    # Basic metadata fields
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, nullable=False)

    # url hash field to store hash of the article for deduplication
    url_hash = Column(String, unique=True, nullable=False)

    title = Column(String, nullable=True)
    source = Column(String, nullable=True)
    author = Column(String, nullable=True)
    summary = Column(String, nullable=True)

    status = Column(String, default="new", nullable=True)
    # Status:example ["new", "parsed", "enriched", "stored", "error"]

    # Enrichment
    tags = Column(Text, nullable=True) # json
    tag_scores = Column(Text, nullable=True) # json

    source_type = Column(String, nullable=True) # "blog", "media", "research_site"
    score = Column(Integer, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow) # when inserted into db
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) # when updated in db
    published_date = Column(DateTime, nullable=True) # when published on the web (optional)

    # NOTE:
    # I am not adding a 'content' field to store the full text of the article, because it can
    # be very large and may not be necessary for our use case. Instead, we can store the URL and metadata,
    # and fetch the content on demand if needed. This keeps our database lightweight and efficient
    # Consider having a separate 'ArticleContent' table in the future if we want to store the full text of
    # articles, and link it to the 'Article' table via a foreign key. This way we can keep the metadata and
    #  content separate, and only fetch the content when necessary.

