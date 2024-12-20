# Import necessary modules and classes
import json
from typing import Dict, List, Tuple

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage
from langchain_core.messages.ai import AIMessage
from langchain_core.messages.human import HumanMessage
from langchain_core.runnables import ConfigurableFieldSpec
from pydantic import BaseModel, Field


class InMemoryHistory(BaseChatMessageHistory, BaseModel):
    """In-memory implementation of chat message history.

    Stores a list of messages within the session.
    """

    messages: List[BaseMessage] = Field(default_factory=list)

    def add_messages(self, messages: List[BaseMessage]):
        """Add a list of messages to the in-memory store."""
        self.messages.extend(messages)

    def clear(self) -> None:
        """Clear all messages from the in-memory store."""
        self.messages = []


class MemoryManager:
    """Manages session history and configuration for user interactions.

    Stores session-specific configurations and provides access to
    session histories.
    """

    def __init__(self):
        """Initialize session manager."""
        self.store: Dict[Tuple[str, str], InMemoryHistory] = {}
        self.history_factory_config = [
            ConfigurableFieldSpec(
                id="user_id",
                annotation=str,
                name="User ID",
                description="Unique identifier for the user.",
                default="",
                is_shared=True,
            ),
            ConfigurableFieldSpec(
                id="conversation_id",
                annotation=str,
                name="Conversation ID",
                description="Unique identifier for the conversation.",
                default="",
                is_shared=True,
            ),
        ]

    def get_session_history(
        self, user_id: str, conversation_id: str
    ) -> BaseChatMessageHistory:
        """Retrieve or create session history for a specific user, conversation.

        Args:
            user_id: Identifier for the user.
            conversation_id: Identifier for the conversation.

        Returns:
            An instance of BaseChatMessageHistory for managing the chat history.
        """
        if (user_id, conversation_id) not in self.store:
            # Initialize new in-memory history if not already stored
            self.store[(user_id, conversation_id)] = InMemoryHistory()

        return self.store[(user_id, conversation_id)]

    def get_history_factory_config(self) -> List[ConfigurableFieldSpec]:
        """Retrieve configuration settings for history factory.

        Returns:
            A list of ConfigurableFieldSpec instances for field configurations.
        """
        return self.history_factory_config

    def save_session_history(self, user_id: str, conversation_id: str) -> None:
        """Save the session history as a txt file.

        Args:
            user_id: Identifier for the user.
            conversation_id: Identifier for the conversation.
        """

        session_history = self.get_session_history(
            user_id=user_id, conversation_id=conversation_id
        )

        # Iterate over messages in the session history
        # and save them to a text file
        with open(f"{user_id}_{conversation_id}_history.txt", "w") as file:
            for message in session_history.messages:
                # Check if is HumanMessage or AIMessage
                if isinstance(message, HumanMessage):
                    file.write(f"User: {message.content}\n")
                elif isinstance(message, AIMessage):
                    file.write(f"Bot: {message.content}\n")
