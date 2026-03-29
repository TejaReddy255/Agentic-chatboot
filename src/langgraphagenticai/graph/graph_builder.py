from langgraph.graph import StateGraph, START, END 
from src.langgraphagenticai.nodes.basic_chatbot_node import BasicChatbotNode
from src.langgraphagenticai.state.state import State
from src.langgraphagenticai.tools.search_tool import get_tools,create_tool_nodes
from langgraph.prebuilt import tools_condition
from src.langgraphagenticai.nodes.tool_chatbot_node import ChatbotToolNode
from src.langgraphagenticai.nodes.ai_new_node import AiNewsNode
class GraphBuilder:

    def __init__(self,model):
        self.llm = model
        self.graph_builder = StateGraph(State)


    def basic_chatbot_graph(self):
        """ Build a basic chatbot graph. This graph consists of a 
        single chatbotnode that processes the input and returns a response. 
        The graph can be extended to include additional nodes and edges as needed.
        """  
        self.basic_chatbot_node = BasicChatbotNode(self.llm)
        self.graph_builder.add_node("chatbot", self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_edge("chatbot", END)
    
    def chatbot_with_tools_graph(self):        
        """ Builds a chatbot graph that includes tool usage. 
        This graph consists of a chatbot node that can call external tools 
        to process the input and return a response. The graph can be extended 
        to include additional nodes and edges as needed.
        """

        # define the tool node and toolnode
        tools = get_tools()
        tool_node = create_tool_nodes(tools)

        llm=self.llm
        self.graph_builder.add_node("chatbot", ChatbotToolNode(llm).create_chatbot(tools))
        self.graph_builder.add_node("tools", tool_node) 
        self.graph_builder.add_edge(START, "chatbot")
        
        self.graph_builder.add_conditional_edges("chatbot",tools_condition,{
            "tools": "tools",   # Matches the node name added above
            "__end__": END      # Standard LangGraph termination
        })
        self.graph_builder.add_edge( "tools","chatbot")
        
    def ai_news_graph_builder(self):
        """Builds a chatbot graph that provides AI news updates. 
        This graph consists of a chatbot node that can call an external tool 
        to fetch the latest AI news and return it as a response. The graph can be extended to include additional nodes and edges as needed.
        """
        ainews=AiNewsNode(self.llm)
        self.graph_builder.add_node("fetch_news", ainews.fetch_news)
        self.graph_builder.add_node("summarize_news", ainews.summarize_news)
        self.graph_builder.add_node("save_news", ainews.save_news)

        self.graph_builder.set_entry_point("fetch_news")
        self.graph_builder.add_edge("fetch_news","summarize_news")
        self.graph_builder.add_edge("summarize_news","save_news")
        self.graph_builder.add_edge("save_news",END)


    def stepup_graph(self,usecase=None):
        """Set up the graph by building the basic chatbot graph. This method can be extended to include additional setup steps as needed.
        """
        
        if usecase == "Basic Chat Bot":
            self.basic_chatbot_graph()   
        elif usecase == "Chat Bot with Web Search":
            self.chatbot_with_tools_graph()       
        elif usecase == "AI NEWS":
            self.ai_news_graph_builder()

        return self.graph_builder.compile()