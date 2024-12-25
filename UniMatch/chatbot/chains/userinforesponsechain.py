from langchain.schema.runnable.base import Runnable

from UniMatch.chatbot.chains.base import PromptTemplate, generate_prompt_templates

class UserInfoResponseChain(Runnable):
    def __init__(self, llm):
        super().__init__()
        self.llm = llm

        prompt = PromptTemplate(
            system_template='''
            You are a friendly chatbot tasked with describing a user and his personal information, given his details in the human prompt.
            You may personalize your answer with the user prompt.
            
            User prompt:
            {customer_message}
            ''',
            human_template='User Info: {user_info}'
        )

        self.prompt = generate_prompt_templates(prompt, memory=False)
        self.chain = self.prompt | self.llm

    def invoke(self, customer_message):
        """
        ARGUMENTS:
            - customer_message: User prompt
            - user_info: UserInfo object
        """
        return self.invoke({'customer_message': customer_message['customer_message'], 'user_info': customer_message['user_info']})

        