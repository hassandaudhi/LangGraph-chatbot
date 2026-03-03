from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict, Literal
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict, Literal, Annotated
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage,AIMessage, SystemMessage, HumanMessage
from langgraph.graph.message import add_messages 
from langgraph.checkpoint.memory import MemorySaver 


class ChatState(TypedDict) :
    messages: Annotated[list[BaseMessage], add_messages]

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
def chat_node(state: ChatState) :
    # Take user query 
    messages = state['messages']
    # Send to llm 
    response = llm.invoke(messages)
    # Save the response in state
    return {'messages' : [response]}

checkpointer = MemorySaver()

graph = StateGraph(ChatState)
graph.add_node('chat_node',chat_node)
graph.add_edge(START,'chat_node')
graph.add_edge('chat_node',END)

chatbot = graph.compile(checkpointer = checkpointer)

