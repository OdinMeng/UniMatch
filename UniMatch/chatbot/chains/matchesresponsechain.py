from langchain.schema.runnable.base import Runnable
from UniMatch.chatbot.chains.base import PromptTemplate, generate_prompt_templates
from UniMatch.chatbot.chains.userinfofetchchain import UserInfoFetchChain

class MatchesResponseChain(Runnable):
    def __init__(self, llm):
        self.llm = llm

        prompt = PromptTemplate(system_template='''
        You are a friendly chatbot whose job is to describe a series of university (and courses) matches to a user, given as the human message.
        You should personalize your answer as much as possible, explaining possible reasons you picked a certain university to be reccomended for him.
        Be as honest as possible with your explaination, do not omit any important details.
        Make short sentences, without sacrificing important details.
                                
        You have access to chat history, user information, user prompt to personalize your answer.
        
        Do NOT include any information not mentioned in the matches.        
                                               
        User Information:
        {user_info}
        
        Matches:
        {matches}
                                
        =========================== READ BELOW FOR FORMATTING! ===================================
                                
        You must structure your answer as follows:
        < Introductory phase, where you say that you are going to enumerate every university reccomendation >
        < Enumerated list >
            < Match Number 1: University and Course Name>
                < Insert Course/University Description >
                < Insert explaination for this match, possible alignments and misalignments >
            ... continue until you finished all of the matches
        < End enumerated list >
        < Conclusion phrase: if the user has any further questions, they can either ask the chatbot or look for further documents to upload into the chatbot >
        
        ''',
        human_template='User Prompt: \n {matches}')
        self.prompt = generate_prompt_templates(prompt, memory=True)

        self.chain = self.prompt | self.llm

    def invoke(self, message):
        """
        TO INCLUDE:
            - chat_history: Chat history
            - user_message: User prompt
            - matches: Matches of user (already extracted or generated)
            - id: User ID
        """

        user_info = UserInfoFetchChain(self.llm).invoke(message['id'])

        return self.chain.invoke({
            'chat_history': message['chat_history'],
            'user_message': message['user_message'],
            'matches': message['matches'],
            'user_info': user_info
        })
        