
from datetime import date
from decimal import Decimal

from PySide6.QtCore import Qt, QDate, QTimer, Signal
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QDialog, QFormLayout,
    QLineEdit, QComboBox, QDoubleSpinBox, QDateEdit,
    QTextEdit, QMessageBox, QHeaderView, QFrame, QCheckBox, QTabWidget,
    QInputDialog, QScrollArea
)

from app.analytics import (
    balance_series, category_totals, monthly_summary, signed, totals,
)
from app.i18n import LANGUAGE, tr
from app.recurrence import FREQUENCIES, add_months_to_first, expand, parse_date
from app.services.supabase_service import supabase as default_supabase
from app.ui.settings import SettingsDialog, AboutDialog
from app.ui.theme import apply_theme, get_theme
from app.tutorial_state import mark_seen, should_show
from app.ui.charts import BalanceLineChart, CategoryDonutChart, MonthlyBarChart
from app.ui.tutorial import TutorialDialog


TEXT = {
    "pt_BR": {
        "title": "Visão geral", "balance": "Saldo líquido",
        "income": "Receitas", "expenses": "Despesas",
        "transactions": "Transações recentes",
        "add": "+ Nova transação", "edit": "Editar",
        "delete": "Excluir", "refresh": "Atualizar",
        "logout": "Sair da conta", "date": "Data",
        "description": "Descrição", "type": "Tipo",
        "category": "Categoria", "amount": "Valor",
        "notes": "Observações", "save": "Salvar",
        "cancel": "Cancelar", "new": "Nova transação",
        "edit_title": "Editar transação", "expense": "Despesa",
        "income_type": "Receita", "food": "Alimentação",
        "housing": "Moradia", "transport": "Transporte",
        "health": "Saúde", "education": "Educação",
        "entertainment": "Lazer", "salary": "Salário",
        "shopping": "Compras", "bills": "Contas",
        "other": "Outros", "confirm_delete": "Excluir esta transação?",
        "confirm_title": "Confirmar exclusão",
        "select": "Selecione uma transação primeiro.",
        "saved": "Transação salva com sucesso!",
        "deleted": "Transação excluída.",
        "error": "Erro", "required": "Informe uma descrição.",
        "currency": "USD", "welcome": "Bem-vindo",
        "empty": "Nenhuma transação cadastrada ainda.",
        "load_error": "Não foi possível carregar as transações.",
        "save_error": "Não foi possível salvar a transação.",
        "delete_error": "Não foi possível excluir a transação.",
        "search": "Buscar transações...",
        "all": "Todas",
        "date_start": "Data / início",
        "amount_each": "Valor (cada vez)",
        "repeats": "Repete",
        "once": "Uma vez", "daily": "Diariamente", "weekly": "Semanalmente",
        "monthly": "Mensalmente", "yearly": "Anualmente",
        "until": "até {}",
        "has_end": "Definir data final", "end_date": "Termina em",
        "end_before_start": "A data final não pode ser anterior ao início.",
        "groceries": "Mercado", "fuel": "Combustível",
        "tab_charts": "Gráficos", "tab_transactions": "Transações",
        "period": "Período",
        "p_month": "Este mês", "p_3": "Últimos 3 meses",
        "p_6": "Últimos 6 meses", "p_year": "Este ano", "p_all": "Tudo",
        "chart_monthly": "Receitas vs. despesas (últimos 6 meses)",
        "chart_category": "Despesas por categoria",
        "chart_balance": "Saldo ao longo do tempo",
        "no_expenses": "sem despesas", "balance_name": "Saldo",
        "migration_needed": (
            "O banco de dados precisa da atualização de recorrência. "
            "Execute migrations/001_add_recurrence.sql no Supabase."
        ),
        "help": "Ajuda",
        "delete_account": "Excluir conta",
        "delete_account_warning": (
            "Isso exclui sua conta e TODAS as suas transações "
            "permanentemente. Essa ação não pode ser desfeita."
        ),
        "delete_account_type_email": "Digite seu e-mail para confirmar:",
        "delete_account_mismatch": "O e-mail não confere. Nada foi excluído.",
        "delete_account_failed": (
            "Não foi possível excluir a conta. Tente novamente mais "
            "tarde ou entre em contato com o suporte."
        ),
        "account_deleted": "Sua conta e seus dados foram excluídos.",
    },
    "en_US": {
        "title": "Overview", "balance": "Net balance",
        "income": "Income", "expenses": "Expenses",
        "transactions": "Recent transactions",
        "add": "+ New transaction", "edit": "Edit",
        "delete": "Delete", "refresh": "Refresh",
        "logout": "Sign out", "date": "Date",
        "description": "Description", "type": "Type",
        "category": "Category", "amount": "Amount",
        "notes": "Notes", "save": "Save",
        "cancel": "Cancel", "new": "New transaction",
        "edit_title": "Edit transaction", "expense": "Expense",
        "income_type": "Income", "food": "Food",
        "housing": "Housing", "transport": "Transport",
        "health": "Health", "education": "Education",
        "entertainment": "Entertainment", "salary": "Salary",
        "shopping": "Shopping", "bills": "Bills",
        "other": "Other", "confirm_delete": "Delete this transaction?",
        "confirm_title": "Confirm deletion",
        "select": "Select a transaction first.",
        "saved": "Transaction saved successfully!",
        "deleted": "Transaction deleted.",
        "error": "Error", "required": "Enter a description.",
        "currency": "USD", "welcome": "Welcome",
        "empty": "No transactions yet.",
        "load_error": "Could not load transactions.",
        "save_error": "Could not save the transaction.",
        "delete_error": "Could not delete the transaction.",
        "search": "Search transactions...",
        "all": "All",
        "date_start": "Date / start",
        "amount_each": "Amount (each time)",
        "repeats": "Repeats",
        "once": "One time", "daily": "Daily", "weekly": "Weekly",
        "monthly": "Monthly", "yearly": "Yearly",
        "until": "until {}",
        "has_end": "Set an end date", "end_date": "Ends on",
        "end_before_start": "The end date can't be before the start date.",
        "groceries": "Groceries", "fuel": "Fuel",
        "tab_charts": "Charts", "tab_transactions": "Transactions",
        "period": "Period",
        "p_month": "This month", "p_3": "Last 3 months",
        "p_6": "Last 6 months", "p_year": "This year", "p_all": "All time",
        "chart_monthly": "Income vs. expenses (last 6 months)",
        "chart_category": "Spending by category",
        "chart_balance": "Balance over time",
        "no_expenses": "no expenses", "balance_name": "Balance",
        "migration_needed": (
            "The database needs the recurrence update. "
            "Run migrations/001_add_recurrence.sql in Supabase."
        ),
        "help": "Help",
        "delete_account": "Delete account",
        "delete_account_warning": (
            "This permanently deletes your account and ALL of your "
            "transactions. This cannot be undone."
        ),
        "delete_account_type_email": "Type your email to confirm:",
        "delete_account_mismatch": "Email doesn't match. Nothing was deleted.",
        "delete_account_failed": (
            "Couldn't delete the account. Please try again later or "
            "contact support."
        ),
        "account_deleted": "Your account and data have been deleted.",
    },
}

T = TEXT[LANGUAGE]

CATEGORIES = [
    "food", "groceries", "housing", "transport", "fuel", "health",
    "education", "entertainment", "salary", "shopping", "bills", "other",
]

MONTHS = {
    "pt_BR": ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
              "Jul", "Ago", "Set", "Out", "Nov", "Dez"],
    "en_US": ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
}[LANGUAGE]

PERIODS = [
    ("p_month", "month"), ("p_3", "3"), ("p_6", "6"),
    ("p_year", "year"), ("p_all", "all"),
]


def money(value):
    amount = Decimal(str(value or 0))
    sign = "-" if amount < 0 else ""
    return f"{sign}${abs(amount):,.2f}"


class TransactionDialog(QDialog):
    def __init__(self, parent=None, transaction=None, client=None, user=None, custom_categories=None):
        super().__init__(parent)
        self.transaction = transaction
        self.client = client or default_supabase
        self.user = user
        self.custom_categories = list(custom_categories or [])
        self.setWindowTitle(T["edit_title"] if transaction else T["new"])
        self.setObjectName("transactionDialog")
        self.setMinimumWidth(470)
        self.resize(500, 570)
        self.setModal(True)

        # Header: title and a compact close button, matching the web dialog.
        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 18, 22, 20)
        layout.setSpacing(13)

        header = QHBoxLayout()
        header.setContentsMargins(0, 0, 0, 0)
        heading = QLabel(T["edit_title"] if transaction else T["new"])
        heading.setObjectName("transactionDialogTitle")
        close_button = QPushButton("×")
        close_button.setObjectName("dialogClose")
        close_button.setFixedSize(38, 38)
        close_button.clicked.connect(self.reject)
        header.addWidget(heading)
        header.addStretch(1)
        header.addWidget(close_button)
        layout.addLayout(header)

        self.title_input = QLineEdit()
        self.title_input.setMaxLength(120)
        self.title_input.setPlaceholderText("e.g. Monthly salary" if LANGUAGE == "en_US" else T["description"])

        self.amount_input = QDoubleSpinBox()
        self.amount_input.setRange(0, 9999999999.99)
        self.amount_input.setDecimals(2)
        self.amount_input.setPrefix("")
        self.amount_input.setGroupSeparatorShown(True)

        self.type_input = QComboBox()
        self.type_input.addItem(T["expense"], "expense")
        self.type_input.addItem(T["income_type"], "income")

        self.category_input = QComboBox()
        self._last_category = "food"
        self._refresh_category_options()
        self.category_input.currentIndexChanged.connect(self._category_changed)
        self.type_input.currentIndexChanged.connect(self._refresh_category_options)

        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat("MM/dd/yyyy")
        self.date_input.setDate(QDate.currentDate())

        # Recurrence remains supported, but the optional end-date controls are
        # only shown when a repeating schedule is selected.
        self.frequency_input = QComboBox()
        for key in FREQUENCIES:
            self.frequency_input.addItem(T[key], key)
        self.frequency_input.currentIndexChanged.connect(self.update_end_controls)

        self.end_check = QCheckBox(T["has_end"])
        self.end_check.toggled.connect(self.update_end_controls)
        self.end_input = QDateEdit()
        self.end_input.setCalendarPopup(True)
        self.end_input.setDisplayFormat("MM/dd/yyyy")
        self.end_input.setDate(QDate.currentDate().addYears(1))

        end_content = QHBoxLayout()
        end_content.setContentsMargins(0, 0, 0, 0)
        end_content.setSpacing(10)
        end_content.addWidget(self.end_check)
        end_content.addWidget(self.end_input, 1)
        self.end_field = QWidget()
        self.end_field.setLayout(end_content)

        self.notes_input = QTextEdit()
        self.notes_input.setMaximumHeight(78)
        self.notes_input.setMinimumHeight(72)
        self.notes_input.setPlaceholderText("Optional notes" if LANGUAGE == "en_US" else T["notes"])

        fields = QGridLayout()
        fields.setContentsMargins(0, 0, 0, 0)
        fields.setHorizontalSpacing(12)
        fields.setVerticalSpacing(11)
        fields.setColumnStretch(0, 1)
        fields.setColumnStretch(1, 1)

        def add_field(label_text, widget, row, column=0, span=1):
            label = QLabel(label_text)
            label.setObjectName("transactionFieldLabel")
            fields.addWidget(label, row * 2, column, 1, span)
            fields.addWidget(widget, row * 2 + 1, column, 1, span)
            widget.setMinimumHeight(46)
            return label

        add_field(T["description"], self.title_input, 0, 0, 2)
        add_field(T["amount"], self.amount_input, 1, 0)
        add_field(T["type"], self.type_input, 1, 1)
        add_field(T["category"], self.category_input, 2, 0, 2)
        add_field(T["date_start"], self.date_input, 3, 0)
        add_field(T["repeats"], self.frequency_input, 3, 1)
        self.end_label = add_field(T["end_date"], self.end_field, 4, 0, 2)
        add_field(T["notes"], self.notes_input, 5, 0, 2)
        layout.addLayout(fields)

        buttons = QHBoxLayout()
        buttons.setContentsMargins(0, 0, 0, 0)
        buttons.addStretch(1)
        cancel = QPushButton(T["cancel"])
        save = QPushButton(T["save"] if LANGUAGE != "en_US" else "Save transaction")
        save.setObjectName("primary")
        cancel.setMinimumWidth(125)
        save.setMinimumWidth(165)
        cancel.setMinimumHeight(46)
        save.setMinimumHeight(46)
        cancel.clicked.connect(self.reject)
        save.clicked.connect(self.validate_and_accept)
        buttons.addWidget(cancel)
        buttons.addWidget(save)
        layout.addLayout(buttons)

        if transaction:
            self.title_input.setText(transaction["title"])
            self.amount_input.setValue(float(transaction["amount"]))
            index = self.type_input.findData(transaction["type"])
            self.type_input.setCurrentIndex(max(0, index))

            category = transaction.get("category", "other")
            index = self.category_input.findData(category)
            if index >= 0:
                self.category_input.setCurrentIndex(index)

            parsed = QDate.fromString(transaction["transaction_date"], "yyyy-MM-dd")
            if parsed.isValid():
                self.date_input.setDate(parsed)

            index = self.frequency_input.findData(transaction.get("frequency") or "once")
            self.frequency_input.setCurrentIndex(max(0, index))

            end = QDate.fromString(transaction.get("end_date") or "", "yyyy-MM-dd")
            if end.isValid():
                self.end_input.setDate(end)
                self.end_check.setChecked(True)

            self.notes_input.setPlainText(transaction.get("notes") or "")

        self.update_end_controls()

    def _refresh_category_options(self):
        previous = self.category_input.currentData()
        tx_type = self.type_input.currentData()
        self.category_input.blockSignals(True)
        self.category_input.clear()
        self.category_input.addItem("+ Create new category...", "__create_new__")
        for key in CATEGORIES:
            self.category_input.addItem(T[key], key)
        for item in sorted(self.custom_categories, key=lambda c: c.get("name", "").lower()):
            if item.get("type") == tx_type:
                self.category_input.addItem(item.get("name", "Custom"), f"custom:{item.get('id')}")
        index = self.category_input.findData(previous)
        if index < 0:
            index = self.category_input.findData("food")
        self.category_input.setCurrentIndex(max(0, index))
        self._last_category = self.category_input.currentData() or "food"
        self.category_input.blockSignals(False)

    def _category_changed(self, index):
        selected_value = self.category_input.itemData(index)
        if selected_value != "__create_new__":
            if selected_value:
                self._last_category = selected_value
            return
        # Restore the last valid category before opening the prompt.
        self.category_input.blockSignals(True)
        restore_index = self.category_input.findData(self._last_category)
        self.category_input.setCurrentIndex(max(0, restore_index))
        self.category_input.blockSignals(False)
        name, ok = QInputDialog.getText(
            self, "Create category", "Category name (up to 32 characters):"
        )
        if not ok:
            return
        name = " ".join(name.strip().split())
        if not name or len(name) > 32:
            QMessageBox.warning(self, T["error"], "Enter a category name of 1–32 characters.")
            return
        tx_type = self.type_input.currentData()
        duplicate = next(
            (c for c in self.custom_categories
             if c.get("type") == tx_type and c.get("name", "").casefold() == name.casefold()),
            None,
        )
        if duplicate:
            category_id = duplicate["id"]
        else:
            try:
                response = self.client.table("custom_categories").insert({
                    "user_id": self.user.id,
                    "name": name,
                    "type": tx_type,
                }).select("id,name,type").execute()
                created_rows = response.data or []
                if not created_rows:
                    raise RuntimeError("Supabase did not return the created category.")
                created = created_rows[0]
                self.custom_categories.append(created)
                category_id = created["id"]
            except Exception as error:
                message = str(error)
                if "custom_categories" in message or "42P01" in message or "PGRST" in message:
                    message = (
                        "Custom categories are not set up in Supabase yet. "
                        "Run migrations/003_custom_categories.sql in the SQL Editor."
                    )
                QMessageBox.warning(self, T["error"], message)
                self._refresh_category_options()
                return
        self._refresh_category_options()
        selected = self.category_input.findData(f"custom:{category_id}")
        if selected >= 0:
            self.category_input.setCurrentIndex(selected)

    def update_end_controls(self):
        repeating = self.frequency_input.currentData() != "once"
        self.end_label.setVisible(repeating)
        self.end_field.setVisible(repeating)
        self.end_check.setEnabled(repeating)
        self.end_input.setEnabled(repeating and self.end_check.isChecked())

    def validate_and_accept(self):
        if not self.title_input.text().strip():
            QMessageBox.warning(self, T["error"], T["required"])
            return
        if self.amount_input.value() <= 0:
            QMessageBox.warning(self, T["error"], "Enter an amount greater than zero." if LANGUAGE == "en_US" else "Informe um valor maior que zero.")
            return
        if (
            self.end_input.isEnabled()
            and self.end_input.date() < self.date_input.date()
        ):
            QMessageBox.warning(self, T["error"], T["end_before_start"])
            return
        self.accept()

    def values(self):
        end_date = None
        if self.end_input.isEnabled():
            end_date = self.end_input.date().toString("yyyy-MM-dd")

        return {
            "title": self.title_input.text().strip(),
            "amount": round(self.amount_input.value(), 2),
            "type": self.type_input.currentData(),
            "category": self.category_input.currentData(),
            "transaction_date": self.date_input.date().toString(
                "yyyy-MM-dd"
            ),
            "frequency": self.frequency_input.currentData(),
            "end_date": end_date,
            "notes": self.notes_input.toPlainText().strip()[:500],
        }


def repeats_label(transaction):
    """Human-readable recurrence, e.g. 'Monthly' or 'Daily until 2026-12-31'."""
    frequency = transaction.get("frequency") or "once"
    label = T.get(frequency, frequency)
    end = transaction.get("end_date")
    if frequency != "once" and end:
        label += " " + T["until"].format(end)
    return label


class Dashboard(QWidget):
    logged_out = Signal()
    add_account_requested = Signal()
    switch_account_requested = Signal(str)

    def __init__(self, user, client=None, account_manager=None, account_id="primary"):
        super().__init__()
        self.user = user
        self.client = client or default_supabase
        self.account_manager = account_manager
        self.account_id = account_id
        self.custom_categories = []
        self.rows = []

        self.setWindowTitle("FinanceTracker")

        # Fit the initial window inside the usable desktop area. The old
        # fixed 1150x800 size pushed the footer below the screen on laptops.
        screen = QGuiApplication.primaryScreen()
        available = screen.availableGeometry() if screen else None
        if available:
            initial_width = min(1150, max(760, available.width() - 64))
            initial_height = min(740, max(540, available.height() - 64))
            self.resize(initial_width, initial_height)
        else:
            self.resize(1050, 680)
        self.setMinimumSize(760, 540)

        # All windows share the app-wide theme stylesheet.


        root = QVBoxLayout(self)
        # The content must reach the bottom edge. Floating actions are overlays,
        # not a footer row that reserves a dark strip below the charts.
        root.setContentsMargins(24, 20, 24, 0)
        root.setSpacing(16)

        self.status = QLabel("")
        self.status.setObjectName("muted")
        self.status.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        header = QHBoxLayout()
        brand = QLabel("FinanceTracker")
        brand.setObjectName("brand")
        header.addWidget(brand)
        # Keep account email inside Settings; the Overview header stays clean.
        header.addStretch()
        header.addWidget(self.status)
        root.addLayout(header)

        title_row = QHBoxLayout()
        title = QLabel(T["title"])
        title.setStyleSheet("font-size: 25px; font-weight: 700;")
        title_row.addWidget(title)
        title_row.addStretch()

        period_label = QLabel(T["period"])
        period_label.setObjectName("muted")
        self.period = QComboBox()
        for text_key, data in PERIODS:
            self.period.addItem(T[text_key], data)
        self.period.setCurrentIndex(0)
        self.period.currentIndexChanged.connect(self.refresh_views)
        title_row.addWidget(period_label)
        title_row.addWidget(self.period)
        root.addLayout(title_row)

        metrics = QHBoxLayout()
        self.balance_value = self.metric_card(T["balance"], metrics)
        self.income_value = self.metric_card(T["income"], metrics)
        self.expense_value = self.metric_card(T["expenses"], metrics)
        root.addLayout(metrics)

        self.tabs = QTabWidget()
        self.tabs.addTab(self.build_charts_tab(), T["tab_charts"])
        self.tabs.addTab(
            self.build_transactions_tab(), T["tab_transactions"]
        )
        root.addWidget(self.tabs, 1)

        # Two independent floating actions, matching the website. They are
        # direct children of the dashboard (not a footer/frame/layout), so
        # absolutely no full-width footer widget or reserved footer space exists.
        self.about_button = QPushButton("ⓘ  About", self)
        self.about_button.setObjectName("floatingAction")
        self.about_button.setToolTip("About FinanceTracker")
        self.about_button.clicked.connect(self.show_about)

        self.settings_button = QPushButton("⚙  Settings", self)
        self.settings_button.setObjectName("floatingAction")
        self.settings_button.setToolTip("FinanceTracker settings")
        self.settings_button.clicked.connect(self.open_settings)
        self._position_floating_actions()

        self.load_transactions()

        # First login on this account: show the tutorial once the window
        # is up (slight delay so it appears on top of the dashboard).
        if should_show(self.user):
            QTimer.singleShot(400, self.show_first_login_tutorial)

    def _position_floating_actions(self):
        """Place About and Settings as separate overlay buttons at bottom-left."""
        if not hasattr(self, "about_button"):
            return
        margin = 24
        bottom = 20
        height = 38
        y = max(8, self.height() - bottom - height)
        self.about_button.setGeometry(margin, y, 84, height)
        self.settings_button.setGeometry(margin + 94, y, 100, height)
        self.about_button.raise_()
        self.settings_button.raise_()

    def resizeEvent(self, event):
        """Keep both action buttons floating over the dashboard content."""
        super().resizeEvent(event)
        self._position_floating_actions()

    def show_tutorial(self):
        TutorialDialog(self).exec()

    def show_first_login_tutorial(self):
        self.show_tutorial()
        # Skipped or finished: either way, don't show it again.
        mark_seen(self.user, self.client)

    # ------------------------------------------------------------ layout
    def build_charts_tab(self):
        # A scrollable chart canvas prevents Qt Charts from being squeezed
        # into overlapping rows on shorter displays or when the window is
        # not maximized.
        page = QWidget()
        page_layout = QVBoxLayout(page)
        page_layout.setContentsMargins(0, 8, 0, 0)
        page_layout.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        canvas = QWidget()
        grid = QGridLayout(canvas)
        grid.setContentsMargins(0, 0, 8, 8)
        grid.setHorizontalSpacing(14)
        grid.setVerticalSpacing(14)

        self.monthly_chart = MonthlyBarChart()
        self.category_chart = CategoryDonutChart()
        self.balance_chart = BalanceLineChart()

        # Give each chart its own predictable vertical space.
        # Slightly shorter cards leave more of the dashboard visible in a
        # normal (non-maximized) laptop window; the chart area remains scrollable.
        self.monthly_chart.setMinimumHeight(225)
        self.category_chart.setMinimumHeight(225)
        self.balance_chart.setMinimumHeight(240)
        grid.addWidget(self.monthly_chart, 0, 0)
        grid.addWidget(self.category_chart, 0, 1)
        grid.addWidget(self.balance_chart, 1, 0, 1, 2)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        grid.setRowMinimumHeight(0, 225)
        grid.setRowMinimumHeight(1, 240)
        grid.setRowStretch(0, 0)
        grid.setRowStretch(1, 0)

        scroll.setWidget(canvas)
        page_layout.addWidget(scroll)
        return page

    def build_transactions_tab(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 8, 0, 0)
        layout.setSpacing(12)

        section = QHBoxLayout()
        section.addWidget(QLabel(T["transactions"]))
        section.addStretch()

        self.search = QLineEdit()
        self.search.setPlaceholderText(T["search"])
        self.search.textChanged.connect(self.filter_rows)
        self.search.setMaximumWidth(230)
        section.addWidget(self.search)

        refresh = QPushButton(T["refresh"])
        refresh.clicked.connect(self.load_transactions)
        section.addWidget(refresh)

        add = QPushButton(T["add"])
        add.setObjectName("primary")
        add.clicked.connect(self.add_transaction)
        section.addWidget(add)
        layout.addLayout(section)

        actions = QHBoxLayout()
        edit = QPushButton(T["edit"])
        edit.clicked.connect(self.edit_transaction)
        delete = QPushButton(T["delete"])
        delete.clicked.connect(self.delete_transaction)
        actions.addWidget(edit)
        actions.addWidget(delete)
        actions.addStretch()
        layout.addLayout(actions)

        self.table = QTableWidget(0, 7)
        self.table.setHorizontalHeaderLabels([
            T["date"], T["description"], T["category"],
            T["type"], T["amount"], T["repeats"], T["notes"]
        ])
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.table.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )
        self.table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.ResizeToContents
        )
        self.table.horizontalHeader().setSectionResizeMode(
            5, QHeaderView.ResizeMode.ResizeToContents
        )
        layout.addWidget(self.table, 1)
        return page

    def metric_card(self, label, parent_layout):
        panel = QFrame()
        panel.setObjectName("panel")
        layout = QVBoxLayout(panel)
        heading = QLabel(label)
        heading.setObjectName("muted")
        value = QLabel("$0.00")
        value.setObjectName("metric")
        layout.addWidget(heading)
        layout.addWidget(value)
        parent_layout.addWidget(panel)
        return value

    # -------------------------------------------------------------- data
    def load_transactions(self):
        try:
            result = (
                self.client.table("transactions")
                .select("*")
                .eq("user_id", self.user.id)
                .order("transaction_date", desc=True)
                .execute()
            )
            self.rows = result.data or []
            try:
                categories_result = (
                    self.client.table("custom_categories")
                    .select("id,name,type")
                    .eq("user_id", self.user.id)
                    .order("name")
                    .execute()
                )
                self.custom_categories = categories_result.data or []
            except Exception as category_error:
                # Existing users can keep using built-in categories if the
                # optional custom-category migration has not been run.
                self.custom_categories = []
                print("Custom category load warning:", str(category_error))
            self.render_rows()
            self.refresh_views()
            self.status.setText("")
        except Exception as error:
            print("Transaction load error:", str(error))
            self.status.setText(T["load_error"])

    def category_label(self, value):
        if str(value).startswith("custom:"):
            category_id = str(value).split(":", 1)[1]
            found = next((c for c in self.custom_categories if str(c.get("id")) == category_id), None)
            return found.get("name", "Custom category") if found else "Custom category"
        return T.get(value, value)

    def render_rows(self):
        query = self.search.text().strip().lower()
        filtered = [
            row for row in self.rows
            if query in " ".join([
                str(row.get("title") or ""),
                self.category_label(row.get("category") or "other"),
                str(row.get("type") or ""),
                str(row.get("notes") or ""),
                repeats_label(row),
            ]).lower()
        ]

        self.table.setRowCount(len(filtered))

        for row_index, transaction in enumerate(filtered):
            category = transaction.get("category") or "other"
            category_label = self.category_label(category)
            type_label = (
                T["income_type"] if transaction["type"] == "income"
                else T["expense"]
            )

            values = [
                transaction.get("transaction_date", ""),
                transaction.get("title", ""),
                category_label,
                type_label,
                money(transaction.get("amount", 0)),
                repeats_label(transaction),
                transaction.get("notes") or "",
            ]

            for column, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                if column == 0:
                    item.setData(Qt.ItemDataRole.UserRole, transaction["id"])
                if column == 4:
                    item.setTextAlignment(
                        Qt.AlignmentFlag.AlignRight
                        | Qt.AlignmentFlag.AlignVCenter
                    )
                self.table.setItem(row_index, column, item)

    def filter_rows(self):
        self.render_rows()

    # ------------------------------------------------- totals and charts
    def period_start(self, today, earliest):
        choice = self.period.currentData()
        if choice == "month":
            return today.replace(day=1)
        if choice == "3":
            return add_months_to_first(today, -2)
        if choice == "6":
            return add_months_to_first(today, -5)
        if choice == "year":
            return date(today.year, 1, 1)
        return earliest  # "all"

    def refresh_views(self):
        """Recompute totals and charts from the stored transactions.

        Recurring transactions are expanded into individual occurrences
        up to today, so a monthly salary counts once per month and a
        daily expense counts once per day.
        """
        today = date.today()

        starts = []
        for row in self.rows:
            try:
                start = parse_date(row.get("transaction_date"))
            except ValueError:
                start = None
            if start:
                starts.append(start)
        earliest = min(starts + [today])

        occurrences = expand(self.rows, earliest, today)
        range_start = self.period_start(today, earliest)

        in_period = [o for o in occurrences if o["date"] >= range_start]
        opening = sum(
            (signed(o) for o in occurrences if o["date"] < range_start),
            Decimal("0"),
        )

        income, expenses = totals(in_period)
        self.income_value.setText(money(income))
        self.expense_value.setText(money(expenses))
        self.balance_value.setText(money(income - expenses))

        months = monthly_summary(occurrences, today, 6)
        self.monthly_chart.set_data(
            months,
            [MONTHS[m[0].month - 1] for m in months],
            T["chart_monthly"], T["income"], T["expenses"],
        )

        self.category_chart.set_data(
            [(self.category_label(k), v) for k, v in category_totals(in_period)],
            T["chart_category"], T["no_expenses"],
        )

        self.balance_chart.set_data(
            balance_series(in_period, opening, range_start, today),
            T["chart_balance"], T["balance_name"],
        )

    # ---------------------------------------------------------- actions
    def save_error_text(self, error):
        text = str(error)
        if "frequency" in text or "end_date" in text:
            return T["migration_needed"]
        return T["save_error"]

    def add_transaction(self):
        dialog = TransactionDialog(
            self, client=self.client, user=self.user,
            custom_categories=self.custom_categories,
        )
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        try:
            values = dialog.values()
            values["user_id"] = self.user.id
            self.client.table("transactions").insert(values).execute()
            self.load_transactions()
            QMessageBox.information(self, "FinanceTracker", T["saved"])
        except Exception as error:
            print("Transaction insert error:", str(error))
            QMessageBox.warning(
                self, T["error"], self.save_error_text(error)
            )

    def selected_transaction(self):
        row_index = self.table.currentRow()
        if row_index < 0:
            QMessageBox.information(self, T["error"], T["select"])
            return None

        transaction_id = self.table.item(
            row_index, 0
        ).data(Qt.ItemDataRole.UserRole)

        return next(
            (item for item in self.rows if item["id"] == transaction_id),
            None
        )

    def edit_transaction(self):
        transaction = self.selected_transaction()
        if not transaction:
            return

        dialog = TransactionDialog(
            self, transaction, client=self.client, user=self.user,
            custom_categories=self.custom_categories,
        )
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        try:
            self.client.table("transactions").update(
                dialog.values()
            ).eq("id", transaction["id"]).eq(
                "user_id", self.user.id
            ).execute()
            self.load_transactions()
            QMessageBox.information(self, "FinanceTracker", T["saved"])
        except Exception as error:
            print("Transaction update error:", str(error))
            QMessageBox.warning(
                self, T["error"], self.save_error_text(error)
            )

    def delete_transaction(self):
        transaction = self.selected_transaction()
        if not transaction:
            return

        answer = QMessageBox.question(
            self, T["confirm_title"], T["confirm_delete"]
        )
        if answer != QMessageBox.StandardButton.Yes:
            return

        try:
            self.client.table("transactions").delete().eq(
                "id", transaction["id"]
            ).eq("user_id", self.user.id).execute()
            self.load_transactions()
            QMessageBox.information(self, "FinanceTracker", T["deleted"])
        except Exception as error:
            print("Transaction delete error:", str(error))
            QMessageBox.warning(self, T["error"], T["delete_error"])

    def show_about(self):
        AboutDialog(self).exec()

    def open_settings(self):
        accounts = self.account_manager.active_accounts() if self.account_manager else [
            {"id": self.account_id, "email": self.user.email or "Account"}
        ]
        dialog = SettingsDialog(self.user, accounts, self.account_id, self)
        dialog.add_account_requested.connect(
            lambda: (dialog.accept(), self.add_account_requested.emit())
        )
        dialog.switch_account_requested.connect(self.switch_account_requested.emit)
        dialog.sign_out_requested.connect(
            lambda: (dialog.accept(), self.logout())
        )
        dialog.delete_account_requested.connect(
            lambda: (dialog.accept(), self.delete_account())
        )
        dialog.help_requested.connect(self.show_tutorial)
        dialog.theme_changed.connect(self.change_theme)
        dialog.exec()

    def change_theme(self, theme):
        from PySide6.QtWidgets import QApplication
        app = QApplication.instance()
        if app:
            apply_theme(app, theme)
            self.refresh_views()
        self.refresh_views()

    def delete_account(self):
        """Permanently delete the user's account and every transaction.

        Needs migrations/002_rls_and_account_deletion.sql (a database function
        that removes the signed-in user; the client can't do it alone).
        """
        answer = QMessageBox.warning(
            self, T["delete_account"], T["delete_account_warning"],
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel,
            QMessageBox.StandardButton.Cancel,
        )
        if answer != QMessageBox.StandardButton.Yes:
            return

        email = (self.user.email or "").strip().lower()
        typed, ok = QInputDialog.getText(
            self, T["delete_account"], T["delete_account_type_email"]
        )
        if not ok:
            return
        if typed.strip().lower() != email:
            QMessageBox.information(
                self, T["delete_account"], T["delete_account_mismatch"]
            )
            return

        try:
            self.client.rpc("delete_my_account").execute()
        except Exception as error:
            print("Account deletion error:", str(error))
            QMessageBox.warning(
                self, T["error"], T["delete_account_failed"]
            )
            return

        try:
            self.client.auth.sign_out()
        except Exception as error:
            print("Sign-out after deletion:", str(error))

        QMessageBox.information(
            self, T["delete_account"], T["account_deleted"]
        )
        self.logged_out.emit()
        self.close()

    def logout(self):
        try:
            self.client.auth.sign_out()
            self.logged_out.emit()
            self.close()
        except Exception as error:
            print("Sign-out error:", str(error))
            QMessageBox.warning(self, T["error"], tr("operation_failed"))
