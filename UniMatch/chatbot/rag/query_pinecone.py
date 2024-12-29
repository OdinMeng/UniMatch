# Script to query from a pinecone DB

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone

# Load environment variables
load_dotenv()

def get_context_from_pineconedb(database_name: str, prompt: str) -> str:
    """Given a PineCone index, make a query from the prompt and find the closest context. 
    
    If no context is available, returns 'None' in string form.
    """
    
    pc = Pinecone()
    index = pc.Index(database_name)

    vector_store = PineconeVectorStore(
        # PineconeVectorStore from LangChain
    index=index, embedding=OpenAIEmbeddings(model="text-embedding-3-small")
    )

    retriever = vector_store.as_retriever(
                search_type="similarity_score_threshold",
                search_kwargs={"k": 1, "score_threshold": 0.5},
        )   
    
    o = retriever.invoke(prompt)

    if len(o) == 0:
        return 'None'
    else:
        return o[0].page_content