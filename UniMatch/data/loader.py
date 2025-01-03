import os

# Base directory for data files.
BASE_DIR = os.path.dirname(__file__)

def get_sqlite_database_path() -> str:
    """Get the path to SQLite database file.

    Returns:
        db_path: The path to the SQLite database file.
    """
    db_path = os.path.join(BASE_DIR, "database", "unimatch.db")
    return db_path

def get_pdfs_folder() -> str:
    """Get the path to the UniMatch PDF folders
    
    Returns:
        pdfs_path: The path to the UniMatch PDF folders
    """
    pdfs_path = os.path.join(BASE_DIR, "pdf")
    return pdfs_path

def get_user_pdfs_folder() -> str:
    """Get the path to the UniMatch PDF folders
    
    Returns:
        pdfs_path: The path to the user-loaded PDF folders
    """
    pdfs_path = os.path.join(BASE_DIR, "user_files")
    return pdfs_path

