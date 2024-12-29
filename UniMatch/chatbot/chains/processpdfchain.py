from langchain.schema.runnable.base import Runnable
from UniMatch.chatbot.chains.base import PromptTemplate, generate_prompt_templates
from UniMatch.chatbot.rag.extract_data import get_text_from_pdfs
# from UniMatch.chatbot.rag.extract_data import translate_docs      # Note: disabled as it consumes too many tokens for a single document
from UniMatch.data.loader import get_user_pdfs_folder
from UniMatch.chatbot.rag.manage_pinecone import store_documents, clear_db
from UniMatch.chatbot.rag.query_pinecone import get_context_from_pineconedb

class ProcessPDFChain(Runnable):
    """Chain to process PDF files. Technically not a real chain, but kept it like this for conceptual purposes"""

    def __init__(self, llm=None):
        super().__init__()
        self.llm = llm

    def invoke(self):
        clear_db('pdfindex')
        docs = get_text_from_pdfs(get_user_pdfs_folder())
        # t_docs = translate_docs(docs=docs) -- Removed translation as it's too expensive
        store_documents(database_name='pdfindex', docs=docs)
        return 0

class ReasoningPDFChain(Runnable):
    """Chain to handle questions about the PDF file"""

    def __init__(self, llm):
        super().__init__()
        self.llm = llm

        self.reason = PromptTemplate(
            system_template='''You are a chatbot tasked with answering a user's question about an external source of text. 
            Use the following pieces of context to answer the question given by the user message.
            
            {context}

            If you cannot get an answer from the context, just say that you don't know as you couldn't find the context, don't try to make up an answer. Attempt to redirect the user towards making more precise questions, or to rephrase their request instead.
            
            Use three sentences maximum and keep the answer as concise as possible. 

            You have access to the previous conversation history to personalize the conversation
            ''',
            human_template='''Question: {question}'''
        )

        self.question_answerer = generate_prompt_templates(self.reason, memory=True)

        self.chain2 = self.question_answerer | self.llm

    def invoke(self, message):
        ctx = get_context_from_pineconedb(database_name='pdfindex', prompt=message['customer_input'])
        
        return self.chain2.invoke({'context': ctx, 'question': message['customer_input'], 'chat_history': message['chat_history']})