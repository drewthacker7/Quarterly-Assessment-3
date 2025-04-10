import tkinter as tk
from tkinter import messagebox
import sqlite3

# Insert question into selected table
def insert_question(category, question, a, b, c, d, correct):
    conn = sqlite3.connect("quiz_bowl.db")
    cursor = conn.cursor()
    cursor.execute(f"""
        INSERT INTO {category} (question, option_a, option_b, option_c, option_d, correct_option)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (question, a, b, c, d, correct))
    conn.commit()
    conn.close()

# Get all quiz categories from the database
def get_categories():
    conn = sqlite3.connect("quiz_bowl.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    return tables

# Open the Add Question form
def open_add_question():
    win = tk.Toplevel()
    win.title("Add Question")
    win.geometry("400x500")

    categories = get_categories()

    tk.Label(win, text="Select Category:").pack()
    category_var = tk.StringVar()
    category_menu = tk.OptionMenu(win, category_var, *categories)
    category_menu.pack()

    tk.Label(win, text="Question Text:").pack()
    question_entry = tk.Text(win, height=3, width=40)
    question_entry.pack()

    entries = []
    for label in ["Option A", "Option B", "Option C", "Option D"]:
        tk.Label(win, text=label + ":").pack()
        entry = tk.Entry(win, width=40)
        entry.pack()
        entries.append(entry)

    correct_answer_var = tk.StringVar()
    tk.Label(win, text="Correct Option (A/B/C/D):").pack()
    correct_menu = tk.OptionMenu(win, correct_answer_var, "A", "B", "C", "D")
    correct_menu.pack()

    def submit():
        cat = category_var.get()
        question = question_entry.get("1.0", tk.END).strip()
        options = [e.get() for e in entries]
        correct = correct_answer_var.get()

        if not (cat and question and all(options) and correct):
            messagebox.showerror("Error", "Please complete all fields.")
            return

        insert_question(cat, question, *options, correct)
        messagebox.showinfo("Success", "Question added successfully!")
        win.destroy()

    tk.Button(win, text="Submit", command=submit).pack(pady=10)

# Test window hook
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Test Add Question")
    root.geometry("200x100")
    tk.Button(root, text="Add Question", command=open_add_question).pack(pady=30)
    root.mainloop()
