from typing import List, Tuple, Dict
from datetime import datetime
import csv
from calendar import monthrange


def get_month_length(dt: datetime) -> int:
    """Gets the number of months using datetime"""
    year = dt.year
    month = dt.month
    return monthrange(year, month)[1]


def total_transactions(transactions: List[Tuple[datetime, float]]) \
        -> Dict[int, float]:
    month_length = get_month_length(transactions[0][0])
    totaled = {}
    for transaction in transactions:
        date, amount = transaction
        if date.day not in totaled:
            totaled[date.day] = amount
            continue
        totaled[date.day] += amount

    for day in range(month_length):
        if day not in totaled:
            totaled[day] = 0.0

    return totaled


def load_transactions(filename: str) -> List[Tuple[datetime, float]]:
    transactions = []
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)

        for line in reader:
            posted_date = datetime.fromisoformat(line["Posted"])
            amount = float(line["Amount"])
            transactions.append((posted_date, amount))

    return transactions
