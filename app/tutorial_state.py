"""Remembers whether a user has already seen the first-login tutorial.

Stored in two places so it survives reinstalls and works offline:
  - the user's Supabase metadata (follows the account across computers)
  - a small local file (~/.financetracker/state.json)

Pure Python (no Qt) so it can be unit tested.
"""

import json
from pathlib import Path

from app.logging_setup import LOG_DIR, logger

STATE_FILE = LOG_DIR / "state.json"


def _load(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def seen_locally(user_id, path=STATE_FILE):
    return str(user_id) in _load(path).get("tutorial_seen", [])


def mark_seen_locally(user_id, path=STATE_FILE):
    path = Path(path)
    data = _load(path)
    seen = set(data.get("tutorial_seen", []))
    seen.add(str(user_id))
    data["tutorial_seen"] = sorted(seen)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data), encoding="utf-8")
    except OSError as error:
        logger.error("Could not save tutorial state: %s", error)


def seen_remotely(user):
    metadata = getattr(user, "user_metadata", None) or {}
    return bool(metadata.get("tutorial_seen"))


def should_show(user, path=STATE_FILE):
    """True the first time this account signs in."""
    return not (seen_remotely(user) or seen_locally(user.id, path))


def mark_seen(user, client=None, path=STATE_FILE):
    """Record that the tutorial was shown (locally and on the account)."""
    mark_seen_locally(user.id, path)
    if client is not None:
        try:
            client.auth.update_user({"data": {"tutorial_seen": True}})
        except Exception as error:  # offline etc.; local flag still works
            logger.error("Could not save tutorial flag on account: %s", error)
