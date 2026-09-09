from fastapi import FastAPI
from backend.chatbot import chatbot
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

@app.get("/")
def greet():
    return 'welcome'

@app.post("/chat")
def chat_backend(payload: MessageInput):

    print("Received:", payload.msg)


    res = chatbot.invoke({
        "messages": [payload.msg]
    })

    print("Response:", res)

    return {
        "status": "success",
        "received_message": res
    }
