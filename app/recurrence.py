"""Expands recurring transactions into individual dated occurrences.

A transaction stored once in the database can repeat daily, weekly,
monthly or yearly. Instead of saving a copy for every day/month, the
app stores a single row and calculates the occurrences when needed.
"""

import calendar
from datetime import date, timedelta
from decimal import Decimal, InvalidOperation

FREQUENCIES = ("once", "daily", "weekly", "monthly", "yearly")


def parse_date(value):
    """Convert 'YYYY-MM-DD' (or a date) to a date. Returns None if empty."""
    if not value:
        return None
    if isinstance(value, date):
        return value
    return date.fromisoformat(str(value)[:10])


def _add_months(start, months):
    """Add months while keeping the original day (clamped to month end).

    Anchoring on the original start date avoids drift: a salary that
    starts on Jan 31 lands on Feb 28, then Mar 31 (not Mar 28).
    """
    index = start.month - 1 + months
    year = start.year + index // 12
    month = index % 12 + 1
    day = min(start.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)


def occurrences(transaction, range_start, range_end):
    """Return every date this transaction happens within the range.

    The range is inclusive. A transaction never occurs before its own
    start date or after its optional end date.
    """
    start = parse_date(transaction.get("transaction_date"))
    if start is None:
        return []

    frequency = transaction.get("frequency") or "once"
    last = range_end
    end = parse_date(transaction.get("end_date"))
    if end is not None and end < last:
        last = end

    if frequency == "once":
        return [start] if range_start <= start <= last else []

    dates = []

    if frequency in ("daily", "weekly"):
        step = 1 if frequency == "daily" else 7
        current = start
        if current < range_start:
            # Jump straight to the first occurrence inside the range.
            skipped = (range_start - start).days // step
            current = start + timedelta(days=skipped * step)
            if current < range_start:
                current += timedelta(days=step)
        while current <= last:
            dates.append(current)
            current += timedelta(days=step)
        return dates

    step_months = 1 if frequency == "monthly" else 12
    n = 0
    while True:
        current = _add_months(start, n * step_months)
        if current > last:
            break
        if current >= range_start:
            dates.append(current)
        n += 1
    return dates


def expand(transactions, range_start, range_end):
    """Flatten transactions into a list of dated occurrences.

    Each item is a dict with: date, amount (Decimal), type, category,
    title and the source transaction id.
    """
    result = []
    for tx in transactions:
        try:
            amount = Decimal(str(tx["amount"]))
            tx_type = tx["type"]
            days = occurrences(tx, range_start, range_end)
        except (KeyError, TypeError, ValueError, InvalidOperation):
            continue  # skip rows with missing/invalid data instead of crashing
        for day in days:
            result.append({
                "date": day,
                "amount": amount,
                "type": tx_type,
                "category": tx.get("category") or "other",
                "title": tx.get("title", ""),
                "id": tx.get("id"),
            })
    result.sort(key=lambda item: item["date"])
    return result


def month_start(day):
    return day.replace(day=1)


def add_months_to_first(day, months):
    """First day of the month that is `months` away from `day`'s month."""
    return _add_months(day.replace(day=1), months)
