# This file defines the functions to interact with the database, for registration functionalities

from UniMatch.data import loader
import sqlite3

def register(username, password, educationlevel=None, age=None, countrycode=None, mainarea=None):
    """
    Attempts to register a user into the database.
        If successful, returns the new ID
        If failed, returns the following values:
            -1 if username is not unique
            -2 if password is an empty string (vulnerability issues)
            -3 if education level is invalid    
            -4 for internal SQL errors
    """
    
    # Preliminary checks
    if password == "":
        return -2
    if educationlevel not in ["High School", "Bachelor's Degree", "Master's Degree", "PhD"]:
        return -3

    # Registration attempt
    conn = sqlite3.connect(loader.get_sqlite_database_path())
    curse = conn.cursor()

    try:
        curse.execute(f'INSERT INTO USERS(Username, Age, Password, CountryCode, EducationLevel, MainArea) VALUES (?, ?, ?, ?, ?, ?)', (username, age, password, countrycode, educationlevel, mainarea))
    except sqlite3.IntegrityError:
        conn.rollback()
        curse.close()
        conn.close()
        return -1
    
    except Exception as e:
        print(e)
        conn.rollback()
        curse.close()
        conn.close()
        return -4
    
    else:
        conn.commit() # Commit transaction
        
        # Obtain newly created user's ID
        x = curse.lastrowid

        curse.close()
        conn.close()

        return x # Return user's ID

def handle_registration(result):
    """
    Parses registration attempt result code as a string, for UI/UX purposes
    """
    hashmap = {
        -1: 'Username already taken',
        -2: 'Insert a password',
        -3: 'Invalid Education Level',
        -4: 'Internal SQL Error, please retry or contact technical support'
    }
    
    if result not in hashmap and result > 0:
        return 'Registration successful'
    else:
        return hashmap[result]