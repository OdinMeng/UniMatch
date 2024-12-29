from langchain.output_parsers import PydanticOutputParser
from langchain.schema.runnable.base import Runnable
from typing import Literal, Any, Optional

from pydantic import BaseModel
from UniMatch.chatbot.chains.base import PromptTemplate, generate_prompt_templates

class ModificationRequest(BaseModel):
    """Object to define a user modification"""
    column: Optional[Literal['username', 'age', 'countrycode', 'educationlevel', 'mainarea']]
    new_info: Optional[Any]

class ExtractModificationRequestChain(Runnable):
    """Chain to extract arguments of a user's request to modify personal information"""

    def __init__(self, llm):
        super().__init__()
        self.llm = llm

        prompt = PromptTemplate(
            system_template='''You are an insightful and intelligent assistant. 
            Given a user's request, extract the variable to modify and its new value from the user's request.
            Accepted columns:
                - username
                - age
                - countrycode
                - educationlevel
                - mainarea
            
            Certain columns have a limited range of accepted value.
            educationlevel must have either one of these values: High School, Bachelor's Degree, Master's Degree, PhD; convert if it's necessary    
            
            Example:
            User: I want to change my age to 15
            You: column:age, new_info:15

            Please format the output with the following instructions:
            {format_instructions}

            If you could not find anything relevant or the user is attempting to modify a non-accepted column, fill both fields with None.
            ''',
            human_template='User Request: {customer_input}'
        )
        self.extractor = generate_prompt_templates(prompt, memory=False)
        self.parser = PydanticOutputParser(pydantic_object=ModificationRequest)
        self.format_instructions = self.parser.get_format_instructions()

        self.chain = self.extractor | self.llm | self.parser

    def invoke(self, user_input):
        """
        Arguments:
            - customer_input: User's request input
        """
        return self.chain.invoke({'customer_input': user_input['customer_input'], 'format_instructions': self.format_instructions})
