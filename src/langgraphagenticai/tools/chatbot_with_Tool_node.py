from src.langgraphagenticai.state.state import State

class ChatbotWithToolNode:
    """
    chatbot logic enchanced with tool integration 
    """

    def __init__(self, model):
        self.llm = model

    def process(self,state:State):
        """
        Process the input state and generates a response with tool integration
        """

        usr_input = state["messages"][-1] if state["messages"] else ""
        llm_response = self.llm.invoke({"role": "user", "content": usr_input})

        tools_response = f"Tool integration for: `{usr_input}`"
        print("state")
        print(tools_response)
        return {
            "messages": [llm_response, tools_response]
        }
    
    def create_chatbot(self, tools):
        """
        Returns a chatbot node function
        """
        llm_with_tools = self.llm.bind_tools(tools)
        def chatbot_node(state: State):
            """
            Chatbot logic for processing the input state and returning a response.
            """
            print("chatbot_node::")
            print(state)
            return {
                "messages": [llm_with_tools.invoke(state["messages"])]
            }
        return chatbot_node
