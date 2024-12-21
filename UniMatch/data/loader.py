import pickle
import os

# Base directory for data files.
BASE_DIR = os.path.dirname(__file__)

def get_sqlite_database_path():
    """
    Get the path to SQLite database file.

    Returns:
        db_path: The path to the SQLite database file.
    """
    db_path = os.path.join(BASE_DIR, "database", "unimatch.db")
    return db_path
