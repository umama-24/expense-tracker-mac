import json
import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog


class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("820x560")
        self.root.configure(bg="#ECEFF1")

        self.file_name = "expenses.json"
        self.expenses = self.load_expenses()

        self.setup_ui()
        self.refresh_table()

    # ------------------ DATA MANAGEMENT ------------------

    def load_expenses(self):
        if not os.path.exists(self.file_name):
            return []
        try:
            with open(self.file_name, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError):
            return []

    def save_expenses(self):
        try:
            with open(self.file_name, "w") as file:
                json.dump(self.expenses, file, indent=4)
        except IOError as e:
            messagebox.showerror("Error", f"Failed to save data: {e}")

    # ------------------ UI SETUP ------------------

    def make_mac_button(self, parent, text, color, command):
        """Creates custom colored canvas button for macOS"""
        canvas = tk.Canvas(parent, height=32, bg="#ECEFF1", highlightthickness=0)
        
        def draw(event=None):
            canvas.delete("all")
            w = canvas.winfo_width()
            canvas.create_rectangle(2, 2, w - 2, 30, fill=color, outline="#B0BEC5", width=1)
            canvas.create_text(w / 2, 16, text=text, fill="white", font=("Arial", 9, "bold"))

        canvas.bind("<Configure>", draw)
        canvas.bind("<Button-1>", lambda e: command())
        return canvas

    def setup_ui(self):
        # Header Banner
        header = tk.Label(
            self.root,
            text="Expense Tracker System",
            font=("Arial", 18, "bold"),
            bg="#2B3E50",
            fg="white",
            pady=12
        )
        header.pack(fill="x")

        # Input Container
        input_container = tk.Frame(self.root, bg="white", highlightthickness=1, highlightbackground="#CFD8DC")
        input_container.pack(fill="x", padx=15, pady=10, ipady=5)

        input_container.columnconfigure(1, weight=1)
        input_container.columnconfigure(3, weight=1)

        # Row 0: Date & Category
        lbl_date = tk.Label(input_container, text="Date", font=("Arial", 10, "bold"), bg="white", fg="black")
        lbl_date.grid(row=0, column=0, padx=(15, 5), pady=8, sticky="w")

        self.entry_date = tk.Entry(input_container, font=("Arial", 10), bg="white", fg="black", relief="solid", bd=1)
        self.entry_date.grid(row=0, column=1, padx=(0, 20), pady=8, sticky="ew")
        self.entry_date.insert(0, datetime.now().strftime("%Y-%m-%d"))

        lbl_cat = tk.Label(input_container, text="Category", font=("Arial", 10, "bold"), bg="white", fg="black")
        lbl_cat.grid(row=0, column=2, padx=(10, 5), pady=8, sticky="w")

        self.combo_category = ttk.Combobox(
            input_container,
            values=["Food", "Health", "Education", "Transport", "Utilities", "Shopping", "Other"],
            font=("Arial", 10)
        )
        self.combo_category.grid(row=0, column=3, padx=(0, 15), pady=8, sticky="ew")

        # Row 1: Description & Amount
        lbl_desc = tk.Label(input_container, text="Description", font=("Arial", 10, "bold"), bg="white", fg="black")
        lbl_desc.grid(row=1, column=0, padx=(15, 5), pady=8, sticky="w")

        self.entry_desc = tk.Entry(input_container, font=("Arial", 10), bg="white", fg="black", relief="solid", bd=1)
        self.entry_desc.grid(row=1, column=1, padx=(0, 20), pady=8, sticky="ew")

        lbl_amt = tk.Label(input_container, text="Amount", font=("Arial", 10, "bold"), bg="white", fg="black")
        lbl_amt.grid(row=1, column=2, padx=(10, 5), pady=8, sticky="w")

        self.entry_amount = tk.Entry(input_container, font=("Arial", 10), bg="white", fg="black", relief="solid", bd=1)
        self.entry_amount.grid(row=1, column=3, padx=(0, 15), pady=8, sticky="ew")

        # Action Buttons Frame (Spans full width across line)
        btn_frame = tk.Frame(self.root, bg="#ECEFF1")
        btn_frame.pack(fill="x", padx=15, pady=5)

        for col_idx in range(6):
            btn_frame.columnconfigure(col_idx, weight=1)

        # Mac-Friendly Vibrant Colored Buttons
        b1 = self.make_mac_button(btn_frame, "Add Expense", "#27AE60", self.add_expense)
        b1.grid(row=0, column=0, padx=3, sticky="ew")

        b2 = self.make_mac_button(btn_frame, "Update", "#7F8C8D", self.update_expense)
        b2.grid(row=0, column=1, padx=3, sticky="ew")

        b3 = self.make_mac_button(btn_frame, "Delete", "#E74C3C", self.delete_expense)
        b3.grid(row=0, column=2, padx=3, sticky="ew")

        b4 = self.make_mac_button(btn_frame, "Search", "#8E44AD", self.search_expenses)
        b4.grid(row=0, column=3, padx=3, sticky="ew")

        b5 = self.make_mac_button(btn_frame, "Monthly Report", "#E67E22", self.monthly_report)
        b5.grid(row=0, column=4, padx=3, sticky="ew")

        b6 = self.make_mac_button(btn_frame, "Total Spending", "#16A085", self.show_total_spending)
        b6.grid(row=0, column=5, padx=3, sticky="ew")

        # Table Section
        table_frame = tk.Frame(self.root, bg="#ECEFF1")
        table_frame.pack(fill="both", expand=True, padx=15, pady=10)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background="#E0E0E0", foreground="black")
        style.configure("Treeview", font=("Arial", 10), rowheight=24, background="white", fieldbackground="white")

        columns = ("date", "category", "description", "amount")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")

        self.tree.heading("date", text="Date")
        self.tree.heading("category", text="Category")
        self.tree.heading("description", text="Description")
        self.tree.heading("amount", text="Amount")

        self.tree.column("date", width=120, anchor="w")
        self.tree.column("category", width=150, anchor="w")
        self.tree.column("description", width=300, anchor="w")
        self.tree.column("amount", width=120, anchor="e")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self.on_select_item)

    # ------------------ OPERATIONS & HELPER FUNCTIONS ------------------

    def validate_inputs(self):
        date_str = self.entry_date.get().strip()
        category = self.combo_category.get().strip()
        description = self.entry_desc.get().strip()
        amount_str = self.entry_amount.get().strip()

        if not date_str or not category or not amount_str:
            messagebox.showwarning("Warning", "Date, Category, and Amount are required.")
            return None

        try:
            amount = float(amount_str)
        except ValueError:
            messagebox.showwarning("Warning", "Amount must be a valid number.")
            return None

        return {
            "date": date_str,
            "category": category,
            "description": description,
            "amount": amount
        }

    def add_expense(self):
        data = self.validate_inputs()
        if not data:
            return

        data["id"] = max([x.get("id", 0) for x in self.expenses], default=0) + 1
        self.expenses.append(data)
        self.save_expenses()
        self.refresh_table()
        self.clear_entries()

    def update_expense(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a record from the table to update.")
            return

        data = self.validate_inputs()
        if not data:
            return

        idx = self.tree.index(selected[0])
        record_id = self.displayed_data[idx]["id"]

        for exp in self.expenses:
            if exp.get("id") == record_id:
                exp.update(data)
                break

        self.save_expenses()
        self.refresh_table()
        self.clear_entries()

    def delete_expense(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a record from the table to delete.")
            return

        idx = self.tree.index(selected[0])
        record_id = self.displayed_data[idx]["id"]

        self.expenses = [exp for exp in self.expenses if exp.get("id") != record_id]
        self.save_expenses()
        self.refresh_table()
        self.clear_entries()

    def search_expenses(self):
        query = simpledialog.askstring("Search", "Enter keyword to search (Title/Category/Date):")
        if query is None:
            return
        query = query.strip().lower()
        if not query:
            self.refresh_table()
            return

        filtered = [
            exp for exp in self.expenses
            if query in exp["category"].lower() or query in exp["description"].lower() or query in exp["date"].lower()
        ]
        self.refresh_table(data_to_display=filtered)

    def monthly_report(self):
        month_query = simpledialog.askstring("Monthly Report", "Enter Year-Month (e.g., YYYY-MM):")
        if not month_query:
            return
        
        filtered = [exp for exp in self.expenses if exp["date"].startswith(month_query.strip())]
        total = sum(exp["amount"] for exp in filtered)
        messagebox.showinfo("Monthly Report", f"Total Spending for {month_query}: ${total:.2f}")

    def show_total_spending(self):
        total = sum(exp["amount"] for exp in self.expenses)
        messagebox.showinfo("Total Spending", f"Overall Total Spending: ${total:.2f}")

    def refresh_table(self, data_to_display=None):
        for row in self.tree.get_children():
            self.tree.delete(row)

        self.displayed_data = data_to_display if data_to_display is not None else self.expenses

        for exp in self.displayed_data:
            self.tree.insert(
                "",
                "end",
                values=(
                    exp["date"],
                    exp["category"],
                    exp["description"],
                    f"{exp['amount']:.1f}"
                )
            )

    def on_select_item(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        idx = self.tree.index(selected[0])
        record = self.displayed_data[idx]

        self.entry_date.delete(0, tk.END)
        self.entry_date.insert(0, record["date"])

        self.combo_category.set(record["category"])

        self.entry_desc.delete(0, tk.END)
        self.entry_desc.insert(0, record["description"])

        self.entry_amount.delete(0, tk.END)
        self.entry_amount.insert(0, str(record["amount"]))

    def clear_entries(self):
        self.entry_date.delete(0, tk.END)
        self.entry_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.combo_category.set("")
        self.entry_desc.delete(0, tk.END)
        self.entry_amount.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()