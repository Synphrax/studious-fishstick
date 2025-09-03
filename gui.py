import tkinter as tk

from backend import Transaction
from backend import ExpenseTracker

LARGE_FONT = ("Arial", 20)
MEDIUM_FONT = ("Arial", 16)
SMALL_FONT = ("Arial", 14)

class createMenu:
    SIZE = "500x400"
    TITLE = "Expense Tracker"

    def __init__(self, root, tracker):
        self.tracker = tracker

        self.root = root
        self.root.geometry(self.SIZE)
        self.root.title(self.TITLE)

        frame = tk.Frame(self.root)
        frame.pack(expand=True, anchor="center")

        # --- Description Label ---
        description = tk.Label(frame, text="Pick an option", font=LARGE_FONT)

        # --- Add Transaction Button ---
        add_transaction = tk.Button(frame, text="Add Transaction", font=SMALL_FONT, width=20, height=2, command=self.create_transaction_menu)

        # --- View Balance Button ---
        view_balance = tk.Button(frame, text="View Balance", font=SMALL_FONT, width=20, height=2, command=self.create_balance_menu)

        # --- View Summary Button ---
        view_summary = tk.Button(frame, text="View Summary", font=SMALL_FONT, width=20, height=2, command=self.create_summary_menu)

        # --- Exit Menu button ---
        exit_button = tk.Button(frame, text="Save & Exit", font=SMALL_FONT, width=20, height=2, command=self.save_and_exit)

        description.pack()
        add_transaction.pack(pady=10)
        view_balance.pack(pady=10)
        view_summary.pack(pady=10)
        exit_button.pack(pady=20)

        self.root.mainloop()

    def create_transaction_menu(self):
        root = tk.Tk()
        menu = createTransactionMenu(root, self.tracker)

    def create_balance_menu(self):
        root = tk.Tk()
        menu = createBalanceMenu(root, self.tracker)

    def create_summary_menu(self):
        multiplier = len(self.tracker.category_summary()) - 2
        size_y = 300 + (multiplier * 50)
        size = "500x" + str(size_y)
        
        root = tk.Tk()
        menu = createSummaryMenu(root, size, self.tracker)

    def save_and_exit(self):
        self.tracker.save_to_file()
        self.root.destroy()

class createTransactionMenu:
    SIZE = "400x300"
    TITLE = "Add Transaction"

    def __init__(self, root, tracker):
        self.tracker = tracker

        self.root = root
        self.root.geometry(self.SIZE)
        self.root.title(self.TITLE)

        # Frame for inputs
        form_frame = tk.Frame(self.root)
        form_frame.pack(pady=20)

        # --- Row 0: Centered Title Label ---
        tk.Label(form_frame, text="Add Transaction Details:", font=(SMALL_FONT)).grid(row=0, column=0, columnspan=2, pady=10)  # span across both columns

        # --- Row 1: Amount Input ---
        tk.Label(form_frame, text="Amount:", font=SMALL_FONT).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        amount_entry = tk.Entry(form_frame, width=25)
        amount_entry.grid(row=1, column=1, padx=10, pady=5)

        # --- Row 2: Category Input ---
        tk.Label(form_frame, text="Category:", font=SMALL_FONT).grid(row=2, column=0, padx=10, pady=5, sticky="e")
        category_entry = tk.Entry(form_frame, width=25)
        category_entry.grid(row=2, column=1, padx=10, pady=5)

        # --- Row 3: Description Input ---
        tk.Label(form_frame, text="Description:", font=SMALL_FONT).grid(row=3, column=0, padx=10, pady=5, sticky="e")
        description_entry = tk.Entry(form_frame, width=25)
        description_entry.grid(row=3, column=1, padx=10, pady=5)

        # --- Bottom Buttons Here ---
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(side="bottom", pady=20)

        add_button = tk.Button(bottom_frame, text="Add Transaction", width=15, height=2, command=lambda: self.save_responses(amount_entry, category_entry, description_entry))
        add_button.pack(side="left", padx=10)

        exit = tk.Button(bottom_frame, text="Exit", width=15, height=2, command=self.root.destroy)
        exit.pack(side="left", padx=10)

    def save_responses(self, amount, category, description):
        amount = int(amount.get())
        category = category.get()
        description = description.get()

        new_transaction = Transaction(amount, category, description)
        self.tracker.add_transaction(new_transaction)
        
        print(f"Transaction Saved: {amount}, {category}, {description}")
        self.root.destroy()

class createBalanceMenu:
    SIZE = "400x150"
    TITLE = "Balance"

    def __init__(self, root, tracker):
        self.tracker = tracker

        self.root = root
        self.root.geometry(self.SIZE)
        self.root.title(self.TITLE)

        frame = tk.Frame(self.root)
        frame.pack(expand=True, anchor="center")

        description = tk.Label(frame, text="Total Balance:", font=LARGE_FONT)

        balance = self.tracker.total_balance()
        formatted_balance = f"£{balance:.2f}"
        balanceText = tk.Label(frame, text=formatted_balance, font=MEDIUM_FONT)

        description.pack()
        balanceText.pack(pady=5)

        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(side="bottom", pady=10)

        exit = tk.Button(bottom_frame, text="Exit", width=15, height=2, command=self.root.destroy)
        exit.pack()

class createSummaryMenu:
    TITLE = "Category Summary"

    def __init__(self, root, size, tracker):
        self.tracker = tracker

        self.root = root
        self.root.geometry(size)
        self.root.title(self.TITLE)

        form_frame = tk.Frame(self.root)
        form_frame.pack(pady=20)

        tk.Label(form_frame, text="Category Summary:", font=(LARGE_FONT)).grid(row=0, column=0, columnspan=2, pady=5)

        summary = self.tracker.category_summary()
        for row, c in enumerate(summary):
            tk.Label(form_frame, text=f"{c}:", font=SMALL_FONT).grid(row=row+1, column=0, padx=5, pady=5, sticky="e")
            
            amount = summary[c]
            formatted_amount = f"£{amount:.2f}"
            tk.Label(form_frame, text=formatted_amount, font=SMALL_FONT).grid(row=row+1, column=1, padx=10, pady=5, sticky="e")

        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(pady=10)

        # --- Income Overview
        tk.Label(bottom_frame, text="Income:", font=(MEDIUM_FONT)).grid(row=0, column=0, padx=5, pady=5)
        
        income = self.tracker.total_income()
        formatted_income = f"£{income:.2f}"
        tk.Label(bottom_frame, text=formatted_income, font=(MEDIUM_FONT)).grid(row=0, column=1, padx=5, pady=5)

        # --- Expenses Overview ---
        tk.Label(bottom_frame, text="Expenses:", font=(MEDIUM_FONT)).grid(row=1, column=0, padx=5, pady=5)

        expenses = self.tracker.total_expenses()
        formatted_expenses = f"£{expenses:.2f}"
        tk.Label(bottom_frame, text=formatted_expenses, font=(MEDIUM_FONT)).grid(row=1, column=1, padx=5, pady=5)

        # --- Net Balance ---
        tk.Label(bottom_frame, text="Net Balance:", font=(MEDIUM_FONT)).grid(row=2, column=0, padx=5, pady=5)

        balance = self.tracker.total_balance()
        formatted_balance = f"£{balance:.2f}"
        tk.Label(bottom_frame, text=formatted_balance, font=(MEDIUM_FONT)).grid(row=2, column=1, padx=5, pady=5)

        exit = tk.Button(bottom_frame, text="Exit", width=15, height=2, command=self.root.destroy).grid(row=3, column=0, columnspan=2, pady=5)