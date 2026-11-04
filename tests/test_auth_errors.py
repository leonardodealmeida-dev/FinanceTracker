from app.auth_errors import classify_auth_error


class Err(Exception):
    def __init__(self, message="", code=None, status=None):
        super().__init__(message)
        self.message, self.code, self.status = message, code, status


class ConnectError(Exception):
    pass


def test_codes():
    assert classify_auth_error(Err("x", code="over_email_send_rate_limit")) == "err_rate_limit"
    assert classify_auth_error(Err("x", code="email_address_not_authorized")) == "err_email_not_authorized"
    assert classify_auth_error(Err("x", code="user_already_exists")) == "err_user_exists"
    assert classify_auth_error(Err("x", code="invalid_credentials")) == "login_failed"


def test_status_429_and_text_fallbacks():
    assert classify_auth_error(Err("whatever", status=429)) == "err_rate_limit"
    assert classify_auth_error(Err("Email address not authorized")) == "err_email_not_authorized"
    assert classify_auth_error(Err("Password should be at least 6 characters")) == "err_weak_password"
    assert classify_auth_error(Err("Invalid API key")) == "err_server_config"


def test_network_and_unknown():
    assert classify_auth_error(ConnectError("boom")) == "err_network"
    assert classify_auth_error(Exception("[Errno -2] Name or service not known")) == "err_network"
    assert classify_auth_error(Exception("something odd")) == "operation_failed"


def test_timeouts_from_the_server():
    assert classify_auth_error(Err("context deadline exceeded", code="request_timeout", status=504)) == "err_timeout"
    assert classify_auth_error(Err("x", status=504)) == "err_timeout"
    assert classify_auth_error(Err("Gateway Time-out")) == "err_timeout"


def test_password_update_errors():
    assert classify_auth_error(Err("New password should be different from the old password.", code="same_password")) == "err_same_password"
    assert classify_auth_error(Err("New password should be different from the old password.")) == "err_same_password"
    assert classify_auth_error(Err("Password should contain at least one character of each: abc")) == "err_weak_password"
