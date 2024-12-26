"""
This file should be the entrypoint of your Streamlit App.
"""

from dotenv import load_dotenv  # Import dotenv to load environment variables

from UniMatch import MainChatbot  # Import the chatbot class
from UniMatch.data.login import validate_login, handle_login

def main(bot: MainChatbot):
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
            bot.memory.save_session_history(bot.user_id, bot.conversation_id)
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
    bot = MainChatbot()

    # Login loop
    while 1:
        print("LOGIN TO UNIMATCH")
        print("="*15)
        username = input("Insert Username (insert -1 for guest mode)\n> ")
        password = input("Insert Password\n> ")

        if username == "-1":
            result = -1
            break

        result = validate_login(username, password)
        print(handle_login(result))
        if result > 0:
            break
        

    bot.user_login(str(result), '1')

    # Display instructions for ending the conversation
    print("Bot initialized. Type 'exit' or 'quit' to end the conversation.")

    # Start the main interaction loop
    main(bot)
