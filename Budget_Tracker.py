import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt

class BudgetManagementApp:
    def __init__(self):
        self.budget = {}
        self.categories = []

        self.app = tk.Tk()
        self.app.title("Budget Tracker")

        self.create_budget_label()
        self.create_income_frame()
        self.create_expense_frame()
        self.create_display_charts_frame()

    def create_budget_label(self):
        self.budget_label = ttk.Label(self.app, text="Budget: ₹0")
        self.budget_label.pack()

    def add_to_budget(self, category_entry, amount_entry, is_income):
        try:
            category = category_entry.get()
            amount = float(amount_entry.get())
            if category in self.budget:
                self.budget[category].append(amount if is_income else -amount)
            else:
                self.budget[category] = [amount if is_income else -amount]
                self.categories.append(category)
            self.budget_label['text'] = f"Budget: ₹{sum(sum(v) for v in self.budget.values()):.2f}"
        except ValueError:
            messagebox.showerror("Error", "Invalid Entry")
        amount_entry.delete(0, 'end')
        category_entry.delete(0, 'end')

    def create_income_frame(self):
        income_frame = ttk.LabelFrame(self.app, text="Add Income")
        income_frame.pack(pady=10)

        income_label = ttk.Label(income_frame, text="Income: ₹")
        income_label.grid(row=0, column=0, padx=5, pady=5)

        income_entry = ttk.Entry(income_frame)
        income_entry.grid(row=0, column=1, padx=5)

        income_category_label = ttk.Label(income_frame, text="Category:")
        income_category_label.grid(row=1, column=0, padx=5, pady=5)

        income_category_entry = ttk.Entry(income_frame)
        income_category_entry.grid(row=1, column=1, padx=5, pady=5)

        add_income_button = ttk.Button(
            income_frame,
            text="Add Income",
            command=lambda: self.add_to_budget(income_category_entry, income_entry, True)
        )
        add_income_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    def create_expense_frame(self):
        expense_frame = ttk.LabelFrame(self.app, text="Add Expense")
        expense_frame.pack(pady=10)

        expense_label = ttk.Label(expense_frame, text="Expense: ₹")
        expense_label.grid(row=0, column=0, padx=5, pady=5)

        expense_entry = ttk.Entry(expense_frame)
        expense_entry.grid(row=0, column=1, padx=5, pady=5)

        expense_category_label = ttk.Label(expense_frame, text="Category:")
        expense_category_label.grid(row=1, column=0, padx=5, pady=5)

        expense_category_entry = ttk.Entry(expense_frame)
        expense_category_entry.grid(row=1, column=1, padx=5, pady=5)

        add_expense_button = ttk.Button(
            expense_frame,
            text="Add Expense",
            command=lambda: self.add_to_budget(expense_category_entry, expense_entry, False)
        )
        add_expense_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    def display_pie_chart(self, values, labels, chart_title):
        plt.pie(values, labels=labels)
        plt.title(chart_title)
        plt.show()

    def display_bar_chart(self, categories, values, chart_title):
        plt.bar(categories, values)
        plt.title(chart_title)
        plt.show()

    def create_display_charts_frame(self):
        display_charts_frame = ttk.LabelFrame(self.app, text="Display Charts")
        display_charts_frame.pack(pady=10)

        chart_types = {
            "Income Pie Chart": lambda: self.display_pie_chart(
                [sum(v) for v in self.budget.values() if sum(v) > 0],
                [category for category, values in self.budget.items() if sum(values) > 0],
                "Income Pie Chart"
            ),
            "Expense Pie Chart": lambda: self.display_pie_chart(
                [abs(sum(v)) for v in self.budget.values() if sum(v) < 0],
                [category for category, values in self.budget.items() if sum(values) < 0],
                "Expense Pie Chart"
            ),
            "Income Bar Chart": lambda: self.display_bar_chart(
                [category for category, values in self.budget.items() if sum(values) > 0],
                [sum(self.budget[category]) for category in self.budget if sum(self.budget[category]) > 0],
                "Income Bar Chart"
            ),
            "Expense Bar Chart": lambda: self.display_bar_chart(
                [category for category, values in self.budget.items() if sum(values) < 0],
                [abs(sum(self.budget[category])) for category in self.budget if sum(self.budget[category]) < 0],
                "Expense Bar Chart"
            )
        }

        for i, (chart_type, chart_function) in enumerate(chart_types.items()):
            chart_button = ttk.Button(display_charts_frame, text=chart_type, command=chart_function)
            chart_button.grid(row=0, column=i, padx=5, pady=5)

    def run(self):
        self.app.mainloop()

# Create and run the budget tracker app
app = BudgetManagementApp()
app.run()
