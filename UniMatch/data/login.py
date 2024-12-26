# This file defines the functions to interact with the database, for login functionalities

from UniMatch.data import loader
import sqlite3

def validate_login(username, password):
    """
    Processes a login attempt. Variables are self-explanatory.
    Output:
        If the login attempt is valid, returns the user ID (any integer >1)
        If the login attempt is invalid, returns -1
        If an internal error occurred (which could be potentially caused by a SQL injection attempt), returns -2
    """
    conn = sqlite3.connect(loader.get_sqlite_database_path())
    curse = conn.cursor()
    try:
        result = curse.execute(f'SELECT * FROM Users WHERE Username=? AND Password=?', (username, password))
    except Exception as e:
        return -2
    info = (result.fetchone())
    curse.close()
    conn.close()

    if info == None:
        return -1
    
    elif len(info) > 1:
        return info[0]
    
def handle_login(result):
    """
    Parses login result into a string.
    """
    if result == -1:
        return 'Invalid username or password'
    elif result == -2:
        return 'Internal error occurred; if this was caused by an attempt of SQL injection, please refrain from doing that again'
    elif result > 0:
        return 'Login successful'