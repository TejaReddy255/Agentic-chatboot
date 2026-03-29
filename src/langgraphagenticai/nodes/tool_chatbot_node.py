from src.langgraphagenticai.state.state import State    

class ChatbotToolNode:
    """A chatbot node that can call external tools to process the input and return a response. This node can be used to handle more complex conversations and can be extended to include additional features such as natural language processing, sentiment analysis, and more.
    """
    def __init__(self, model):
        self.llm = model
    
    def process(self, state:State)->dict:
        """Process the input and return a response. This method can be overridden to implement custom behavior for the chatbot node.
        """
        user_input =state['messages'][-1] if state['messages'] else ""
        llm_response =self.llm.invoke([{"role": "user", "content": user_input}])

        tools_response = f"Tool interaction for:' {user_input}'"

        return {"messages": [llm_response, tools_response]}
    
    def create_chatbot(self, tools):
        """Create a chatbot node that can call external tools. This method can be extended to include additional logic for creating the chatbot node as needed.
        """
        llm_with_tools=self.llm.bind_tools(tools)
        def chatbot_node(state:State):
            print('hello')
            return {"messages": llm_with_tools.invoke(state["messages"])}
        
        return chatbot_node
