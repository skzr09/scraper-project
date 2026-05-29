"""
Database setup using SQLAlchemy. 
    This module defines the database engine, session, and base class for SQLAlchemy models.
"""

from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# define database path and engine
DB_NAME = "db"
DB_FILE = "scraper.db"
DB_PATH = Path(__file__).resolve().parent.parent / DB_NAME / DB_FILE

# Create the database engine and session
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
