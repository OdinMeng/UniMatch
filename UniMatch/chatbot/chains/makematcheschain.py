from langchain.schema.runnable.base import Runnable
from UniMatch.chatbot.chains.base import PromptTemplate, generate_prompt_templates
from pydantic import BaseModel
from typing import Optional, List
from langchain.output_parsers import PydanticOutputParser
import sqlite3
from UniMatch.data.loader import get_sqlite_database_path
from UniMatch.chatbot.chains.userinfofetchchain import UserInfoFetchChain
from UniMatch.chatbot.chains.parse_to_objects import ConvertRawToUniInfo
from UniMatch.chatbot.bot_objects import Matches

class MatchRankings(BaseModel):
    IDUniversity: int
    IDCourse: Optional[int]
    rating: int

class Rating(BaseModel):
    rating: int

class MakeMatchesChain(Runnable):
    def __init__(self, llm):
        super().__init__()
        self.llm = llm

        evaluate_prompt = PromptTemplate(
            system_template="""You are a highly intelligent chatbot tasked with associating an affinity score to an user for each university and course. 
            To do it, you must consider the chat history, the user's informations (in particular his preferences) and the prompt.

            User Info:
            {user_info}

            Description:
            {uni_info}
            
            Return the result as a tuple containing the following numbers: (IDUniversity, IDCourse, rating). The rating must belong in the range [0, 100].
                - 0 if there's no compatibility at all
                - 100 if completely compatible
            If some requests or preferences are left unanswered or unclear, you can lower slightly the score.

            Format the output as the following:
                - Ranking: the number you assigned

            Format instructions: {format_instructions}
            """,
            human_template="""User Prompt: {customer_message}"""
        )   

        self.evaluate_uni = generate_prompt_templates(evaluate_prompt, memory=True)
        self.output_parser = PydanticOutputParser(pydantic_object=Rating)
        self.format_instructions = self.output_parser.get_format_instructions()

        self.get_mainarea_query = 'SELECT MAINAREA FROM USERS WHERE IDUSER = ?'

        self.get_candidates_query = '''
            SELECT U.IDUNIVERSITY, C.IDCOURSE, U.UNIVERSITYNAME || ' -> ' || COALESCE(CS.TXT, C.COURSENAME) 
            FROM COURSES C, UNIVERSITIES U, COURSES_SEARCH CS 
            WHERE C.AREA = ? AND C.IDUNIVERSITY = U.IDUNIVERSITY AND C.IDCOURSE = CS.IDCOURSE; 
        '''

        self.query_selected_matches = '''
            SELECT U.UNIVERSITYNAME || ' -> ' || COALESCE(CS.TXT, C.COURSENAME) 
            FROM COURSES C, UNIVERSITIES U, COURSES_SEARCH CS 
            WHERE C.IDCOURSE=? AND U.IDUNIVERSITY = ? AND C.IDCOURSE = CS.IDCOURSE; 
        '''

        self.rank_chain = self.evaluate_uni | llm | self.output_parser

    def invoke(self, message):
        """
        TO INCLUDE:
            - id: id of user
            - customer_message: input
            - chat_history: chat history    
        """
        con = sqlite3.connect(get_sqlite_database_path())
        curse = con.cursor()
        
        id = message['id']

        # Get info
        user_info = UserInfoFetchChain(self.llm).invoke(id)
        mainarea = curse.execute(self.get_mainarea_query, (id,)).fetchone()[0]

        # Case where user did not indicate a preferred area (it impedes to avoid excessive token usage)
        if not(isinstance(mainarea, int)):
            return None
        
        rankings: List[MatchRankings] = []

        # Get candidates
        candidates = curse.execute(self.get_candidates_query, (mainarea,)).fetchall()
        for candidate in candidates:
            rankings.append(
            MatchRankings(
                IDUniversity=candidate[0],
                IDCourse=candidate[1],
                rating=self.rank_chain.invoke({'user_info': str(user_info), 
                                                    'uni_info': str(candidate), 
                                                    'format_instructions': self.format_instructions,
                                                    'customer_message': message['customer_message'],
                                                    'chat_history': message['chat_history']}
                                        ).rating
                )
            )
            
        # Get top k candidates with best ratings (k:=|candidates|//3+1)
        k = len(candidates)//3 + 1
        rankings = sorted(rankings, key=lambda x: x.rating)
        best_candidates = rankings[::-1][0:k]

        # Parse into Matches instance
        RETVAL : Matches = Matches(matches=[])
        for best_candidate in best_candidates:
            to_process = curse.execute(self.query_selected_matches, (best_candidate.IDCourse, best_candidate.IDUniversity)).fetchone()
            processed = ConvertRawToUniInfo(self.llm, memory=False).invoke({'raw': to_process})
            RETVAL.matches.append(processed)

        curse.close()
        con.close()

        return RETVAL
        


