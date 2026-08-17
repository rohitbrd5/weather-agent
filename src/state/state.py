from typing import TypedDict, Annotated, List
import operator
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    """Represents the state of our agent."""
    messages: Annotated[List[BaseMessage], operator.add]
    user_query: str
    tool_output: str
