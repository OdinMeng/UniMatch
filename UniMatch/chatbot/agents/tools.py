# Define tools for PersonalInformationManager 
# Tools:
#   - ModifyBasicUserInfoTool: modifies a specific information about the user. 
#       - Figures out the keywords () -> runs external function -> gets result -> runs external function
#   - ModifyUserPreferencesTool: modifies user preferences
#       - Figures out user preferences -> runs external function -> gets result -> runs external function
#   - InformUserTool:
#       - Extracts user info (chain)

# Import modules
from typing import Type, Any, Dict
from langchain.tools import BaseTool
from langchain_openai import ChatOpenAI

# Import external functions
from UniMatch.data.user_info import modify_user_info, modify_user_preferences
from UniMatch.chatbot.chains.userinfofetchchain import UserInfoFetchChain
from UniMatch.chatbot.chains.extractmodificationrequestchain import ExtractModificationRequestChain, ModificationRequest
from UniMatch.chatbot.chains.parse_to_objects import ConvertRawToPreferences
from UniMatch.chatbot.bot_objects import Preferences
from pydantic import BaseModel
from dotenv import load_dotenv

class CustomerInput(BaseModel):
    id: int
    customer_message: str

# Define tools
class InformUserTool(BaseTool):
    name : str = "ExtractUserInformationTool"
    description : str = "Use this tool when a user requests what the chatbot knows about himself"
    args_schema: Type[BaseModel] = CustomerInput
    return_direct: bool = False

    def _run(self, id: int, customer_message: str) -> str:
        """
        ARGUMENTS:
            - id: User ID
            - customer_message: User Input
        """
        llm = ChatOpenAI(model="gpt-4o-mini")
        userinfofetcher = UserInfoFetchChain(llm)

        userinfo = userinfofetcher.invoke(userid=id)

        return userinfo

class ModifyBasicUserInfoTool(BaseTool):
    name: str = "ModifyUserInformationTool"
    description: str = "Use this tool when you want to handle a user's request to modify a certain variable of his personal information."
    args_schema: Type[BaseModel] = CustomerInput
    return_direct: bool = False

    def _run(self, id: int, customer_message: str) -> str:
        """
        ARGUMENTS:
            - id: User ID
            - customer_message: User Input
        """
        llm = ChatOpenAI(model="gpt-4o-mini")
        extractor = ExtractModificationRequestChain(llm)
        modifier = modify_user_info

        args : ModificationRequest = extractor.invoke({'customer_input': customer_message})

        if args.column==None or args.new_info==None:
            return "Operation Not Accepted"
        
        result : int = modifier(userid=id, column=args.column, new_info=args.new_info)

        if result == 0:
            return "Operation Successful"
        elif result == -1:
            return "Operation Failed"
        else:
            return "Unexpected Result" # this should NOT happen
        
class ModifyUserPreferencesTool(BaseTool):
    name : str = "ModifyUserPreferences"
    description: str = "Use this tool when the user requests to modify his user preferences."
    args_schema: Type[BaseModel] = CustomerInput
    return_direct: bool = False

    def _run(self, id:int , customer_message:str) -> str:
        """
        ARGUMENTS:
            - id: User ID
            - customer_message: User Input
        """
        llm = ChatOpenAI(model="gpt-4o-mini")
        preferences_parser = ConvertRawToPreferences(llm)
        modifier = modify_user_preferences
    
        new_preferences : Preferences = preferences_parser.invoke({'raw': customer_message})
        result : int = modifier(userid=id, new_preferences=new_preferences)

        if result == 0:
            return "Operation Successful"
        
        elif result == 1:
            return "Operation Failed (Invalid Input Structure)"
        
        elif result == 2:
            return "Operation Failed (Invalid Weights)"
        
        elif result == 3:
            return "Operation Failed (Internal SQL Server Error)"
        
        else:
            return "Unexpected Result" # This should not happen