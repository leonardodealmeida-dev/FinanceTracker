"""First-login tutorial: a short, skippable walkthrough."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog, QHBoxLayout, QLabel, QPushButton, QStackedWidget, QVBoxLayout,
    QWidget,
)

from app.i18n import LANGUAGE

TEXTS = {
    "pt_BR": {
        "window": "Bem-vindo ao FinanceTracker",
        "skip": "Pular", "back": "Voltar", "next": "Próximo",
        "done": "Começar!",
        "steps": [
            ("Bem-vindo ao FinanceTracker! 👋",
             "Aqui você acompanha suas <b>receitas</b> e <b>despesas</b> e vê "
             "para onde seu dinheiro está indo.<br><br>"
             "Este tour rápido leva cerca de 1 minuto. Você pode pular e "
             "abri-lo de novo a qualquer momento pelo botão <b>Ajuda</b>."),
            ("1. Adicione sua primeira transação",
             "Abra a aba <b>Transações</b> e clique em <b>Adicionar</b>.<br><br>"
             "Informe a descrição, o valor, se é <b>receita</b> ou "
             "<b>despesa</b>, a categoria e a data. Depois é só salvar."),
            ("2. Transações que se repetem",
             "Não precisa lançar seu salário todo mês! No campo "
             "<b>Repete</b>, escolha <b>diariamente, semanalmente, "
             "mensalmente ou anualmente</b>.<br><br>"
             "Exemplos: salário (mensal), combustível (diário), mercado "
             "(semanal). Você também pode definir uma <b>data final</b>."),
            ("3. Veja tudo em gráficos",
             "A aba <b>Gráficos</b> mostra receitas vs. despesas dos últimos "
             "6 meses, gastos por categoria e a evolução do seu saldo.<br><br>"
             "Use o seletor de <b>Período</b> no topo (este mês, 3 meses, "
             "este ano, tudo) para mudar o que é exibido."),
            ("4. Seus dados, sob seu controle",
             "Na aba Transações você pode <b>editar</b>, <b>excluir</b> e "
             "<b>buscar</b> lançamentos.<br><br>"
             "Cada pessoa só vê os próprios dados. Se quiser, "
             "<b>Excluir conta</b> apaga sua conta e tudo que está nela. "
             "Pronto, é só começar!"),
        ],
    },
    "en_US": {
        "window": "Welcome to FinanceTracker",
        "skip": "Skip", "back": "Back", "next": "Next",
        "done": "Get started!",
        "steps": [
            ("Welcome to FinanceTracker! 👋",
             "Track your <b>income</b> and <b>expenses</b> and see where your "
             "money is going.<br><br>"
             "This quick tour takes about a minute. You can skip it and "
             "reopen it any time with the <b>Help</b> button."),
            ("1. Add your first transaction",
             "Open the <b>Transactions</b> tab and click <b>Add</b>.<br><br>"
             "Enter a description, the amount, whether it's <b>income</b> or "
             "an <b>expense</b>, the category and the date. Then save."),
            ("2. Transactions that repeat",
             "No need to enter your salary every month! In the "
             "<b>Repeats</b> field choose <b>daily, weekly, monthly or "
             "yearly</b>.<br><br>"
             "Examples: salary (monthly), gas (daily), groceries (weekly). "
             "You can also set an <b>end date</b>."),
            ("3. See it all in charts",
             "The <b>Charts</b> tab shows income vs. expenses for the last "
             "6 months, spending by category and how your balance changes.<br><br>"
             "Use the <b>Period</b> selector at the top (this month, 3 "
             "months, this year, all time) to change what's shown."),
            ("4. Your data, your control",
             "In the Transactions tab you can <b>edit</b>, <b>delete</b> and "
             "<b>search</b> entries.<br><br>"
             "Everyone only sees their own data. If you ever want to leave, "
             "<b>Delete account</b> removes your account and everything in "
             "it. That's it, you're ready!"),
        ],
    },
}[LANGUAGE]


class TutorialDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(TEXTS["window"])
        self.setMinimumSize(540, 360)
        self.setModal(True)

        steps = TEXTS["steps"]
        self.last = len(steps) - 1

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 20)
        layout.setSpacing(14)

        self.pages = QStackedWidget()
        for title, body in steps:
            page = QWidget()
            page_layout = QVBoxLayout(page)
            page_layout.setContentsMargins(0, 0, 0, 0)

            heading = QLabel(title)
            heading.setStyleSheet(
                "font-size: 21px; font-weight: 700; color: #7ee2a8;"
            )
            heading.setWordWrap(True)

            text = QLabel(body)
            text.setTextFormat(Qt.TextFormat.RichText)
            text.setWordWrap(True)
            text.setAlignment(Qt.AlignmentFlag.AlignTop)
            text.setStyleSheet("font-size: 14px; line-height: 150%;")

            page_layout.addWidget(heading)
            page_layout.addSpacing(6)
            page_layout.addWidget(text, 1)
            self.pages.addWidget(page)
        layout.addWidget(self.pages, 1)

        self.dots = QLabel()
        self.dots.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dots.setStyleSheet("color: #7ee2a8; font-size: 16px;")
        layout.addWidget(self.dots)

        buttons = QHBoxLayout()
        self.skip_button = QPushButton(TEXTS["skip"])
        self.back_button = QPushButton(TEXTS["back"])
        self.next_button = QPushButton(TEXTS["next"])
        self.next_button.setObjectName("primary")
        self.skip_button.clicked.connect(self.reject)
        self.back_button.clicked.connect(self.go_back)
        self.next_button.clicked.connect(self.go_next)
        buttons.addWidget(self.skip_button)
        buttons.addStretch()
        buttons.addWidget(self.back_button)
        buttons.addWidget(self.next_button)
        layout.addLayout(buttons)

        self.update_controls()

    def go_next(self):
        index = self.pages.currentIndex()
        if index >= self.last:
            self.accept()
            return
        self.pages.setCurrentIndex(index + 1)
        self.update_controls()

    def go_back(self):
        index = self.pages.currentIndex()
        if index > 0:
            self.pages.setCurrentIndex(index - 1)
            self.update_controls()

    def update_controls(self):
        index = self.pages.currentIndex()
        self.dots.setText(
            "  ".join("●" if i == index else "○" for i in range(self.last + 1))
        )
        self.back_button.setVisible(index > 0)
        self.skip_button.setVisible(index < self.last)
        self.next_button.setText(
            TEXTS["done"] if index == self.last else TEXTS["next"]
        )
