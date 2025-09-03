import tkinter as tk

from backend import Transaction
from backend import ExpenseTracker

from gui import createMenu

def main():
    tracker = ExpenseTracker()
    tracker.load_from_file()

    root = tk.Tk()
    menu = createMenu(root, tracker)

if __name__ == "__main__":
    main()