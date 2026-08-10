# Personal Finance Tracker

Application to track income and expenses, view financial summaries, and visualize spending patterns.

## Features

- Add income or expense transactions with date, amount, category, and description
- Input validation for date, amount, and category
- View transactions within a custom date range
- Filter by All / Income only / Expense only
- Automatic summary: Total Income, Total Expense, and Net Savings
- Optional line chart of daily income vs expenses
- Data stored in a CSV file

## Requirements

- Python 3
- pandas
- matplotlib

Install the required packages:

```bash
pip install pandas matplotlib
```

## How to Run
```bash
python main.py
```
## Usage Example
```bash
1. Add a new transaction
2. View transactions and summary within a date range
3. Exit

Enter your choice: 2

Enter the start date (MM-DD-YYYY): 07-01-2026
Enter the end date (MM-DD-YYYY): 07-02-2026

Filter options:
---------------
A - All transactions
I - Income only
E - Expense only

Choose filter (A/I/E): A

Transactions from 07-01-2026 to 07-02-2026
-------------------------------------------------------------------------------------
      date    amount category description
07-01-2026 $1,000.00   Income      Salary
07-02-2026    $50.00  Expense   Groceries
-------------------------------------------------------------------------------------
Summary:

Total Income: $1,000.00
Total Expense: $50.00
Net Savings: $950.00
-------------------------------------------------------------------------------------

Do you want to plot the transactions? (y/n): n
