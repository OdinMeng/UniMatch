import streamlit as st
from dotenv import load_dotenv  # Import dotenv to load environment variables
from UniMatch.data.login import validate_login, handle_login
from UniMatch.pages.main_navigator import main as st_main

if __name__ == '__main__':
    load_dotenv()
    st.set_page_config("UniMatch")
    print("Starting UniMatch...")

    # Main Streamlit Page
    st_main()