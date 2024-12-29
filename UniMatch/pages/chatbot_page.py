# Página do Chatbot
import streamlit as st
from UniMatch import MainChatbot  # Import the chatbot class

from UniMatch.data.loader import get_user_pdfs_folder

import os 
import time
import json

BASE_DIR = os.path.dirname(__file__)

@st.cache_resource
def load_bot():
    """Loads chatbot into the cache resource."""

    bot = MainChatbot()

    print(st.session_state['user_id'], st.session_state['logged_in'])
    # User mode
    if "logged_in" in st.session_state and st.session_state['logged_in']:
        bot.user_login(
            user_id=st.session_state['user_id'],
            conversation_id='1'
        )

    else:
    # Guest mode
        bot.user_login(
            user_id='-1',
            conversation_id='1'
        )

    return bot

def stream_text(text):
    """Given a text, turn a string into a stream of text."""
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.02)


def chatbot_page():
    # Load bot    
    bot = load_bot()

    # Reloads bot if the user has changed his status (logged on, out, changed user, et cetera...)
    if st.session_state['user_id'] != bot.user_id:
        print("DEBUG: RELOADING BOT...")
        st.cache_resource.clear()    
        load_bot()
        st.rerun()

    st.title("UniMatch Chatbot")

    # Chat history container
    chat_container = st.container()

    # Input section
    input_container = st.container()

    # To add: Warn guest is in user mode if not logged in
    if bot.user_id == "-1":
        with chat_container:
            with st.chat_message('ai'):
                st.markdown("""**Welcome to UniMatch! 🎓✨**  
Hi there! 👋 We're thrilled to have you here. Whether you're exploring options or just curious, UniMatch is here to help guide your journey. 🌟  

⚠️ **Heads-up:** You're currently in **Guest Mode**. This means you have access to some of our awesome features, but not everything just yet. For the full UniMatch experience, consider signing up—it’s quick, easy, and free!  

🚀 Ready to explore? Let's help you take the next step toward your dream university! 🏫💡  

Feel free to ask me anything! 😊""")
    
    # Caixa de texto para interação com o chatbot
    if 'chat_history' not in st.session_state:
        to_load = bot.memory.get_filename(bot.user_id, bot.conversation_id)
        try:
            with open(to_load, "r") as f:
                st.session_state['chat_history'] = json.load(f)
        except:
            st.session_state["chat_history"] = []

    # Exibir histórico de mensagens
    with chat_container:
        for message in st.session_state["chat_history"]:
            if not(isinstance(message, dict)):
                continue

            if 'HumanMessage' in message.keys():
                with st.chat_message('human'):
                    st.markdown(message['HumanMessage'])
            elif 'AIMessage' in message.keys():
                with st.chat_message('ai'):
                    st.markdown(message['AIMessage'])
            else:
                continue

    # Chat Input
    with input_container:
        chat_input = st.chat_input(placeholder="> ...")

    if chat_input:
        with chat_container:
            # Process message and save to memory
            st.session_state["chat_history"].append({'HumanMessage': chat_input})
            with st.chat_message('human'):
                st.write_stream(stream_text(chat_input))

            # Get bot response
            bot_response = bot.process_user_input({"customer_input": chat_input})
            st.session_state["chat_history"].append({'AIMessage': bot_response})

            # Write as stream
            with st.chat_message('ai'):
                st.write_stream(stream_text(bot_response))

            # Make bot save the history
        bot.memory.save_session_history(user_id=bot.user_id, conversation_id=bot.conversation_id)
    
    with input_container:
        st.header("Manage Conversation")
        delete = st.button("Delete Chat History")

    with input_container:
        st.header("Upload External Documents")
        st.markdown("Here you can upload *external files* for the chatbot to analyze. When the analysis is done, you can say something like 'I have uploaded the PDF file' followed by a question to get a retrieval-augmented answer!")
        load_folder = get_user_pdfs_folder()
        external_container = st.columns(3)
        uploaded_pdf = external_container[0].file_uploader(label="Upload a PDF File", type="pdf", accept_multiple_files=False)
        uploaded_link = external_container[1].text_input(label="Upload a Link")
        analysis = external_container[2].button('Upload and Analyze Documents')

    if analysis:
    # User clicks on "Analyze Documents" button
        with chat_container:
        # Dummy Messages, just to warn user that this will take a long time
            # Process and save to memory
            dummy_input = "Analyze External Files"
            st.session_state["chat_history"].append({'HumanMessage': dummy_input})
            with st.chat_message('human'):
                st.write_stream(stream_text(dummy_input))

            dummy_answer = "Sure! I will analyze the external files you provided. This is a lengthy operation and can take minutes, so please be patient!"
            st.session_state["chat_history"].append({'AIMessage': dummy_answer})

            # Write as stream
            with st.chat_message('ai'):
                st.write_stream(stream_text(dummy_answer))
                

        if uploaded_pdf is not None:
            with open(os.path.join(load_folder, "USER_FILE.pdf"), "wb") as f:
                f.write(uploaded_pdf.getbuffer())

        if uploaded_link == "":
            uploaded_link = None
            
        bot_response = bot.handle_process_externals(uploaded_link)
        with chat_container:
            with st.chat_message('ai'):
                st.write_stream(stream_text(bot_response))

        bot.memory.save_session_history(user_id=bot.user_id, conversation_id=bot.conversation_id)

                
    if delete:
        del st.session_state["chat_history"]

        session = bot.memory.get_session_history(bot.user_id, bot.conversation_id)
        if session == None:
            st.rerun()

        session.clear()
        bot.memory.save_session_history(user_id=bot.user_id, conversation_id=bot.conversation_id)

        st.rerun()
