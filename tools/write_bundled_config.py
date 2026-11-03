"""Writes app/bundled_config.py from environment variables (used by CI).

SUPABASE_URL=... SUPABASE_KEY=... python tools/write_bundled_config.py
"""

import os
import sys
from pathlib import Path

url = os.environ.get("SUPABASE_URL", "").strip()
key = os.environ.get("SUPABASE_KEY", "").strip()

if not url or not key:
    sys.exit("SUPABASE_URL and SUPABASE_KEY must be set (GitHub secrets).")

if "service_role" in key or key.startswith("sb_secret_"):
    sys.exit("Refusing to bundle a secret/service-role key. Use the publishable key.")

target = Path(__file__).resolve().parent.parent / "app" / "bundled_config.py"
target.write_text(
    '"""Generated at build time. Do not commit."""\n\n'
    f"SUPABASE_URL = {url!r}\n"
    f"SUPABASE_KEY = {key!r}\n"
)
print("Wrote", target)
