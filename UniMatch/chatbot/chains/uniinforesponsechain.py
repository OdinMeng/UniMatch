from langchain.schema.runnable.base import Runnable
from UniMatch.chatbot.chains.base import PromptTemplate, generate_prompt_templates

class UniInfoResponseChain(Runnable):
    def __init__(self, llm):
        super().__init__()
        self.llm = llm

        negative_answer_prompt = PromptTemplate(system_template='You are a chatbot whose query returned no results. Comunicate such answer to the user, encouraing them to try more specific requests or generalizing it. You can use the user prompt and the chat history to personalize the answer.',
                                                human_template='User prompt: {customer_message}')
        self.negative_answer = generate_prompt_templates(negative_answer_prompt, memory=True)

        
        positive_answer_prompt = PromptTemplate(system_template='''
                                    You are a friendly chatbot who has to describe a university, or a course, to an user.
                                    The item to describe is as follows:
                                                
                                    {to_describe}

                                    You should make the answer as personalized as possible. To do it, you can use the chat history and the information about the user:

                                    User Information
                                    {user_info}
                                                
                                    At the end, encourage the user to search the websites for himself and then provide it to the chatbot to analyize, if they wish to look into it further.
                                                
                                    Avoid markdown formatting. You can write up to four short paragraphs maximum.
        ''', human_template='User Prompt: {customer_message}')
        self.positive_answer = generate_prompt_templates(positive_answer_prompt, memory=True)

        self.negative_chain = self.negative_answer | self.llm
        self.positive_chain = self.positive_answer | self.llm

    def invoke(self, message):
        if message['to_describe'] in ["None", None]:
            return self.negative_chain.invoke({'customer_message': message['customer_input'], 'chat_history': message['chat_history']})
        else:
            return self.positive_chain.invoke({'to_describe': message['to_describe'], 'user_info': message['user_info'], 'customer_message': message['customer_input'], 'chat_history': message['chat_history']})