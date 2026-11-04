"""Checks that sign-up against your Supabase project works.

Run from the repo root (uses .env, or the bundled config):

    python tools/check_auth.py --email you+test1@gmail.com

--email must be an address you control: sign-up sends a confirmation
email there (if "Confirm email" is on) and creates a user.
"""

import argparse
import secrets
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.auth_errors import classify_auth_error  # noqa: E402
from app.config import ConfigError, get_supabase_settings  # noqa: E402

HINTS = {
    "err_rate_limit": "Email rate limit hit. Set up custom SMTP (Auth -> SMTP Settings) or wait an hour.",
    "err_email_not_authorized": "Built-in email only sends to team members. Set up custom SMTP, or turn off 'Confirm email' while testing.",
    "err_user_exists": "That email already has an account. Use a different +alias.",
    "err_weak_password": "Password rejected by your Supabase password rules.",
    "err_signup_disabled": "Enable 'Allow new users to sign up' in Auth settings.",
    "err_server_config": "URL/key rejected. Check the SUPABASE_URL / SUPABASE_KEY values.",
    "err_network": "Can't reach Supabase. Check internet / project URL / paused project.",
    "invalid_email": "Supabase rejected the email address.",
    "operation_failed": "Unknown error: see the raw details above.",
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--email", required=True)
    args = parser.parse_args()

    try:
        url, key = get_supabase_settings()
    except ConfigError as error:
        sys.exit(f"[FAIL] {error}")
    print(f"[ok] settings found for {url}")
    if key.startswith("sb_secret_") or "service_role" in key:
        sys.exit("[FAIL] this is a SECRET key. Use the publishable key.")

    from supabase import create_client
    client = create_client(url, key)
    print("[ok] client created")

    # Not signed in: RLS must hide every row.
    try:
        rows = client.table("transactions").select("id").limit(1).execute().data
        print("[ok] anonymous read returns no rows (RLS working)"
              if not rows else "[FAIL] anonymous user can READ transactions. Fix RLS!")
    except Exception as error:
        print(f"[ok] anonymous read blocked: {type(error).__name__}")

    password = secrets.token_urlsafe(14)
    try:
        response = client.auth.sign_up({"email": args.email, "password": password})
    except Exception as error:
        key_name = classify_auth_error(error)
        print("[FAIL] sign-up failed")
        print("  raw :", type(error).__name__,
              getattr(error, "code", None), getattr(error, "status", None), error)
        print("  type:", key_name)
        print("  fix :", HINTS.get(key_name, HINTS["operation_failed"]))
        sys.exit(1)

    if response.session:
        print("[ok] sign-up worked and signed in immediately "
              "(email confirmation is OFF)")
    else:
        print("[ok] sign-up accepted. Check the inbox of", args.email,
              "for the confirmation email (confirmation is ON).")
        print("     If no email arrives, your SMTP isn't delivering.")
    print("Test password used:", password)


if __name__ == "__main__":
    main()
