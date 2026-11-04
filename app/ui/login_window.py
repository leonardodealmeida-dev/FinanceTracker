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
from app.services.supabase_service import supabase


class LoginWindow(QWidget):
    authenticated = Signal(object)

    def __init__(self):
        super().__init__()

        self.signup_mode = False
        self.setWindowTitle("FinanceTracker")
        self.resize(440, 560)
        self.setMinimumSize(380, 500)

        self.setStyleSheet("""
            QWidget {
                background-color: #101512;
                color: #edf5ef;
                font-family: "Noto Sans", sans-serif;
                font-size: 14px;
            }
            QFrame#card {
                background-color: #19221c;
                border: 1px solid #2b3b30;
                border-radius: 18px;
            }
            QLabel#brand {
                color: #7ee2a8;
                font-size: 29px;
                font-weight: 800;
            }
            QLabel#subtitle { color: #a6b7aa; font-size: 13px; }
            QLineEdit {
                background-color: #101512;
                border: 1px solid #35463a;
                border-radius: 9px;
                padding: 12px;
                color: white;
            }
            QLineEdit:focus { border: 1px solid #65cf91; }
            QPushButton#primary {
                background-color: #65cf91;
                color: #102016;
                border: none;
                border-radius: 9px;
                padding: 13px;
                font-weight: 700;
            }
            QPushButton#primary:hover { background-color: #82e5aa; }
            QPushButton#secondary {
                background: transparent;
                color: #85e5aa;
                border: none;
                padding: 8px;
            }
            QLabel#status { color: #f2b8a8; font-size: 12px; }
            QLabel#version { color: #6f8174; font-size: 11px; }
            QDialog QPushButton {
                background: #26332a;
                border: 1px solid #35463a;
                border-radius: 8px;
                padding: 9px 12px;
            }
        """)

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
        layout.addWidget(version)

        root.addWidget(card)

    def forgot_password(self):
        dialog = ResetPasswordDialog(self, self.email.text().strip())
        dialog.setStyleSheet(self.styleSheet())
        dialog.exec()

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
                response = supabase.auth.sign_up({
                    "email": email,
                    "password": password,
                })

                if response.session and response.user:
                    self.status.clear()
                    self.authenticated.emit(response.user)
                    return

                QMessageBox.information(
                    self,
                    tr("check_email_title"),
                    tr("check_email_message"),
                )
                self.toggle_mode()

            else:
                response = supabase.auth.sign_in_with_password({
                    "email": email,
                    "password": password,
                })

                if response.user and response.session:
                    self.status.clear()
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
