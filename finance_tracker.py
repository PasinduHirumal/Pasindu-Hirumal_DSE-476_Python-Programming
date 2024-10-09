import os
import time
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class FinanceEntry:
    def __init__(self, entry_type, amount, category, date=None):
        # Initialize a FinanceEntry object with entry type, amount, category, and date.      
        self.entry_type = entry_type
        self.amount = amount
        self.category = category
        self.date = date or time.strftime('%Y-%m-%d', time.localtime())

class FinanceTracker:
    def __init__(self):
        # Initialize a FinanceTracker object with an empty list of entries and load existing data.
        self.entries = []  # List to store financial entries
        self.load_data()   # Load existing data from the file

    def load_data(self):
        # Load financial data from a file ('financial_data.txt') if it exists.
        if os.path.exists('financial_data.txt'):
            with open('financial_data.txt', 'r') as file:
                # Read lines from the file and create FinanceEntry objects
                for line in file.readlines():
                    entry_data = line.strip().split(',')
                    entry_type, amount, category, date = entry_data
                    self.entries.append(FinanceEntry(entry_type, float(amount), category, date))

    def save_data(self):
        # Save financial data to a file ('financial_data.txt').
        with open('financial_data.txt', 'w') as file:
            # Write each entry as a line in the file
            for entry in self.entries:
                file.write(f"{entry.entry_type},{entry.amount},{entry.category},{entry.date}\n")

    def record_entry(self, entry_type, amount, category, date=None):
        # Record a new financial entry, validate input, and save the data.
        if not date:
            messagebox.showerror("Error", "Date is mandatory. Please enter a valid date.")
            return
        try:
            formatted_date = time.strftime('%Y-%m-%d', time.strptime(date, '%Y-%m-%d'))
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
            return
        if formatted_date != date:
            messagebox.showerror("Error", "Invalid date order. Please enter the date in the format YYYY-MM-DD.")
            return
        new_entry = FinanceEntry(entry_type, float(amount), category, formatted_date)
        self.entries.append(new_entry)
        self.save_data()

    def calculate_totals(self):
        # Calculate total income, total expenses, and net income from the recorded entries.
        total_income = sum(entry.amount for entry in self.entries if entry.entry_type == 'income')
        total_expenses = sum(entry.amount for entry in self.entries if entry.entry_type == 'expense')
        net_income = total_income - total_expenses
        return total_income, total_expenses, net_income

class FinanceTrackerGUI:
    def __init__(self, root):
        # Initialize the GUI for the Finance Tracker application.
        self.root = root
        self.root.title("Finance Tracker")
        self.root.geometry("460x170")
        self.root.configure(bg='#f0f0f0')

        self.finance_tracker = FinanceTracker()

        self.create_widgets()

    def create_widgets(self):
        # Create the main widgets for the GUI.
        style = ttk.Style()
        style.configure('TButton', foreground='#1F2833', background='#4CAF50', padding=5)

        ttk.Label(self.root, text="Finance Tracker", font=('Helvetica', 16), background='#f0f0f0').grid(row=0, column=1, pady=10)

        ttk.Button(self.root, text="Record a new entry", command=self.record_entry, style='TButton').grid(row=1, column=0, padx=10, pady=10)
        ttk.Button(self.root, text="View all entries", command=self.view_all_entries, style='TButton').grid(row=1, column=1, padx=10, pady=10)
        ttk.Button(self.root, text="View financial summary", command=self.view_summary, style='TButton').grid(row=1, column=2, padx=10, pady=10)
        ttk.Button(self.root, text="Exit", command=self.root.destroy, style='TButton').grid(row=2, column=1, pady=10)

    def record_entry(self):
        # Open a new window to record a financial entry.
        entry_window = tk.Toplevel(self.root)
        entry_window.title("Record Entry")
        entry_window.geometry("340x190")
        entry_window.configure(bg='#f0f0f0')

        ttk.Label(entry_window, text="Enter a new record", font=('Helvetica', 14), background='#f0f0f0').grid(row=0, column=0, columnspan=2, pady=10, padx=15)

        entry_type_var = tk.StringVar()
        ttk.Label(entry_window, text="Entry type:", background='#f0f0f0').grid(row=1, column=0)

        # Radio buttons for entry type
        income_radio = ttk.Radiobutton(entry_window, text="Income", variable=entry_type_var, value="income")
        expense_radio = ttk.Radiobutton(entry_window, text="Expense", variable=entry_type_var, value="expense")

        income_radio.grid(row=1, column=1)
        expense_radio.grid(row=1, column=2)

        amount_var = tk.StringVar()
        ttk.Label(entry_window, text="Amount (LKR):", background='#f0f0f0').grid(row=2, column=0)
        amount_entry = ttk.Entry(entry_window, textvariable=amount_var)
        amount_entry.grid(row=2, column=1)

        category_var = tk.StringVar()
        ttk.Label(entry_window, text="Category:", background='#f0f0f0').grid(row=3, column=0)
        category_entry = ttk.Entry(entry_window, textvariable=category_var)
        category_entry.grid(row=3, column=1)

        date_var = tk.StringVar()
        ttk.Label(entry_window, text="Date (YYYY-MM-DD):", background='#f0f0f0').grid(row=4, column=0)
        date_entry = ttk.Entry(entry_window, textvariable=date_var)
        date_entry.grid(row=4, column=1)

        ttk.Button(entry_window, text="Record Entry", command=lambda:
                   self.record_and_close(entry_type_var.get(), amount_var.get(), category_var.get(), date_var.get(), entry_window)).grid(row=5, column=0, columnspan=3, pady=10)

    def record_and_close(self, entry_type, amount, category, date, window):
        # Validate and record a financial entry, then close the entry window.
        if entry_type not in ("income", "expense"):
            messagebox.showerror("Error", "Invalid entry type. Please select either 'Income' or 'Expense'.")
            return
        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Invalid amount. Please enter a valid number.")
            return
        if amount <= 0:
            messagebox.showerror("Error", "Invalid amount. Please enter a positive number.")
            return
        try:
            formatted_date = time.strftime('%Y-%m-%d', time.strptime(date, '%Y-%m-%d'))
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
            return
        if formatted_date != date:
            messagebox.showerror("Error", "Invalid date order. Please enter the date in the format YYYY-MM-DD.")
            return
        
        self.finance_tracker.record_entry(entry_type, amount, category, formatted_date)
        window.destroy()
        messagebox.showinfo("Success", "Data has been successfully added!")

    def view_all_entries(self):
        # Open a new window to view all recorded financial entries. 
        entries_window = tk.Toplevel(self.root)
        entries_window.title("All Entries")
        entries_window.geometry("700x310")
        entries_window.configure(bg='#f0f0f0')

        ttk.Label(entries_window, text="All Entries", font=('Helvetica', 14), background='#f0f0f0').grid(row=0, column=0, columnspan=3, pady=10, padx=20)

        # Create Treeview widget for displaying entries in a table
        columns = ["Entry Type", "Amount (LKR)", "Category", "Date"]
        treeview = ttk.Treeview(entries_window, columns=columns, show="headings")

        # Configure column headings
        for col in columns:
            treeview.heading(col, text=col)

        # Insert data into the table
        for entry in self.finance_tracker.entries:
            treeview.insert("", "end", values=(entry.entry_type, entry.amount, entry.category, entry.date))

        treeview.grid(row=1, column=0, columnspan=3, padx=40, pady=10)

        # Add vertical scrollbar to the Treeview
        vsb = ttk.Scrollbar(entries_window, orient="vertical", command=treeview.yview)
        vsb.grid(row=1, column=3, sticky='ns')
        treeview.configure(yscrollcommand=vsb.set)

        # Add horizontal scrollbar to the Treeview
        hsb = ttk.Scrollbar(entries_window, orient="horizontal", command=treeview.xview)
        hsb.grid(row=2, column=0, columnspan=3, sticky='ew')
        treeview.configure(xscrollcommand=hsb.set)

        # Disable editing of the entries in the table
        for col in columns:
            treeview.heading(col, text=col, command=lambda c=col: self.sort_treeview(treeview, c, False))
            treeview.column(col, width=150, minwidth=50, anchor=tk.CENTER)

    def sort_treeview(self, tree, col, reverse):
        # Sort the Treeview widget based on the selected column.
        data = [(tree.set(child, col), child) for child in tree.get_children('')]
        try:
            data.sort(key=lambda t: float(t[0]), reverse=reverse)
        except ValueError:
            data.sort(reverse=reverse)
        for i, item in enumerate(data):
            tree.move(item[1], '', i)

    def view_summary(self):
        # Open a new window to view the financial summary.
        summary_window = tk.Toplevel(self.root)
        summary_window.title("Financial Summary")
        summary_window.geometry("1250x560")
        summary_window.configure(bg='#f0f0f0')

        ttk.Label(summary_window, text="View Financial Summary", font=('Helvetica', 14), background='#f0f0f0').grid(row=0, column=0, columnspan=2, pady=10)

        year_var = tk.IntVar()
        month_var = tk.IntVar()

        ttk.Label(summary_window, text="Enter year:", background='#f0f0f0').grid(row=1, column=0)
        year_entry = ttk.Entry(summary_window, textvariable=year_var)
        year_entry.grid(row=1, column=1)

        ttk.Label(summary_window, text="Enter month (1-12):", background='#f0f0f0').grid(row=2, column=0)
        month_entry = ttk.Entry(summary_window, textvariable=month_var)
        month_entry.grid(row=2, column=1)

        ttk.Button(summary_window, text="View Summary", command=lambda:
                   self.display_summary(year_var.get(), month_var.get(), summary_window)).grid(row=3, column=0, columnspan=2, pady=10)

    def display_summary(self, year, month, window):
        # Display the financial summary for the specified year and month.
        if not (1 <= month <= 12):
            messagebox.showerror("Error", "Invalid month. Please enter a value between 1 and 12.")
            return

        month_entries = [entry for entry in self.finance_tracker.entries if
                        time.strptime(entry.date, '%Y-%m-%d').tm_mon == month
                        and time.strptime(entry.date, '%Y-%m-%d').tm_year == year]

        total_income = sum(entry.amount for entry in month_entries if entry.entry_type == 'income')
        total_expenses = sum(entry.amount for entry in month_entries if entry.entry_type == 'expense')
        net_income = total_income - total_expenses

        # Update the summary_text to include the selected month and year
        summary_text = f"Summary for {time.strftime('%B %Y', time.strptime(f'{year}-{month}', '%Y-%m'))}:\n"
        summary_text += f"Total Income: LKR {total_income}\n"
        summary_text += f"Total Expenses: LKR {total_expenses}\n"
        summary_text += f"Net Income: LKR {net_income}\n"

        # Create a Treeview widget for displaying entries in a table
        columns = ["Entry Type", "Amount (LKR)", "Category", "Date"]
        treeview = ttk.Treeview(window, columns=columns, show="headings")

        # Configure column headings
        for col in columns:
            treeview.heading(col, text=col)
            treeview.column(col, width=150, minwidth=50, anchor=tk.CENTER)

        # Insert data into the table
        for entry in month_entries:
            treeview.insert("", "end", values=(entry.entry_type, entry.amount, entry.category, entry.date))

        treeview.grid(row=4, column=0, columnspan=2, padx=10, pady=10) # Decreased the number of columns

        # Add horizontal scrollbar to the Treeview
        hsb = ttk.Scrollbar(window, orient="horizontal", command=treeview.xview)
        hsb.grid(row=5, column=0, columnspan=2, sticky='ew')
        treeview.configure(xscrollcommand=hsb.set)

        text_widget = tk.Text(window, height=5, width=60, bg='#ffffff')
        text_widget.grid(row=6, column=0, columnspan=2, padx=10, pady=10)
        text_widget.insert(tk.END, summary_text)
        text_widget.configure(state='disabled')

        # Create the circle chart
        fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

        # Data for the chart
        labels = 'Total Income', 'Total Expenses'
        sizes = [total_income, total_expenses]
        colors = ['#4CAF50', '#FF5733']

        # Plot the chart
        wedges, texts, autotexts = ax.pie(sizes, autopct='%1.1f%%', startangle=90, colors=colors)

        ax.legend(wedges, labels, title="Categories", loc="upper left", bbox_to_anchor=(1, 0, 0.5, 1))
        plt.setp(autotexts, size=8, weight="bold")

        # Embed the chart in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()
        canvas.get_tk_widget().grid(row=4, column=2, padx=10)

        plt.close(fig) # Close the figure to avoid a memory leak

if __name__ == "__main__":
    # Initialize the main Tkinter window and start the application loop.
    root = tk.Tk()
    app = FinanceTrackerGUI(root)
    root.mainloop()