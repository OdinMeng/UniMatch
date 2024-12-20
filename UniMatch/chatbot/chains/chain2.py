from langchain.output_parsers import PydanticOutputParser
from langchain.schema.runnable.base import Runnable
from pydantic import BaseModel

from company_name.chatbot.chains.base import PromptTemplate, generate_prompt_templates


class OrderId(BaseModel):
    order_id: int


class Chain2(Runnable):
    def __init__(self, llm, memory=False):
        super().__init__()

        self.llm = llm
        prompt_template = PromptTemplate(
            system_template=""" 
            You are a part of the e-commerce team. 
            Your task is to identify the order_id from the user input.

            Here is the user input:
            {customer_input}

            {format_instructions}
            """,
            human_template="Customer Query: {customer_input}",
        )

        self.prompt = generate_prompt_templates(prompt_template, memory)
        self.output_parser = PydanticOutputParser(pydantic_object=OrderId)
        self.format_instructions = self.output_parser.get_format_instructions()

        self.chain = self.prompt | self.llm | self.output_parser

    def invoke(self, inputs):
        return self.chain.invoke(
            {
                "customer_input": inputs["customer_input"],
                "format_instructions": self.format_instructions,
            },
        )
