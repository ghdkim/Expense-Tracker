from expenses import Expenses
import csv
import os
import datetime
import calendar

def main():
    print(f"🤑Welcome to this Expense Tracker!")
    budget_file_path = "budget.txt"
    month_file_path = "month.txt"

    current_month = datetime.datetime.now().month
    current_year = datetime.datetime.now().year
    expenses_file_path = f"expenses_{current_year}_{current_month}.csv"

    while True:
        budget = get_budget(budget_file_path, month_file_path, current_year, current_month)

        print(f"Monthly Budget: ${budget}")

        with open(budget_file_path, "w") as f:
            f.write(str(budget))
        with open(month_file_path, "w") as f:
            f.write(f"{current_year},{current_month}")

        expenses = get_user_expenses()
        save_expenses_to_file(expenses, expenses_file_path)
        summarize_expenses(expenses_file_path, budget)

        response = input("\nPlease type 'yes' to continue or 'no' to exit: ").lower()
        if response != 'yes':
            break

def get_budget (budget_file_path, month_file_path, current_year, current_month):
# producing a file path to save information on the user's monthly budget and also to help reset the expenses tracker on a new month
    if os.path.exists (budget_file_path) and os.path.exists(month_file_path):
        with open (month_file_path, "r") as f:
            saved_dates = f.read().strip().split(',')
            if len(saved_dates) != 2:
                print("Invalid data in 'month.txt'. Please input your budget again.")
                budget = float(input("What is your monthly budget? $"))
            else:
                saved_year, saved_month = map(int,saved_dates)

                expenses_file_path = f"expenses_{current_year}_{current_month}.csv"
                if current_month != saved_month or current_year !=saved_year:
                    print("A new month has started. Please input your budget again.")
                    budget = float(input("What is your monthly budget? $"))
                    with open(expenses_file_path,"w") as f:
                        f.write('Name, Category, Amount')
                else:
                    with open(budget_file_path, "r") as f:
                        budget = float(f.read().strip())
    else:
        budget = float(input("What is your monthly budget? $"))
    return budget

def get_user_expenses():
    print(f"💸Getting User Expenses")
    expenses = [] # Created a list to store the expenses objects on the file

    app_running = True
    while app_running:
        expense_name = input("Enter expense name: ")
        expense_amount = float(input("Enter expense amount: $"))
        expense_categories = [
            "🍽️Restaurants",
            "🛒Groceries",
            "🏡Housing",
            "🎁Shopping",
            "🏥Healthcare",
            "🍾Entertainment",
            "🚗Transport",
            "⭐️Miscellaneous"
        ]

        print("Select a category: ")
        for i, category_name in enumerate(expense_categories):
            print(f"    {i+1}. {category_name}")

        value_range = f"[1 - {len(expense_categories)}]"

        try:
            selected_index = int(input(f"Enter a category number from {value_range}: ")) - 1

        except ValueError:
            print("Invalid input. Please enter a number!")
            continue

        if selected_index in range (len(expense_categories)):
            selected_category = expense_categories[selected_index]
            new_expense = Expenses(name=expense_name, category=selected_category, amount=float(expense_amount))
            expenses.append(new_expense)
        else:
            print("Invalid input. Please enter a number within the category range!")
            continue

        app_running = False

    return expenses
def save_expenses_to_file(expenses, expenses_file_path):
# saving the expenses data to an expenses file
    print(f"🗂️Saving User Expenses: {expenses} to {expenses_file_path}")

    try:
        with open(expenses_file_path, "a+") as f:
            f.seek(0)
            data = f.read(100)

            if len(data) == 0:
                f.write ("Name, Category, Amount\n")

            for expense in expenses:
                f.write (f"{expense.name},{expense.category},{expense.amount}\n")
    except IOError as e:
        print("An error occurred writing to the file: ", e)
def summarize_expenses(expenses_file_path, budget):
# presenting the summary of the expenses by name, category and amount
    print(f"💰Summarizing User Expenses")

    expenses = []

    try:
        with open(expenses_file_path, "r") as f:
            lines = csv.reader(f)
            next(lines,None)
            for row in lines:
                print(f"{row[0]:<25}\t{row[1]:<28}\t{row[2]:<25}")
                expenses.append(Expenses(name=row[0], category=row[1], amount=float(row[2])))
    except IOError as e:
        print("An error occurred reading the file: ", e)

# checking the sum of the expenses by category
    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount


# threshold to trigger advice. I set the threshold to 25% of total budget

    thresholds = {
        "🍽️Restaurants": 0.12 * budget,
        "🏡Housing": 0.40 * budget,
        "🎁Shopping": 0.12 * budget,
        "🍾Entertainment": 0.12 * budget,
        "🚗Transport": 0.18 * budget,
        "⭐️Miscellaneous": 0.06 * budget,
    }

    advice_dict = {
        "🍽️Restaurants": "You are spending too much eating out. Consider buying groceries to reduce your cost.",
        "🏡Housing": "Your housing expenses are high. Consider saving on utilities or maintenance costs.",
        "🎁Shopping": "You are spending too much on shopping. Consider saving your money for other expenses." ,
        "🍾Entertainment": "You are spending too much on entertainment related costs. Consider saving your money for other expenses.",
        "🚗Transport": "You are spending too much on Transportation. Consider using less expensive modes of transport like public transport, walking or cycling.",
        "⭐️Miscellaneous": "You are spending too much on these expenses. Consider saving your money for other expenses.",
    }

    print("\nExpenses By Category: ")
    for key, amount in amount_by_category.items():
        print(f"    {key}: ${amount: .2f}")
        if key in advice_dict and amount > thresholds.get(key,0):
            print (f"   Advice: {advice_dict[key]} Don't exceed over ${thresholds[key]} for {key}.\n")

# checking total spent expenses
    total_spent = sum([ex.amount for ex in expenses])
    if total_spent >= budget:
        print(red(f"\nTotal Spent This Month: ${total_spent:.2f}"))
    else:
        print (green(f"\nTotal Spent This Month: ${total_spent:.2f}"))

# checking the remaining budget for the month and budget per day
    remaining_budget = budget - total_spent
    if remaining_budget >= 0:
        print(green(f"\nRemaining Budget This Month: ${remaining_budget:.2f}"))
    else:
        print(red(f"\nRemaining Budget This Month: ${remaining_budget:.2f}"))

    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day

    daily_budget = remaining_budget / remaining_days
    if daily_budget >= 0:
        print(green(f"\nBudget Per Day: ${daily_budget:.2f}"))
    else:
        print(red(f"\nBudget Per Day: ${daily_budget:.2f}"))

# changing colour of the text depending on whether the remaining budget is negative or positive or whether the expenses has passed the monthly budget
def green(text):
    return f"\033[92m{text}\033[0m"
def red(text):
    return f"\033[91m{text}\033[0m"

if __name__ == "__main__":
    main()