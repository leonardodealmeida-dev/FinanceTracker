from datetime import date

from app.recurrence import occurrences, expand


def tx(start, freq="once", end=None, amount=10, kind="expense"):
    return {"id": 1, "transaction_date": start, "frequency": freq,
            "end_date": end, "amount": amount, "type": kind,
            "category": "other", "title": "t"}


def test_once_inside_and_outside_range():
    t = tx("2026-03-10")
    assert occurrences(t, date(2026, 3, 1), date(2026, 3, 31)) == [date(2026, 3, 10)]
    assert occurrences(t, date(2026, 4, 1), date(2026, 4, 30)) == []


def test_missing_frequency_means_once():
    t = tx("2026-03-10")
    del t["frequency"]
    assert len(occurrences(t, date(2026, 1, 1), date(2026, 12, 31))) == 1


def test_daily_count_and_range_start_after_start():
    t = tx("2026-01-01", "daily")
    assert len(occurrences(t, date(2026, 1, 1), date(2026, 1, 31))) == 31
    got = occurrences(t, date(2026, 2, 1), date(2026, 2, 28))
    assert got[0] == date(2026, 2, 1) and len(got) == 28


def test_weekly_alignment():
    t = tx("2026-01-05", "weekly")  # a Monday
    got = occurrences(t, date(2026, 2, 1), date(2026, 2, 28))
    assert got == [date(2026, 2, 2), date(2026, 2, 9), date(2026, 2, 16), date(2026, 2, 23)]


def test_monthly_clamps_without_drift():
    t = tx("2026-01-31", "monthly")
    got = occurrences(t, date(2026, 1, 1), date(2026, 4, 30))
    assert got == [date(2026, 1, 31), date(2026, 2, 28), date(2026, 3, 31), date(2026, 4, 30)]


def test_yearly_leap_day():
    t = tx("2024-02-29", "yearly")
    got = occurrences(t, date(2024, 1, 1), date(2026, 12, 31))
    assert got == [date(2024, 2, 29), date(2025, 2, 28), date(2026, 2, 28)]


def test_end_date_stops_recurrence():
    t = tx("2026-01-15", "monthly", end="2026-03-20")
    got = occurrences(t, date(2026, 1, 1), date(2026, 12, 31))
    assert got == [date(2026, 1, 15), date(2026, 2, 15), date(2026, 3, 15)]


def test_nothing_before_start():
    t = tx("2026-06-01", "monthly")
    assert occurrences(t, date(2026, 1, 1), date(2026, 5, 31)) == []


def test_expand_sorted_and_skips_bad_rows():
    rows = [tx("2026-01-01", "monthly", amount=5), {"type": "expense"}]
    out = expand(rows, date(2026, 1, 1), date(2026, 3, 31))
    assert [o["date"].month for o in out] == [1, 2, 3]
