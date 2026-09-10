from langgraph.graph import StateGraph, START, END
from typing import TypedDict , Annotated
from langchain_huggingface import HuggingFaceEndpoint,ChatHuggingFace
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage , HumanMessage
# from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool, BaseTool
import asyncio
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
from langgraph.graph.message import add_messages
from langchain_ollama import ChatOllama


load_dotenv()

conn = sqlite3.connect(database='chatbot.db',check_same_thread=False)
# config = {
#     "configurable": {
#             'thread_id' : '1sdsd'
#         }
# }
checkpointer = SqliteSaver(conn=conn)

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage],add_messages]


# model = HuggingFaceEndpoint(
#     repo_id="Qwen/Qwen3.8-2.4T-A95B",
#     task="conversational",
#     max_new_tokens=200,
#     temperature=0,
# )

# llm = ChatHuggingFace(llm=model, verbose=True)

llm = ChatOllama(
    model="gpt-oss:120b-cloud",
    temperature=0,
    # other params...
)

def chat_node(state: ChatState):
    messages = state["messages"]
    response =  llm.invoke(messages)

    return {
        "messages": [response]
    }



graph = StateGraph(ChatState)


graph.add_node(chat_node,'chat_node')
graph.add_edge(START,'chat_node')
graph.add_edge("chat_node", END)


     
chatbot = graph.compile(checkpointer=checkpointer)

def retrive_all_threads():
    all_threads = set()  # we used set here so that it help to store unique.
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])
    return list(all_threads)

# result  =  chatbot.invoke({
#             "messages": [
#                 "what is the 22k gold means"
#             ]
# }, config=config)

# print(result["messages"][-1].content)
