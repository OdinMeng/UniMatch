from UniMatch.data.loader import get_sqlite_database_path
import sqlite3
from typing import List

def clear_matches(id):
    delete_statement = 'DELETE FROM MATCHES WHERE IDUSER=?'
    con = sqlite3.connect(get_sqlite_database_path())
    curse = con.cursor()
    try:
        curse.execute(delete_statement, (id,))
    except Exception as e:
        con.rollback()
        curse.close()
        con.close()
        raise Exception(f'InternalSQLError: {e}')
    
    con.commit()
    curse.close()
    con.close()
    return 0

def add_matches(id, raw_matches):
    insert_statement = 'INSERT INTO MATCHES (IDUSER, IDUNIVERSITY, IDCOURSE) VALUES (?,?,?)'
    con = sqlite3.connect(get_sqlite_database_path())
    curse = con.cursor()

    for match in raw_matches:
        try:  
            curse.execute(insert_statement, (id, match.IDUniversity, match.IDCourse))
        except Exception as e:
            con.rollback()
            curse.close()
            con.close()
            raise Exception(f'InternalSQLError: {e}')
    con.commit()
    curse.close()
    con.close()

    return 0