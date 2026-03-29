from typing_extensions import Annotated, TypedDict
from langgraph.graph.message import add_messages

class State(TypedDict):
    """Represent the structure of the state used in graph
    This state is used to store the current state of the graph, including the messages and any other relevant information. It can be extended to include additional fields as needed.
    """
    messages:Annotated[list, add_messages]
   