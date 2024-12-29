# Functions to use (and manage) PineCone DBs
from typing import List

from dotenv import load_dotenv
from langchain_core.documents.base import Document
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pinecone import Pinecone

load_dotenv()

def store_documents(database_name: str, docs: List[Document]):
    """
    Given a list of documents, follows the following pipeline:
        1. Split text
        2. Generate embeddings
        3. Adds the embeddings to the pinecone database (specified in the input)
    """
    last_id = 0
    for doc in docs:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,  # Maximum size of each chunk
            chunk_overlap=100,  # Overlap between chunks to preserve context
            separators=["\n\n", "\n", "\t", ""], # Define separators
            add_start_index=True
            )

        all_splits = text_splitter.split_documents(doc)

        pc = Pinecone()
        index = pc.Index(database_name)

        vector_store = PineconeVectorStore(
            # PineconeVectorStore from LangChain
        index=index, embedding=OpenAIEmbeddings(model="text-embedding-3-small")
        )

        ids = [str(i) for i in range(last_id+1, len(all_splits)+last_id+1)]
        last_id = int(ids[-1])

        vector_store.add_documents(documents=all_splits, ids=ids)
    return 0 # Terminate

def clear_db(database_name : str):
    """
    Clears a database (given an ID) from all of the elements.
    """

    pc = Pinecone()
    index = pc.Index(database_name)

    try:
        index.delete(delete_all=True, namespace='') # Clear
    except Exception as e:
        return e # Fail
    else:
        return 0 # Success