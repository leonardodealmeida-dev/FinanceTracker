"""Manage multiple signed-in Supabase accounts for the desktop app."""
import json
import uuid

from PySide6.QtCore import QSettings

from app.services.supabase_service import get_supabase_client, supabase as primary_client


class AccountManager:
    ORGANIZATION = "LeonardoDeAlmeida"
    APPLICATION = "FinanceTracker"

    def __init__(self):
        self.settings = QSettings(self.ORGANIZATION, self.APPLICATION)
        self.clients = {}
        self.accounts = []
        self.active_id = "primary"

    @staticmethod
    def new_account_id():
        return str(uuid.uuid4())

    def create_client(self, account_id):
        if account_id not in self.clients:
            self.clients[account_id] = (
                primary_client if account_id == "primary"
                else get_supabase_client(account_id)
            )
        return self.clients[account_id]

    def _save(self):
        self.settings.setValue("accounts", json.dumps(self.accounts))
        self.settings.setValue("active_account", self.active_id)
        self.settings.sync()

    def restore(self):
        """Restore saved sessions; invalid/expired accounts are omitted."""
        try:
            stored = json.loads(self.settings.value("accounts", "[]"))
        except (TypeError, ValueError):
            stored = []
        wanted = str(self.settings.value("active_account", "primary"))
        valid = []
        restored = {}
        for item in stored if isinstance(stored, list) else []:
            if not isinstance(item, dict):
                continue
            account_id = str(item.get("id", ""))
            if not account_id:
                continue
            try:
                client = self.create_client(account_id)
                session = client.auth.get_session()
                user = getattr(session, "user", None) if session else None
                if user:
                    account = {
                        "id": account_id,
                        "email": getattr(user, "email", None) or item.get("email", "Account"),
                    }
                    valid.append(account)
                    restored[account_id] = (user, client)
            except Exception:
                continue
        self.accounts = valid
        selected = wanted if wanted in restored else (valid[0]["id"] if valid else "primary")
        self.active_id = selected
        self._save()
        if selected in restored:
            user, client = restored[selected]
            return user, client, selected
        return None

    def register(self, account_id, user, client):
        self.clients[account_id] = client
        email = getattr(user, "email", None) or "Account"
        self.accounts = [a for a in self.accounts if a["id"] != account_id]
        self.accounts.append({"id": account_id, "email": email})
        self.active_id = account_id
        self._save()

    def activate(self, account_id):
        client = self.clients.get(account_id) or self.create_client(account_id)
        session = client.auth.get_session()
        user = getattr(session, "user", None) if session else None
        if not user:
            self.remove(account_id)
            return None
        self.active_id = account_id
        self._save()
        return user, client

    def remove(self, account_id, sign_out=False):
        client = self.clients.get(account_id)
        if sign_out and client:
            try:
                client.auth.sign_out()
            except Exception:
                pass
        self.accounts = [a for a in self.accounts if a["id"] != account_id]
        self.clients.pop(account_id, None)
        if self.active_id == account_id:
            self.active_id = self.accounts[0]["id"] if self.accounts else "primary"
        self._save()

    def discard_client(self, account_id, sign_out=True):
        client = self.clients.pop(account_id, None)
        if sign_out and client:
            try:
                client.auth.sign_out()
            except Exception:
                pass

    def active_accounts(self):
        return list(self.accounts)
