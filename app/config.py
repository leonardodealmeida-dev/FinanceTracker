"""Where the app gets its Supabase settings, and where bundled files live."""

import os
import sys
from pathlib import Path


class ConfigError(RuntimeError):
    """Supabase settings are missing."""


def is_frozen():
    return getattr(sys, "frozen", False)


def resource_path(relative):
    base = getattr(sys, "_MEIPASS", None) or Path(__file__).resolve().parent.parent
    return str(Path(base) / relative)


def get_supabase_settings():
    """Load Supabase settings from environment or an adjacent .env file."""

    from dotenv import load_dotenv

    if is_frozen():
        exe_dir = Path(sys.executable).resolve().parent
        candidates = [
            exe_dir / ".env",
            exe_dir.parent / ".env",
            exe_dir.parent.parent / ".env",
            Path.cwd() / ".env",
        ]
    else:
        project_dir = Path(__file__).resolve().parent.parent
        candidates = [
            project_dir / ".env",
            Path.cwd() / ".env",
        ]

    # Load available .env files without overwriting existing environment variables.
    checked = set()
    for env_file in candidates:
        env_file = env_file.resolve()
        if env_file not in checked and env_file.is_file():
            load_dotenv(dotenv_path=env_file, override=False)
            checked.add(env_file)

    url = os.getenv("SUPABASE_URL", "").strip()
    key = os.getenv("SUPABASE_KEY", "").strip()

    if not url or not key:
        from app import bundled_config
        url = url or bundled_config.SUPABASE_URL.strip()
        key = key or bundled_config.SUPABASE_KEY.strip()

    if not url or not key:
        raise ConfigError(
            "SUPABASE_URL / SUPABASE_KEY are not configured. "
            "Place a .env file beside the executable or use an official build."
        )

    return url, key
