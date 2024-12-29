## Import necessary classes and modules for chatbot functionality
# Typing
from typing import Callable, Dict, Optional

# Langchain modules
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

# Chains and Agents
from UniMatch.chatbot.chains.controlchain import ControlChain, DiscourageUserChain
from UniMatch.chatbot.chains.conversationchain import ConversationChain
from UniMatch.chatbot.chains.companyinformationchain import CompanyInformationChain
from UniMatch.chatbot.chains.processpdfchain import ProcessPDFChain,ReasoningPDFChain
from UniMatch.chatbot.chains.processwebsitechain import ProcessWebsiteChain, ReasoningWebsiteChain
from UniMatch.chatbot.chains.classify_rag import ClassifyRAG
from UniMatch.chatbot.chains.userinfofetchchain import UserInfoFetchChain
from UniMatch.chatbot.chains.uniinfosearchchain import UniInfoSearchChain
from UniMatch.chatbot.chains.uniinforesponsechain import UniInfoResponseChain
from UniMatch.chatbot.chains.makematcheschain import MakeMatchesChain
from UniMatch.chatbot.chains.extractmatcheschain import ExtractMatchesChain
from UniMatch.chatbot.chains.matchesresponsechain import MatchesResponseChain
from UniMatch.chatbot.agents.userinfomanager import UserInfoManager
from UniMatch.chatbot.chains.denyuserintentionchain import DenyUserIntentionChain
from UniMatch.chatbot.chains.handleerrorchain import HandleErrorChain

# Memory
from UniMatch.chatbot.memory import MemoryManager

# Main intention router
from UniMatch.chatbot.router.loader import load_intention_classifier

class MainChatbot:
    """A bot that handles customer service interactions by processing user inputs and routing them through configured reasoning and response chains."""

    def __init__(self):
        """Initialize the bot with session and language model configurations."""
        # Initialize the memory manager to manage session history
        self.memory = MemoryManager()

        # Configure the language model with specific parameters for response generation
        self.llm = ChatOpenAI(temperature=0.0, model="gpt-4o-mini")

        # Import chains for every feature
        # Filter
        self.filter = ControlChain(llm = self.llm)
        self.discourager = DiscourageUserChain(llm = self.llm)
        
        # Chitchat
        self.chitchatter = ConversationChain(llm = self.llm)
        
        # Company Information
        self.informer = CompanyInformationChain(llm = self.llm)
        
        # External Information Processing and RAG
        self.pdfprocesser = ProcessPDFChain()
        self.pdfreasoner = ReasoningPDFChain(llm = self.llm)
        self.webprocesser = ProcessWebsiteChain()
        self.webreasoner = ReasoningWebsiteChain(llm = self.llm)
        self.ragclassifier = ClassifyRAG(llm = self.llm)

        # Auxiliary Chains
        self.userinfofetcher = UserInfoFetchChain(llm = self.llm)
        self.uniinfosearcher = UniInfoSearchChain(llm = self.llm)
        
        # University, course, scholarships, ..., information responder
        self.uniinforeponser = UniInfoResponseChain(llm = self.llm)

        # Handle and query matches
        self.matchmaker = MakeMatchesChain(llm = self.llm)
        self.matchesextractor = ExtractMatchesChain(llm = self.llm)
        self.matchesreponder = MatchesResponseChain(llm = self.llm)

        # Handle user information
        self.userinfomanager = UserInfoManager(llm = self.llm)

        # Handle denied requests or errors
        self.denier = DenyUserIntentionChain(llm = self.llm)
        self.errorhandler = HandleErrorChain(llm = self.llm)

        # Map of intentions to their corresponding handlers
        self.intent_handlers: Dict[Optional[str], Callable[[Dict[str, str]], str]] = {
            "manage_personal_info": self.handle_personal_info, 
            "search_scholarships_and_internationals": self.handle_search_scholarships_and_internationals,
            "search_universities": self.handle_search_universities_and_courses , 
            "matchmaking": self.handle_matchmaking, 
            "query_matches": self.handle_query_matches, 
            "leverage_rag": self.handle_rag, 
            "company_info": self.handle_company_info,
            None: self.handle_unknown_intent
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

    def handle_error(self, error_input: Dict[str, str]) -> str:
        """Fallback chain to handle errors."""

        # Prepare input message to invoke the chain
        input_message = {}
        input_message['user_prompt'] = error_input['customer_input']
        input_message["chat_history"] = self.memory.get_session_history(
            self.user_id, self.conversation_id
        ).messages
        input_message['exception'] = error_input['exception']

        # Invoke chain
        content = self.errorhandler.invoke(input_message).content

        # Save Q, A to memory
        memory = self.memory.get_session_history(self.user_id, self.conversation_id)
        memory.add_user_message(error_input["customer_input"])
        memory.add_ai_message(content)

        return content
    
    def handle_denial(self, user_input: Dict[str, str]) -> str:
        """Fallback chain to handle denied requests"""

        # Prepare input message to invoke the chain
        input_message = {}
        input_message['user_prompt'] = user_input['customer_input']
        input_message["chat_history"] = self.memory.get_session_history(
            self.user_id, self.conversation_id
        ).messages

        # Get answer
        content = self.denier.invoke(input_message).content

        # Save to memory
        memory = self.memory.get_session_history(self.user_id, self.conversation_id)
        memory.add_user_message(user_input["customer_input"])
        memory.add_ai_message(content)

        return content
    
    def handle_process_externals(self, link: Optional[str]) -> None:
        """Processes external files, by getting their texts, splitting them and storing them in the vector database. This will be handled by UI elements to avoid excessive token usage.>"""

        self.pdfprocesser.invoke()

        if link is not None:
            self.webprocesser.invoke(link)
        
        return "External Documents Processed"

    def handle_personal_info(self, user_input: Dict[str, str]) -> str:
        """Handles the request to manage personal information"""

        # Feature available only to logged in users
        if self.user_id == "-1":
            return self.handle_denial(user_input)

        # Prepare reuqest
        input_message = {}
        input_message['id'] = self.user_id
        input_message['customer_message'] = user_input['customer_input']
        input_message["chat_history"] = self.memory.get_session_history(
            self.user_id, self.conversation_id
        ).messages

        # Get result
        try:
            out = self.userinfomanager.invoke(input_message)
        except Exception as e:
            print("DEBUG: ERROR OCCURRED", e)
            user_input['exception'] = str(e)
            return self.handle_error(user_input)
        
        # Parse result
        try:
            content = out.content
        except:
            content = out['output']

        # Save to memory
        memory = self.memory.get_session_history(self.user_id, self.conversation_id)
        memory.add_user_message(user_input["customer_input"])
        memory.add_ai_message(content)

        return content
    
    def handle_search_scholarships_and_internationals(self, user_input: Dict[str, str]) -> str:
        """This feature is merged with below as they are similar"""
        
        return self.handle_search_universities_and_courses(user_input)

    def handle_search_universities_and_courses(self, user_input: Dict[str, str]) -> str:
        """Handles the request to search the database for courses, scholarships, internationals or universities."""

        # Prepare message for chain
        input_message = {}
        input_message['customer_input'] = user_input['customer_input']
        memory = self.memory.get_session_history(self.user_id, self.conversation_id)
        input_message["chat_history"] = self.memory.get_session_history(
            self.user_id, self.conversation_id
        ).messages
        # Fallback case for guest
        if self.user_id == "-1":
            input_message['user_info'] = "NO USER INFO AVAIBLE: USER IS IN GUEST MODE"
        else:
            user_info = self.userinfofetcher.invoke(self.user_id)
            input_message['user_info'] = str(user_info)

        # Get UniInfo
        try:
            to_describe = self.uniinfosearcher.invoke({'customer_input': user_input['customer_input']})
        except Exception as e:
            print("DEBUG: ERROR OCCURRED", e)
            user_input['exception'] = str(e)
            return self.handle_error(user_input)
        
        input_message['to_describe'] = to_describe

        # Describe UniInfo
        try:
            response = self.uniinforeponser.invoke(input_message).content
        except Exception as e:
            print("DEBUG: ERROR OCCURRED", e)
            user_input['exception'] = str(e)
            return self.handle_error(user_input)

        # Save to Memory
        memory.add_user_message(user_input["customer_input"])
        memory.add_ai_message(response)

        return response

    def handle_matchmaking(self, user_input: Dict[str, str]) -> str:
        """Handles request to make matches."""

        if self.user_id == "-1": # Feature available only for non-guests
            return self.handle_denial(user_input)

        # Prepare two input messages; one to make the matches, other to describe the maches.
        input_message = {}
        final_message = {}

        input_message['id'] = self.user_id
        input_message['customer_message'] = user_input['customer_input']
        input_message["chat_history"] = self.memory.get_session_history(
            self.user_id, self.conversation_id
        ).messages

        try: # Make matches
            matches = self.matchmaker.invoke(input_message)
        except Exception as e:
            print("DEBUG: ERROR OCCURRED", e)
            user_input['exception'] = str(e)
            return self.handle_error(user_input)

        # Prepare final message
        final_message['id'] = self.user_id
        final_message['user_message'] = user_input['customer_input']
        final_message['matches'] = str(matches)
        final_message['chat_history'] = self.memory.get_session_history(
            self.user_id, self.conversation_id
        ).messages

        try: # Describe matches
            out = self.matchesreponder.invoke(final_message).content
        except Exception as e:
            print("DEBUG: ERROR OCCURRED", e)
            user_input['exception'] = str(e)
            return self.handle_error(user_input)

        # Save to memory
        memory = self.memory.get_session_history(self.user_id, self.conversation_id)
        memory.add_user_message(user_input["customer_input"])
        memory.add_ai_message(out)

        return out


    def handle_query_matches(self, user_input: Dict[str, str]) -> str:
        """Handles request to query matches."""

        if self.user_id == "-1": # Feature available only for non-guests
            return self.handle_denial(user_input)

        # Prepares messages
        input_message = {}
        final_message = {}

        input_message['id'] = self.user_id

        # Get matches
        matches = self.matchesextractor.invoke(input_message) 

        # Prepares final message
        final_message['id'] = self.user_id
        final_message['user_message'] = user_input['customer_input']
        final_message['matches'] = str(matches)
        final_message['chat_history'] = self.memory.get_session_history(
            self.user_id, self.conversation_id
        ).messages


        try: # Describe matches
            out = self.matchesreponder.invoke(final_message).content
        except Exception as e:
            print("DEBUG: ERROR OCCURRED", e)
            user_input['exception'] = str(e)
            return self.handle_error(user_input)
        
        # Save to memory
        memory = self.memory.get_session_history(self.user_id, self.conversation_id)

        memory.add_user_message(user_input["customer_input"])
        memory.add_ai_message(out)

        return out

    def handle_rag(self, user_input: Dict[str, str]) -> str:
        """Handles questions for user-uploaded files. Leverages RAG"""

        # Prepare inptu messages
        input_message = {}
        input_message["customer_input"] = user_input["customer_input"]
        input_message['chat_history'] = self.memory.get_session_history(
            self.user_id, self.conversation_id
        ).messages


        # Classifies whether the user is asking questions about the PDF or the website link
        case_rag = self.ragclassifier.invoke(input_message).content

        if case_rag == 'PDF':
            output = self.pdfreasoner.invoke(input_message).content
        elif case_rag == 'link':
            output = self.webreasoner.invoke(input_message).content
        else:
            # This could be due to the main router's misclassification, so it will be handled as a None intention
            output = self.handle_unknown_intent(input_message)

        # Save to memory
        memory = self.memory.get_session_history(self.user_id, self.conversation_id)
        memory.add_user_message(user_input["customer_input"])
        memory.add_ai_message(output)

        return output

    def handle_company_info(self, user_input: Dict[str, str]) -> str:
        """Handles questions about the company. Leverages RAG"""
    
        # Prepares input message
        input_message = {}

        input_message["customer_input"] = user_input["customer_input"]
        input_message["chat_history"] = self.memory.get_session_history(
            self.user_id, self.conversation_id
        ).messages

        try: # Get answer
            output = self.informer.invoke(input_message)
        except Exception as e:
            print("DEBUG: ERROR OCCURRED", e)
            user_input['exception'] = str(e)
            return self.handle_error(user_input)
        
        # Save to memory
        memory = self.memory.get_session_history(self.user_id, self.conversation_id)
        memory.add_user_message(user_input["customer_input"])
        memory.add_ai_message(output.content)

        return output.content


    def handle_unknown_intent(self, user_input: Dict[str, str]) -> str:
        """Handle unknown intents by providing a chitchat response."""

        # Prepares input
        input_message = {}

        input_message["customer_input"] = user_input["customer_input"]
        input_message["chat_history"] = self.memory.get_session_history(
            self.user_id, self.conversation_id
        ).messages


        try: # Get chitchat answer
            chitchat_output = self.chitchatter.invoke(input_message)
        except Exception as e:
            print("DEBUG: ERROR OCCURRED", e)
            user_input['exception'] = str(e)
            return self.handle_error(user_input)
        
        # Save to memory
        memory = self.memory.get_session_history(self.user_id, self.conversation_id)
        memory.add_user_message(user_input["customer_input"])
        memory.add_ai_message(chitchat_output.content)

        return chitchat_output.content

    def handle_harmful(self, user_input: Dict[str, str]) -> str:
        """Handle harmful intents, such as prompt injection attempts."""
        
        # Prepare input message
        input_message = {}

        input_message["customer_input"] = user_input["customer_input"]
        input_message["chat_history"] = self.memory.get_session_history(
            self.user_id, self.conversation_id
        ).messages

        try: # Get answer
            bot_output = self.discourager.invoke(input_message).content
        except Exception as e:
            print("DEBUG: ERROR OCCURRED", e)
            user_input['exception'] = str(e)
            return self.handle_error(user_input)

        memory = self.memory.get_session_history(self.user_id, self.conversation_id)
        memory.add_user_message(user_input["customer_input"])
        memory.add_ai_message(bot_output)

        return bot_output


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

        # Filter harmful messages
        process_filter = self.filter.invoke(user_input)
        is_harmful = process_filter.is_harmful
        
        if is_harmful:
            return self.handle_harmful(user_input)   
    
        # Classify the user's intent based on their input
        intention = self.get_user_intent(user_input)

        print("Intent:", intention)

        # Route the input based on the identified intention
        handler = self.intent_handlers[intention]
        return handler(user_input)
