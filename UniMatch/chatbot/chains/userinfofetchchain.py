from langchain import callbacks
from langchain.output_parsers import PydanticOutputParser
from langchain.schema.runnable.base import Runnable
import sqlite3

from pydantic import BaseModel, Field
from UniMatch.chatbot.bot_objects import UniInfo
from dotenv import load_dotenv
from UniMatch.chatbot.chains.parse_to_objects import ConvertRawToUserInfo
from UniMatch.data.loader import get_sqlite_database_path

class UserInfoFetchChain(Runnable):
    def __init__(self, llm):
        super().__init__()
        self.llm = llm

        self.sql_query = '''SELECT DISTINCT
                                U.USERNAME, 
                                U.AGE, 
                                C.COUNTRY, 
                                U.EDUCATIONLEVEL, 
                                UP.PREFERENCES, 
                                UP.WEIGHT,
                                CASE
                                    WHEN U.MAINAREA IS NULL THEN NULL
                                    ELSE A.AREANAME
                                END
                            FROM
                                USERS U 
                                    LEFT JOIN COUNTRIES C
                                        ON U.COUNTRYCODE = C.COUNTRY
                                    LEFT JOIN USERPREFERENCES UP
                                        ON U.IDUSER = UP.USERID
                                    LEFT JOIN AREAS A
                                        ON U.MAINAREA = A.IDAREA
                            WHERE
                                U.IDUSER = ?
'''

    def invoke(self, userid):
        conn = sqlite3.connect(get_sqlite_database_path())
        cursor = conn.cursor()

        res = cursor.execute(self.sql_query, (userid,))

        all_rows = res.fetchall()

        cursor.close()
        conn.close()

        print(all_rows)

        RETVAL = ConvertRawToUserInfo(self.llm).invoke(all_rows)

        return RETVAL
