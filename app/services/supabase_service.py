"""Supabase client factory with per-account OS-keyring session storage.

Session tokens are kept in the operating system credential store when
available. If no keyring backend is available, sessions remain in memory
for the current run; passwords are never stored by FinanceTracker.
"""
from supabase import create_client

try:
    from supabase import ClientOptions
except ImportError:  # compatibility with older supabase-py releases
    ClientOptions = None

from app.config import get_supabase_settings


class MemoryStorage:
    def __init__(self):
        self.values = {}

    def get_item(self, key):
        return self.values.get(key)

    def set_item(self, key, value):
        self.values[key] = value

    def remove_item(self, key):
        self.values.pop(key, None)


class KeyringStorage:
    SERVICE = "FinanceTracker Supabase sessions"

    def __init__(self, account_id):
        self.account_id = str(account_id)
        self.memory = MemoryStorage()
        try:
            import keyring
            backend = keyring.get_keyring()
            self.keyring = keyring if getattr(backend, "priority", 0) > 0 else None
        except Exception:
            self.keyring = None

    def _username(self, key):
        return f"{self.account_id}:{key}"

    def get_item(self, key):
        if self.keyring:
            try:
                value = self.keyring.get_password(self.SERVICE, self._username(key))
                if value is not None:
                    return value
            except Exception:
                pass
        return self.memory.get_item(key)

    def set_item(self, key, value):
        if self.keyring:
            try:
                self.keyring.set_password(self.SERVICE, self._username(key), value)
                return
            except Exception:
                pass
        self.memory.set_item(key, value)

    def remove_item(self, key):
        if self.keyring:
            try:
                self.keyring.delete_password(self.SERVICE, self._username(key))
            except Exception:
                pass
        self.memory.remove_item(key)


def get_supabase_client(account_id="primary"):
    url, key = get_supabase_settings()
    storage = KeyringStorage(account_id)
    if ClientOptions is not None:
        try:
            options = ClientOptions(
                storage=storage,
                persist_session=True,
                auto_refresh_token=True,
            )
            return create_client(url, key, options=options)
        except TypeError:
            # Older SDK versions may not expose all auth storage options.
            pass
    return create_client(url, key)


# Backwards-compatible default client for utility scripts.
supabase = get_supabase_client("primary")


def test_connection():
    """Testa o acesso à tabela de transações."""
    return supabase.table("transactions").select("id").limit(1).execute()
