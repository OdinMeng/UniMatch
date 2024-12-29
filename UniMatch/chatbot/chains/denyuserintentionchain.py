from langchain.schema.runnable.base import Runnable
from UniMatch.chatbot.chains.base import PromptTemplate, generate_prompt_templates

class DenyUserIntentionChain(Runnable):
    """Chain to handle denied user intentions (for guest mode)."""
    def __init__(self, llm):
        self.llm = llm

        prompt = PromptTemplate(
            system_template="""
        You are a friendly chatbot assistant. You have to deny the user a feature he is trying to use, as he is in guest mode and thus has only access to limited features.

        Be polite and attempt to convince the user to register or login to UniMatch.

        You have access to chat history and the user's prompt to personalize your answer.
        """,
            human_template='User Prompt: {user_prompt}'
        )
        self.prompt = generate_prompt_templates(prompt, memory=True)
        self.chain = self.prompt | self.llm

    def invoke(self, user_payload):
        """Arguments:
            - user_prompt: user prompt
            - chat_history
        """
        return self.chain.invoke({'user_prompt': user_payload['user_prompt'],
                           'chat_history': user_payload['chat_history']})