import streamlit as st
import os
from src.langgraphagenticai.UI.uiconfigfile import Config

class LoadStreamlitUI:
    def __init__(self):
        self.config = Config()
        self.user_control={}
    def load_streamlit_ui(self):
        st.set_page_config(page_title="🤖 "+self.config.get_page_title(),layout="wide")
        st.title("🤖 "+self.config.get_page_title())
        st.session_state.time_frame=None
        st.session_state.Isfetchbuttonclicked=False

        with st.sidebar:

            llm_options=self.config.get_llm_options()
            usecase_options=self.config.get_usecase_options()
            
            self.user_control['selected_llm']=st.selectbox("Select LLM", llm_options)
            if self.user_control['selected_llm']=="Groq":
                model_options=self.config.get_groq_model_options()
                self.user_control["selected_groq_model"]=st.selectbox("Select Groq Model", model_options)
                self.user_control['groq_api_key']=st.session_state['groq_api_key']=st.text_input("Enter API Key", key="key_input", type="password")
                if not self.user_control['groq_api_key']:
                    st.warning("Please enter your Groq API key to use Groq LLM.")
            self.user_control['selected_usecase']=st.selectbox("Select Use Case", usecase_options)

            if self.user_control['selected_usecase']=="Chat Bot with Web Search" or self.user_control['selected_usecase']=="AI NEWS":
                os.environ['TAVILY_API_KEY'] = self.user_control['tavi_api_key'] = st.session_state['TAVILY_API_KEY'] = st.text_input("Enter Tavi API Key", key="tavi_key_input", type="password")
                if not self.user_control['tavi_api_key']:
                    st.warning("Please enter your Tavi API key to use the Chat Bot with Web Search use case.")

            if self.user_control['selected_usecase']=="AI NEWS":
                
                st.subheader("📰AI News")
                with st.sidebar:
                    time_frame=st.selectbox("📅 Select Time Frame", ["Daily","Weekly", "Monthly"], index=0)
                    if st.button("🔍Get AI News",use_container_width=True):
                        st.session_state['time_frame']=time_frame
                        st.session_state['Isfetchbuttonclicked']=True

        return self.user_control