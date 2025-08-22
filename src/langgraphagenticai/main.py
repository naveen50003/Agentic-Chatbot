import streamlit as st

from src.langgraphagenticai.ui.streamlitui.loadui import LoadStreamlitUI
from src.langgraphagenticai.LLMS.groqllm import GroqLLM
from src.langgraphagenticai.graph.graph_builder import GraphBuilder
from src.langgraphagenticai.ui.streamlitui.display_result import DisplayResultsStreamlit

def load_langgraph_agenticai_app():
    """
        Loads and runs the Langgraph AgenticAI application with streamlit Ui.
        This function initializes the UI, handles user input, configures the LLM Model
        sets up the graph based on the selected use case and displays the output while implementing exception handling for robustness.
    """
   
   ## Load Ui
    ui = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()

    if not user_input:
       st.error("Error::: Failed to load user input on UI.")

    
    if st.session_state.IsFetchButtonClicked:
        user_message = st.session_state.timeframe 

    else:
        user_message = st.chat_input("Enter your message:")

    print("user_message")
    print(user_message)
    if user_message:
        try:
            obj_llm_config = GroqLLM(user_controls_input=user_input)
            model=obj_llm_config.get_llm_model()

            if not model:
                st.error("Error: LLm Model could not be initialized")
                return
            
            usecase= user_input.get("selected_usecase")

            if not usecase:
                st.error("Error: No Usecase is selected")
                return
            
            graph_builder = GraphBuilder(model)

            try:
                graph = graph_builder.setup_graph(usecase)
                DisplayResultsStreamlit(usecase,graph,user_message).display_result_on_ui()
            except Exception as e:
                st.error(f"Error: Graph set up failed. {e}")
                return
            
        except Exception as e:
            st.error(f"Error: user_message failed. {e}")
            return