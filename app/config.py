"""Where the app gets its Supabase settings, and where bundled files live."""

import os
import sys
from pathlib import Path


class ConfigError(RuntimeError):
    """Supabase settings are missing."""


def is_frozen():
    """True when running as a packaged (PyInstaller) app."""
    return getattr(sys, "frozen", False)


def resource_path(relative):
    """Path to a bundled file, in development and in a packaged app."""
    base = getattr(sys, "_MEIPASS", None) or Path(__file__).resolve().parent.parent
    return str(Path(base) / relative)


def get_supabase_settings():
    """Return (url, key).

    Order: environment variables (and a local .env, development only),
    then the values baked in at build time.
    """
    if not is_frozen():
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except ImportError:
            pass

    url = os.getenv("SUPABASE_URL", "").strip()
    key = os.getenv("SUPABASE_KEY", "").strip()

    if not url or not key:
        from app import bundled_config
        url = url or bundled_config.SUPABASE_URL.strip()
        key = key or bundled_config.SUPABASE_KEY.strip()

    if not url or not key:
        raise ConfigError(
            "SUPABASE_URL / SUPABASE_KEY are not configured. "
            "Create a .env file (see README) or use an official build."
        )
    return url, key
