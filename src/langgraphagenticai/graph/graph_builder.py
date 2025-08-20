from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from src.langgraphagenticai.state.state import State
from src.langgraphagenticai.tools.basic_chatbot_node import BasicChatbotNode
from src.langgraphagenticai.tools.search_tool import get_tools, create_tool_node
from src.langgraphagenticai.tools.chatbot_with_Tool_node import ChatbotWithToolNode

class GraphBuilder:
    def __init__(self,model):
        self.llm = model
        self.graph_builder = StateGraph(State)

    def basic_chatbot_build_graph(self):
        """
        Builds a basci chatbot graph using LangGraph
        This method initializes a chatbot node usin the `BasicChatBotNode` class
        and integrate it into the graph. The chatbot node is set as both the
        entry and exit point of the graph.
        """

        self.basic_chatbot_node = BasicChatbotNode(self.llm)
        
        self.graph_builder.add_node("chatbot",self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_edge("chatbot", END)

    def chatbot_with_tools_build_graph(self):
        """
        Builds a advance chatbot graph with tool integreation
        This method creates a chatbot graph that indicates both a chatbot node
        and a tool node. It defines tools, initializes the chatbot with tool
        capabilities and sets up conditional and direct edges between nodes.
        The chatbot node is set as the entry point
        """

        tools= get_tools()
        tool_node = create_tool_node(tools)

        obj_chatbot_with_node = ChatbotWithToolNode(self.llm)
        chatbot_node = obj_chatbot_with_node.create_chatbot(tools)
        
        self.graph_builder.add_node("chatbot",chatbot_node)
        self.graph_builder.add_node("tools",tool_node)


        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_conditional_edges("chatbot", tools_condition)
        self.graph_builder.add_edge("tools", "chatbot")

        

    def setup_graph(self, usecase: str):
        """
         set up the graph for the selected use case
        """
        if usecase == "Basic Chatbot":
            self.basic_chatbot_build_graph()
        if usecase == "Chatbot With Web":
            print("entere usecase2")
            self.chatbot_with_tools_build_graph()

        return self.graph_builder.compile()