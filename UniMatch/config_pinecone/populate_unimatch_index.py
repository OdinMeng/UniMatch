# Automatically run script to populate unimatch index

from pinecone import Pinecone
from UniMatch.data.loader import get_pdfs_folder
from UniMatch.chatbot.rag.extract_data import get_text_from_pdfs
from UniMatch.chatbot.rag.manage_pinecone import clear_db, store_documents

def populate():
    """Populate the unimatch index if necessary"""
    pc = Pinecone()
    idx = pc.Index(name='unimatch')
    if idx.describe_index_stats()['total_vector_count'] > 0:
        print("DEBUG: UNIMATCH INDEX ALREADY POPULATED")
        return

    docs = get_text_from_pdfs(get_pdfs_folder())

    clear_db('unimatch')
    store_documents('unimatch', docs)

    print("DEBUG: UNIMATCH INDEX POPULATED")