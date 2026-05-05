from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
import json
import uuid

from services.llm_service import generate_response, stream_response
from services.chat_history import save_message_to_db, get_session_history
from services.market_research import research_market_duckduckgo, research_github
from services.prompts import get_prompt

# Програмний продукт розроблено Соколом Андрієм - Falkon AI

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    stage: Optional[str] = "greeting"
    is_guest: Optional[bool] = False

class StartRequest(BaseModel):
    session_id: Optional[str] = None
    is_guest: Optional[bool] = False

@router.post("/start")
async def start_acceleration(request: StartRequest):
    """Ініціює нову сесію акселерації — спрацьовує при натисканні 'Почати акселерацію'"""
    session_id = request.session_id or str(uuid.uuid4())
    
    greeting_messages = [
        {"role": "system", "content": get_prompt("greeting")},
        {"role": "user", "content": "Почати акселерацію"}
    ]
    
    reply = await generate_response(greeting_messages, model="gpt-4o-mini")
    
    # Зберігаємо початок сесії
    if not request.is_guest:
        save_message_to_db(session_id, "assistant", reply)
    
    return {
        "reply": reply,
        "session_id": session_id,
        "stage": "brainstorming",
        "status": "success"
    }

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """Основний endpoint чату — обробляє повідомлення та керує переходами між етапами"""
    session_id = request.session_id or str(uuid.uuid4())
    stage = request.stage or "brainstorming"
    
    # Визначаємо модель залежно від етапу
    model = "gpt-4o" if stage == "artifact_generation" else "gpt-4o-mini"
    
    # Отримуємо історію сесії для контексту
    history = []
    if not request.is_guest:
        history = get_session_history(session_id)
    
    # Зберігаємо повідомлення користувача
    if not request.is_guest:
        save_message_to_db(session_id, "user", request.message)
    
    # ── Етап 1: МОЗКОВИЙ ШТУРМ ──────────────────────────────────────
    if stage == "brainstorming":
        messages = [{"role": "system", "content": get_prompt("brainstorming")}]
        messages.extend(history[-6:])  # Останні 6 повідомлень для контексту
        messages.append({"role": "user", "content": request.message})
        
        reply = await generate_response(messages, model=model)
        next_stage = "market_analysis"
    
    # ── Етап 2: АНАЛІЗ РИНКУ ────────────────────────────────────────
    elif stage == "market_analysis":
        # Паралельно шукаємо інформацію про конкурентів
        search_results = await research_market_duckduckgo(request.message)
        github_results = await research_github(request.message)
        
        # Формуємо контекст з реальними даними ринку
        market_context = ""
        if search_results:
            market_context += "\n\nРезультати пошуку конкурентів та кейсів:\n"
            for r in search_results[:3]:
                market_context += f"- {r.get('title', '')}: {r.get('body', '')[:200]}...\n  URL: {r.get('href', '')}\n"
        
        if github_results:
            market_context += "\n\nПов'язані GitHub проекти:\n"
            for r in github_results[:3]:
                market_context += f"- {r.get('full_name', '')}: ⭐{r.get('stars', 0)} зірок | {r.get('description', '')[:100]}\n  {r.get('url', '')}\n"
        
        messages = [{"role": "system", "content": get_prompt("market_analysis") + market_context}]
        messages.extend(history[-6:])
        messages.append({"role": "user", "content": f"Ідея: {request.message}"})
        
        reply = await generate_response(messages, model=model)
        next_stage = "deep_questions"
    
    # ── Етап 3: ГЛИБИННІ ПИТАННЯ (мінімум 20!) ────────────────────
    elif stage == "deep_questions":
        # Рахуємо скільки питань вже задано (повідомлення AI в deep_questions)
        questions_asked = sum(1 for m in history if m["role"] == "assistant")
        
        # Формуємо системний промпт з контекстом про кількість питань
        system_prompt = get_prompt("deep_questions")
        if questions_asked < 20:
            system_prompt += f"\n\n[ВНУТРІШНІЙ СТАТУС: задано {questions_asked} питань з мінімальних 20. ОБОВ'ЯЗКОВО продовжуй задавати питання.]"
        elif questions_asked < 30:
            system_prompt += f"\n\n[ВНУТРІШНІЙ СТАТУС: задано {questions_asked} питань. Ти можеш завершити якщо відповіді вичерпні, або продовжити до 30 якщо є прогалини.]"
        
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(history[-30:])  # Більше контексту для збереження нитки розмови
        messages.append({"role": "user", "content": request.message})
        
        reply = await generate_response(messages, model=model)
        
        # Перевіряємо чи AI вирішив перейти до генерації (і питань мінімум 20)
        transition_signals = [
            "генерую ваш повний пакет",
            "є все необхідне",
            "дякую за вичерпні відповіді"
        ]
        should_transition = questions_asked >= 20 and any(s in reply.lower() for s in transition_signals)
        next_stage = "artifact_generation" if should_transition else "deep_questions"
    
    # ── Етап 4: ГЕНЕРАЦІЯ АРТЕФАКТІВ (gpt-4o!) ──────────────────────
    elif stage == "artifact_generation":
        # Збираємо всю історію для генерації фінального документу
        full_history = get_session_history(session_id) if not request.is_guest else history
        
        messages = [{"role": "system", "content": get_prompt("artifact_generation")}]
        messages.extend(full_history[-40:])  # Вся розмова для контексту
        messages.append({"role": "user", "content": "Згенеруй повний пакет документів на основі нашої розмови."})
        
        reply = await generate_response(messages, model="gpt-4o", temperature=0.6)
        next_stage = "completed"
    
    else:
        reply = "Акселерацію завершено! Ви можете переглянути ваші документи в особистому кабінеті."
        next_stage = "completed"
    
    # Зберігаємо відповідь AI
    if not request.is_guest:
        save_message_to_db(session_id, "assistant", reply)
    
    return {
        "reply": reply,
        "session_id": session_id,
        "stage": next_stage,
        "status": "success"
    }

@router.get("/session/{session_id}")
async def get_session(session_id: str):
    """Отримує повну історію сесії для відновлення чату"""
    history = get_session_history(session_id)
    return {
        "session_id": session_id,
        "messages": history,
        "status": "success"
    }
