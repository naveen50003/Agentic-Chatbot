import streamlit as st

from src.langgraphagenticai.ui.streamlitui.loadui import LoadStreamlitUI

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

    user_message = st.chat_input("Enter your message:")