# Prompt templates for parsing text data (or SQL queries) into chatbot objects, namely:
#   - UserInfo
#   - UniInfo
#   - Preferences

# Import necessary modules and classes
from langchain.output_parsers import PydanticOutputParser
from langchain.schema.runnable.base import Runnable

from UniMatch.chatbot.bot_objects import UniInfo, UserInfo, Preferences
from langchain.output_parsers import PydanticOutputParser

from UniMatch.chatbot.chains.base import PromptTemplate, generate_prompt_templates

class ConvertRawToUniInfo(Runnable):
    """Convert a raw message (either a SQL query or text) to a UniInfo instance"""

    def __init__(self, llm):
        super().__init__()
        self.llm = llm

        prompt_template = PromptTemplate(system_template='''You are tasked with extracting information about a university or a course from a raw source of data, given in the last row. It can be either tuples representing a query result, or it can be raw text.
        You have to extract the following informations and attempt to structure it in JSON, which can be parsed later:
            - name: Name of University
            - location: Location
            - courses: Courses, as a list
            - course_descriptions: Descriptions of each course, as a list.
            - subjects: Subjects, associated to a course as a dictionary 
            - scholarships: Scholarships associated to each course, as a dictionary
            - requisites: Requisites associated to each course or scholarship, as a dictionary
            - areas: Thematic Areas of Study, as a list
        If you cannot extract something, just place the missing field as empty. Return only and exclusively the JSON structure, without backticks or external text.
                                         
        {format_instructions}''',
        human_template='''Raw source to extract from:{raw}''')

        self.prompt = generate_prompt_templates(prompt_template=prompt_template, memory=False)
        self.output_parser = PydanticOutputParser(pydantic_object=UniInfo)
        self.format_instructions = self.output_parser.get_format_instructions()

        self.chain = self.prompt | self.llm | self.output_parser

    def invoke(self, raw):
        return self.chain.invoke({'raw': raw, 'format_instructions': self.format_instructions})


class ConvertRawToUserInfo(Runnable):
    """Convert a raw message (either a SQL query or text) to a UserInfo instance"""

    def __init__(self, llm):
        super().__init__()
        self.llm = llm

        prompt_template = PromptTemplate(system_template='''You are tasked with extracting information about a user of an application.
        You have to extract the following informations:
            - name: Name of the user
            - age: Age of the user
            - country: Country of the user
            - education_level: the user's current education level. 
            - preferences: Preferences of the user, represented as a dictionary with string associated to a number (its weight).
            - main_area: Main thematic academic area of the user, as a string
        If you cannot extract something, just omit it.

        Please follow this formatting instructions:
        {format_instructions}''',
        human_template='''Raw source to extract from: {raw} ''')

        self.prompt = generate_prompt_templates(prompt_template=prompt_template, memory=False)
        self.output_parser = PydanticOutputParser(pydantic_object=UserInfo)
        self.format_instructions = self.output_parser.get_format_instructions()

        self.chain = self.prompt | self.llm | self.output_parser

    def invoke(self, raw):
        return self.chain.invoke({'raw': raw, 'format_instructions': self.format_instructions})

class ConvertRawToPreferences(Runnable):
    """Convert raw message to user preferences."""

    def __init__(self, llm):
        super().__init__()
        self.llm = llm

        prompt_template = PromptTemplate(system_template='''You are tasked with extracting the preferences of an user.
        You have to extract a preference and associate it to a weight. Structure it as a dictionary containing two lists, namely:
            - preferences: strings describing a preference. It should be a short phrase in first person.
            - weights: a number associated to the preference. make sure weights sum up to 100
                                         
        Please format your output with the following instructions:
        {format_instructions}''',
        human_template='''Text source to extract from:{raw}''')

        prompt_template_2 = PromptTemplate(system_template='''You are tasked with reading a list of preferences and weights and you have to verify that the weights sum up to 100.
        If they do not sum to 100, modify them in a way the sum to 100.
                                           
        Please format your output with the following instructions:
        {format_instructions}
        - preferences: strings describing a preference
        - weights: a number associated to the preference. make sure weights sum up to 100''',
        human_template='''To verify:{weights}''')

        # Define prompts
        self.prompt_makepreferences = generate_prompt_templates(prompt_template=prompt_template, memory=False)
        self.prompt_checkweights = generate_prompt_templates(prompt_template=prompt_template_2, memory=False)
        self.output_parser = PydanticOutputParser(pydantic_object=Preferences)
        self.format_instructions = self.output_parser.get_format_instructions()

        # Two chains: one to extract user preferences, another to check the weights.
        self.chain1 = self.prompt_makepreferences | self.llm | self.output_parser
        self.chain2 = self.prompt_checkweights | self.llm | self.output_parser

    def invoke(self, raw):
        partial = self.chain1.invoke({'raw': raw, 'format_instructions':self.format_instructions})
        return self.chain2.invoke({'weights': partial, 'format_instructions': self.format_instructions})