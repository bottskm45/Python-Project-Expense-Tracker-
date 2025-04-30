import argparse
import sqlite3
import re
import csv
import os
from datetime import datetime

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Track your expenses for your Costa Rica trip!"
    )

    parser.add_argument('--add', nargs=3, metavar=('amount', 'category', 'date'),
                        help='Add a new expense. Example: --add 250.00 "Food" 2025-06-12')

    parser.add_argument('--summary', action='store_true',
                        help='Display total spending and category breakdown.')

    parser.add_argument('--filter-category', metavar='CATEGORY',
                        help='Show all expenses in a specific category.')

    parser.add_argument('--export', metavar='FILENAME',
                        help='Export all expenses to a CSV file.')
    
    parser.add_argument('--view-all', action='store_true',
                    help='View all recorded expenses.')


    return parser.parse_args()

def connect_db():
    conn = sqlite3.connect("trip_expenses.db")
    cursor = conn.cursor()

    # Create the expenses table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            note TEXT
        )
    ''')

    conn.commit()
    return conn, cursor

def add_expense(cursor, conn, amount, category, date):
    # Regex to validate amount: 12.34
    if not re.match(r'^\d+(\.\d{2})$', amount):
        print("Invalid amount format. Use format like 250.00")
        return

    # Regex to validate date: YYYY-MM-DD
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', date):
        print("Invalid date format. Use YYYY-MM-DD")
        return

    try:
        # Make sure the date is real (e.g., not 2025-02-31)
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        print("Invalid calendar date.")
        return

    cursor.execute('''
        INSERT INTO expenses (amount, category, date)
        VALUES (?, ?, ?)
    ''', (float(amount), category, date))

    conn.commit()
    print(f"Added: ${amount} to '{category}' on {date}")

def show_summary(cursor):
    print("\n Expense Summary")
    print("---------------------")

    # Get total spending
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0]
    if total is None:
        print("No expenses found.")
        return

    print(f"Total spent: ${total:.2f}\n")

    # Get spending by category
    cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    rows = cursor.fetchall()

    print("Spending by Category:")
    for category, amount in rows:
        print(f" - {category}: ${amount:.2f}")
    print()

def filter_by_category(cursor, category):
    print(f"\n Expenses in category: {category}")
    print("-----------------------------------")

    cursor.execute('''
        SELECT amount, category, date
        FROM expenses
        WHERE category = ?
        ORDER BY date
    ''', (category,))

    rows = cursor.fetchall()

    if not rows:
        print("No matching expenses found.")
        return

    for amount, category, date in rows:
        print(f" - {date}: ${amount:.2f}")

def export_to_csv(cursor, filename):
    cursor.execute("SELECT amount, category, date FROM expenses ORDER BY date")
    rows = cursor.fetchall()

    if not rows:
        print("No data to export.")
        return

    try:
        with open(filename, mode='w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Amount', 'Category', 'Date'])  # Header
            writer.writerows(rows)

        print(f"Expenses exported to {filename}")
    except Exception as e:
        print(f"Failed to write file: {e}")

def view_all_expenses(cursor):
    print("\n All Expenses")
    print("----------------------------")

    cursor.execute("SELECT amount, category, date FROM expenses ORDER BY date")
    rows = cursor.fetchall()

    if not rows:
        print("No expenses recorded.")
        return

    for amount, category, date in rows:
        print(f" - {date}: ${amount:.2f} for {category}")

if __name__ == "__main__":
    args = parse_arguments()
    conn, cursor = connect_db()

    if args.add:
        amount, category, date = args.add
        add_expense(cursor, conn, amount, category, date)

    if args.summary:
        show_summary(cursor)

    if args.filter_category:
        filter_by_category(cursor, args.filter_category)

    if args.export:
        export_to_csv(cursor, args.export)

    if args.view_all:
        view_all_expenses(cursor)