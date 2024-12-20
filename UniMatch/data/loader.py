import pickle
import os

# Base directory for data files.
BASE_DIR = os.path.dirname(__file__)


def load_database_file(filename: str):
    """
    Load data from a file in the `data` folder.

    Args:
        filename (str): The name of the file to load.

    Returns:
        Data in a format based on the file type (e.g., dict for JSON, DataFrame for CSV).

    Raises:
        ValueError: If the file type is not supported.
    """
    file_path = os.path.join(BASE_DIR, "database", filename)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, "rb") as handle:
        data = pickle.load(handle)

    return data


def get_sqlite_database_path():
    """
    Get the path to SQLite database file.

    Returns:
        db_path: The path to the SQLite database file.
    """
    db_path = os.path.join(BASE_DIR, "database", "ecommerce.db")
    return db_path
