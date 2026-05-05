from fastapi import APIRouter, Depends
from pydantic import BaseModel
from services.llm_service import generate_response

# Програмний продукт розроблено Соколом Андрієм - Falkon AI

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    session_id: str

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    # Тут буде логіка отримання контексту сесії з БД
    # Тимчасова заглушка:
    messages = [
        {"role": "system", "content": "Ти — Автономний AI-Архітектор Продуктів."},
        {"role": "user", "content": request.message}
    ]
    
    reply = await generate_response(messages)
    
    return {
        "reply": reply,
        "session_id": request.session_id,
        "status": "success"
    }
