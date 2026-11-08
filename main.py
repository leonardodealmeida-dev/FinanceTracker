import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMessageBox

from app.config import ConfigError, resource_path
from app.i18n import tr
from app.logging_setup import setup_logging
from app.version import APP_NAME, __version__
from app.ui.theme import apply_theme, get_theme


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
    apply_theme(app, get_theme())

    try:
        from app.ui.login_window import LoginWindow
        from app.ui.dashboard import Dashboard
        from app.services.account_manager import AccountManager
        manager = AccountManager()
        restored = manager.restore()
    except ConfigError as error:
        QMessageBox.critical(None, APP_NAME, f"{tr('config_error')}\n\n{error}")
        sys.exit(1)

    windows = []

    def show_login(account_id="primary", add_mode=False, previous_dashboard=None):
        client = manager.create_client(account_id)
        login = LoginWindow(client=client, show_cancel=add_mode)
        windows.append(login)

        def authenticated(user):
            manager.register(account_id, user, client)
            login.close()
            if previous_dashboard:
                previous_dashboard.close()
            open_dashboard(user, client, account_id)

        login.authenticated.connect(authenticated)

        if add_mode:
            def cancelled():
                manager.discard_client(account_id, sign_out=True)
                login.close()
            login.cancelled.connect(cancelled)

        login.show()
        return login

    def open_dashboard(user, client, account_id):
        dashboard = Dashboard(
            user, client=client, account_manager=manager,
            account_id=account_id,
        )
        windows.append(dashboard)

        def add_account():
            new_id = manager.new_account_id()
            show_login(new_id, add_mode=True, previous_dashboard=dashboard)

        def switch_account(next_id):
            try:
                result = manager.activate(next_id)
            except Exception as error:
                QMessageBox.warning(dashboard, "FinanceTracker", f"Could not switch account:\n{error}")
                return
            if not result:
                QMessageBox.warning(
                    dashboard, "FinanceTracker",
                    "This saved session has expired. Please sign in again.",
                )
                return
            next_user, next_client = result
            dashboard.close()
            open_dashboard(next_user, next_client, next_id)

        def logged_out():
            manager.remove(account_id, sign_out=True)
            dashboard.close()
            if manager.accounts:
                next_id = manager.accounts[0]["id"]
                result = manager.activate(next_id)
                if result:
                    next_user, next_client = result
                    open_dashboard(next_user, next_client, next_id)
                    return
            show_login("primary")

        dashboard.add_account_requested.connect(add_account)
        dashboard.switch_account_requested.connect(switch_account)
        dashboard.logged_out.connect(logged_out)
        dashboard.show()

    if restored:
        user, client, account_id = restored
        open_dashboard(user, client, account_id)
    else:
        show_login("primary")

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
