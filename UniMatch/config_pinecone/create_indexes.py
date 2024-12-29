# Automatically run script to create indexes

from pinecone import Pinecone
from pinecone import ServerlessSpec
from dotenv import load_dotenv  # Import dotenv to load environment variables

def initialize_indexes():
    """Create necessary indexes for UniMatch if not present"""
    load_dotenv()

    pc = Pinecone()
    # Get index names
    index_names = [index['name'] for index in pc.list_indexes()]

    # Configs for each index
    # HTML
    htmlindex_config = {
    'name':"htmlindex",
    'dimension': 1536,
    'metric': "cosine",
    'spec': ServerlessSpec(cloud='aws', region='us-east-1')
    }

    # PDF
    pdfindex_config = {
    'name':"pdfindex",
    'dimension': 1536,
    'metric': "cosine",
    'spec': ServerlessSpec(cloud='aws', region='us-east-1')
    }

    # UniMatch
    unimatch_config = {
    'name':"unimatch",
    'dimension': 1536,
    'metric': "cosine",
    'spec': ServerlessSpec(cloud='aws', region='us-east-1')
    }

    if 'htmlindex' not in index_names:
        pc.create_index(**htmlindex_config)
        print("DEBUG: HTML INDEX CREATED")
    else:
        print("DEBUG: HTML INDEX ALREADY EXISTS")

    if 'pdfindex' not in index_names:
        pc.create_index(**pdfindex_config)
        print("DEBUG: PDF INDEX CREATED")
    else:
        print("DEBUG: HTML INDEX ALREADY EXISTS")


    if 'unimatch' not in index_names:
        pc.create_index(**unimatch_config)
        print("DEBUG: UNIMATCH INDEX CREATED")
    else:
        print("DEBUG: HTML INDEX ALREADY EXISTS")
