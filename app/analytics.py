"""Aggregations that feed the charts. Pure Python, no Qt."""

from datetime import date
from decimal import Decimal

from app.recurrence import add_months_to_first


def signed(item):
    """Income is positive, expenses are negative."""
    return item["amount"] if item["type"] == "income" else -item["amount"]


def totals(items):
    income = sum((i["amount"] for i in items if i["type"] == "income"), Decimal("0"))
    expenses = sum((i["amount"] for i in items if i["type"] == "expense"), Decimal("0"))
    return income, expenses


def monthly_summary(items, today, months=6):
    """Income/expenses for each of the last `months` months (oldest first).

    Returns a list of (first_day_of_month, income, expenses).
    """
    first = add_months_to_first(today, -(months - 1))
    buckets = {}
    for i in range(months):
        buckets[add_months_to_first(first, i)] = [Decimal("0"), Decimal("0")]

    for item in items:
        key = item["date"].replace(day=1)
        if key not in buckets:
            continue
        slot = 0 if item["type"] == "income" else 1
        buckets[key][slot] += item["amount"]

    return [(k, v[0], v[1]) for k, v in sorted(buckets.items())]


def category_totals(items, kind="expense"):
    """Total per category for one type, largest first."""
    result = {}
    for item in items:
        if item["type"] != kind:
            continue
        result[item["category"]] = result.get(item["category"], Decimal("0")) + item["amount"]
    return sorted(result.items(), key=lambda pair: pair[1], reverse=True)


def balance_series(items, opening, start, end):
    """Running balance as (date, balance) points from start to end.

    `items` must lie inside [start, end]; `opening` is the balance
    just before `start`.
    """
    per_day = {}
    for item in items:
        per_day[item["date"]] = per_day.get(item["date"], Decimal("0")) + signed(item)

    points = [(start, opening)]
    running = opening
    for day in sorted(per_day):
        running += per_day[day]
        points.append((day, running))
    if points[-1][0] != end:
        points.append((end, running))
    return points
