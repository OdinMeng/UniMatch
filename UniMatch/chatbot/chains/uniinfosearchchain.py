from langchain.schema.runnable.base import Runnable
import sqlite3
from UniMatch.chatbot.chains.parse_to_objects import ConvertRawToUniInfo
from UniMatch.data.loader import get_sqlite_database_path
from UniMatch.chatbot.chains.base import PromptTemplate, generate_prompt_templates

class UniInfoSearchChain(Runnable):
    """Chain to search universities given a prompt"""
    def __init__(self, llm):
        super().__init__()
        self.llm = llm

        # Keyword Finder
        prompt_1 = PromptTemplate(system_template='''
                        You are a highly intelligent and efficient taskbot specializing in identifying relevant keywords related to universities, courses, and fields of study from user queries. 

                        Your goals are:
                        1. Understand the user's query about universities, courses, or education.
                        2. Extract the most relevant keywords or phrases representing universities, course names, fields of study, levels of education (e.g., bachelor's, master's), and geographical locations.

                        Guidelines:
                        - Focus on proper nouns (e.g., university names, course titles, city names) and important descriptors (e.g., "online," "scholarship," "distance learning").
                        - Avoid generic terms like "I want to" or "tell me about," unless they are part of a proper noun or key phrase.
                        - Include up to 1-5 keywords that are the most representative of the query's intent and topic.

                        Respond with a comma-separated list of keywords or phrases, with no additional text.

                        Example 1:
                        User: "What are the best engineering programs in Canada?"
                        You: "engineering, Canada, best"

                        Example 2:
                        User: "Tell me about scholarships for studying computer science at MIT."
                        You: "scholarships, computer science, MIT"

                        Example 3:
                        Are there any Bachelor's courses in AI?
                        You: "bachelor's, course, AI"

                        Example 4:
                        User: "What are the top universities in Europe for studying psychology?"
                        You: "top, Europe, psychology"

                        Begin extracting keywords now. Return the keywords only as a string, containing exclusively the keywords you extracted.
                                  ''',
                                  human_template='Message: {message}')
        self.keywords_finder = generate_prompt_templates(prompt_1, memory=False)

        # Schema Getter
        con = sqlite3.connect(get_sqlite_database_path())
        cursor = con.cursor()
        schema_unformatted = cursor.execute("SELECT sql FROM sqlite_master WHERE type='table';").fetchall()
        self.schema = "\n".join(row[0] for row in schema_unformatted)
        cursor.close()
        con.close()

        # SQL Statement generator (queries)
        prompt_sql = PromptTemplate(system_template="""
                    You are an intelligent and a highly efficient chatbot specializing in generating SQLite queries, given some keywords representing a user's query for a university, scholarship or a course.
                    Your query must be limited to, at most, 1 result.
                    Query all of the columns given a table; however, if there are foreign keys identifiers, you should translate them to the name of the pointed entry by joining tables.
                    
                    Try to get as much information as possible from a query.

                    You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.
                    You should ONLY return the SQL statement
                                    
                    DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database. You can only make queries.
                                    
                    To start you should ALWAYS look at the tables in the database to see what you can query.
                    Do NOT skip this step.
                    Then you should query the schema of the most relevant tables.
                    
                    {schema}
                                    
                    Example 1:
                    Keywords: Course, AI, Bachelor's
                    Resulting Statement:
                    SELECT COURSES_SEARCH.TXT FROM COURSES_SEARCH WHERE COURSES_SEARCH.TXT MATCH 'AI and Bachelor' LIMIT 1;
                                    
                    Keywords 2:
                    Keywords: Pilot
                    Resulting Statement: SELECT COURSE_NAME FORM COURSES WHERE COURSE_NAME LIKE %Pilot% LIMIT 1;
                    
                    Here are some further guidelines to keep in mind while generating your SQL statement.
                        Remark: Ignore tables ending in _config, _docsize, _content, _idx, _data.
                        Remark: You can use full-text-search capabilities (e.g. MATCH keyword) ONLY for tables ending with _Search
                        Remark: Make sure that every tables selected are included in the FROM statement. Make sure that if you have selected _Search, you have also selected the one without _Search!
                                              
                    Return the result as a string containing the SQL statement.""",
                    human_template='''keywords: {keywords}''')
        self.sql_generator = generate_prompt_templates(prompt_sql, memory=False)

        # SQL Statement checker
        prompt_check_sql = PromptTemplate(system_template="""You are highly intelligent and precise system specializing in checking the syntactical correctness of a SQLite3 query, supporting Full-Text-Search (FTS4) only on tables ending with _search. 
                                        If there is something wrong, correct the errors; 
                                        Otherwise, do not do anything and return the original query as a string, without quotating marks or any modification. 
                                          
                                        Make sure that the query follows the following guidelines:
                                            - Every table selected must exist in the FROM statement
                                            - If using Full-Text-Search capabilities, MAKE SURE THAT THE TABLES USED END in _Search!!!
                                            - Make sure the tables exist!
                                          
                                        To check the correctness, you can help yourself with the following schema:

                                          {schema}  

                                          Return the result as a string containing exclusively the SQL statement""",
                                          human_template='query: {query}')
        
        self.sql_checker = generate_prompt_templates(prompt_check_sql, memory=False)

        # Define necessary chains
        self.initial_chain = self.keywords_finder | self.llm
        self.sql_gen_chain = self.sql_generator | self.llm
        self.check_sql_chain = self.sql_checker | self.llm

    def invoke(self, message):
        # Get keywords from the message
        keywords = self.initial_chain.invoke({'message': message['customer_input']}).content

        # Generte SQLite query
        query = self.sql_gen_chain.invoke({'schema': self.schema, 'keywords': keywords}).content
        
        # Check SQLite query
        query_checked = self.check_sql_chain.invoke({'schema': self.schema, 'query': query}).content

        # Execute query
        con = sqlite3.connect(get_sqlite_database_path())
        cursor = con.cursor()
        try:
            result = cursor.execute(query_checked).fetchall()
        except Exception as e:
            cursor.close()
            con.close()
            raise Exception('Internal server error. Please retry.')

        cursor.close()
        con.close()

        # Return UniInfo instance converted to string
        if result == []:
            return None
        else:
            return ConvertRawToUniInfo(self.llm).invoke({'raw': str(result)})

        