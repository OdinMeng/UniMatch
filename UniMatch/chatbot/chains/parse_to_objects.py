# Prompt templates for parsing text data (or SQL queries) into chatbot objects, namely:
#   - UserInfo
#   - UniInfo
#   - Matches

# Import necessary modules and classes
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)
from pydantic import BaseModel, Field
from UniMatch.chatbot.bot_objects import UniInfo, UserInfo, Matches

# START
