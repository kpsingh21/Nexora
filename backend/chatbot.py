from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from langchain_huggingface import HuggingFaceEndpoint,ChatHuggingFace
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage , HumanMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool, BaseTool
import asyncio


load_dotenv()

class ChatState(TypedDict):
    messages: list[str]


model = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen3.8-2.4T-A95B",
    task="conversational",
    max_new_tokens=200,
    temperature=0,
)

llm = ChatHuggingFace(llm=model, verbose=True)

async def chat_node(state: ChatState):
    messages = state["messages"]
    response = await llm_with_tools.ainvoke(messages)
    return {
        "messages": [response]
    }

# graph = StateGraph(ChatState)

client = MultiServerMCPClient(
    {
        "arith": {
            "transport": "stdio",
            "command": "/home/krishna_chouhan/projects/Nexora/.venv/bin/python",
            "args": ["/home/krishna_chouhan/projects/Nexora/expense-tracker-mcp/main.py"],          
        }
        
    }
)

# =========================================================
# LOAD MCP TOOLS
# =========================================================

async def load_mcp_tools() -> list[BaseTool]:

    try:

        tools = await client.get_tools()

        print("\nMCP Tools:")

        for t in tools:
            print("-", t.name)

        return tools

    except Exception as e:

        print("Error loading MCP tools:", e)

        return []


async def main():

    # Load MCP tools

    mcp_tools = await load_mcp_tools()
    
    tools = mcp_tools
    
    # ---------------------------------------------
    # Bind tools
    # ---------------------------------------------

    if tools:

        llm_with_tools_local = llm.bind_tools(tools)

    else:

        llm_with_tools_local = llm
    


    graph = StateGraph(ChatState)


    async def chat_node(state: ChatState):

        messages = state["messages"]

        response = await llm_with_tools_local.ainvoke(
            messages
        )

        return {
            "messages": [response]
        }
    

    
    graph.add_node(chat_node,'chat_node')
    graph.add_edge(START,'chat_node')


       
    if tools:
        tool_node = ToolNode(tools)

        graph.add_node("tools", tool_node)
        graph.add_conditional_edges("chat_node", tools_condition)
        graph.add_edge("tools", "chat_node")
    else:
        graph.add_edge("chat_node", END)

        
    chatbot = graph.compile()

    result  = await chatbot.ainvoke({
            "messages": [
                ""'Add an expense with date 2026-09-05, amount 50, category transport, subcategory empty, and note Traveling to home town for Diwali vacation'""
            ]
    })

        # ---------------------------------------------
        # Print result
        # ---------------------------------------------

    print("\n==============================")
    print("FINAL RESPONSE")
    print("==============================")

    print(
            result["messages"][-1].content
    )


if __name__ == "__main__":
    asyncio.run(main())


