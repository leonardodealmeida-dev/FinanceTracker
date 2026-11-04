"""Turns Supabase/network exceptions into a specific, friendly message key.

Pure Python (no Qt) so it can be unit tested. Returns an i18n key.
"""

_BY_CODE = {
    "over_email_send_rate_limit": "err_rate_limit",
    "over_request_rate_limit": "err_rate_limit",
    "over_sms_send_rate_limit": "err_rate_limit",
    "email_address_not_authorized": "err_email_not_authorized",
    "user_already_exists": "err_user_exists",
    "email_exists": "err_user_exists",
    "weak_password": "err_weak_password",
    "same_password": "err_same_password",
    "signup_disabled": "err_signup_disabled",
    "email_provider_disabled": "err_signup_disabled",
    "email_address_invalid": "invalid_email",
    "invalid_credentials": "login_failed",
    "email_not_confirmed": "err_email_not_confirmed",
    "request_timeout": "err_timeout",
    "bad_jwt": "err_server_config",
    "no_authorization": "err_server_config",
}

# (substring in the lowercase message, key) checked in order
_BY_TEXT = [
    ("context deadline exceeded", "err_timeout"),
    ("request_timeout", "err_timeout"),
    ("gateway time-out", "err_timeout"),
    ("rate limit", "err_rate_limit"),
    ("too many requests", "err_rate_limit"),
    ("not authorized", "err_email_not_authorized"),
    ("already registered", "err_user_exists"),
    ("already been registered", "err_user_exists"),
    ("should be different from the old", "err_same_password"),
    ("password should", "err_weak_password"),
    ("signups not allowed", "err_signup_disabled"),
    ("signup is disabled", "err_signup_disabled"),
    ("email not confirmed", "err_email_not_confirmed"),
    ("invalid login credentials", "login_failed"),
    ("invalid api key", "err_server_config"),
    ("invalid jwt", "err_server_config"),
    ("apikey", "err_server_config"),
    ("name or service not known", "err_network"),
    ("getaddrinfo", "err_network"),
    ("timed out", "err_network"),
    ("connection", "err_network"),
    ("network", "err_network"),
]

_NETWORK_TYPES = {
    "connecterror", "connecttimeout", "readtimeout", "timeoutexception",
    "networkerror", "connectionerror", "gaierror", "timeouterror",
}


def classify_auth_error(error):
    """Return the i18n key that best describes `error`."""
    code = str(getattr(error, "code", "") or "").lower()
    if code in _BY_CODE:
        return _BY_CODE[code]

    status = getattr(error, "status", None)
    if status == 429:
        return "err_rate_limit"
    if status in (502, 503, 504):
        return "err_timeout"

    if type(error).__name__.lower() in _NETWORK_TYPES:
        return "err_network"

    text = str(getattr(error, "message", "") or error).lower()
    for needle, key in _BY_TEXT:
        if needle in text:
            return key

    return "operation_failed"
