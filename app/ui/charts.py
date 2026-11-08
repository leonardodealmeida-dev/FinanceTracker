"""Chart widgets for the dashboard (built on Qt Charts, ships with PySide6)."""

from PySide6.QtCharts import (
    QBarCategoryAxis, QBarSeries, QBarSet, QChart, QChartView,
    QDateTimeAxis, QLineSeries, QPieSeries, QValueAxis,
)
from PySide6.QtCore import QDate, QDateTime, QMargins, QTime, Qt
from PySide6.QtGui import QColor, QFont, QPainter, QPen

BG = QColor("#19221c")
TEXT = QColor("#c7d7cb")
GRID = QColor("#2b3b30")
GREEN = QColor("#65cf91")
RED = QColor("#e8836f")


def set_chart_theme(theme):
    """Update chart colors when the application theme changes."""
    global BG, TEXT, GRID, GREEN, RED
    if theme == "light":
        BG = QColor("#ffffff")
        TEXT = QColor("#294535")
        GRID = QColor("#d5e4d9")
        GREEN = QColor("#209b65")
        RED = QColor("#d96b5d")
    else:
        BG = QColor("#19221c")
        TEXT = QColor("#c7d7cb")
        GRID = QColor("#2b3b30")
        GREEN = QColor("#65cf91")
        RED = QColor("#e8836f")

PALETTE = [
    "#65cf91", "#e8836f", "#6fb7e8", "#e8c46f", "#b28ee8",
    "#e88fc0", "#6fe8d9", "#a3e86f", "#e8a06f", "#8f9ee8",
    "#9aa8a0",
]


def _money(value):
    return f"-${abs(value):,.2f}" if value < 0 else f"${value:,.2f}"


def _new_chart(title):
    chart = QChart()
    chart.setTitle(title)
    chart.setTitleBrush(TEXT)
    font = QFont()
    font.setPointSize(11)
    font.setBold(True)
    chart.setTitleFont(font)
    chart.setBackgroundBrush(BG)
    chart.setBackgroundPen(QPen(GRID))
    chart.setBackgroundRoundness(12)
    chart.setMargins(QMargins(8, 8, 8, 8))
    chart.setAnimationOptions(QChart.AnimationOption.NoAnimation)
    chart.legend().setLabelColor(TEXT)
    chart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)
    return chart


def _style_axis(axis):
    axis.setLabelsColor(TEXT)
    axis.setGridLineColor(GRID)
    axis.setLinePenColor(GRID)


def _refresh_chart_style(chart):
    chart.setTitleBrush(TEXT)
    chart.setBackgroundBrush(BG)
    chart.setBackgroundPen(QPen(GRID))
    chart.legend().setLabelColor(TEXT)


def _clear(chart):
    chart.removeAllSeries()
    for axis in chart.axes():
        chart.removeAxis(axis)


class MonthlyBarChart(QChartView):
    """Income vs expenses for the last few months."""

    def __init__(self):
        super().__init__(_new_chart(""))
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setStyleSheet("background: transparent; border: none;")
        self.setMinimumHeight(240)

    def set_data(self, rows, month_labels, title, income_label, expense_label):
        """rows: [(first_day, income, expenses)], month_labels: [str]."""
        chart = self.chart()
        _clear(chart)
        _refresh_chart_style(chart)
        chart.setTitle(title)

        income_set = QBarSet(income_label)
        expense_set = QBarSet(expense_label)
        income_set.setColor(GREEN)
        expense_set.setColor(RED)
        income_set.setBorderColor(GREEN)
        expense_set.setBorderColor(RED)

        top = 0.0
        for _, income, expenses in rows:
            income_set.append(float(income))
            expense_set.append(float(expenses))
            top = max(top, float(income), float(expenses))

        series = QBarSeries()
        series.append(income_set)
        series.append(expense_set)
        series.setBarWidth(0.7)
        series.hovered.connect(self._on_hover)
        chart.addSeries(series)

        axis_x = QBarCategoryAxis()
        axis_x.append(month_labels)
        _style_axis(axis_x)
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axis_x)

        axis_y = QValueAxis()
        axis_y.setRange(0, top * 1.15 if top > 0 else 100)
        axis_y.setLabelFormat("$%.0f")
        axis_y.setTickCount(5)
        _style_axis(axis_y)
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_y)

    def _on_hover(self, status, index, bar_set):
        if status:
            self.setToolTip(f"{bar_set.label()}: {_money(bar_set.at(index))}")
        else:
            self.setToolTip("")


class CategoryDonutChart(QChartView):
    """Where the money goes: expenses by category."""

    def __init__(self):
        super().__init__(_new_chart(""))
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setStyleSheet("background: transparent; border: none;")
        self.setMinimumHeight(240)

    def set_data(self, rows, title, empty_text):
        """rows: [(label, amount)] largest first."""
        chart = self.chart()
        _clear(chart)
        # Unlike the other chart widgets, the donut previously kept the
        # palette from the theme active when it was first created.
        _refresh_chart_style(chart)

        if not rows:
            chart.setTitle(f"{title} — {empty_text}")
            chart.legend().setVisible(False)
            return

        chart.setTitle(title)
        chart.legend().setVisible(True)

        total = sum(float(amount) for _, amount in rows)
        series = QPieSeries()
        series.setHoleSize(0.5)
        series.setPieSize(0.8)

        # Keep the donut readable: top 7 slices, the rest grouped.
        shown, rest = rows[:7], rows[7:]
        if rest:
            shown = shown + [("…", sum(a for _, a in rest))]

        for index, (label, amount) in enumerate(shown):
            value = float(amount)
            pct = value / total * 100 if total else 0
            slice_ = series.append(f"{label} — {_money(value)} ({pct:.0f}%)", value)
            slice_.setBrush(QColor(PALETTE[index % len(PALETTE)]))
            slice_.setPen(QPen(BG, 2))
            slice_.setLabelVisible(False)
            tooltip_text = f"{label}: {_money(value)} ({pct:.0f}%)"
            slice_.hovered.connect(
                lambda hovered, text=tooltip_text: self.setToolTip(text if hovered else "")
            )

        chart.addSeries(series)
        chart.legend().setAlignment(Qt.AlignmentFlag.AlignRight)


class BalanceLineChart(QChartView):
    """Running balance over the selected period."""

    def __init__(self):
        super().__init__(_new_chart(""))
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setStyleSheet("background: transparent; border: none;")
        self.setMinimumHeight(240)

    @staticmethod
    def _ms(day):
        return QDateTime(QDate(day.year, day.month, day.day), QTime(0, 0)).toMSecsSinceEpoch()

    def set_data(self, points, title, name):
        """points: [(date, balance)] in chronological order."""
        chart = self.chart()
        _clear(chart)
        _refresh_chart_style(chart)
        chart.setTitle(title)
        chart.legend().setVisible(False)

        series = QLineSeries()
        series.setName(name)
        pen = QPen(GREEN)
        pen.setWidth(3)
        series.setPen(pen)

        # Step-style line: the balance holds until the next event.
        previous = None
        low = high = float(points[0][1]) if points else 0.0
        for day, balance in points:
            value = float(balance)
            if previous is not None:
                series.append(self._ms(day), previous)
            series.append(self._ms(day), value)
            previous = value
            low, high = min(low, value), max(high, value)

        chart.addSeries(series)

        axis_x = QDateTimeAxis()
        axis_x.setFormat("dd MMM yy")
        axis_x.setTickCount(6)
        if points:
            first, last = points[0][0], points[-1][0]
            if first == last:
                last = last.fromordinal(last.toordinal() + 1)
            axis_x.setRange(
                QDateTime.fromMSecsSinceEpoch(self._ms(first)),
                QDateTime.fromMSecsSinceEpoch(self._ms(last)),
            )
        _style_axis(axis_x)
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axis_x)

        pad = max((high - low) * 0.1, 10)
        axis_y = QValueAxis()
        axis_y.setRange(low - pad, high + pad)
        axis_y.setLabelFormat("$%.0f")
        axis_y.setTickCount(5)
        _style_axis(axis_y)
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_y)
