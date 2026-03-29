from src.langgraphagenticai.graph.graph_builder import GraphBuilder
from src.langgraphagenticai.llms.groqllm import GroqLLM
import streamlit as st
from src.langgraphagenticai.UI.streamlitui.loadui import LoadStreamlitUI
from src.langgraphagenticai.UI.streamlitui.display_results import DisplayResults

def load_langgraph_agent_app():
    """Load the LangGraph agent application.
    
        This function initializes the Streamlit UI for the LangGraph agent application, allowing users to select their preferred LLM, use case, and other configurations. It returns a dictionary containing the user's selections and inputs for further processing in the application.

    Return: A dictionary containing the user's selections and inputs from the Streamlit UI, including:
        - 'selected_llm': The LLM selected by the user.     
        - 'selected_groq_model': The Groq model selected by the user (if Groq is selected as the LLM).
        - 'groq_api_key': The API key entered by the user for Groq (
            if Groq is selected as the LLM).
        - 'selected_usecase': The use case selected by the user.

    """
    
    ui_loader = LoadStreamlitUI()
    user_control = ui_loader.load_streamlit_ui()
    if not user_control:
        st.error("Error loading user controls. Please check the Streamlit UI configuration.")
        return
    if st.session_state.get('Isfetchbuttonclicked') and user_control.get('selected_usecase')=="AI NEWS":
        user_message=st.session_state.get('time_frame')
    else:
        user_message=st.chat_input("Enter your message:")
    if user_message:
        try:
            ## Configure LLM
            obj_llm_config=GroqLLM(user_controls=user_control)
            llm_model=obj_llm_config.get_llm_model()
            if llm_model is None:
                st.error("LLM model could not be initialized. Please check your API key and model selection.")
                return
            usecase=user_control.get('selected_usecase')
            if not usecase:
                st.error("Please select a use case to proceed.")
                return
            graph_builder = GraphBuilder(model=llm_model)
            try:
                graph=graph_builder.stepup_graph(usecase=usecase)
               
                DisplayResults(usecase, graph, user_message).display_chatbot_response()
            except Exception as e:
                st.error(f"Error setting up the graph: {str(e)}")
                return
        except Exception as e:
            st.error(f"Error configuring LLM: {str(e)}")
            return
            
            
            
    
    return user_control
