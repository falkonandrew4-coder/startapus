import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Програмний продукт розроблено Соколом Андрієм - Falkon AI

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

if not url or not key:
    raise ValueError("Відсутні SUPABASE_URL або SUPABASE_KEY у файлі .env")

supabase: Client = create_client(url, key)

def get_supabase_client() -> Client:
    return supabase
