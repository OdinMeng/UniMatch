import streamlit as st
from dotenv import load_dotenv  # Import dotenv to load environment variables
from UniMatch.pages.main_navigator import main as st_main
from UniMatch.config_pinecone.create_indexes import initialize_indexes
from UniMatch.config_pinecone.populate_unimatch_index import populate 

if __name__ == '__main__':
    # Load environment variables
    load_dotenv()

    # Set up pinecone databases if necessary
    initialize_indexes()
    populate()

    # Define page title
    st.set_page_config("UniMatch") 
    
    # Debug
    print("Starting UniMatch...")

    # Main Streamlit Page
    st_main()