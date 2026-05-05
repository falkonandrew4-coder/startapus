import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Програмний продукт розроблено Соколом Андрієм - Falkon AI

load_dotenv()

_supabase_client: Client = None

def get_supabase_client() -> Client:
    global _supabase_client
    if _supabase_client is None:
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")
        if not url or not key:
            raise ValueError("Відсутні SUPABASE_URL або SUPABASE_KEY")
        _supabase_client = create_client(url, key)
    return _supabase_client
