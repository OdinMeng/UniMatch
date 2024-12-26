from langchain.agents import create_tool_calling_agent, AgentExecutor
from UniMatch.chatbot.agents.tools import InformUserTool, ModifyBasicUserInfoTool, ModifyUserPreferencesTool
from UniMatch.chatbot.chains.base import PromptTemplate, generate_agent_prompt_template
from langgraph.prebuilt import create_react_agent
from langchain.tools import BaseTool

class UserInfoManager:
    def __init__(self, llm):
        self.llm = llm
        self.toolkit = [InformUserTool(), ModifyBasicUserInfoTool(), ModifyBasicUserInfoTool()]

        prompt_template = PromptTemplate(
        system_template = """
        You are a helpful and resourceful assistant, tasked with managing users' personal information.
        
        You have access to the following tools:
        ExtractUserInformationTool: Use this tool when a user requests what the chatbot knows about himself
        ModifyUserInformationTool: Use this tool when you want to handle a user's request to modify a certain variable of his personal information
        ModifyUserPreferences: Use this tool when the user requests to modify his user preferences

        When a user asks you a question, think step-by-step about how to answer it. If needed, use one of the tools to assist you, and clearly explain your reasoning.

        Example Workflow:
        1. Understand the user's question.
        2. Determine which tool (if any) can help.
        3. Use the tool by providing the correct input.
        4. Return the tool's result and parse it as a friendly answer

        You have access to the chat history to personalize the answer. If you think that you cannot handle the user requests with your tools, do not do anything and say that to the user.
        """,

        human_template="User ID: {id}\nUser's Request: {customer_message}"
        )

        self.prompt = generate_agent_prompt_template(prompt_template=prompt_template)
        self.agent = create_tool_calling_agent(llm, self.toolkit, self.prompt)
        self.agent_executor = AgentExecutor(agent=self.agent, tools=self.toolkit)

    def invoke(self, customer_input):
        """
        NEEDED:
            - chat_history
            - id
            - customer_message        
        """
        return self.agent_executor.invoke({'chat_history': customer_input['chat_history'], 
                                    'id': customer_input['id'],
                                    'customer_message': customer_input['customer_message']})