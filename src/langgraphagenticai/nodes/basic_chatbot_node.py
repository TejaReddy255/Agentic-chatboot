
from src.langgraphagenticai.state.state import State


class BasicChatbotNode:
    """A basic chatbot node that can be used as a starting point for building more complex chatbot nodes. This node can be used to handle simple conversations and can be extended to include more advanced features such as natural language processing, sentiment analysis, and more.
    """
    def __init__(self, model):
        self.llm =model
    
    def process(self, state:State)->dict:
        """Process the input and return a response. This method can be overridden to implement custom behavior for the chatbot node.
        """

        return {"messages": self.llm.invoke(state["messages"])}