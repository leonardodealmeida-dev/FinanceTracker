"""Supabase settings baked into release builds.

This file is intentionally empty in git. The release workflow overwrites
it (via tools/write_bundled_config.py) with the project URL and the
*publishable* key taken from GitHub Actions secrets.

Never put a service-role / secret key here: everything in a desktop
app can be extracted by users. Row Level Security is what protects data.
"""

SUPABASE_URL = ""
SUPABASE_KEY = ""
