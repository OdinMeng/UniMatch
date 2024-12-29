from langchain.schema.runnable.base import Runnable
from UniMatch.chatbot.chains.base import PromptTemplate, generate_prompt_templates
from UniMatch.chatbot.rag.query_pinecone import get_context_from_pineconedb

class CompanyInformationChain(Runnable):
    """Chain to answer a user's question about the company UniMatch."""
    def __init__(self, llm):
        super().__init__()

        self.llm = llm

        prompt_template = PromptTemplate(
            system_template='''
            You are a friendly chatbot specialized in giving users information about the company UniMatch.

            Use the following pieces of context to answer the question given by the user message.
            
            {context}

            If you cannot get an answer from the context, just say that you don't know, don't try to make up an answer. Attempt to redirect the user towards making more precise questions, or to rephrase their request instead.
            Use three sentences maximum and keep the answer as concise as possible. 
            
            You have acess to the previous conversation history to personalize the conversation
            ''',
            human_template="User message: {question}"
        )

        self.prompt = generate_prompt_templates(prompt_template, memory=True)
        self.chain = self.prompt | self.llm

    def invoke(self, message):
        """
        Arguments:
            - question: user prompt
            - chat_history
            - context: context found by the vector database search
        """
        # Find context with vector DB
        ctx = get_context_from_pineconedb('unimatch', message['customer_input'])

        # Invoke chain
        return self.chain.invoke({'question': message['customer_input'],
                                  'chat_history': message['chat_history'],
                                  'context': ctx},
        )