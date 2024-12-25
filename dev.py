"""
This file should be the entrypoint of your Streamlit App.
"""

from dotenv import load_dotenv  # Import dotenv to load environment variables

from UniMatch import DevChatbot  # Import the chatbot class


def main(bot: DevChatbot):
    """Main interaction loop for the chatbot.

    Args:
        bot: An instance of the MainChatbot.
    """
    while True:
        # Prompt the user for input
        user_input = input("You: ").strip()

        # Allow the user to exit the conversation
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            bot.memory.save_session_history('1', '1')
            break

        try:
            # Process the user's input using the bot and display the response
            response = bot.process_user_input({"customer_input": user_input})
            print(f"Bot: {response}")
        except Exception as e:
            # Handle any exceptions and prompt the user to try again
            print(f"Error: {str(e)}")
            print("Please try again with a different query.")


if __name__ == "__main__":
    # Load environment variables from a .env file
    load_dotenv()

    # Notify the user that the bot is starting
    print("Starting the bot...")

    # Initialize the CustomerServiceBot with dummy user and conversation IDs
    bot = DevChatbot(user_id='1', conversation_id='1', intentions=["manage_personal_information", "search_scholarships_and_internationals","search_universities" , "matchmaking", "query_matches", "leverage_rag", "company_info"])

    # Display instructions for ending the conversation
    print("Bot initialized. Type 'exit' or 'quit' to end the conversation.")

    # Start the main interaction loop
    main(bot)
