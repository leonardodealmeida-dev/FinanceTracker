
from datetime import date
from decimal import Decimal

from PySide6.QtCore import Qt, QDate, Signal;
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QDialog, QFormLayout,
    QLineEdit, QComboBox, QDoubleSpinBox, QDateEdit,
    QTextEdit, QMessageBox, QHeaderView, QFrame
)

from app.i18n import LANGUAGE
from app.services.supabase_service import supabase


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
    },
}

T = TEXT[LANGUAGE]

CATEGORIES = [
    "food", "housing", "transport", "health", "education",
    "entertainment", "salary", "shopping", "bills", "other",
]


def money(value):
    amount = Decimal(str(value or 0))
    return f"${amount:,.2f}"


class TransactionDialog(QDialog):
    def __init__(self, parent=None, transaction=None):
        super().__init__(parent)
        self.transaction = transaction
        self.setWindowTitle(
            T["edit_title"] if transaction else T["new"]
        )
        self.setMinimumWidth(390)

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

        self.notes_input = QTextEdit()
        self.notes_input.setMaximumHeight(85)
        self.notes_input.setPlaceholderText(T["notes"])

        form.addRow(T["description"], self.title_input)
        form.addRow(T["amount"], self.amount_input)
        form.addRow(T["type"], self.type_input)
        form.addRow(T["category"], self.category_input)
        form.addRow(T["date"], self.date_input)
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

            self.notes_input.setPlainText(transaction.get("notes", ""))

    def validate_and_accept(self):
        if not self.title_input.text().strip():
            QMessageBox.warning(self, T["error"], T["required"])
            return
        self.accept()

    def values(self):
        return {
            "title": self.title_input.text().strip(),
            "amount": round(self.amount_input.value(), 2),
            "type": self.type_input.currentData(),
            "category": self.category_input.currentData(),
            "transaction_date": self.date_input.date().toString(
                "yyyy-MM-dd"
            ),
            "notes": self.notes_input.toPlainText().strip()[:500],
        }


class Dashboard(QWidget):
    logged_out = Signal()

    def __init__(self, user):
        super().__init__()
        self.user = user
        self.rows = []

        self.setWindowTitle("FinanceTracker")
        self.resize(1050, 700)
        self.setMinimumSize(760, 520)

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

        header.addWidget(brand)
        header.addStretch()
        header.addWidget(self.user_label)
        header.addWidget(logout)
        root.addLayout(header)

        title = QLabel(T["title"])
        title.setStyleSheet("font-size: 25px; font-weight: 700;")
        root.addWidget(title)

        metrics = QHBoxLayout()
        self.balance_value = self.metric_card(T["balance"], metrics)
        self.income_value = self.metric_card(T["income"], metrics)
        self.expense_value = self.metric_card(T["expenses"], metrics)
        root.addLayout(metrics)

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
        root.addLayout(section)

        actions = QHBoxLayout()
        edit = QPushButton(T["edit"])
        edit.clicked.connect(self.edit_transaction)
        delete = QPushButton(T["delete"])
        delete.clicked.connect(self.delete_transaction)
        actions.addWidget(edit)
        actions.addWidget(delete)
        actions.addStretch()
        root.addLayout(actions)

        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels([
            T["date"], T["description"], T["category"],
            T["type"], T["amount"], T["notes"]
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
        root.addWidget(self.table, 1)

        self.status = QLabel("")
        self.status.setObjectName("muted")
        root.addWidget(self.status)

        self.load_transactions()

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
            self.update_totals()
            self.status.setText("")
        except Exception as error:
            print("Transaction load error:", str(error))
            self.status.setText(T["load_error"])

    def render_rows(self):
        query = self.search.text().strip().lower()
        filtered = [
            row for row in self.rows
            if query in " ".join([
                str(row.get("title", "")),
                str(row.get("category", "")),
                str(row.get("type", "")),
                str(row.get("notes", "")),
            ]).lower()
        ]

        self.table.setRowCount(len(filtered))

        for row_index, transaction in enumerate(filtered):
            category = transaction.get("category", "other")
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
                transaction.get("notes", ""),
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

    def update_totals(self):
        income = sum(
            (Decimal(str(row["amount"])) for row in self.rows
             if row["type"] == "income"),
            Decimal("0")
        )
        expenses = sum(
            (Decimal(str(row["amount"])) for row in self.rows
             if row["type"] == "expense"),
            Decimal("0")
        )
        self.income_value.setText(money(income))
        self.expense_value.setText(money(expenses))
        self.balance_value.setText(money(income - expenses))

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
            QMessageBox.warning(self, T["error"], T["save_error"])

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
            QMessageBox.warning(self, T["error"], T["save_error"])

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

    def logout(self):
        try:
            supabase.auth.sign_out()
            self.logged_out.emit()
            self.close()
        except Exception as error:
            print("Sign-out error:", str(error))
            QMessageBox.warning(self, T["error"], T["operation_failed"])
