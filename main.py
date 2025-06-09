from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from chatbot import EconomicsChatbot
from config import settings

app = FastAPI(title="Economics Expert Chatbot")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize chatbot
chatbot = EconomicsChatbot()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

class HistoryResponse(BaseModel):
    history: List[dict]

@app.get("/")
async def read_root():
    return FileResponse("static/index.html")

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        response = chatbot.get_response(request.message)
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history", response_model=HistoryResponse)
async def get_history():
    try:
        history = chatbot.get_chat_history()
        return HistoryResponse(history=history)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/clear")
async def clear_history():
    try:
        chatbot.clear_history()
        return {"message": "History cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    ) 