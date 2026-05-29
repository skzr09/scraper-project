"""
Database Models (tables)
    This module defines the database models for storing scraped data and configurations.
    It uses SQLAlchemy to define the models and their relationships.
"""

from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from db.db import Base


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    source = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow) # when inserted into db
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) # when updated in db
    #
    # Additional fields can be added here based on the configuration and requirements
    #

    # tags
    # summary
    # published_date
    # author
    # content
    
