import streamlit as st
from UniMatch.data.login import validate_login, handle_login


# Login Page
def login_page():
    st.title("Login")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.form_submit_button("Login")

    if st.button("Back"):
        st.session_state["show_login"] = False

    if login_button:
        login_result = validate_login(username, password) 
        if login_result > 0:
            st.session_state["logged_in"] = True
            st.session_state["current_user"] = username
            st.session_state["show_login"] = False
            st.session_state['user_id'] = login_result
            st.success(handle_login(login_result))
        else:
            st.error(handle_login(login_result))

