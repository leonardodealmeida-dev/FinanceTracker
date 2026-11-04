import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMessageBox

from app.config import ConfigError, resource_path
from app.i18n import tr
from app.logging_setup import setup_logging
from app.version import APP_NAME, __version__


def set_windows_app_id():
    """Lets Windows show our icon in the taskbar instead of Python's."""
    if sys.platform == "win32":
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            "usaleonardo.financetracker"
        )


def main():
    setup_logging()
    set_windows_app_id()

    app = QApplication(sys.argv)
    app.setApplicationName(tr("brand"))
    app.setApplicationVersion(__version__)
    app.setWindowIcon(QIcon(resource_path("assets/icon.png")))

    # Importing the UI creates the Supabase client, which needs settings.
    try:
        from app.ui.login_window import LoginWindow
        from app.ui.dashboard import Dashboard
    except ConfigError as error:
        QMessageBox.critical(None, APP_NAME, f"{tr('config_error')}\n\n{error}")
        sys.exit(1)

    login = LoginWindow()
    windows = []

    def open_dashboard(user):
        dashboard = Dashboard(user)
        windows.append(dashboard)

        def return_to_login():
            login.email.clear()
            login.password.clear()
            login.status.clear()
            login.show()
            login.raise_()
            login.activateWindow()

        dashboard.logged_out.connect(return_to_login)
        dashboard.show()
        login.hide()

    login.authenticated.connect(open_dashboard)
    login.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
