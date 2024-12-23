from langchain import callbacks
from langchain.output_parsers import PydanticOutputParser
from langchain.schema.runnable.base import Runnable

from pydantic import BaseModel, Field
from UniMatch.chatbot.bot_objects import UniInfo
from dotenv import load_dotenv

from UniMatch.chatbot.chains.parse_to_objects import ConvertRawToUniInfo
from UniMatch.chatbot.chains.base import PromptTemplate, generate_prompt_templates
from UniMatch.chatbot.rag.extract_data import get_text_from_link
from UniMatch.chatbot.rag.extract_data import translate_docs
from UniMatch.chatbot.rag.manage_pinecone import store_documents, clear_db
from UniMatch.chatbot.rag.query_pinecone import get_context_from_pineconedb

load_dotenv()

class ProcessWebsiteChain(Runnable):
    def __init__(self, llm, memory=False):
        super().__init__()
        self.llm = llm
        self.memory = memory

        self.find_link_prompt = PromptTemplate(
            system_template='''You are a chatbot tasked with finding hyperlinks within a message. 
            If there are no hyperlinks at all, return 0. If there are more, pick the first one you find.
            ''',
            human_template='''Message: {message}'''
        )

        self.link_finder = generate_prompt_templates(self.find_link_prompt, memory=self.memory)
        self.crawler = get_text_from_link
        self.translator = translate_docs
        self.converter = ConvertRawToUniInfo(self.llm, memory=False)

        self.chain = self.link_finder | self.llm

    def invoke(self, message):
        link = self.chain.invoke({'message': message['customer_input']})

        if link.content == '0':
            return 'No link found'
        
        try:
            docs = self.crawler(link.content)
        except Exception as e:
            print("!!! ERROR OCCURRED !!!", e)
            return -1 # Error flag
        else:
            clear_db('htmlindex')
            store_documents('htmlindex', docs)

class ReasoningWebsiteChain(Runnable):
    def __init__(self, llm, memory=False):
        super().__init__()
        self.llm = llm
        self.memory = memory

        self.reason = PromptTemplate(
            system_template='''You are a chatbot tasked with answering a user's question about an external source of text. 
            Use the following pieces of context to answer the question given by the user message.
            
            {context}

            If you cannot get an answer from the context, just say that you don't know, don't try to make up an answer. Attempt to redirect the user towards making more precise questions, or to rephrase their request instead.
            Use three sentences maximum and keep the answer as concise as possible. 
            You have access to the previous conversation history to personalize the conversation

            If there are no questions at all, say that you have successfully analyzed the document and if the user has any more questions he can do them.
            ''',
            human_template='''Question: {question}'''
        )

        self.question_answerer = generate_prompt_templates(self.reason, memory=self.memory)

        self.chain2 = self.question_answerer | self.llm

    def invoke(self, message):
        ctx = get_context_from_pineconedb(database_name='htmlindex', prompt=message['customer_input'])
        
        return self.chain2.invoke({'context': ctx, 'question': message['customer_input']})