"""
Initialize the database.
    Creates all tables defined in db.models.
Usage:
    python -m scripts.init_db
Notes:
    - Run from project root as a module.
    - This should be run before starting the server or API to ensure the database is set up.
    - If the database file already exists, it will skip initialization to avoid overwriting data.
"""

from db.db import engine
from db.models import Base

def init_db():

    print("[INFO] Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("[INFO] Database initialized successfully.")

if __name__ == "__main__":
    init_db()

