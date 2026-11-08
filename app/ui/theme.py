"""Shared light/dark theme for every PySide6 window and dialog."""
from pathlib import Path

from PySide6.QtCore import QSettings

ORG = "LeonardoDeAlmeida"
APP = "FinanceTracker"

PALETTES = {
    "dark": {
        "bg": "#101512", "panel": "#19221c", "panel_alt": "#202d24",
        "text": "#edf5ef", "muted": "#a6b7aa", "border": "#2b3b30",
        "input": "#101512", "green": "#65cf91", "green_hover": "#82e5aa",
        "green_text": "#102016", "selection": "#315c40",
        "danger": "#f28b78", "grid": "#2b3b30",
    },
    "light": {
        "bg": "#f3f8f4", "panel": "#ffffff", "panel_alt": "#edf5ef",
        "text": "#193326", "muted": "#64796c", "border": "#cfe2d4",
        "input": "#f7fbf8", "green": "#209b65", "green_hover": "#167d50",
        "green_text": "#ffffff", "selection": "#d7f0e1",
        "danger": "#d94f42", "grid": "#d5e4d9",
    },
}


def get_theme():
    value = str(QSettings(ORG, APP).value("theme", "dark"))
    return value if value in PALETTES else "dark"


def save_theme(theme):
    QSettings(ORG, APP).setValue("theme", theme)


def stylesheet(theme=None):
    c = PALETTES[theme or get_theme()]
    arrow_path = (Path(__file__).resolve().parents[2] / "assets" / "chevron-down.svg").as_posix()
    return f"""
QWidget {{
    background-color: {c['bg']};
    color: {c['text']};
    font-family: "Noto Sans", sans-serif;
    font-size: 13px;
}}
QDialog, QMainWindow {{ background: {c['bg']}; }}
QDialog#transactionDialog {{
    background: {c['panel']};
    border: 1px solid {c['border']};
    border-radius: 16px;
}}
QLabel#transactionDialogTitle {{
    color: {c['text']}; font-size: 20px; font-weight: 750;
    background: transparent;
}}
QLabel#transactionFieldLabel {{
    color: {c['muted']}; font-size: 12px; background: transparent;
}}
QPushButton#dialogClose {{
    background: {c['panel_alt']}; color: {c['text']};
    border: 1px solid {c['border']}; border-radius: 9px;
    padding: 0; font-size: 20px; font-weight: 400;
}}
QPushButton#dialogClose:hover {{
    background: {c['selection']}; border-color: {c['green']};
}}
QLabel {{ background: transparent; }}
QFrame {{ background: transparent; }}
QFrame#panel, QFrame#settingsCard, QFrame#aboutCard, QFrame#card {{
    background: {c['panel']};
    border: 1px solid {c['border']};
    border-radius: 13px;
}}
QLabel#brand {{ color: {c['green']}; font-size: 24px; font-weight: 800; }}
QLabel#metric {{ color: {c['green']}; font-size: 24px; font-weight: 700; }}
QLabel#muted, QLabel#settingsMuted {{ color: {c['muted']}; }}
QPushButton {{
    background: {c['panel_alt']};
    color: {c['text']};
    border: 1px solid {c['border']};
    border-radius: 8px;
    padding: 9px 13px;
}}
QPushButton:hover {{ border-color: {c['green']}; background: {c['selection']}; }}
QPushButton#floatingAction {{
    background: {c['panel_alt']};
    border: 1px solid {c['border']};
    border-radius: 10px;
    padding: 8px 11px;
    font-weight: 600;
}}
QPushButton#floatingAction:hover {{
    background: {c['selection']}; border-color: {c['green']};
}}
QPushButton:disabled {{ color: {c['muted']}; }}
QPushButton#primary {{
    background: {c['green']}; color: {c['green_text']};
    border: none; font-weight: 700;
}}
QPushButton#primary:hover {{ background: {c['green_hover']}; }}
QPushButton#danger {{ color: {c['danger']}; border-color: {c['danger']}; }}
QPushButton#link {{ background: transparent; border: none; color: {c['green']}; }}
QLineEdit, QComboBox, QDoubleSpinBox, QDateEdit, QTextEdit {{
    background: {c['input']}; color: {c['text']};
    border: 1px solid {c['border']}; border-radius: 8px; padding: 9px;
    selection-background-color: {c['selection']};
}}
QLineEdit:focus, QComboBox:focus, QDoubleSpinBox:focus, QDateEdit:focus, QTextEdit:focus {{
    border: 1px solid {c['green']};
}}
QComboBox {{
    padding-right: 34px;
}}
QComboBox::drop-down {{
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 30px;
    border: none;
    background: transparent;
}}
QComboBox::down-arrow {{
    image: url("{arrow_path}");
    width: 11px;
    height: 11px;
}}
QComboBox QAbstractItemView {{
    background: {c['panel']}; color: {c['text']};
    selection-background-color: {c['selection']};
    selection-color: {c['text']}; border: 1px solid {c['border']};
    outline: 0;
    padding: 4px;
}}
QScrollBar:vertical {{
    background: transparent;
    width: 9px;
    margin: 2px 1px 2px 1px;
    border: none;
}}
QScrollBar::handle:vertical {{
    background: {c['border']};
    min-height: 34px;
    border-radius: 4px;
}}
QScrollBar::handle:vertical:hover {{ background: {c['green']}; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
    width: 0px;
    border: none;
    background: transparent;
}}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
    background: transparent;
}}
QScrollBar:horizontal {{
    background: transparent;
    height: 9px;
    margin: 1px 2px;
    border: none;
}}
QScrollBar::handle:horizontal {{
    background: {c['border']};
    min-width: 34px;
    border-radius: 4px;
}}
QScrollBar::handle:horizontal:hover {{ background: {c['green']}; }}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    height: 0px;
    width: 0px;
    border: none;
    background: transparent;
}}
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
    background: transparent;
}}
QTabWidget::pane {{ border: none; }}
QTabBar::tab {{
    background: {c['panel']}; color: {c['muted']};
    padding: 9px 18px; border: 1px solid {c['border']};
    border-radius: 8px; margin-right: 6px;
}}
QTabBar::tab:selected {{
    background: {c['selection']}; color: {c['text']}; font-weight: 700;
}}
QTableWidget {{
    background: {c['panel']}; alternate-background-color: {c['panel_alt']};
    color: {c['text']}; border: 1px solid {c['border']};
    border-radius: 8px; gridline-color: {c['border']};
    selection-background-color: {c['selection']};
    selection-color: {c['text']};
}}
QHeaderView::section {{
    background: {c['panel_alt']}; color: {c['muted']};
    padding: 9px; border: none;
}}
QScrollArea {{ border: none; background: transparent; }}
QCheckBox {{ spacing: 8px; }}
QToolTip {{
    background: {c['panel']}; color: {c['text']};
    border: 1px solid {c['border']}; padding: 6px;
}}
"""


def apply_theme(app, theme):
    from app.ui.charts import set_chart_theme
    app.setStyleSheet(stylesheet(theme))
    set_chart_theme(theme)
    save_theme(theme)
