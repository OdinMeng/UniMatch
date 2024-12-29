# Functions to load text from PDFs and website links

# Import modules
import os
from typing import List

from dotenv import load_dotenv
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents.base import Document
from langchain_community.document_loaders import RecursiveUrlLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain_openai import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

load_dotenv()

def get_text_from_pdfs(folder: str) -> List[Document]:
    """
    Given a  path containing folders, extract text from each pdf in the folder.
    """
    docs: List[Document] = []
    pdf_files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith('.pdf')]

    for pdf_file in pdf_files:
        # Initialize the PyMuPDFLoader with the given PDF file
        loader = PyMuPDFLoader(pdf_file)
            # You can use any PDF loader, PyMuPDFLoader is better as it is integrated with LangChain

        # Initialize an empty list to store the pages
        pages: List[Document] = []
            # Document class is from LangChain, contains:
                # Metadata
                # Page content

        # Iterate over each loaded page and add it to the list
        for page in loader.load():
            pages.append(page)

        docs.append(pages)

    # Return all documents
    return docs

def get_text_from_link(link: str) -> List[Document]:
    """
    Given a hyperlink referencing a website, extract text the page recursively (with depth of one).
    """
    l = []

    loader = RecursiveUrlLoader(
        url=link,
        max_depth=1, # With a higher budget this can be increased
        base_url=link,
    )
    try:
        docs: List[Document] = loader.load()
    except Exception as e:
        raise e # This should not happen
    else:
        # Transform raw html into beautifulsoup
        bs_transformer = BeautifulSoupTransformer()

        # Return the soup
        soup = bs_transformer.transform_documents(documents=docs, unwanted_tags=['a', 'script', 'style'])
        l.append(soup)

        return l
    
def translate_docs(docs: List[Document]) -> List[Document]:
    """
    Given a list of documents, translate each of them in English. This functionality ended up being dropped as it is too expensive.
    """
    # Set up retval 
    translated_docs: List[Document] = []

    # Set up translator
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

    system_message_template = SystemMessagePromptTemplate.from_template(
        """Translate the document that is delimited by triple backticks into English language. If it's already in english, do not do anything."""
    ) # System message

    translated_docs = []
    for doc in docs:
        translated_pages = []
        for page in doc:
            human_message_template = HumanMessagePromptTemplate.from_template(
                "document: ```{text}```"
            )

            # Combine them into a chat prompt template
            prompt_template = ChatPromptTemplate.from_messages([
                system_message_template,
                human_message_template,
            ])

            prompt = prompt_template.format_messages(text = page.page_content)
            answer = llm.invoke(prompt)

            new_page = Document(page_content=answer.content, metadata=page.metadata)
            translated_pages.append(new_page)
        translated_docs.append(translated_pages)

    return translated_docs

