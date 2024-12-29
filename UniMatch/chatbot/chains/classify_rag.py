from langchain.schema.runnable.base import Runnable
from UniMatch.chatbot.chains.base import PromptTemplate, generate_prompt_templates

class ClassifyRAG(Runnable):
    """Chain to classify questions for the RAG-related intentions."""
    def __init__(self, llm):
        super().__init__()

        self.llm = llm

        prompt_template = PromptTemplate(
            system_template='''
            A user has uploaded a PDF file or a link to a website to the database, and he has some questions about it.

            Determine if the prompt contains questions about the PDF or to the link.
                - If it's a PDF, return PDF
                - If it's a website link, return link
                - If it's none of either, return None
            ''',
            human_template="User message: {message}"
        )

        self.prompt = generate_prompt_templates(prompt_template, memory=False)

        self.chain = self.prompt | self.llm

    def invoke(self, message):
        return self.chain.invoke({'message': message['customer_input']})