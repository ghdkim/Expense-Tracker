# Creating a class for expenses to access the name, category and amount for the selected category. This information is appended into a list
class Expenses:

    def __init__(self, name, category, amount) -> None:
        self.name = name
        self.category = category
        self.amount = amount

    def __repr__(self):
        return f"<Expenses: {self.name}, {self.category}, ${self.amount:.2f}>"