# Import necessary classes and modules for chatbot functionality
from typing import Callable, Dict, Optional

from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

from company_name.chatbot.agents.agent1 import Agent1
from company_name.chatbot.chains.chain3 import ReasoningChain3, ResponseChain3
from company_name.chatbot.memory import MemoryManager
from company_name.chatbot.router.loader import load_intention_classifier


class MainChatbot:
    """A bot that handles customer service interactions by processing user inputs and
    routing them through configured reasoning and response chains.
    """

    def __init__(self):
        """Initialize the bot with session and language model configurations."""
        # Initialize the memory manager to manage session history
        self.memory = MemoryManager()

        # Configure the language model with specific parameters for response generation
        self.llm = ChatOpenAI(temperature=0.0, model="gpt-4o-mini")

        # Map intent names to their corresponding reasoning and response chains
        self.chain_map = {
            "product_information": {
                "reasoning": ReasoningChain3(llm=self.llm),  # Reasoning chain
                "response": self.add_memory_to_runnable(
                    ResponseChain3(llm=self.llm)  # Response chain with memory
                ),
            }
        }

        self.agent_map = {
            "order": self.add_memory_to_runnable(Agent1(llm=self.llm).agent_executor)
        }

        self.rag = self.add_memory_to_runnable(
            RAGPipeline(
                index_name="rag",
                embeddings_model="text-embedding-3-small",
                llm=self.llm,
                memory=True,
            ).rag_chain
        )

        # Map of intentions to their corresponding handlers
        self.intent_handlers: Dict[Optional[str], Callable[[Dict[str, str]], str]] = {
            "product_information": self.handle_product_information,
            "create_order": self.handle_order_intent,
            "order_status": self.handle_order_intent,
            "support_information": self.handle_support_information,
        }

        # Load the intention classifier to determine user intents
        self.intention_classifier = load_intention_classifier()

    def user_login(self, user_id: str, conversation_id: str) -> None:
        """Log in a user by setting the user and conversation identifiers.

        Args:
            user_id: Identifier for the user.
            conversation_id: Identifier for the conversation.
        """
        self.user_id = user_id
        self.conversation_id = conversation_id
        self.memory_config = {
            "configurable": {
                "user_id": self.user_id,
                "conversation_id": self.conversation_id,
            }
        }

    def add_memory_to_runnable(self, original_runnable):
        """Wrap a runnable with session history functionality.

        Args:
            original_runnable: The runnable instance to which session history will be added.

        Returns:
            An instance of RunnableWithMessageHistory that incorporates session history.
        """
        return RunnableWithMessageHistory(
            original_runnable,
            self.memory.get_session_history,  # Retrieve session history
            input_messages_key="customer_input",  # Key for user inputs
            history_messages_key="chat_history",  # Key for chat history
            history_factory_config=self.memory.get_history_factory_config(),  # Config for history factory
        ).with_config(
            {
                "run_name": original_runnable.__class__.__name__
            }  # Add runnable name for tracking
        )

    def get_chain(self, intent: str):
        """Retrieve the reasoning and response chains based on user intent.

        Args:
            intent: The identified intent of the user input.

        Returns:
            A tuple containing the reasoning and response chain instances for the intent.
        """
        return self.chain_map[intent]["reasoning"], self.chain_map[intent]["response"]

    def get_agent(self, intent: str):
        """Retrieve the agent based on user intent.

        Args:
            intent: The identified intent of the user input.

        Returns:
            The agent instance for the intent.
        """
        return self.agent_map[intent]

    def get_user_intent(self, user_input: Dict):
        """Classify the user intent based on the input text.

        Args:
            user_input: The input text from the user.

        Returns:
            The classified intent of the user input.
        """
        # Retrieve possible routes for the user's input using the classifier
        intent_routes = self.intention_classifier.retrieve_multiple_routes(
            user_input["customer_input"]
        )

        # Handle cases where no intent is identified
        if len(intent_routes) == 0:
            return None
        else:
            intention = intent_routes[0].name  # Use the first matched intent

        # Validate the retrieved intention and handle unexpected types
        if intention is None:
            return None
        elif isinstance(intention, str):
            return intention
        else:
            # Log the intention type for unexpected cases
            intention_type = type(intention).__name__
            print(
                f"I'm sorry, I didn't understand that. The intention type is {intention_type}."
            )
            return None

    def handle_product_information(self, user_input: Dict):
        """Handle the product information intent by processing user input and providing a response.

        Args:
            user_input: The input text from the user.

        Returns:
            The content of the response after processing through the chains.
        """
        # Retrieve reasoning and response chains for the product information intent
        reasoning_chain, response_chain = self.get_chain("product_information")

        # Process user input through the reasoning chain
        reasoning_output = reasoning_chain.invoke(user_input)

        # Generate a response using the output of the reasoning chain
        response = response_chain.invoke(reasoning_output, config=self.memory_config)

        return response.content

    def handle_order_intent(self, user_input: Dict):
        """Handle the order intent by processing user input and providing a response.

        Args:
            user_input: The input text from the user.

        Returns:
            The content of the response after processing through the chains.
        """
        # Retrieve the agent for the order intent
        agent = self.get_agent("order")

        # Process user input through the agent
        response = agent.invoke(
            {
                "customer_id": self.user_id,
                "customer_input": user_input["customer_input"],
            },
            config=self.memory_config,
        )

        return response["output"]

    def handle_unknown_intent(self, user_input: Dict[str, str]) -> str:
        """Handle unknown intents by providing a chitchat response.

        Args:
            user_input: The input text from the user.

        Returns:
            The content of the response after processing through the new chain.
        """
        possible_intention = [
            "Product Information",
            "Create Order",
            "Order Status",
            "Support Information",
            "Chitchat",
        ]

        chitchat_reasoning_chain, _ = self.get_chain("chitchat")

        input_message = {}

        input_message["customer_input"] = user_input["customer_input"]
        input_message["possible_intentions"] = possible_intention
        input_message["chat_history"] = self.memory.get_session_history(
            self.user_id, self.conversation_id
        )

        reasoning_output1 = chitchat_reasoning_chain.invoke(input_message)

        if reasoning_output1.chitchat:
            print("Chitchat")
            return self.handle_chitchat_intent(user_input)
        else:
            router_reasoning_chain2, _ = self.get_chain("router")
            reasoning_output2 = router_reasoning_chain2.invoke(input_message)
            new_intention = reasoning_output2.intent
            print("New Intention:", new_intention)
            new_handler = self.intent_handlers.get(new_intention)
            return new_handler(user_input)

    def save_memory(self) -> None:
        """Save the current memory state of the bot."""
        self.memory.save_session_history(self.user_id, self.conversation_id)

    def process_user_input(self, user_input: Dict[str, str]) -> str:
        """Process user input by routing through the appropriate intention pipeline.

        Args:
            user_input: The input text from the user.

        Returns:
            The content of the response after processing through the chains.
        """
        # Classify the user's intent based on their input
        intention = self.get_user_intent(user_input)

        print("Intent:", intention)

        # Route the input based on the identified intention
        handler = self.intent_handlers.get(intention, self.handle_unknown_intent)
        return handler(user_input)
