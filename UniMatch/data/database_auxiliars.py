"""
Auxiliar functions for the Streamlit pages. 
    - get_countries: Get a dictionary of country codes
    - get_areas: Get area levels
"""
import sqlite3
from typing import Dict
from UniMatch.data.loader import get_sqlite_database_path

def get_countries() -> Dict[str, str]:
    """
    Extract the countries hash-table from the SQL database
    """
    con = sqlite3.connect(get_sqlite_database_path())
    con.row_factory = sqlite3.Row

    cursor = con.cursor()

    result = cursor.execute("SELECT * FROM COUNTRIES").fetchall()

    cursor.close()
    con.close()

    return dict(result)

def get_areas() -> Dict[int, str]:
    """
    Extract the areas hash-table from the SQL database    
    """
    con = sqlite3.connect(get_sqlite_database_path())
    con.row_factory = sqlite3.Row

    cursor = con.cursor()

    result = cursor.execute("SELECT * FROM AREAS").fetchall()

    cursor.close()
    con.close()

    return dict(result)
