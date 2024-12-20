import ast
import re

from langchain.output_parsers import PydanticOutputParser
from langchain.schema.runnable.base import Runnable
from langchain_community.utilities.sql_database import SQLDatabase
from pydantic import BaseModel

from company_name.chatbot.chains.base import PromptTemplate, generate_prompt_templates


class OrderInformation(BaseModel):
    product_name: str
    quantity: int


class Chain1(Runnable):
    def __init__(self, llm, db_path, memory=False):
        super().__init__()

        self.llm = llm

        self.db = SQLDatabase.from_uri(f"sqlite:///{db_path}")
        self.products_list = self.query_as_list("SELECT Name FROM products")

        prompt_template = PromptTemplate(
            system_template=""" 
            You are a part of the e-commerce team. 
            Your task is to identify the product name and quantity from the user input.

            Here is the list of available products:
            {products_list}

            Here is the user input:
            {customer_input}

            {format_instructions}
            """,
            human_template="Customer Query: {customer_input}",
        )

        self.prompt = generate_prompt_templates(prompt_template, memory=memory)
        self.output_parser = PydanticOutputParser(pydantic_object=OrderInformation)
        self.format_instructions = self.output_parser.get_format_instructions()

        self.chain = self.prompt | self.llm | self.output_parser

    def query_as_list(self, query):
        res = self.db.run(query)
        res = [el for sub in ast.literal_eval(res) for el in sub if el]
        res = [re.sub(r"\b\d+\b", "", string).strip() for string in res]
        return list(set(res))

    def invoke(self, inputs):
        return self.chain.invoke(
            {
                "customer_input": inputs["customer_input"],
                "products_list": self.products_list,
                "format_instructions": self.format_instructions,
            },
        )
