from src.langgraphagenticai import graph
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage,ToolMessage
import json

class DisplayResults:
    """Class to handle the display of results in the Streamlit UI.
    This class provides methods to display messages and results in a structured format, making it easier for users to understand the interactions with the LangGraph agent.
    """
    
    def __init__(self,usercase,graph,user_message):
        self.usercase = usercase
        self.graph = graph
        self.user_message = user_message
    
    def display_chatbot_response(self):
        """Display the chatbot response in the Streamlit UI. This method retrieves the response from the graph and displays it in a user-friendly format.
        """
       
        usecase=self.usercase
        graph=self.graph
        user_message=self.user_message
        if usecase == "Basic Chat Bot":
            print("Displaying chatbot response...")
            for event in graph.stream({'messages': ("user", user_message)}):
                print(event.values())
                for value in event.values():
                    print(f"Received value: {value}")
                    print(value['messages'])
                    with st.chat_message("user"):
                        st.write(user_message)
                    with st.chat_message("assistant"):
                        print(f"Assistant message: {value['messages']}")
                        st.write(value['messages'].content)
        elif usecase == "Chat Bot with Web Search":
            initial_state = {'messages': [user_message]}
            for output in graph.stream(initial_state):
                for _, state_update in output.items():
                    new_messages = state_update.get("messages")
                    
                    # Handle both single messages and lists of messages
                    if not isinstance(new_messages, list):
                        messages_to_process = [new_messages]
                    else:
                        messages_to_process = new_messages

                    for msg in messages_to_process:
                        if isinstance(msg, AIMessage):
                            with st.chat_message("assistant"):
                                st.write(msg.content)
                        elif isinstance(msg, ToolMessage):
                            with st.chat_message("assistant"):
                                # Depending on your ToolMessage version, 
                                # use .content or custom attributes
                                st.write(f"**Tool Output:** {msg.content}")
                        elif isinstance(msg, HumanMessage):
                            with st.chat_message("user"):
                                st.write(msg.content)
        elif usecase == "AI NEWS":
            frequency=self.user_message
           
            with st.spinner("Fetching and processing AI news..."):
                result= graph.invoke({'messages': frequency})
                try:

                    AI_NEWS_PATH=F'./AINews/{frequency}_summary.md'
                    with open(AI_NEWS_PATH, 'r') as file:
                        news_summary = file.read()
                    st.markdown(news_summary,unsafe_allow_html=True)
                except FileNotFoundError:
                    st.error(f"Summary file for '{frequency}' news not found. Please ensure the graph has been executed to fetch and summarize the news.")
                except Exception as e:
                    st.error(f"Error loading news summary: {str(e)}")