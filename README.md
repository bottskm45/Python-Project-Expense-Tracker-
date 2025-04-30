<<<<<<< HEAD
# Costa Rica Trip Expense Tracker

This is a simple Python script I made for a class project (IT3038C - Scripting Languages). It helps track how much money was spent during a two-week vacation to Costa Rica. Everything runs in the command line and uses a small local database to save the expenses.

---

## What This Script Does

This script lets you:
- Add new expenses with a category and date
- View a summary of your total spending
- Look at all expenses you've added
- Filter by a specific category (like "Food" or "Airfare")
- Export everything to a CSV file (you can open it in Excel or Google Sheets)

---

## Why It's Useful

Vacations are expensive and it's easy to lose track of where the money goes. This helps keep everything organized in one place without needing any fancy app or spreadsheet. Just a few quick commands and you're good.

---

## How to Use the Script

Make sure you're in the project folder and run the script using Python 3.

### Add an Expense
ex. python tracker.py --add 250.00 Food 2025-06-12

### View Summary of Spending
ex. python tracker.py --summary

### View All Expenses
ex python tracker.py -view-all

### Filter by Category
ex. python tracker.py --filter-category (Airfare, Food, Lodging, etc, whatever categories you want to keep track of)

### Export All Expenses to a CSV File
ex. python tracker.py --export trip_expenses.csv

### For Help
ex. python tracker.py --help

### How It Works
All of the expenses you enter get saved into a small local database file called trip_expenses.db. You don’t need to install anything or set up a server — it just works right from your computer.

When you add an expense, the script double-checks that the amount looks like a dollar value (like 100.00) and that the date is typed correctly. If it doesn’t match, it lets you know right away so you can fix it.

Everything runs in the command line, and the database keeps all your info saved even if you close the terminal.

### What I Used to Build It
I used Python 3 to write the script.I used

argparse: to handle the command-line input (like --add or --summary)

sqlite3: to create and use a simple database that keeps all the expenses saved

re: to check that your amount and date inputs are valid

csv: so you can export your expenses to a file and open it in Excel or Google Sheets


### Message to Professor

Thank you for the time and instruction you took to do this class. I learned a lot. Have a great summer!

-Kaleb Botts_

