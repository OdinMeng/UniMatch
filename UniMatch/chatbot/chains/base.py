# Import necessary modules and classes
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)
from pydantic import BaseModel, Field


class PromptTemplate(BaseModel):
    """Defines templates for system and human messages used in a conversation."""

    system_template: str = Field(
        description="Template for the system message in the conversation"
    )
    human_template: str = Field(
        description="Template for the human message in the conversation"
    )


def generate_prompt_templates(
    prompt_template: PromptTemplate, memory: bool
) -> ChatPromptTemplate:
    """Generate a chat prompt template based on given templates and memory setting.

    Args:
        prompt_template: An instance of PromptTemplate containing system and human templates.
        memory: A boolean flag indicating whether to include chat history in the prompt.

    Returns:
        A configured ChatPromptTemplate with specified message structure.
    """
    # Create prompt template including chat history if memory is enabled
    if memory:
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(
                    prompt_template.system_template
                ),
                MessagesPlaceholder(variable_name="chat_history"),
                HumanMessagePromptTemplate.from_template(
                    prompt_template.human_template
                ),
            ]
        )
    else:
        # Create prompt template without chat history
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(
                    prompt_template.system_template
                ),
                HumanMessagePromptTemplate.from_template(
                    prompt_template.human_template
                ),
            ]
        )

    return prompt


def generate_agent_prompt_template(
    prompt_template: PromptTemplate,
) -> ChatPromptTemplate:
    """Generate a chat prompt template based on given templates and memory setting.

    Args:
        prompt_template: An instance of PromptTemplate containing system and human templates.

    Returns:
        A configured ChatPromptTemplate with specified message structure.
    """
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(prompt_template.system_template),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template(prompt_template.human_template),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    return prompt
