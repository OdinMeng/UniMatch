# Import necessary classes and modules for chatbot functionality
from typing import Dict

from company_name.chatbot.bot import MainChatbot
from company_name.chatbot.router.auxiliar import add_message


class DevChatbot(MainChatbot):
    """A development bot that extends the base customer service bot to allow
    interaction with developers for testing and updating intents.
    """

    def __init__(self, user_id: str, conversation_id: str, intentions: list):
        """Initialize the development bot with additional functionality.

        Args:
            user_id: Identifier for the user.
            conversation_id: Identifier for the conversation.
            intentions: A list of available intentions for the bot.
        """
        # Initialize the base bot class
        super().__init__(user_id, conversation_id)
        self.intentions = intentions  # Store the list of available intentions

    def get_choice_from_list(self):
        """Present a list of available intentions to the user and allow selection.

        Returns:
            The selected intention from the list.
        """
        print("Available intentions:")
        # Display each intention with a numbered choice
        for i, choice in enumerate(self.intentions, 1):
            print(f"{i}. {choice}")

        while True:
            try:
                # Prompt the user to select an intention by number
                user_input = int(input("Select a new intention: "))
                if 1 <= user_input <= len(self.intentions):
                    return self.intentions[user_input - 1]
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def validate_intention(self, intention: str):
        """Confirm with the user if the predicted intention is correct.

        Args:
            intention: The intention predicted by the bot.

        Returns:
            True if the intention is correct, False if incorrect, or None if no valid input.
        """
        print("")
        print(f"Predicted Intention: {intention}")
        is_correct = input("It's correct? [Y/N]: ").strip()
        print("")

        if is_correct.lower() == "y":
            return True  # User confirmed the intention is correct
        elif is_correct.lower() == "n":
            return False  # User indicated the intention is incorrect
        else:
            return None  # Invalid input received

    def create_new_user_messages(self, user_input: Dict):
        """Allow the user to create a new intention and save it to the intention list.

        Args:
            user_input: The input message from the user.
        """
        # Prompt the user to select a new intention from the list
        new_intention = self.get_choice_from_list()
        new_item = {
            "Intention": new_intention,
            "Message": user_input["customer_input"],  # User's input message
        }
        # Save the new intention and message to a JSON file
        add_message(new_item, "new_intentions.json")

    def process_user_input(self, user_input: Dict):
        """Process user input by routing through the intention pipeline or allowing for updates.

        Args:
            user_input: The input text from the user.

        Returns:
            The content of the response after processing or a message indicating a new intention.
        """
        # Classify the user's intent using the base bot's classifier
        intention = self.get_user_intent(user_input)

        # Check if the intention is a string or None
        if intention is None:
            return "I'm sorry, I don't understand that intention."
        else:
            # Validate the predicted intention with the user
            is_correct = self.validate_intention(intention)

            # If the intention is validated as correct
            if is_correct:
                # Process the input using the identified intention
                if intention == "product_information":
                    response = self.handle_product_information(user_input)
                elif intention == "create_order" or intention == "get_order":
                    response = self.handle_order_intent(user_input)
                else:
                    # Default response for unrecognized intents
                    response = "Not implemented yet."
                return response
            else:
                # Handle invalid validation input
                if is_correct is None:
                    print("You should enter 'Y' or 'N'. Please try again.")
                else:
                    # Create a new intention and notify the user
                    self.create_new_user_messages(user_input)
                    return "New intention added successfully."
