"""In-app password reset using the one-time code Supabase emails.

Flow: request code by email -> enter code + new password.
Requires the "Reset Password" email template in Supabase to include
{{ .Token }} (see docs/SUPABASE_SETUP.md).
"""

import re

from PySide6.QtWidgets import (
    QDialog, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QPushButton,
    QVBoxLayout,
)

from app.auth_errors import classify_auth_error
from app.i18n import tr
from app.logging_setup import logger
from app.services.supabase_service import supabase


class ResetPasswordDialog(QDialog):
    def __init__(self, parent=None, email=""):
        super().__init__(parent)
        self.setWindowTitle(tr("reset_title"))
        self.setMinimumWidth(380)
        self.email_value = ""
        self.verified = False  # code already accepted (session is active)

        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        self.intro = QLabel(tr("reset_intro"))
        self.intro.setWordWrap(True)

        self.email = QLineEdit(email)
        self.email.setPlaceholderText(tr("email_placeholder"))

        self.send_button = QPushButton(tr("reset_send_code"))
        self.send_button.setObjectName("primary")
        self.send_button.clicked.connect(self.send_code)

        self.code = QLineEdit()
        self.code.setPlaceholderText(tr("reset_code_placeholder"))
        self.new_password = QLineEdit()
        self.new_password.setPlaceholderText(tr("reset_new_password"))
        self.new_password.setEchoMode(QLineEdit.EchoMode.Password)

        self.confirm_button = QPushButton(tr("reset_confirm"))
        self.confirm_button.setObjectName("primary")
        self.confirm_button.clicked.connect(self.confirm)

        self.status = QLabel("")
        self.status.setWordWrap(True)

        cancel = QPushButton(tr("cancel"))
        cancel.clicked.connect(self.reject)

        layout.addWidget(self.intro)
        layout.addWidget(self.email)
        layout.addWidget(self.send_button)
        layout.addWidget(self.code)
        layout.addWidget(self.new_password)
        layout.addWidget(self.confirm_button)
        layout.addWidget(self.status)
        row = QHBoxLayout()
        row.addStretch()
        row.addWidget(cancel)
        layout.addLayout(row)

        # Step 2 stays disabled until a code has been requested.
        self.set_step_two(False)

    def set_step_two(self, enabled):
        for widget in (self.code, self.new_password, self.confirm_button):
            widget.setEnabled(enabled)

    def send_code(self):
        email = self.email.text().strip().lower()
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            self.status.setText(tr("invalid_email"))
            return

        self.send_button.setEnabled(False)
        try:
            supabase.auth.reset_password_for_email(email)
            self.email_value = email
            self.status.setText(tr("reset_code_sent"))
            self.set_step_two(True)
            self.code.setFocus()
        except Exception as error:
            logger.error(
                "Password reset request error: %s: %s",
                type(error).__name__, error,
            )
            key = classify_auth_error(error)
            self.status.setText(
                tr("reset_send_failed") if key == "operation_failed"
                else tr(key)
            )
        finally:
            self.send_button.setEnabled(True)

    def confirm(self):
        # People often paste codes with spaces ("123 456").
        code = "".join(self.code.text().split())
        password = self.new_password.text()

        if not self.verified and not code:
            self.status.setText(tr("fill_fields"))
            return
        if not password:
            self.status.setText(tr("fill_fields"))
            return
        if len(password) < 8:
            self.status.setText(tr("password_short"))
            return

        self.confirm_button.setEnabled(False)

        # Step 1: check the emailed code (single use).
        if not self.verified:
            try:
                supabase.auth.verify_otp({
                    "email": self.email_value,
                    "token": code,
                    "type": "recovery",
                })
                self.verified = True
            except Exception as error:
                logger.error(
                    "Password reset: code check failed: %s: %s",
                    type(error).__name__, error,
                )
                self.status.setText(tr("reset_failed"))
                self.confirm_button.setEnabled(True)
                return

        # Step 2: set the new password. If this fails the code is already
        # used up, so we stay signed in and let the user try another
        # password without requesting a new code.
        try:
            supabase.auth.update_user({"password": password})
        except Exception as error:
            logger.error(
                "Password reset: setting password failed: %s: %s",
                type(error).__name__, error,
            )
            key = classify_auth_error(error)
            self.status.setText(
                tr("reset_update_failed") if key == "operation_failed"
                else tr(key)
            )
            self.confirm_button.setEnabled(True)
            return

        self.sign_out_quietly()
        self.verified = False
        QMessageBox.information(self, tr("reset_title"), tr("reset_done"))
        self.accept()

    def sign_out_quietly(self):
        try:
            supabase.auth.sign_out()
        except Exception as error:
            logger.error("Sign-out after reset: %s", error)

    def reject(self):
        # Closing after the code was accepted: don't leave a session open.
        if self.verified:
            self.sign_out_quietly()
            self.verified = False
        super().reject()
