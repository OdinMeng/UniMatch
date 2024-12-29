import streamlit as st

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

        - **Q. Does the chatbot support any other languages than English?**  
          While the chatbot can handle conversations in other languages, it is best to maintain interactions 
          in English to avoid potential errors. However, it is totally safe to upload external documents in 
          foreign languages, as the chatbot is specifically designed to translate them for you.
    """)

    st.write(
        "**Our support team is always ready to assist you!** Contact us at any moment, and we'll ensure that you enjoy working with us.")

