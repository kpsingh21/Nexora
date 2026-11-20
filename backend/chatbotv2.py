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

# to import retriver fun from rag
# from rag.retriever import retriever
from backend.rag.retriever import retriever


load_dotenv()

conn = sqlite3.connect(database='chatbot.db',check_same_thread=False)
# config = {
#     "configurable": {
#             'thread_id' : '1sssffrsdsdddd'
#         }
# }
checkpointer = SqliteSaver(conn=conn)

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage],add_messages]
    context: str
    route: str


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


def route_question(state: ChatState):

    question = state["messages"][-1].content       
    prompt = f"""
    You are a query router for an AI assistant.

    The assistant already has access to a pre-indexed knowledge base
    through a RAG retrieval system.

    Your job is ONLY to decide whether the user's question should be
    answered using:

    RAG  = Search the existing knowledge base for relevant information,
        then use that information to answer.

    DIRECT = Answer directly using the LLM's general knowledge and reasoning,
            without searching the knowledge base.
     
    Return ONLY one word:

    RAG
    or
    DIRECT

    Choose RAG when:
    - The user explicitly refers to a document, file, or the knowledge base.
    - The user asks "according to the document", "from the document", etc.
    - The user asks about private or project-specific information.
    - The answer is likely to be contained in the existing knowledge base.
    - The user asks to summarize, explain, or extract information from
    information stored in the knowledge base.

    Choose DIRECT when:
    - The question can be answered using general knowledge.
    - The user asks for general programming help or code generation.
    - The user asks for general explanations or concepts.
    - The user asks for reasoning, brainstorming, or casual conversation.
    - Searching the knowledge base would not provide useful additional information.

    Important:
    - The documents have ALREADY been indexed.
    - Do NOT interpret this as a request to upload or index a document.
    - Do NOT perform retrieval yourself.
    - Simply decide whether the existing RAG pipeline should be used.
    - Return ONLY one value: RAG or DIRECT.

    User question:
    {question}
    """

    response = llm.invoke(prompt)

    decision = response.content.strip().upper()

    print(decision,"decision")

    return {
        "route": decision
    }

def chat_node(state: ChatState):

    messages = state["messages"]
    context = state.get("context", "")
    route = state.get("route", "DIRECT")

    if route == "RAG":

        system_prompt = f"""
You are a helpful AI assistant.

Answer the user's question using the
retrieved document context below.

Retrieved context:
{context}

Rules:
- Use the context when answering document-related questions.
- Do not invent information.
- If the answer cannot be found in the context,
  clearly say that the information is not available
  in the provided documents.
"""

    else:

        system_prompt = """
You are a helpful general-purpose AI assistant.

Answer the user's question directly using your
general knowledge and reasoning.

You do not need to use any external documents
unless the user explicitly asks about them.
"""

    response = llm.invoke([
        ("system", system_prompt),
        *messages
    ])

    return {
        "messages": [response]
    }


def retrieve_node(state: ChatState):

    question = state["messages"][-1].content
    documents = retriever.invoke(question)
    context = "\n\n".join(
        document.page_content
        for document in documents
    )
    return {
        "context": context
    }


def decide_route(state: ChatState):

    if state["route"] == "RAG":
        return "retrieve_node"

    return "chat_node"

graph = StateGraph(ChatState)


graph.add_node("router", route_question)
graph.add_node(chat_node,'chat_node')
# for RAG retrival
graph.add_node(retrieve_node,'retrieve_node')
graph.add_edge(START,'router')

graph.add_conditional_edges("router",decide_route,{
        "retrieve_node": "retrieve_node",
        "chat_node": "chat_node"
    }
)

graph.add_edge("retrieve_node", "chat_node")
graph.add_edge("chat_node", END)


     
chatbot = graph.compile(checkpointer=checkpointer)

def retrive_all_threads():
    all_threads = set()  # we used set here so that it help to store unique.
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])
    return list(all_threads)

# result  =  chatbot.invoke({
#             "messages": [
#                 "what is AGI in AI"
#             ]
# }, config=config)

# print("myres",(result["messages"]))
