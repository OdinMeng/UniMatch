# Manage User's information: extract, modify, remove or add. 

from UniMatch.data.loader import get_sqlite_database_path
import sqlite3
from UniMatch.chatbot.bot_objects import Preferences
from typing import Dict, List, Union

def extract_user_preferences(userid: int) -> Preferences:
    """ Given an User ID, extract his preferences.
    
    Output type is a Preferences object, containing two lists: one for preferences, one for weights.
        - i-th weight is associated to the i-th preference
    
    Note: this is to be processed by the chatbot to be transformed into an UniInfo instance
    """
    # Connect to DB
    conn = sqlite3.connect(get_sqlite_database_path())
    curse = conn.cursor()

    # Query UserID
    query = curse.execute('SELECT * FROM USERPREFERENCES WHERE USERID=?', (userid,))
    obj = query.fetchall()

    # Exit from DB
    curse.close()
    conn.close()

    # Parse object into a dictionary
    RETVAL = {
        "preferences": [],
        "weights": []
    }

    for item in obj:
        RETVAL['preferences'].append(item[2])
        RETVAL['weights'].append(item[3])

    # Transform into Preferences data type
    RETVAL = Preferences(preferences=RETVAL['preferences'], weights= RETVAL['weights'])

    return RETVAL

def modify_user_preferences(userid: int, new_preferences: Union[Preferences, Dict[str, List]]) -> int:
    """ Given a data type containing the user preferences, updates the UserPreferences accordingly.
    This function accepts both Preference datatype and dictionaries containing two lists. In case of a dictionary, it must be structured in the following way:
    { 'preferences' : [...], 'weights': [...] }

    This function will preliminaliry check whether the given input is valid or less.

    Return values:
        0: successful
        1: failed (invalid input structure)
        2: failed (invalid weights)
        3: failed (internal SQL error)
    """
    ## Preliminary checks

    # Convert to Preferences datatype if needed
    if not isinstance(new_preferences, Preferences):
        try:
            new_preferences = Preferences(preferences=new_preferences['preferences'], weights=new_preferences['weights'])
        except:
            return 1

    # Structure
    try:
        new_preferences.preferences
        weights = new_preferences.weights
    except Exception:
        return 1
    
    if len(new_preferences.preferences) != len(new_preferences.weights): # Lists must be equally-sized
        return 1
    
    # Weight
    s=0
    for weight in weights:
        if not isinstance(weight, int):
            return 2
        s += weight
    if s != 100:
        return 2

    ## Connect to database
    conn = sqlite3.connect(get_sqlite_database_path())
    curse = conn.cursor()

    # Execute SQL queries to clear user preferences
    try:
        curse.execute('DELETE FROM UserPreferences WHERE UserID = ?', (userid,))
    except Exception as e:
        conn.rollback()
        curse.close()
        conn.close()
        return 3

    # Execute SQL queries to insert new preferences
    for i in range(len(new_preferences.preferences)):
        try:
            payload = (userid, new_preferences.preferences[i], new_preferences.weights[i]) # Define payload for new row
            curse.execute('INSERT INTO UserPreferences(UserID, Preferences, Weight) VALUES (?,?,?)', payload)
        except Exception as e:
            conn.rollback()
            curse.close()
            conn.close()
            return 3

    # Commit and close
    conn.commit()
    curse.close()
    conn.close()

    return 0

def modify_user_info(userid: int, column: str, new_info: Union[str, int]) -> int:
    """ Modify an information (column) about an user.
    Arguments:
        - userid: ID of the user
        - column: the information type to modify, for a list of accepted columns see below
        - new_info: the new piece of information to replace

    Modifiable columns (accepted values for the column argument):
        - username
        - age
        - countrycode
        - educationlevel
        - mainarea

    Returns 0 if operation successful, -1 otherwise.
    """
    conn = sqlite3.connect(get_sqlite_database_path())
    curse = conn.cursor()

    # Preprocess input
    column_input = column.lower()
    
    # Handle each column case by case

    # Username
    if column_input == 'username':
        res = curse.execute('SELECT Username FROM USERS WHERE Username = ?;', (new_info,))
        
        # Foreign key integrity and username mustn't be null
        if len(res.fetchall()) > 0 or new_info in [None, '']:
            conn.rollback()
            curse.close()
            conn.close()
            return -1
        
        try:
            curse.execute('UPDATE USERS SET Username=? WHERE IDUser=?', (new_info, userid))
        except:
            conn.rollback()
            curse.close()
            conn.close()
            return -1
        else:
            conn.commit()
            curse.close()
            conn.close()
            return 0

    # Age
    elif column_input == 'age':
        if not isinstance(new_info, int):
            return -1
        
        try:
            curse.execute('UPDATE USERS SET Age=? WHERE IDUser=?', (new_info, userid))
        except:
            conn.rollback()
            curse.close()
            conn.close()
            return -1
        else:
            conn.commit()
            curse.close()
            conn.close()
            return 0

    # Country
    elif column_input == 'countrycode':
        try:
            curse.execute('UPDATE USERS SET CountryCode=? WHERE IDUser=?', (new_info, userid))
        except:
            conn.rollback()
            curse.close()
            conn.close()
            return -1
        else:
            conn.commit()
            curse.close()
            conn.close()
            return 0

    # Education Level
    elif column_input == 'educationlevel':
        # Flag to allow empty new value
        flag = 0        
        if new_info == None:
            flag = 1

        # Check for vali value
        if new_info not in ["High School", "Bachelor's Degree", "Master's Degree", "PhD"] and not flag:
            return -1
        
        # Execute
        try:
            curse.execute('UPDATE USERS SET EducationLevel=? WHERE IDUser=?', (new_info, userid))
        except:
            conn.rollback()
            curse.close()
            conn.close()
            return -1
        else:
            conn.commit()
            curse.close()
            conn.close()
            return 0

    # Main Area
    elif column_input == 'mainarea':
        # Convert to None if necessary
        if new_info in ["", "None", "No Area", "Empty"]:
            new_info = None

        if isinstance(new_info, str):
            # Parse new_info into a code if it's a string
            code = curse.execute('SELECT IDAREA FROM AREAS WHERE AREANAME LIKE ?', (f"%{new_info}%",)).fetchone()
            
            if code is None:
                return -1

            else:
                new_info = code[0] # Replace new value

        res = curse.execute('SELECT IDArea FROM AREAS WHERE IDArea=?', (new_info,))

        # Accepts for empty entries
        flag = 0        
        if new_info is None:
            flag = 1

        # Foreign key integrity
        if len(res.fetchall()) == 0 and not flag:
            conn.rollback()
            curse.close()
            conn.close()
            return -1
        
        try:
            # Execution Attempt
            curse.execute('UPDATE USERS SET MainArea=? WHERE IDUser=?', (new_info, userid))
        except:
            conn.rollback()
            curse.close()
            conn.close()
            return -1
        else:
            conn.commit()
            curse.close()
            conn.close()
            return 0

    else: # Invalid column
        return -1


def modify_user_password(userid, old_password, new_password):
    """ Modify a user's password. 
    old_password must match with the current password, as a safety measure.
    new_password will be the new password.
    
    Returns 0 if successful. If not, returns -1 if old_password mismatches or returns -2 if there is an internal error.
    """

    conn = sqlite3.connect(get_sqlite_database_path())
    curse = conn.cursor()

    r = curse.execute('SELECT password FROM USERS WHERE IDUser=?', (userid,))
    current_pwd = r.fetchone()[0]

    if old_password != current_pwd:
        conn.rollback()
        curse.close()
        conn.close()
        return -1
    
    else:
        try:
            curse.execute('UPDATE USERS SET password=? WHERE IDUser=?', (new_password, userid))
        except:
            conn.rollback()
            curse.close()
            conn.close()
            return -2
        else:
            conn.commit()
            curse.close()
            conn.close()
            return 0