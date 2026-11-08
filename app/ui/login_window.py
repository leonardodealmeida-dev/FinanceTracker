import re

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QFrame
)

from app.auth_errors import classify_auth_error
from app.i18n import tr
from app.logging_setup import logger
from app.ui.reset_password import ResetPasswordDialog
from app.version import __version__
from app.services.supabase_service import supabase as default_supabase


class LoginWindow(QWidget):
    authenticated = Signal(object)
    cancelled = Signal()

    def __init__(self, client=None, show_cancel=False):
        super().__init__()

        self.client = client or default_supabase
        self.show_cancel = show_cancel
        self._auth_completed = False
        self._cancel_emitted = False
        self.signup_mode = False
        self.setWindowTitle("FinanceTracker")
        self.resize(440, 560)
        self.setMinimumSize(380, 500)

        # The application-wide theme stylesheet is applied by main.py.


        root = QVBoxLayout(self)
        root.setContentsMargins(28, 24, 28, 24)
        root.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card = QFrame()
        card.setObjectName("card")
        card.setMaximumWidth(390)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(28, 30, 28, 26)
        layout.setSpacing(14)

        brand = QLabel(tr("brand"))
        brand.setObjectName("brand")
        brand.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel(tr("tagline"))
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.heading = QLabel(tr("login_heading"))
        self.heading.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.heading.setStyleSheet(
            "font-size: 19px; font-weight: 700; margin-top: 8px;"
        )

        self.email = QLineEdit()
        self.email.setPlaceholderText(tr("email_placeholder"))
        self.email.setClearButtonEnabled(True)

        self.password = QLineEdit()
        self.password.setPlaceholderText(tr("password_placeholder"))
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        self.status = QLabel("")
        self.status.setObjectName("status")
        self.status.setWordWrap(True)

        self.submit_button = QPushButton(tr("login"))
        self.submit_button.setObjectName("primary")
        self.submit_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.submit_button.clicked.connect(self.submit)

        self.toggle_button = QPushButton(tr("create_account"))
        self.toggle_button.setObjectName("secondary")
        self.toggle_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.toggle_button.clicked.connect(self.toggle_mode)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setObjectName("link")
        self.cancel_button.setVisible(show_cancel)
        self.cancel_button.clicked.connect(self.cancel_add_account)

        self.forgot_button = QPushButton(tr("forgot_password"))
        self.forgot_button.setObjectName("secondary")
        self.forgot_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.forgot_button.clicked.connect(self.forgot_password)

        version = QLabel(f"v{__version__}")
        version.setObjectName("version")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(brand)
        layout.addWidget(subtitle)
        layout.addSpacing(12)
        layout.addWidget(self.heading)
        layout.addWidget(self.email)
        layout.addWidget(self.password)
        layout.addWidget(self.status)
        layout.addWidget(self.submit_button)
        layout.addWidget(self.forgot_button)
        layout.addWidget(self.toggle_button)
        layout.addWidget(self.cancel_button)
        layout.addWidget(version)

        root.addWidget(card)

    def forgot_password(self):
        dialog = ResetPasswordDialog(
            self, self.email.text().strip(), client=self.client
        )
        dialog.exec()

    def cancel_add_account(self):
        if not self._cancel_emitted:
            self._cancel_emitted = True
            self.cancelled.emit()

    def closeEvent(self, event):
        if self.show_cancel and not self._auth_completed:
            self.cancel_add_account()
        super().closeEvent(event)

    def toggle_mode(self):
        self.signup_mode = not self.signup_mode
        self.status.clear()
        self.forgot_button.setVisible(not self.signup_mode)

        if self.signup_mode:
            self.heading.setText(tr("signup_heading"))
            self.submit_button.setText(tr("signup"))
            self.toggle_button.setText(tr("have_account"))
        else:
            self.heading.setText(tr("login_heading"))
            self.submit_button.setText(tr("login"))
            self.toggle_button.setText(tr("create_account"))

    def submit(self):
        email = self.email.text().strip()
        password = self.password.text()

        if not email or not password:
            self.status.setText(tr("fill_fields"))
            return

        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            self.status.setText(tr("invalid_email"))
            return

        if self.signup_mode and len(password) < 8:
            self.status.setText(tr("password_short"))
            return

        self.submit_button.setEnabled(False)
        self.submit_button.setText(tr("wait"))
        self.status.setText(tr("connecting"))

        try:
            if self.signup_mode:
                response = self.client.auth.sign_up({
                    "email": email,
                    "password": password,
                })

                if response.session and response.user:
                    self.status.clear()
                    self._auth_completed = True
                    self.authenticated.emit(response.user)
                    return

                QMessageBox.information(
                    self,
                    tr("check_email_title"),
                    tr("check_email_message"),
                )
                self.toggle_mode()

            else:
                response = self.client.auth.sign_in_with_password({
                    "email": email,
                    "password": password,
                })

                if response.user and response.session:
                    self.status.clear()
                    self._auth_completed = True
                    self.authenticated.emit(response.user)
                else:
                    self.status.setText(tr("login_failed"))

        except Exception as error:
            logger.error(
                "Authentication error (%s): %s: %s",
                "signup" if self.signup_mode else "login",
                type(error).__name__, error,
            )
            self.status.setText(tr(classify_auth_error(error)))

        finally:
            self.submit_button.setEnabled(True)
            self.submit_button.setText(
                tr("signup") if self.signup_mode else tr("login")
            )
