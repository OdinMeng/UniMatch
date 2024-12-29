# External functions to manage matches in the database.

from UniMatch.data.loader import get_sqlite_database_path
import sqlite3
from typing import List

def clear_matches(id: int) -> int:
    """ Attempts to clear the matches of a user.

    Returns 1 if an error occurred, 0 otherwise.
    """
    # Base statement
    delete_statement = 'DELETE FROM MATCHES WHERE IDUSER=?'
    
    # Connect to DB
    con = sqlite3.connect(get_sqlite_database_path())
    curse = con.cursor()

    # Attempt to delete matches
    try:
        curse.execute(delete_statement, (id,))
    except Exception as e: # Rollback in case of error
        con.rollback()
        curse.close()
        con.close()
        raise 1
    
    # Close and commit in case everything went well
    con.commit()
    curse.close()
    con.close()
    return 0

def add_matches(id: int, raw_matches: List) -> int:
    """ Attempts to add matches of a user, given a list of matches.

    Returns 1 if an error occurred, 0 otherwise.
    """

    # SQL Insert base statement
    insert_statement = 'INSERT INTO MATCHES (IDUSER, IDUNIVERSITY, IDCOURSE) VALUES (?,?,?)'
    
    # Connect to DB
    con = sqlite3.connect(get_sqlite_database_path())
    curse = con.cursor()

    # Iterate over matches
    for match in raw_matches:
        try:  
            curse.execute(insert_statement, (id, match.IDUniversity, match.IDCourse))
        except Exception as e:
            # Rollback modifications made to the database
            con.rollback()
            curse.close()
            con.close()
            raise 1
    
    # Close connection
    con.commit()
    curse.close()
    con.close()

    return 0