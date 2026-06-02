"""
Database setup using SQLAlchemy. 
    This module defines the database engine, session, and base class for SQLAlchemy models.
"""

from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from config import config
from scraper.logger import log

# define database path and engine
DB_FILE = config.database.path #["database"]["path"]
DB_PATH = Path(__file__).resolve().parent.parent / DB_FILE

log.info(f"Database path: {DB_PATH}")

try:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    log.info(f"Database directory exists: {DB_PATH.parent}")

    # Create the database engine and session
    engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)

    SessionLocal = sessionmaker(bind=engine)
    Base = declarative_base()
    log.info(f"Database created at: {DB_PATH}")

except Exception as e:
    log.error(f"Error initializing database: {e}")
    print(f"[ERR ] Failed to initialize database: {e}")
    raise

