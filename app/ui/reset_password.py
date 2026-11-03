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

from app.i18n import tr
from app.services.supabase_service import supabase


class ResetPasswordDialog(QDialog):
    def __init__(self, parent=None, email=""):
        super().__init__(parent)
        self.setWindowTitle(tr("reset_title"))
        self.setMinimumWidth(380)
        self.email_value = ""

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
        email = self.email.text().strip()
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
            print("Password reset request error:", str(error))
            self.status.setText(tr("reset_send_failed"))
        finally:
            self.send_button.setEnabled(True)

    def confirm(self):
        code = self.code.text().strip()
        password = self.new_password.text()

        if not code or not password:
            self.status.setText(tr("fill_fields"))
            return
        if len(password) < 8:
            self.status.setText(tr("password_short"))
            return

        self.confirm_button.setEnabled(False)
        try:
            supabase.auth.verify_otp({
                "email": self.email_value,
                "token": code,
                "type": "recovery",
            })
            supabase.auth.update_user({"password": password})
            supabase.auth.sign_out()
        except Exception as error:
            print("Password reset error:", str(error))
            self.status.setText(tr("reset_failed"))
            self.confirm_button.setEnabled(True)
            return

        QMessageBox.information(self, tr("reset_title"), tr("reset_done"))
        self.accept()
