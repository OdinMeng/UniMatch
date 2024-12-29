# Import basic modules
import streamlit as st
import os

# Import other pages
from UniMatch.pages.about_page import about_page
from UniMatch.pages.login_page import login_page
from UniMatch.pages.main_page import home_page
from UniMatch.pages.register_page import register_page
from UniMatch.pages.chatbot_page import chatbot_page
from UniMatch.pages.support_page import support_page

# Define base directory
BASE_DIR = os.path.dirname(__file__)

def add_header():
    col1, col2 = st.columns([1, 3])  # Logo and Buttons Column

    # Logo on the left
    with col1:
        st.image(os.path.join(BASE_DIR, 'images', 'UniMatch logotipo.png'), width= 1000)

    # Buttons on the right
    with col2:
        if st.session_state.get("logged_in", False):
            st.write(f"Hi, {st.session_state['current_user']} 👋")
            if st.button("Logout"):
                st.session_state["logged_in"] = False
                st.session_state["current_user"] = ""
                st.session_state['user_id'] = '-1'
                st.rerun()
                
        else:
            if st.button("Login"):
                st.session_state["show_login"] = True
                st.session_state["show_register"] = False  # Ensure the registration page is closed
            if st.button("Register"):
                st.session_state["show_register"] = True
                st.session_state["show_login"] = False  # Ensure the login page is closed

def main():
    # Initialize required states
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "current_user" not in st.session_state:
        st.session_state["current_user"] = ""
    if "show_login" not in st.session_state:
        st.session_state["show_login"] = False
    if "show_register" not in st.session_state:
        st.session_state["show_register"] = False
    if "user_id" not in st.session_state:
        st.session_state['user_id'] = "-1"

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to:", ["Home", "About", "Chatbot", "Support"])

    # Add header with login/logout
    add_header()

    # Navigation page
    if st.session_state["show_login"]:
        login_page()
    elif st.session_state["show_register"]:
        register_page()
    elif page == "Home":
        home_page()
    elif page == "About":
        about_page()
    elif page == "Chatbot":
        chatbot_page()
    elif page == "Support":
        support_page()
