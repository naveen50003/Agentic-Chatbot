from src.langgraphagenticai.state.state import State

class BasicChatbotNode:
    """
    Basic Chatbot login implementation
    """

    def __init__(self, model):
        self.llm = model

    def process(self,state:State):
        """
        Process the input state and generates a chatbot response
        """
        print("state")
        print(state)
        return {
            "messages": self.llm.invoke(state["messages"])
        }