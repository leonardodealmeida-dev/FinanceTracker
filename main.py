
import sys

from PySide6.QtWidgets import QApplication

from app.i18n import tr
from app.ui.login_window import LoginWindow
from app.ui.dashboard import Dashboard


def main():
    app = QApplication(sys.argv)
    app.setApplicationName(tr("brand"))

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

