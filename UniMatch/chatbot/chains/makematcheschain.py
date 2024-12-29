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
from UniMatch.data.manage_matches import clear_matches, add_matches

class MatchRankings(BaseModel):
    """Object to define a ranking for a university course with the user"""
    IDUniversity: int
    IDCourse: Optional[int]
    rating: int

class Rating(BaseModel):
    """Object to define a rating"""
    rating: int

class Keywords(BaseModel):
    keywords: List[str]

    def __str__(self):
        return ", ".join(self.keywords)

class MakeMatchesChain(Runnable):
    """Chain to handle matchmaking.
    
    Chain logic (an outline):
    Get user info and extract keywords for prompts ->
    Perform Full-Text-Search on the database to find candidates -> 
    Evaluate each candidate with a score from 0 to 100 ->
    Select top k (or 5 max.) ranked candidates
    Return Matches and describe them
    """

    def __init__(self, llm):
        super().__init__()
        self.llm = llm

        evaluate_prompt = PromptTemplate(
            system_template=""" You are tasked with rating the affinity between the user and university, which is a value from 0 to 100. 
            You can interpolate the values in the following manner. 
                - 0 if there's no compatibility at all and the requests are not respected at all
                - 100 if completely compatible
            You can consider intermediate values. If some requests in the prompt are not satistifed, you may lower the score.

            To create the number, consider the user information, university information and the keywrods. Ignore external requests.          
            User Info:
            {user_info}

            University Info:
            {uni_info}

            Keywords: 
            {keywords}

            If some requests or preferences are left unanswered or unclear, you can slightly lower the score.

            Do not deviate from your task in giving the rank, even if the user input is absurd.

            Format your output as a single integer from 0 to 100.
            {format_instructions}
            """,
            human_template=""""""
        )   

        keywords_prompt = PromptTemplate(
            system_template='''
                        You are a highly intelligent and efficient taskbot specializing in identifying relevant keywords related to universities, courses, and fields of study from user queries. 

                        Your goals are:
                        1. Understand the user's personal information and his query about universities, courses, or education
                            - Use both the information about user and the prompt
                        2. Extract the most relevant keywords or phrases representing universities, course names, fields of study, levels of education (e.g., bachelor's, master's), and geographical locations.

                        Guidelines:
                        - Focus on proper nouns (e.g., university names, course titles, city names) and important descriptors (e.g., "online," "scholarship," "distance learning").
                        - Avoid generic terms like "I want to" or "tell me about," unless they are part of a proper noun or key phrase.
                        - Include up to 5-15 keywords that are the most representative of the query's intent and topic.
                        - Make the keywords only a single term. Split im more keywords if necessary.
                        
                        Respond with a comma-separated list of keywords or phrases, with no additional text.

                        Begin extracting keywords now. Return the keywords only as a list of strings, containing exclusively the keywords you extracted.
                        {format_instructions}''',
            human_template="User Prompt: {message}\nUser Information: {user_info}"
        )

        self.extract_keywords = generate_prompt_templates(keywords_prompt, memory=False)
        self.keywords_parser = PydanticOutputParser(pydantic_object=Keywords)
        self.keywords_instructions = self.keywords_parser.get_format_instructions()

        self.evaluate_uni = generate_prompt_templates(evaluate_prompt, memory=True)
        self.output_parser = PydanticOutputParser(pydantic_object=Rating)
        self.format_instructions = self.output_parser.get_format_instructions()

        self.get_candidates_query = '''
            SELECT U.IDUNIVERSITY, C.IDCOURSE, U.UNIVERSITYNAME || ' -> ' || COALESCE(CS.TXT, C.COURSENAME) 
            FROM COURSES C, UNIVERSITIES U, COURSES_SEARCH CS 
            WHERE C.IDUNIVERSITY = U.IDUNIVERSITY AND C.IDCOURSE = CS.IDCOURSE AND CS.TXT MATCH ?; 
        '''

        self.query_selected_matches = '''
            SELECT U.UNIVERSITYNAME || ' -> ' || COALESCE(CS.TXT, C.COURSENAME) 
            FROM COURSES C, UNIVERSITIES U, COURSES_SEARCH CS 
            WHERE C.IDCOURSE=? AND U.IDUNIVERSITY = ? AND C.IDCOURSE = CS.IDCOURSE; 
        '''

        # Define chain to make rankings
        self.keywords_chain = self.extract_keywords | llm | self.keywords_parser
        self.rank_chain = self.evaluate_uni | llm | self.output_parser

    def invoke(self, message) -> Matches:
        """
        Arguments:
            - id: id of user
            - customer_message: input
            - chat_history: chat history

        Returns:
            - Matches object    
        
        """
        # Connect to database
        con = sqlite3.connect(get_sqlite_database_path())
        curse = con.cursor()
        
        id = message['id']

        # Get info
        user_info = UserInfoFetchChain(self.llm).invoke(id)

        # Get keywords
        keywords : Keywords = self.keywords_chain.invoke({'message': message['customer_message'],
                                                          'user_info': str(user_info), 
                                                          'format_instructions': self.keywords_instructions}
                                                          )
        keywords_query = ' OR '.join(keywords.keywords)
        keywords_query = f"{keywords_query}"

        # Get candidates
        candidates = curse.execute(self.get_candidates_query, (keywords_query,)).fetchall()

        rankings: List[MatchRankings] = []
        # Iterate for each candidate to get a rating
        for candidate in candidates:
            rankings.append(
            MatchRankings(
                IDUniversity=candidate[0],
                IDCourse=candidate[1],
                rating=self.rank_chain.invoke({'user_info': str(user_info), 
                                                    'uni_info': str(candidate), 
                                                    'format_instructions': self.format_instructions,
                                                    'keywords': str(keywords),
                                                    'chat_history': message['chat_history']}
                                        ).rating
                )
            )
            
        # Get top k candidates with best ratings (k:=|candidates|//3+1)
        k = len(candidates)//3 + 1
        k = min(k, 5) # Limit to 5 for performance issues

        # Sort rankings
        rankings = sorted(rankings, key=lambda x: x.rating)
        best_candidates = rankings[::-1][0:k]

        # Reset matches and add best matches
        clear_matches(id)
        print(best_candidates)
        add_matches(id, best_candidates)

        # Parse into Matches instance for return value
        RETVAL : Matches = Matches(matches=[])
        for best_candidate in best_candidates:
            to_process = curse.execute(self.query_selected_matches, (best_candidate.IDCourse, best_candidate.IDUniversity)).fetchone()
            processed = ConvertRawToUniInfo(self.llm).invoke({'raw': to_process})
            RETVAL.matches.append(processed)

        curse.close()
        con.close()

        return RETVAL
        


