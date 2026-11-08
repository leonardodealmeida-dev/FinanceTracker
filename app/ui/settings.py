"""Full-page Settings and About windows matching the FinanceTracker web UI."""
from PySide6.QtCore import Qt, Signal, QUrl
from PySide6.QtGui import QDesktopServices, QPixmap
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton,
    QFrame, QScrollArea, QWidget, QDialogButtonBox,
)

from app.config import resource_path
from app.ui.theme import get_theme


class SettingsDialog(QDialog):
    add_account_requested = Signal()
    switch_account_requested = Signal(str)
    sign_out_requested = Signal()
    delete_account_requested = Signal()
    help_requested = Signal()
    theme_changed = Signal(str)

    def __init__(self, user, accounts, active_account_id, parent=None):
        super().__init__(parent)
        self.user = user
        self.accounts = accounts
        self.active_account_id = active_account_id
        self.theme = get_theme()
        self.setWindowTitle("FinanceTracker — Settings")
        self.resize(1050, 760)
        self.setMinimumSize(760, 600)
        self.setWindowState(self.windowState() | Qt.WindowState.WindowMaximized)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(26, 22, 26, 22)
        outer.setSpacing(16)

        heading = QHBoxLayout()
        title_col = QVBoxLayout()
        eyebrow = QLabel("PREFERENCES & ACCOUNT")
        eyebrow.setObjectName("settingsMuted")
        title = QLabel("Settings")
        title.setStyleSheet("font-size: 27px; font-weight: 800;")
        subtitle = QLabel("Manage your accounts, appearance and FinanceTracker preferences.")
        subtitle.setObjectName("settingsMuted")
        title_col.addWidget(eyebrow)
        title_col.addWidget(title)
        title_col.addWidget(subtitle)
        heading.addLayout(title_col)
        heading.addStretch()
        close = QPushButton("← Back to Overview")
        close.clicked.connect(self.accept)
        heading.addWidget(close)
        outer.addLayout(heading)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        grid = QGridLayout(content)
        grid.setContentsMargins(0, 4, 8, 4)
        grid.setHorizontalSpacing(18)
        grid.setVerticalSpacing(18)

        accounts_card = self._card("ACCOUNT", "Your accounts", "Switch between accounts or add another one.")
        accounts_layout = accounts_card.layout()
        for account in accounts:
            row = QHBoxLayout()
            avatar = QLabel("●")
            avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
            avatar.setFixedSize(36, 36)
            avatar.setStyleSheet("color: #209b65; background: rgba(32,155,101,0.12); border-radius: 10px; font-size: 17px;")
            copy = QVBoxLayout()
            is_active = account["id"] == active_account_id
            name = QLabel("Current account" if is_active else "Saved account")
            name.setStyleSheet("font-weight: 700;")
            email = QLabel(account.get("email", "Account"))
            email.setObjectName("settingsMuted")
            copy.addWidget(name)
            copy.addWidget(email)
            row.addWidget(avatar)
            row.addLayout(copy, 1)
            if is_active:
                status = QLabel("Active")
                status.setStyleSheet("color: #209b65; font-weight: 700; padding: 5px 9px;")
                row.addWidget(status)
            else:
                switch = QPushButton("Switch")
                switch.clicked.connect(lambda checked=False, account_id=account["id"]: self._switch(account_id))
                row.addWidget(switch)
            accounts_layout.addLayout(row)

        add = QPushButton("+   Add another account")
        add.setObjectName("primary")
        add.clicked.connect(self.add_account_requested.emit)
        accounts_layout.addWidget(add)

        support_card = self._card("SUPPORT", "Help & contact", "Learn how to use the app or get in touch.")
        support_layout = support_card.layout()
        tour = QPushButton("ⓘ   Help & quick tour")
        tour.clicked.connect(self.help_requested.emit)
        support_layout.addWidget(tour)
        contact = QPushButton("✉   Contact us — financetracker.security@gmail.com")
        contact.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("mailto:financetracker.security@gmail.com")))
        support_layout.addWidget(contact)

        security_card = self._card("SESSION & SECURITY", "Account actions", "Sign out of this account or permanently delete it.")
        security_layout = security_card.layout()
        signout = QPushButton("⇥   Sign out")
        signout.clicked.connect(self.sign_out_requested.emit)
        security_layout.addWidget(signout)
        delete = QPushButton("♲   Delete account")
        delete.setObjectName("danger")
        delete.clicked.connect(self.delete_account_requested.emit)
        security_layout.addWidget(delete)
        note = QLabel("Account actions apply only to the currently active FinanceTracker account.")
        note.setWordWrap(True)
        note.setObjectName("settingsMuted")
        security_layout.addWidget(note)

        appearance_card = self._card("APPEARANCE", "Theme", "Choose how FinanceTracker looks on this device.")
        appearance_layout = appearance_card.layout()
        theme_row = QHBoxLayout()
        theme_copy = QVBoxLayout()
        self.theme_title = QLabel()
        self.theme_title.setStyleSheet("font-weight: 700;")
        self.theme_description = QLabel()
        self.theme_description.setObjectName("settingsMuted")
        theme_copy.addWidget(self.theme_title)
        theme_copy.addWidget(self.theme_description)
        theme_row.addLayout(theme_copy, 1)
        self.theme_button = QPushButton()
        self.theme_button.clicked.connect(self.toggle_theme)
        theme_row.addWidget(self.theme_button)
        appearance_layout.addLayout(theme_row)
        self._update_theme_labels()

        # Appearance intentionally sits directly underneath Session & Security.
        grid.addWidget(accounts_card, 0, 0)
        grid.addWidget(security_card, 0, 1)
        grid.addWidget(support_card, 1, 0)
        grid.addWidget(appearance_card, 1, 1)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        scroll.setWidget(content)
        outer.addWidget(scroll, 1)

    def _card(self, kicker, title, description):
        card = QFrame()
        card.setObjectName("settingsCard")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(12)
        eyebrow = QLabel(kicker)
        eyebrow.setStyleSheet("color: #209b65; font-size: 10px; font-weight: 800; letter-spacing: 1px;")
        heading = QLabel(title)
        heading.setStyleSheet("font-size: 19px; font-weight: 800;")
        desc = QLabel(description)
        desc.setWordWrap(True)
        desc.setObjectName("settingsMuted")
        layout.addWidget(eyebrow)
        layout.addWidget(heading)
        layout.addWidget(desc)
        return card

    def _switch(self, account_id):
        self.switch_account_requested.emit(account_id)
        self.accept()

    def toggle_theme(self):
        self.theme = "light" if self.theme == "dark" else "dark"
        self.theme_changed.emit(self.theme)
        self._update_theme_labels()

    def _update_theme_labels(self):
        is_light = self.theme == "light"
        self.theme_title.setText("Light theme" if is_light else "Dark theme")
        self.theme_description.setText(
            "Clean white background with green accents" if is_light
            else "Dark background with green accents"
        )
        self.theme_button.setText("☼  Light" if is_light else "☾  Dark")


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About FinanceTracker")
        self.setMinimumWidth(480)
        self.setMaximumWidth(620)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(26, 24, 26, 24)
        layout.setSpacing(14)

        kicker = QLabel("THE STORY BEHIND THE APP")
        kicker.setStyleSheet("color: #209b65; font-size: 10px; font-weight: 800; letter-spacing: 1px;")
        layout.addWidget(kicker)

        profile = QHBoxLayout()
        photo = QLabel()
        photo.setFixedSize(104, 104)
        photo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pixmap = QPixmap(resource_path("assets/leonardo-about.jpeg"))
        if not pixmap.isNull():
            # Circular avatar, matching the web About card. Crop from the
            # top of the portrait so the face stays centered in the circle.
            size = photo.size()
            scaled = pixmap.scaled(
                size, Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation,
            )
            x = max(0, (scaled.width() - size.width()) // 2)
            y = 0
            avatar = QPixmap(size)
            avatar.fill(Qt.GlobalColor.transparent)
            from PySide6.QtGui import QPainter, QPainterPath
            painter = QPainter(avatar)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            clip = QPainterPath()
            clip.addEllipse(1, 1, size.width() - 2, size.height() - 2)
            painter.setClipPath(clip)
            painter.drawPixmap(0, 0, scaled, x, y, size.width(), size.height())
            painter.end()
            photo.setPixmap(avatar)
            photo.setStyleSheet(
                "background: transparent; border: 2px solid #209b65; border-radius: 52px;"
            )
        else:
            photo.setText("LD")
            photo.setStyleSheet("font-size: 28px; font-weight: 800; color: #209b65; border: 2px solid #209b65; border-radius: 52px;")
        profile.addWidget(photo)
        text_col = QVBoxLayout()
        title = QLabel("About FinanceTracker")
        title.setStyleSheet("font-size: 21px; font-weight: 800;")
        byline = QLabel("Created by Leonardo De Almeida")
        byline.setStyleSheet("font-weight: 700;")
        text_col.addWidget(title)
        text_col.addWidget(byline)
        text_col.addStretch()
        profile.addLayout(text_col, 1)
        layout.addLayout(profile)

        description = QLabel(
            "FinanceTracker was designed and developed by Leonardo De Almeida, "
            "a full-stack developer passionate about building useful, thoughtful "
            "technology. The goal is simple: make personal finance easier to "
            "understand, organize, and manage."
        )
        description.setWordWrap(True)
        layout.addWidget(description)

        github = QPushButton("↗   Visit my GitHub")
        github.setObjectName("primary")
        github.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/leonardodealmeida-dev")))
        layout.addWidget(github)

        footer = QLabel("FinanceTracker · Personal finance, made clearer.")
        footer.setObjectName("settingsMuted")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(footer)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        buttons.rejected.connect(self.reject)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)
