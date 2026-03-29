import os
import streamlit as st
from langchain_groq import ChatGroq

class GroqLLM:
    def __init__(self,user_controls):
        self.user_controls = user_controls
    def get_llm_model(self):

        try:
            groq_api_key=self.user_controls['groq_api_key']
            selected_model=self.user_controls['selected_groq_model']
            if groq_api_key == "" :
                st.error("Please enter your Groq API key to use the Groq LLM.")
                return None
            print(f"Selected Groq model: {selected_model}")
            llm = ChatGroq(model=selected_model, api_key=groq_api_key)
            #print(llm)
        except Exception as e:
            raise ValueError(f"Error initializing Groq LLM: {str(e), llm,selected_model, groq_api_key}")
        return llm
    
    