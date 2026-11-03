
from datetime import date
from decimal import Decimal

from PySide6.QtCore import Qt, QDate, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QDialog, QFormLayout,
    QLineEdit, QComboBox, QDoubleSpinBox, QDateEdit,
    QTextEdit, QMessageBox, QHeaderView, QFrame, QCheckBox, QTabWidget,
    QInputDialog
)

from app.analytics import (
    balance_series, category_totals, monthly_summary, signed, totals,
)
from app.i18n import LANGUAGE, tr
from app.recurrence import FREQUENCIES, add_months_to_first, expand, parse_date
from app.services.supabase_service import supabase
from app.ui.charts import BalanceLineChart, CategoryDonutChart, MonthlyBarChart


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
        "date_start": "Date / starts on",
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
    def __init__(self, parent=None, transaction=None):
        super().__init__(parent)
        self.transaction = transaction
        self.setWindowTitle(
            T["edit_title"] if transaction else T["new"]
        )
        self.setMinimumWidth(420)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.title_input = QLineEdit()
        self.title_input.setMaxLength(120)
        self.title_input.setPlaceholderText(T["description"])

        self.amount_input = QDoubleSpinBox()
        self.amount_input.setRange(0.01, 9999999999.99)
        self.amount_input.setDecimals(2)
        self.amount_input.setPrefix("$ ")
        self.amount_input.setGroupSeparatorShown(True)

        self.type_input = QComboBox()
        self.type_input.addItem(T["expense"], "expense")
        self.type_input.addItem(T["income_type"], "income")

        self.category_input = QComboBox()
        for key in CATEGORIES:
            self.category_input.addItem(T[key], key)

        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat("yyyy-MM-dd")
        self.date_input.setDate(QDate.currentDate())

        # Recurrence: one-time, or repeating (daily/weekly/monthly/yearly)
        self.frequency_input = QComboBox()
        for key in FREQUENCIES:
            self.frequency_input.addItem(T[key], key)
        self.frequency_input.currentIndexChanged.connect(
            self.update_end_controls
        )

        self.end_check = QCheckBox(T["has_end"])
        self.end_check.toggled.connect(self.update_end_controls)
        self.end_input = QDateEdit()
        self.end_input.setCalendarPopup(True)
        self.end_input.setDisplayFormat("yyyy-MM-dd")
        self.end_input.setDate(QDate.currentDate().addYears(1))

        end_row = QHBoxLayout()
        end_row.addWidget(self.end_check)
        end_row.addWidget(self.end_input, 1)

        self.notes_input = QTextEdit()
        self.notes_input.setMaximumHeight(85)
        self.notes_input.setPlaceholderText(T["notes"])

        form.addRow(T["description"], self.title_input)
        form.addRow(T["amount_each"], self.amount_input)
        form.addRow(T["type"], self.type_input)
        form.addRow(T["category"], self.category_input)
        form.addRow(T["date_start"], self.date_input)
        form.addRow(T["repeats"], self.frequency_input)
        form.addRow(T["end_date"], end_row)
        form.addRow(T["notes"], self.notes_input)
        layout.addLayout(form)

        buttons = QHBoxLayout()
        cancel = QPushButton(T["cancel"])
        save = QPushButton(T["save"])
        save.setObjectName("primary")
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

            parsed = QDate.fromString(
                transaction["transaction_date"], "yyyy-MM-dd"
            )
            if parsed.isValid():
                self.date_input.setDate(parsed)

            index = self.frequency_input.findData(
                transaction.get("frequency") or "once"
            )
            self.frequency_input.setCurrentIndex(max(0, index))

            end = QDate.fromString(
                transaction.get("end_date") or "", "yyyy-MM-dd"
            )
            if end.isValid():
                self.end_input.setDate(end)
                self.end_check.setChecked(True)

            self.notes_input.setPlainText(transaction.get("notes") or "")

        self.update_end_controls()

    def update_end_controls(self):
        repeating = self.frequency_input.currentData() != "once"
        self.end_check.setEnabled(repeating)
        self.end_input.setEnabled(repeating and self.end_check.isChecked())

    def validate_and_accept(self):
        if not self.title_input.text().strip():
            QMessageBox.warning(self, T["error"], T["required"])
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

    def __init__(self, user):
        super().__init__()
        self.user = user
        self.rows = []

        self.setWindowTitle("FinanceTracker")
        self.resize(1150, 800)
        self.setMinimumSize(900, 620)

        self.setStyleSheet("""
            QWidget {
                background: #101512;
                color: #edf5ef;
                font-family: "Noto Sans", sans-serif;
                font-size: 13px;
            }
            QFrame#panel {
                background: #19221c;
                border: 1px solid #2b3b30;
                border-radius: 12px;
            }
            QLabel#brand {
                color: #7ee2a8;
                font-size: 23px;
                font-weight: 800;
            }
            QLabel#metric {
                color: #7ee2a8;
                font-size: 24px;
                font-weight: 700;
            }
            QLabel#muted { color: #a6b7aa; }
            QPushButton {
                background: #26332a;
                border: 1px solid #35463a;
                border-radius: 8px;
                padding: 9px 12px;
            }
            QPushButton:hover { background: #35483a; }
            QPushButton#primary {
                background: #65cf91;
                color: #102016;
                border: none;
                font-weight: 700;
            }
            QLineEdit, QComboBox, QDoubleSpinBox, QDateEdit, QTextEdit {
                background: #101512;
                border: 1px solid #35463a;
                border-radius: 7px;
                padding: 8px;
            }
            QComboBox QAbstractItemView {
                background: #19221c;
                selection-background-color: #315c40;
            }
            QTabWidget::pane { border: none; }
            QTabBar::tab {
                background: #19221c;
                color: #a6b7aa;
                padding: 9px 18px;
                border: 1px solid #2b3b30;
                border-radius: 8px;
                margin-right: 6px;
            }
            QTabBar::tab:selected {
                background: #26332a;
                color: #edf5ef;
                font-weight: 700;
            }
            QTableWidget {
                background: #19221c;
                alternate-background-color: #1d2921;
                border: 1px solid #2b3b30;
                border-radius: 8px;
                gridline-color: #2b3b30;
                selection-background-color: #315c40;
            }
            QHeaderView::section {
                background: #202d24;
                color: #c7d7cb;
                padding: 9px;
                border: none;
            }
        """)

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(16)

        header = QHBoxLayout()
        brand = QLabel("FinanceTracker")
        brand.setObjectName("brand")

        self.user_label = QLabel(user.email or "")
        self.user_label.setObjectName("muted")

        logout = QPushButton(T["logout"])
        logout.clicked.connect(self.logout)

        delete_account = QPushButton(T["delete_account"])
        delete_account.setStyleSheet(
            "color: #f2b8a8; border: 1px solid #5a3a33;"
        )
        delete_account.clicked.connect(self.delete_account)

        header.addWidget(brand)
        header.addStretch()
        header.addWidget(self.user_label)
        header.addWidget(delete_account)
        header.addWidget(logout)
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

        self.status = QLabel("")
        self.status.setObjectName("muted")
        root.addWidget(self.status)

        self.load_transactions()

    # ------------------------------------------------------------ layout
    def build_charts_tab(self):
        page = QWidget()
        grid = QGridLayout(page)
        grid.setContentsMargins(0, 8, 0, 0)
        grid.setSpacing(14)

        self.monthly_chart = MonthlyBarChart()
        self.category_chart = CategoryDonutChart()
        self.balance_chart = BalanceLineChart()

        grid.addWidget(self.monthly_chart, 0, 0)
        grid.addWidget(self.category_chart, 0, 1)
        grid.addWidget(self.balance_chart, 1, 0, 1, 2)
        grid.setRowStretch(0, 1)
        grid.setRowStretch(1, 1)
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
                supabase.table("transactions")
                .select("*")
                .eq("user_id", self.user.id)
                .order("transaction_date", desc=True)
                .execute()
            )
            self.rows = result.data or []
            self.render_rows()
            self.refresh_views()
            self.status.setText("")
        except Exception as error:
            print("Transaction load error:", str(error))
            self.status.setText(T["load_error"])

    def render_rows(self):
        query = self.search.text().strip().lower()
        filtered = [
            row for row in self.rows
            if query in " ".join([
                str(row.get("title") or ""),
                str(row.get("category") or ""),
                str(row.get("type") or ""),
                str(row.get("notes") or ""),
                repeats_label(row),
            ]).lower()
        ]

        self.table.setRowCount(len(filtered))

        for row_index, transaction in enumerate(filtered):
            category = transaction.get("category") or "other"
            category_label = T.get(category, category)
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
            [(T.get(k, k), v) for k, v in category_totals(in_period)],
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
        dialog = TransactionDialog(self)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        try:
            values = dialog.values()
            values["user_id"] = self.user.id
            supabase.table("transactions").insert(values).execute()
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

        dialog = TransactionDialog(self, transaction)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        try:
            supabase.table("transactions").update(
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
            supabase.table("transactions").delete().eq(
                "id", transaction["id"]
            ).eq("user_id", self.user.id).execute()
            self.load_transactions()
            QMessageBox.information(self, "FinanceTracker", T["deleted"])
        except Exception as error:
            print("Transaction delete error:", str(error))
            QMessageBox.warning(self, T["error"], T["delete_error"])

    def delete_account(self):
        """Permanently delete the user's account and every transaction.

        Needs migrations/002_account_deletion.sql (a database function
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
            supabase.rpc("delete_my_account").execute()
        except Exception as error:
            print("Account deletion error:", str(error))
            QMessageBox.warning(
                self, T["error"], T["delete_account_failed"]
            )
            return

        try:
            supabase.auth.sign_out()
        except Exception as error:
            print("Sign-out after deletion:", str(error))

        QMessageBox.information(
            self, T["delete_account"], T["account_deleted"]
        )
        self.logged_out.emit()
        self.close()

    def logout(self):
        try:
            supabase.auth.sign_out()
            self.logged_out.emit()
            self.close()
        except Exception as error:
            print("Sign-out error:", str(error))
            QMessageBox.warning(self, T["error"], tr("operation_failed"))
