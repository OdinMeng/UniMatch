# Import necessary classes and modules for chatbot functionality
from typing import Callable, Dict, Optional

from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

# from UniMatch.chatbot.agents.agent1 import Agent1
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

from UniMatch.chatbot.memory import MemoryManager
from UniMatch.chatbot.router.loader import load_intention_classifier

#TODO: DELETE
from UniMatch.chatbot.chains.parse_to_objects import ConvertRawToPreferences

class MainChatbot:
    """
    A bot that handles customer service interactions by processing user inputs and
    routing them through configured reasoning and response chains.
    """

    def __init__(self):
        """Initialize the bot with session and language model configurations."""
        # Initialize the memory manager to manage session history
        self.memory = MemoryManager()

        # Configure the language model with specific parameters for response generation
        self.llm = ChatOpenAI(temperature=0.0, model="gpt-4o-mini")

        # Import chains
        self.filter = ControlChain(llm = self.llm)
        self.discourager = DiscourageUserChain(llm = self.llm)
        
        self.chitchatter = ConversationChain(llm = self.llm)
        
        self.informer = CompanyInformationChain(llm = self.llm)
        
        self.pdfprocesser = ProcessPDFChain()
        self.pdfreasoner = ReasoningPDFChain(llm = self.llm)
        self.webprocesser = ProcessWebsiteChain(llm = self.llm)
        self.webreasoner = ReasoningWebsiteChain(llm = self.llm)

        self.ragclassifier = ClassifyRAG(llm = self.llm)
        self.userinfofetcher = UserInfoFetchChain(llm = self.llm)

        self.uniinfosearcher = UniInfoSearchChain(llm = self.llm)
        self.uniinforeponser = UniInfoResponseChain(llm = self.llm)

        self.matchmaker = MakeMatchesChain(llm = self.llm)
        self.matchesextractor = ExtractMatchesChain(llm = self.llm)
        self.matchesreponder = MatchesResponseChain(llm = self.llm)

        self.userinfomanager = UserInfoManager(llm = self.llm)

        self.denier = DenyUserIntentionChain(llm = self.llm)

        # Map intent names to their corresponding reasoning and response chains
        self.chain_map = {
        }

        # self.agent_map = {
        #     "order": self.add_memory_to_runnable(Agent1(llm=self.llm).agent_executor)
        # }

        # self.rag = self.add_memory_to_runnable(
        #    RAGPipeline(
        #        index_name="rag",
        #        embeddings_model="text-embedding-3-small",
        #        llm=self.llm,
        #        memory=True,
        #   ).rag_chain
        #)

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

    '''
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
    '''
    def handle_denial(self, user_input: Dict[str, str]) -> str:
        input_message = {}
        input_message['user_prompt'] = user_input['customer_input']
        input_message["chat_history"] = self.memory.get_session_history(
            self.user_id, self.conversation_id
        ).messages

        content = self.denier.invoke(input_message).content

        memory = self.memory.get_session_history(self.user_id, self.conversation_id)

        memory.add_user_message(user_input["customer_input"])
        memory.add_ai_message(content)

        return content


    def handle_personal_info(self, user_input: Dict[str, str]) -> str:
        input_message = {}

        if self.user_id == "-1":
            return self.handle_denial(user_input)

        input_message['id'] = self.user_id
        input_message['customer_message'] = user_input['customer_input']
        input_message["chat_history"] = self.memory.get_session_history(
            self.user_id, self.conversation_id
        ).messages

        out = self.userinfomanager.invoke(input_message)
        try:
            content = out.content
        except:
            content = out['output']

        memory = self.memory.get_session_history(self.user_id, self.conversation_id)

        memory.add_user_message(user_input["customer_input"])
        memory.add_ai_message(content)

        return content
    
    def handle_search_scholarships_and_internationals(self, user_input: Dict[str, str]) -> str:
        # We decided to merge this with the universities and courses since that they're implemented by the same chains
        return self.handle_search_universities_and_courses(user_input)

    def handle_search_universities_and_courses(self, user_input: Dict[str, str]) -> str:
        input_message = {}
        input_message['customer_input'] = user_input['customer_input']

        memory = self.memory.get_session_history(self.user_id, self.conversation_id)
        input_message["chat_history"] = self.memory.get_session_history(
            self.user_id, self.conversation_id
        ).messages

        if self.user_id == "-1":
            input_message['user_info'] = "NO USER INFO AVAIBLE: USER IS IN GUEST MODE"

        else:
            user_info = self.userinfofetcher.invoke(self.user_id)
            input_message['user_info'] = str(user_info)

        to_describe = self.uniinfosearcher.invoke({'customer_input': user_input['customer_input']})
        input_message['to_describe'] = to_describe

        response = self.uniinforeponser.invoke(input_message).content

        memory.add_user_message(user_input["customer_input"])
        memory.add_ai_message(response)

        return response

    def handle_matchmaking(self, user_input: Dict[str, str]) -> str:
        input_message = {}
        final_message = {}

        input_message['id'] = self.user_id

        if self.user_id == "-1":
            return self.handle_denial(user_input)

        input_message['customer_message'] = user_input['customer_input']
        input_message["chat_history"] = self.memory.get_session_history(
            self.user_id, self.conversation_id
        ).messages

        matches = self.matchmaker.invoke(input_message)

        final_message['id'] = self.user_id
        final_message['user_message'] = user_input['customer_input']
        final_message['matches'] = str(matches)
        final_message['chat_history'] = self.memory.get_session_history(
            self.user_id, self.conversation_id
        ).messages

        out = self.matchesreponder.invoke(final_message).content

        memory = self.memory.get_session_history(self.user_id, self.conversation_id)
        memory.add_user_message(user_input["customer_input"])
        memory.add_ai_message(out)

        return out


    def handle_query_matches(self, user_input: Dict[str, str]) -> str:
        input_message = {}
        final_message = {}

        input_message['id'] = self.user_id

        if self.user_id == "-1":
            return self.handle_denial(user_input)

        matches = self.matchesextractor.invoke(input_message)

        final_message['id'] = self.user_id
        final_message['user_message'] = user_input['customer_input']
        final_message['matches'] = str(matches)
        final_message['chat_history'] = self.memory.get_session_history(
            self.user_id, self.conversation_id
        ).messages

        memory = self.memory.get_session_history(self.user_id, self.conversation_id)

        out = self.matchesreponder.invoke(final_message).content

        memory.add_user_message(user_input["customer_input"])
        memory.add_ai_message(out)

        return out

    def handle_rag(self, user_input: Dict[str, str]) -> str:
        memory = self.memory.get_session_history(self.user_id, self.conversation_id)

        input_message = {}
        input_message["customer_input"] = user_input["customer_input"]

        case_rag = self.ragclassifier.invoke(input_message).content

        if case_rag == 'PDF':
            # self.pdfprocesser.invoke() This will be done by using UI
            output = self.pdfreasoner.invoke(input_message).content
        elif case_rag == 'link':
            # self.webprocesser.invoke() same as above
            output = self.webreasoner.invoke(input_message).content
        else:
            output = 'The file you mentioned seems to be non-existant. Please retry.'

        memory.add_user_message(user_input["customer_input"])
        memory.add_ai_message(output)

        return output

    def handle_company_info(self, user_input: Dict[str, str]) -> str:
        companyinfo_chain = self.informer

        input_message = {}

        memory = self.memory.get_session_history(self.user_id, self.conversation_id)

        input_message["customer_input"] = user_input["customer_input"]
        input_message["chat_history"] = self.memory.get_session_history(
            self.user_id, self.conversation_id
        ).messages

        output = companyinfo_chain.invoke(input_message)

        memory.add_user_message(user_input["customer_input"])
        memory.add_ai_message(output.content)

        return output.content


    def handle_unknown_intent(self, user_input: Dict[str, str]) -> str:
        """Handle unknown intents by providing a chitchat response.

        Args:
            user_input: The input text from the user.
        

        Returns:
            The content of the response after processing through the new chain.
        """
        chitchat_reasoning_chain = self.chitchatter

        input_message = {}

        input_message["customer_input"] = user_input["customer_input"]
        input_message["chat_history"] = self.memory.get_session_history(
            self.user_id, self.conversation_id
        ).messages

        memory = self.memory.get_session_history(self.user_id, self.conversation_id)

        chitchat_output = chitchat_reasoning_chain.invoke(input_message)

        memory.add_user_message(user_input["customer_input"])
        memory.add_ai_message(chitchat_output.content)

        return chitchat_output.content

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
        
        # ================== Process Message Router ==================================|
        # If harmful                                                                  |
        if is_harmful:                                                               #|
            return self.discourager.invoke(user_input).content                       #|
                                                                                     #|
        # If NOT harmful                                                             #|
        # ================== Main Router =============================================|
    
        # Classify the user's intent based on their input
        intention = self.get_user_intent(user_input)

        print("Intent:", intention)

        # Route the input based on the identified intention
        handler = self.intent_handlers[intention]
        return handler(user_input)
