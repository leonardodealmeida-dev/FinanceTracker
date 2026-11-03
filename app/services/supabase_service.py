from supabase import create_client

from app.config import get_supabase_settings


def get_supabase_client():
    url, key = get_supabase_settings()
    return create_client(url, key)


supabase = get_supabase_client()


def test_connection():
    """Testa o acesso à tabela de transações."""
    return supabase.table("transactions").select("id").limit(1).execute()
