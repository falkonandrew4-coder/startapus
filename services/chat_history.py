from app.database import get_supabase_client

# Програмний продукт розроблено Соколом Андрієм - Falkon AI

def save_message_to_db(session_id: str, role: str, content: str):
    """
    Зберігає кожне повідомлення чату в Supabase для відновлення історії.
    """
    try:
        supabase = get_supabase_client()
        supabase.table("chat_history").insert({
            "session_id": session_id,
            "role": role,
            "content": content
        }).execute()
    except Exception as e:
        print(f"Помилка збереження повідомлення: {e}")

def get_session_history(session_id: str) -> list:
    """
    Отримує історію чату для передачі контексту в LLM.
    """
    try:
        supabase = get_supabase_client()
        response = supabase.table("chat_history").select("*").eq("session_id", session_id).order("created_at").execute()
        return [{"role": msg["role"], "content": msg["content"]} for msg in response.data]
    except Exception as e:
        print(f"Помилка завантаження історії: {e}")
        return []
