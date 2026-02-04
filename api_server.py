"""
FastAPI backend for Anton AI Companion
This replaces the Gradio UI with a proper REST API for the Next.js frontend
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.llm_service import LLMService
from services.user_service import UserService

app = FastAPI(
    title="Anton AI Companion API",
    description="Backend API for Anton AI Companion",
    version="1.0.0"
)

# Add CORS middleware for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    user_input: str
    memory: List[Message] = []

class ChatResponse(BaseModel):
    response: str

class UserStatusResponse(BaseModel):
    username: str
    onboarding_step: int
    onboarding_complete: bool
    created_at: str
    last_message_at: str

# Global user service
user_service = None

@app.on_event("startup")
async def startup():
    """Initialize services on startup"""
    global user_service
    user_service = UserService("default_user")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Send a message and get a response from Anton
    """
    try:
        # Convert memory to format expected by LLMService
        memory = [
            {"role": msg.role, "content": msg.content}
            for msg in request.memory
        ]
        
        response = LLMService.generate_response(
            request.user_input,
            memory,
            max_tokens=50
        )
        
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/user", response_model=UserStatusResponse)
async def get_user_status():
    """Get current user status and onboarding progress"""
    try:
        status = user_service.get_user_status()
        return UserStatusResponse(
            username=status["username"],
            onboarding_step=status["onboarding_step"],
            onboarding_complete=status["onboarding_complete"],
            created_at=status["created_at"],
            last_message_at=status["last_message_at"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/user/message")
async def process_message(request: ChatRequest):
    """Process user message through UserService"""
    try:
        response, show_mark = user_service.process_user_message(request.user_input)
        return {
            "response": response,
            "show_mark_button": show_mark,
            "status": user_service.get_user_status()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/user/mark-complete")
async def mark_day_complete():
    """Mark current day as complete and move to next"""
    try:
        message, is_complete = user_service.mark_day_complete()
        return {
            "message": message,
            "onboarding_complete": is_complete,
            "status": user_service.get_user_status()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/user/export")
async def export_user_data():
    """Export user's onboarding responses as JSON"""
    try:
        data = user_service.export_data()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    
    # Check for HF_TOKEN
    if not os.getenv("HF_TOKEN"):
        print("⚠️  Warning: HF_TOKEN not set. AI responses will fail.")
        print("Set it with: export HF_TOKEN='your_token_here'")
    
    print("🚀 Starting Anton API Server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
