import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from data_entry import get_date, get_amount, get_category, get_description

class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]
    FORMAT = "%m-%d-%Y"

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        try:
            df = pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)

        new_entry = pd.DataFrame([{
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        }])
        
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_csv(cls.CSV_FILE, index=False)
        print("\nEntry added successfully")

    @classmethod
    def get_transactions(cls, start_date, end_date, category_filter): 
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT)
        start_date = datetime.strptime(start_date, CSV.FORMAT)
        end_date = datetime.strptime(end_date, CSV.FORMAT)

        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask]

        filtered_df = filtered_df.sort_values("date")

        if category_filter == "Income":
            filtered_df = filtered_df[filtered_df["category"] == "Income"]
        elif category_filter == "Expense":
            filtered_df = filtered_df[filtered_df["category"] == "Expense"]
        
        if filtered_df.empty:
            print("No transactions found in the given date range.")
        else:
            print(f"\nTransactions from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}")

            if category_filter != "All":
                print(f"Filter: {category_filter} only")
            print("-" * 85)

            display_df = filtered_df.copy()
            display_df["date"] = display_df["date"].dt.strftime(CSV.FORMAT)
            display_df["amount"] = display_df["amount"].map("${:,.2f}".format)

            print(display_df.to_string(index=False))
            print("-" * 85)

            total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
            total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()
            print("Summary:\n")
            print(f"Total Income: ${total_income:,.2f}")
            print(f"Total Expense: ${total_expense:,.2f}")
            print(f"Net Savings: ${(total_income - total_expense):,.2f}")
            print("-" * 85)

        return filtered_df
        
def add():
    CSV.initialize_csv()
    date = get_date("Enter the date of the transaction (MM-DD-YYYY) or enter for today's date: ", allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)

def plot_transactions(df):
    df = df.copy()
    df.set_index("date", inplace=True)

    income_df = df.loc[df["category"] == "Income", "amount"].resample("D").sum()
    expense_df = df.loc[df["category"] == "Expense", "amount"].resample("D").sum()

    plt.figure(figsize=(10, 5))

    if not income_df.empty:
        plt.plot(income_df.index, income_df, label="Income", color="g")
    if not expense_df.empty:
        plt.plot(expense_df.index, expense_df, label="Expense", color="r")

    plt.title("Daily Income and Expense")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def main():
    while True:
        print("\n1. Add a new transaction")
        print("2. View transactions and summary within a date range")
        print("3. Exit")
        choice = input("\nEnter your choice: ")
        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("\nEnter the start date (MM-DD-YYYY): ")
            end_date = get_date("Enter the end date (MM-DD-YYYY): ")

            print("\nFilter options:")
            print("---------------")
            print("A - All transactions")
            print("I - Income only")
            print("E - Expense only")
            filter_choice = input("\nChoose filter (A/I/E): ").strip().upper()
            
            category_filter = "All"
            if filter_choice == "I":
                category_filter = "Income"
            elif filter_choice == "E":
                category_filter = "Expense"

            df = CSV.get_transactions(start_date, end_date, category_filter)

            if not df.empty and input("\nDo you want to plot the transactions? (y/n): ").lower() == "y":
                plot_transactions(df)

        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Enter 1, 2 or 3.")


if __name__ == "__main__":
    main()