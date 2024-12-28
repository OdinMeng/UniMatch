from langchain.schema.runnable.base import Runnable
from UniMatch.chatbot.chains.base import PromptTemplate, generate_prompt_templates

class HandleErrorChain(Runnable):
    def __init__(self, llm):
        self.llm = llm

        prompt = PromptTemplate(
            system_template="""
        You are a friendly chatbot assistant. A user's request resulted in an error, and you have to communicate such result.

        Use the exception, chat history and the original prompt to personalize your answer. If possible, hide the fact that there was an error.
        """,
            human_template='User Prompt: {user_prompt} \nException: {exception}'
        )

        self.prompt = generate_prompt_templates(prompt, memory=True)
        self.chain = self.prompt | self.llm

    def invoke(self, user_payload):
        """ARGS:
            - user_prompt
            - chat_history
            - exception
        """
        return self.chain.invoke({'user_prompt': user_payload['user_prompt'],
                           'chat_history': user_payload['chat_history'],
                           'exception': user_payload['exception']})