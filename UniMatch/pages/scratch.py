import streamlit as st
import json
import os
import re

#file to save all credentials(This way the credentials are saved permanently and are not deleted with each update.
users_file = "users.json"

# Load user data from a JSON file
def load_users():
    if os.path.exists(users_file):
        with open(users_file, "r") as f:
            return json.load(f)
    else:
        return {}

def save_users(users_db):
    with open(users_file, "w") as f:
        json.dump(users_db, f)

# Function to check credentials
def check_credentials(username, password):
    users_db = load_users()
    return users_db.get(username) == password

# Function to register a new user
def register_user(first_name, last_name, username, password, email):
    users_db = load_users()
    if username in users_db:
        return False  # Username already exists
    else:
        # Store user data as a dictionary
        users_db[username] = {
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "password": password,
            "email": email
        }
        save_users(users_db)
        return True

# Function to create the header
def add_header():
    col1, col2 = st.columns([1, 3])  # Logo and Buttons Column

    # Logo on the left
    with col1:
        st.image("C:/Users/migue/PycharmProjects/pythonProject/cenas/resources/UniMatch logotipo.jpg", width= 1000)

    # Buttons on the right
    with col2:
        if st.session_state.get("logged_in", False):
            st.write(f"Hi, {st.session_state['current_user']} 👋")
            if st.button("Logout"):
                st.session_state["logged_in"] = False
                st.session_state["current_user"] = ""
        else:
            if st.button("Login"):
                st.session_state["show_login"] = True
                st.session_state["show_register"] = False  # Ensure the registration page is closed
            if st.button("Register"):
                st.session_state["show_register"] = True
                st.session_state["show_login"] = False  # Ensure the login page is closed

# Home page
def home_page():
    st.title("Welcome to UniMatch!")
    st.write("We’re thrilled to introduce you to UniMatch, your intelligent companion for navigating the complexities of university applications, scholarships, and academic programs. Designed with a deep understanding of student needs, this chatbot will provide personalized recommendations and information tailored to your preferences. Let’s walk you through how you can make the most out of this tool!")

    pdf_path = "C:/Users/migue/PycharmProjects/pythonProject/cenas/resources/chatbot_info.pdf"

    with open(pdf_path, "rb") as pdf_file:
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

# About Page
def about_page():
    st.title("About Us")

    # Subheader About UniMatch
    st.subheader("**About UniMatch**")
    st.write("""
            UniMatch is a company created with the main goal of helping graduated students
            find suitable universities and/or areas of study, assisting their transition to higher
            education. It intends to achieve this goal by making the best use of LLMs and
            generative AI technologies to provide the users with a new level of personalization
            and to find information which would be hard to access.

            The platform provides information about a wide range of university courses and their
            subjects, and any requirements for applying. It also aids students discover
            international mobility opportunities, and applicable scholarships for any area of
            study. UniMatch is designed for a wide range of users, including high school
            graduates looking for undergraduate programs, undergraduates seeking Master’s
            degrees, and those interested in pursuing PhDs. By making the process simpler and
            more personalized, UniMatch ensures students can make better decisions for their
            education and future careers.
        """)

    # Mission Statement
    st.subheader("**MISSION STATEMENT**")
    st.write("""
            The mission of UniMatch is to enable students and aspiring academics by guiding
            them towards academic paths, whether the person is searching for a university, Master’s programmes,
            scholarship, Erasmus+ programmes, etc. By helping these people find the right fit in the academic world,
            UniMatch contributes to a smaller dropout rate and higher satisfaction in these programs,
            ensuring students are allocated in tailored programs to achieve their individual goals.
        """)

    # Vision Statement
    st.subheader("**VISION STATEMENT**")
    st.write("""
            UniMatch aims to become a viable and mainstream tool for those who need guidance
            choosing where and/or what to study. You can find more information in the Future Perspectives section below.
        """)

    # Company Values
    st.subheader("**COMPANY VALUES**")
    st.write("""
            UniMatch is committed to the following values:
            - **Inclusion:** Our solution helps every kind of student with guidance to have guaranteed access to
              university-related matters, i.e., finding scholarships programmes.
            - **Internationalization:** One of our features is to help students look for international opportunities or
              universities abroad.
            - **Education:** The main goal of UniMatch is to provide students with guidance in their higher education path.
            - **Innovation:** We achieve our goals through innovative technologies, namely LLMs and generative AI.
        """)

    # How was UniMatch born?
    st.subheader("**How was UniMatch born?**")
    st.write("""
            UniMatch is a startup born as a university project for the Capstone Project course (at NOVA IMS, Lisbon),
            driven by the desire to address a common challenge faced by students.

            The idea came from the creators seeing many of their peers struggle to choose a university,
            often feeling lost and unsure. UniMatch was created to make this process easier by providing personalized
            advice to help students pick the right university and program for their interests and goals.
        """)

    # Future Perspectives
    st.subheader("**Future Perspectives**")
    st.write("""
            UniMatch is a small startup focused on showcasing how generative AI can solve
            industry challenges, such as helping students make informed decisions about their
            education or streamlining administrative processes in universities.

            Currently, the internal database contains only basic information—such as the name,
            location, and main website—on about 0.21% of universities worldwide, and only 20%
            of these have detailed data on courses, prerequisites, scholarships, and other relevant
            details. As a result, UniMatch is still in the early stages of development.

            However, we love to believe that the potential is there: UniMatch could grow into a
            mainstream tool for students by providing personalized university recommendations
            based on their unique preferences, academic background, and career goals, offering
            detailed insights to help them make well-informed decisions about their future.

            In the future, we might expand our database to cover all universities in the European
            Union and add new features like multimedia support.
        """)

    # Team Section in Columns
    st.subheader("About the Team")
    col1, col2 = st.columns(2)

    with col1:
        st.write("### Dino Meng")
        st.write("""
                - Is a Italian exchange student from the University of Trieste,
                  pursuing a bachelor's degree in "Artificial Intelligence & Data Analytics".
                - Interests: pure mathematics, machine learning, coding, and generative AI technologies.
            """)

        st.write("### Lourenço Passeiro")
        st.write("""
                - Third-year student at NOVA IMS pursuing a degree in Data Science.
                - Passionate about machine learning, with aspirations to create impactful models for decision-making.
                - Experienced in regression, classification, clustering, and deep learning.
            """)

        st.write("### Miguel Marques")
        st.write("""
                - Third-year student at NOVA IMS pursuing a degree in Data Science.
                - Enthusiast in data science and databases, with a strong focus on insights extraction.
                - Extensive experience with SQL and database optimization.
            """)

    with col2:
        st.write("### Peter Lekszycki")
        st.write("""
                - Third-year student at NOVA IMS pursuing a degree in Data Science.
                - Passionate about entrepreneurship and using data for real-world innovation.
                - Aspires to create a data-centric startup leveraging AI technologies.
            """)

        st.write("### Tomás Gonçalves")
        st.write("""
                - Third-year student at NOVA IMS pursuing a degree in Data Science.
                - Focuses on data analytics and generating business insights for decision-making.
                - Experienced in data cleaning, EDA, and visualization using Python, SQL, and Power BI.
            """)


# Página de Suporte
def support_page():
    st.title("UniMatch: Support & Contact Information")
    st.write(""" 
        **At UniMatch, customer satisfaction is our main goal.** We provide user resources, 
        technical support, and a strong support system to guarantee you have the greatest 
        experience. You can find all the information you require to utilize our support services below:
    """)

    st.subheader("1. Customer Support")
    st.write(""" 
        Our **customer service team** is available to assist you with any questions or concerns. 
        We offer multiple channels to make it easier for you to get in touch:

        - **Phone Support:** +351 210 893 723  
          Available every day, from 8:00 AM to 10:00 PM GMT.
        - **Email Support:** support@unimatch.com  
          We’ll respond to your inquiries within **24 hours**.
        - **Social Media Support:** @unimatch on **Facebook, Instagram, and X**.  
          Follow our official social media accounts to keep up with any updates.
        - **Chatbot:** In some cases, the chatbot itself might be enough to provide you technical support!
    """)
    st.subheader("2. Frequently Asked Questions (FAQs)")
    st.write("""
        Our **FAQs** are designed to provide instant answers to common questions. Topics include:

        - **Accounts**
        - **Personal data & preferences**
        - **Privacy concerns**
        - **University/Course queries**
        - **Matching results breakdown**

        Visit our FAQ page for more questions than the ones included in this file.
    """)

    st.write("**Here are some of the common FAQs:**")
    st.write("""
        - **Q. Is it necessary to have an account?**  
          No, you can interact with the chatbot as a “guest” to try out its potentialities; however, it won’t 
          be possible to add any form of personalization.

        - **Q. Do I have to pay anything?**  
          No, UniMatch is a completely free service! In the future, we might plan to add expansions that 
          require a form of payment, but as of now, it’s completely free.

        - **Q. How do I fill out my preferences about the university?**  
          All you have to do is talk about it to the chatbot, saying something like “I would like a university 
          with [X] characteristics”, and the chatbot will automatically fill out your preferences!

        - **Q. Can I use the chatbot without sharing any private information?**  
          Technically, it is possible to receive the chatbot’s services without sharing any personal data. 
          However, it is best to share a few pointers with the chatbot to guarantee a completely personalized 
          interaction.

        - **Q. Can I delete my account and data permanently?**  
          Yes! UniMatch is completely GDPR-compliant, guaranteeing total transparency in personal information 
          handling. When you want to delete your account and data, you can either ask the chatbot to do it or 
          do it via the user interface.

        - **Q. Does the chatbot support any other languages than English?**  
          While the chatbot can handle conversations in other languages, it is best to maintain interactions 
          in English to avoid potential errors. However, it is totally safe to upload external documents in 
          foreign languages, as the chatbot is specifically designed to translate them for you.
    """)

    st.write(
        "**Our support team is always ready to assist you!** Contact us at any moment, and we'll ensure that you enjoy working with us.")



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
        if check_credentials(username, password):
            st.session_state["logged_in"] = True
            st.session_state["current_user"] = username
            st.session_state["show_login"] = False
            st.success("Log In efetuado com sucesso")
        else:
            st.error("Username or password incorrect. Please try again.")

import re

# Função para verificar a força da senha
def is_strong_password(password):
    # Verify the conditions
    if (len(password) >= 8 and
        re.search(r'[A-Z]', password) and  # Check if there is a capital letter
        re.search(r'[a-z]', password) and  # Check if it has a lowercase letter
        re.search(r'[0-9]', password) and  # Check if there is a number
        re.search(r'[!@#$%^&*(),.?":{}|<>]', password)):  # Check if there is a special character
        return True
    return False

# Página do Chatbot
def chatbot_page():
    st.title("How can I help?")
    st.write("Interact with our chatbot below:")

    # Caixa de texto para interação com o chatbot
    chat_input = st.text_input("Type your message:")
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    if st.button("Send"):
        if chat_input:
            st.session_state["chat_history"].append(f"You: {chat_input}")
            # Aqui você pode integrar a lógica do bot para gerar uma resposta
            bot_response = "This is the bot's response."  # Exemplo de resposta
            st.session_state["chat_history"].append(f"Bot: {bot_response}")
        else:
            st.warning("Please enter a message.")

    # Exibir histórico de mensagens
    for message in st.session_state["chat_history"]:
        st.write(message)

# Register Page
def register_page():
    st.title("Register")
    with st.form("register_form"):
        first_name = st.text_input("First Name:")
        last_name = st.text_input("Last Name:")
        username = st.text_input("Choose a Username")
        password = st.text_input("Choose a Password", type="password")
        email = st.text_input("Email:")
        register_button = st.form_submit_button("Register")

    if st.button("Back"):
        st.session_state["show_register"] = False

    if register_button:
        if not first_name or not last_name or not username or not password or not email:
            st.error("All fields are mandatory")
        elif not is_strong_password(password):
            st.error("Password must be at least 8 characters long, contain an uppercase letter, a lowercase letter, a number, and a special character.")
        elif register_user(first_name, last_name, username, password, email):
            st.success("Profile created successfully! Please log in.")
            st.session_state["show_register"] = False
        else:
            st.error("Username already exists. Please choose another one.")
# Page Manager
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

# Main execution
if __name__ == "__main__":
    st.set_page_config(page_title="UniMatch", layout="wide")
    main()
