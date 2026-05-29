"""
Initialize the database.
    Creates all tables defined in db.models.
"""

# Run from project root with as a 'module'
#   python -m scripts.init_db

from db.db import engine
from db.models import Base

def init_db():

    print("[INFO] Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("[INFO] Database initialized successfully.")

if __name__ == "__main__":
    init_db()