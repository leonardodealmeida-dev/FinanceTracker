from datetime import date
from decimal import Decimal as D

from app.analytics import monthly_summary, category_totals, balance_series, totals


def item(day, amount, kind, cat="other"):
    return {"date": day, "amount": D(amount), "type": kind, "category": cat}


def test_monthly_summary_window_and_year_wrap():
    items = [item(date(2025, 12, 5), "100", "income"),
             item(date(2026, 2, 1), "40", "expense"),
             item(date(2024, 1, 1), "999", "income")]  # outside window
    out = monthly_summary(items, date(2026, 2, 10), months=3)
    assert [m[0] for m in out] == [date(2025, 12, 1), date(2026, 1, 1), date(2026, 2, 1)]
    assert out[0][1] == D("100") and out[2][2] == D("40")
    assert sum(m[1] for m in out) == D("100")


def test_category_totals_sorted_and_filtered():
    items = [item(date(2026, 1, 1), "5", "expense", "food"),
             item(date(2026, 1, 2), "20", "expense", "housing"),
             item(date(2026, 1, 3), "7", "expense", "food"),
             item(date(2026, 1, 4), "900", "income", "salary")]
    assert category_totals(items) == [("housing", D("20")), ("food", D("12"))]


def test_balance_series_opening_and_endpoints():
    items = [item(date(2026, 1, 5), "100", "income"), item(date(2026, 1, 5), "30", "expense"),
             item(date(2026, 1, 9), "10", "expense")]
    pts = balance_series(items, D("50"), date(2026, 1, 1), date(2026, 1, 31))
    assert pts == [(date(2026, 1, 1), D("50")), (date(2026, 1, 5), D("120")),
                   (date(2026, 1, 9), D("110")), (date(2026, 1, 31), D("110"))]


def test_totals():
    items = [item(date(2026, 1, 1), "10.10", "income"), item(date(2026, 1, 1), "0.20", "income"),
             item(date(2026, 1, 2), "3", "expense")]
    assert totals(items) == (D("10.30"), D("3"))
