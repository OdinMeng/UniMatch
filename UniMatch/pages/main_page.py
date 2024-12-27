import streamlit as st
import os
BASE_DIR = os.path.dirname(__file__)

# Home page
def home_page():
    st.title("Welcome to UniMatch!")
    st.write("We’re thrilled to introduce you to UniMatch, your intelligent companion for navigating the complexities of university applications, scholarships, and academic programs. Designed with a deep understanding of student needs, this chatbot will provide personalized recommendations and information tailored to your preferences. Let’s walk you through how you can make the most out of this tool!")

    with open(os.path.join(BASE_DIR, '..', 'data', 'pdf', 'chatbot_info.pdf'), "rb") as pdf_file:
        pdf_data = pdf_file.read()

    st.write(
        "If you are already familiar with the tool, navigate through the menu on the left. "
        "Otherwise, download the Chatbot User Manual below."
    )
    st.download_button(
        label="Download Chatbot User Manual",
        data=pdf_data,
        file_name="chatbot_info.pdf",
        mime="application/pdf",
    )
