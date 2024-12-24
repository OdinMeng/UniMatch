import sqlite3
from UniMatch.chatbot.bot_objects import Matches
from UniMatch.chatbot.chains.parse_to_objects import ConvertRawToUniInfo
from langchain.schema.runnable.base import Runnable
from UniMatch.data.loader import get_sqlite_database_path

class ExtractMatchesChain(Runnable):
    def __init__(self, llm):
        super().__init__()
        self.llm = llm

        self.query_selected_matches = '''
            SELECT U.UNIVERSITYNAME || ' -> ' || COALESCE(CS.TXT, C.COURSENAME) 
            FROM COURSES C, UNIVERSITIES U, COURSES_SEARCH CS 
            WHERE C.IDCOURSE=? AND U.IDUNIVERSITY = ? AND C.IDCOURSE = CS.IDCOURSE; 
        '''
        
        self.query_get_matches = '''
        SELECT IDUSER, IDUNIVERSITY, IDCOURSE FROM MATCHES WHERE IDUSER=?
        '''

    def invoke(self, message):
        """
        Required argument:
            - id: User ID
        """
        con = sqlite3.connect(get_sqlite_database_path())
        curse = con.cursor()

        id = message['id']

        matches = curse.execute(self.query_get_matches, (id,))

        RETVAL : Matches = Matches(matches=[])
        for match in matches:
            to_process = curse.execute(self.query_selected_matches, (match[2], match[1])).fetchone()
            processed = ConvertRawToUniInfo(self.llm, memory=False).invoke({'raw': to_process})
            RETVAL.matches.append(processed)

        curse.close()
        con.close()
        return RETVAL
