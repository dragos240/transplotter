#!/usr/bin/env python3
import sys

from transplotter import parser
from transplotter import plotter


def main():
    transactions = parser.load_transactions(sys.argv[1])
    first_transaction_dt = transactions[0][0]
    year = first_transaction_dt.year
    month = first_transaction_dt.month
    totalled = parser.total_transactions(transactions)

    plotter.create_expenses_heatmap((year, month), totalled)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Specify exactly one csv file!")

    main()
