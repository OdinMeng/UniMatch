from langchain import callbacks
from langchain.output_parsers import PydanticOutputParser
from langchain.schema.runnable.base import Runnable
import sqlite3

from pydantic import BaseModel, Field
from UniMatch.chatbot.bot_objects import UniInfo
from dotenv import load_dotenv
from UniMatch.chatbot.chains.parse_to_objects import ConvertRawToUserInfo
from UniMatch.data.loader import get_sqlite_database_path

from langchain_community.vectorstores import SQLiteVec
from UniMatch.chatbot.chains.base import PromptTemplate, generate_prompt_templates

class UniInfoSearchChain(Runnable):
    def __init__(self, llm):
        super().__init__()
        self.llm = llm

        # Step 1: Find keywords
        prompt_1 = ()
        self.keywords_finder = None

        # Step 2: Connect to SQL database and get SQL schema

        # Step 3: Generate SQL statement, using either basic SQL queries (for number-based searches) or full-text-search.

        # Step 4: Verify correctness of SQL statement

        # Step 5: Run SQL statement

        # Step 6: Report results. If empty tuple, return None which flags the bot to generate a rejection message; otherwise allow for it to pass to reasoning chain
        