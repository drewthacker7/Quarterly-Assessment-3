import tkinter as tk
import sqlite3
from tkinter import messagebox

# Fetch quiz categories (table names) from the database
def get_categories():
    conn = sqlite3.connect("quiz_bowl.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    categories = [row[0] for row in cursor.fetchall()]
    conn.close()
    return categories

# Handle selection of a category
def start_quiz(category):
    messagebox.showinfo("Quiz Start", f"You selected: {category}\n(Quiz screen coming soon!)")

# Build category selection window
def open_category_selection():
    cat_window = tk.Toplevel()
    cat_window.title("Select Quiz Category")
    cat_window.geometry("300x300")

    tk.Label(cat_window, text="Choose a Quiz Category", font=("Helvetica", 14)).pack(pady=10)

    for cat in get_categories():
        tk.Button(cat_window, text=cat.replace("_", " ").title(), width=25,
                  command=lambda c=cat: start_quiz(c)).pack(pady=5)

# Launch main menu
def main():
    root = tk.Tk()
    root.title("Quiz Bowl App")
    root.geometry("400x250")

    tk.Label(root, text="Welcome to the Quiz Bowl App", font=("Helvetica", 16)).pack(pady=30)

    tk.Button(root, text="Admin Login", width=20, height=2,
              command=lambda: messagebox.showinfo("Admin", "Admin interface coming soon!")).pack(pady=10)

    tk.Button(root, text="Take a Quiz", width=20, height=2,
              command=open_category_selection).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
