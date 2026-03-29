from langchain_community.tools.tavily_search import TavilySearchResults

from langgraph.prebuilt import ToolNode

def get_tools():
    """ Return a list of tools to be used in the chatbot graph. This function can be extended to include additional tools as needed.
    """
    tools = [TavilySearchResults(max_results=2)]
    
    return tools

def create_tool_nodes(tools):
    """ Create tool nodes for the given tools. This function can be extended to include additional logic for creating tool nodes as needed.
    """
   
    
    return ToolNode(tools=tools)