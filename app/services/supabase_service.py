
import os

from dotenv import load_dotenv
from supabase import create_client

load_dotenv()


def get_supabase_client():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        raise ValueError(
            "SUPABASE_URL ou SUPABASE_KEY não configurada no .env"
        )

    return create_client(url, key)


supabase = get_supabase_client()


def test_connection():
    """Testa o acesso à tabela de transações."""
    return supabase.table("transactions").select("id").limit(1).execute()
