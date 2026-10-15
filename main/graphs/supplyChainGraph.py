from langchain_core.tools import tool

from langgraph.graph import StateGraph
from typing import TypedDict, Annotated, List, Literal, Dict, Any
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph.message import add_messages

from supplyChainBot.main.config import llm
from langgraph_supervisor import create_supervisor
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

from supplyChainBot.main.graphs.dynamicDataRetrieval import doSKUReorder, getInventoryDetails, getShipmentDetails
from supplyChainBot.main.graphs.retrieveVectorSearchData import getVectorStoreData



class SupplyChainState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]

RAG_Tool = create_agent(
    model=llm,
    tools=[getVectorStoreData],
    system_prompt="You are RAG agent who is responsible to retrive raw excerpts with source metadata",
    name="RAGAgent"
)

LiveData_Tool = create_agent(
    model=llm,
    tools=[getInventoryDetails, getShipmentDetails, doSKUReorder],
    system_prompt="You are agent who is responsible to perform the operations in the API which handles dynamic data."
                    "Verify the query, if it's about retrieval information, perform the required GET operation"
                    "If the query is about psting any data or require the mainulation of the data, perform the required POST call",
    name="LiveDataAgent"
)

agentSupervisor = create_supervisor(
    model=llm,
    prompt="You are a Supply chain bot agent assign task accordingly"
            "If the query is about retrieval of static data from knowledge base like to get policy details, call the RAG tool"
            "If it's about the dynamic data which changes day to day, call the LIVE data tool",
    agents=[RAG_Tool, LiveData_Tool]
)

app = agentSupervisor.compile(checkpointer=InMemorySaver())
