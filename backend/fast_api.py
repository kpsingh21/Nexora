from fastapi import FastAPI
# from backend.chatbot import chatbot ,retrive_all_threads
from backend.chatbotv2 import chatbot ,retrive_all_threads
# from chatbotv2 import chatbot ,retrive_all_threads

from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


# Allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173",   "http://127.0.0.1:5173",],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




class MessageInput(BaseModel):
    msg : str
    thread_id:str

@app.get("/")
def greet():
    return 'welcome'


# Assuming your Pydantic schema looks something like this
class MessageInput(BaseModel):
    msg: str
    thread_id: str

@app.post("/chat")
def chat_backend(payload: MessageInput):
    print("Received:", payload.msg)
    
    # Unified quote styles for cleaner syntax
    config = {
        "configurable": {
            "thread_id": payload.thread_id
        }
    }
    
    # Invoking the LangChain agent/chatbot
    res = chatbot.invoke(
        {"messages": [payload.msg]}, 
        config=config
    )
    
    print("Response:", res)
    
    # If res is a LangChain Message object (e.g., AIMessage), 
    # you might want to return res.content instead of the whole object.
    return {
        "status": "success",
        "received_message": res
    }

@app.get("/retrive_all_threads")
def retrive_all_uniquethreads():
    all_threads = retrive_all_threads()
    return all_threads

@app.post("/load_convo/{thread_id}")
async def update_item(thread_id: str):
    state = chatbot.get_state(config={'configurable': {'thread_id': thread_id}})
    # Check if messages key exists in state values, return empty list if not
    print("hii",state.values.get('messages', []))
    return state.values.get('messages', [])



# messageHistory = [
#     {
#       "role": "user",
#       "text": "How do I configure a webhook?",
#       "timestamp": "2026-09-09T14:30:00Z"
#     },
#     {
#       "role": "assistant",
#       "type": "generative_answer",
#       "text": "To configure a webhook in your system, you need to navigate to **Settings > Integrations** [1]. There, you will find options for multiple types of alerts [2].",
#       "timestamp": "2026-09-09T14:30:02Z"
#     }
#   ],


# @app.post("/load_convo/{thread_id}")
# async def update_item(thread_id: str):
#     # state = chatbot.get_state(config={'configurable': {'thread_id': thread_id}})
#     # Check if messages key exists in state values, return empty list if not
#     # convo = state.values.get('messages', [])
#     # thread_id = f"thread_id + {thread_id}"
#     return messageHistory