import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_core.output_parsers import StrOutputParser
import json

class DisplayResultsStreamlit:
    def __init__(self, usecase,graph, user_message):
        self.usecase= usecase
        self.graph=graph
        self.user_message=user_message

    def display_result_on_ui(self):
        print("display")
        usecase=self.usecase
        graph=self.graph
        user_message= self.user_message
        print(user_message)
        if usecase == 'Basic Chatbot':
            for event in graph.stream({'messages': user_message}):
                print(event)
                print(event.values())
                for value in event.values():
                    print(":::1:::")
                    #print(value)
                    print(value['messages'])
                    with st.chat_message("user"):
                        print(":::2:::")
                        st.write(user_message)
                    with st.chat_message("assistant"):
                        st.write(value["messages"].content)
        
        elif usecase == 'Chatbot With Web':
            initial_state = {"messages": user_message}
            res=graph.invoke(initial_state)
            for message in res["messages"]:
                if type(message) == HumanMessage:
                    with st.chat_message("user"):
                        st.write(message.content)
                elif type(message) == ToolMessage:
                    with st.chat_message("ai"):
                        st.write("Tool call start")
                        st.write(message.content)
                        st.write("Tool call end")

                elif type(message) == AIMessage and message.content:
                    with st.chat_message("assistant"):
                        st.write(message.content)

