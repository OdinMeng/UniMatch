from langchain.output_parsers import PydanticOutputParser
from langchain.schema.runnable.base import Runnable
from UniMatch.chatbot.chains.base import PromptTemplate, generate_prompt_templates

class ConversationChain(Runnable):
    def __init__(self, llm):
        super().__init__()

        self.llm = llm

        prompt_template = PromptTemplate(
            system_template='''
            You are a friendly Chatbot specialized in making idle chatter with users.

            Attempt to redirect the user towards making a more pertinent request, such as:
                - Asking questions about the company UniMatch
                - Asking to search for universities, scholarships, international opportunities, courses
                - Asking questions about the Chatbot, like how it works

            If the user asks a question, answer only if you have the necessary data to do so. Otherwise, say that you do not know and you are not specialized to answer those questions.
            You can use the chat history to personalize the conversation.
            ''',
            human_template="User message: {message}"
        )

        self.prompt = generate_prompt_templates(prompt_template, memory=True)

        self.chain = self.prompt | self.llm

    def invoke(self, message):
        return self.chain.invoke({'message': message['customer_input'],
                                  'chat_history': message['chat_history']})