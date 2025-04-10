import tkinter as tk
from tkinter import messagebox
import sqlite3
import random

# ===== DATABASE HELPERS =====

def get_categories():
    conn = sqlite3.connect("quiz_bowl.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    categories = [row[0] for row in cursor.fetchall()]
    conn.close()
    return categories

def load_questions(category):
    conn = sqlite3.connect("quiz_bowl.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT question, option_a, option_b, option_c, option_d, correct_option FROM {category}")
    questions = cursor.fetchall()
    conn.close()
    random.shuffle(questions)
    return questions

def insert_question(category, question, a, b, c, d, correct):
    conn = sqlite3.connect("quiz_bowl.db")
    cursor = conn.cursor()
    cursor.execute(f"""
        INSERT INTO {category} (question, option_a, option_b, option_c, option_d, correct_option)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (question, a, b, c, d, correct))
    conn.commit()
    conn.close()

def fetch_questions(category):
    conn = sqlite3.connect("quiz_bowl.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT id, question FROM {category}")
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_question(category, qid):
    conn = sqlite3.connect("quiz_bowl.db")
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {category} WHERE id = ?", (qid,))
    conn.commit()
    conn.close()

# ===== QUIZ FLOW =====

class Quiz:
    def __init__(self, master, category):
        self.master = master
        self.category = category
        self.questions = load_questions(category)
        self.index = 0
        self.score = 0
        self.answered = False

        self.question_label = tk.Label(master, text="", wraplength=450, font=("Helvetica", 14))
        self.question_label.pack(pady=20)

        self.var = tk.StringVar()
        self.options = []
        for val in ["A", "B", "C", "D"]:
            btn = tk.Radiobutton(master, text="", variable=self.var, value=val, font=("Helvetica", 12))
            btn.pack(anchor="w")
            self.options.append(btn)

        self.feedback = tk.Label(master, text="", font=("Helvetica", 12))
        self.feedback.pack(pady=5)

        self.next_button = tk.Button(master, text="Submit", command=self.submit_or_next)
        self.next_button.pack(pady=10)

        self.display_question()

    def display_question(self):
        if self.index < len(self.questions):
            q = self.questions[self.index]
            self.question_label.config(text=f"Q{self.index + 1}: {q[0]}")
            for i, opt in enumerate(q[1:5]):
                self.options[i].config(text=f"{chr(65+i)}. {opt}")
            self.var.set(None)
            self.feedback.config(text="")
            self.answered = False
            self.next_button.config(text="Submit")
        else:
            self.question_label.config(text=f"Quiz Complete! Your score: {self.score}/{len(self.questions)}")
            for btn in self.options:
                btn.pack_forget()
            self.feedback.config(text="")
            self.next_button.pack_forget()

    def submit_or_next(self):
        if not self.answered:
            self.check_answer()
        else:
            self.index += 1
            self.display_question()

    def check_answer(self):
        if not self.var.get():
            messagebox.showwarning("Select an answer", "Please choose an answer before submitting.")
            return
        correct = self.questions[self.index][5]
        if self.var.get() == correct:
            self.score += 1
            self.feedback.config(text="Correct!", fg="green")
        else:
            self.feedback.config(text=f"Incorrect. Correct answer was {correct}.", fg="red")
        self.answered = True
        self.next_button.config(text="Next")

# ===== QUIZ UI =====

def start_quiz(category):
    quiz_window = tk.Toplevel()
    quiz_window.title(f"Quiz: {category.replace('_', ' ').title()}")
    quiz_window.geometry("500x400")
    Quiz(quiz_window, category)

def open_category_selection():
    cat_window = tk.Toplevel()
    cat_window.title("Select Quiz Category")
    cat_window.geometry("300x300")
    tk.Label(cat_window, text="Choose a Quiz Category", font=("Helvetica", 14)).pack(pady=10)
    for cat in get_categories():
        tk.Button(cat_window, text=cat.replace("_", " ").title(), width=25,
                  command=lambda c=cat: start_quiz(c)).pack(pady=5)

# ===== ADMIN FEATURES =====

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

def open_view_edit_delete():
    win = tk.Toplevel()
    win.title("Edit/Delete Questions")
    win.geometry("500x400")

    categories = get_categories()

    tk.Label(win, text="Select Category:").pack()
    category_var = tk.StringVar()
    category_menu = tk.OptionMenu(win, category_var, *categories)
    category_menu.pack()

    listbox = tk.Listbox(win, width=60)
    listbox.pack(pady=10)

    def load_questions():
        listbox.delete(0, tk.END)
        cat = category_var.get()
        if not cat:
            return
        for qid, qtext in fetch_questions(cat):
            listbox.insert(tk.END, f"{qid}: {qtext[:60]}")

    def delete_selected():
        selection = listbox.curselection()
        if not selection:
            return
        index = selection[0]
        selected = listbox.get(index)
        qid = int(selected.split(":")[0])
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this question?")
        if confirm:
            delete_question(category_var.get(), qid)
            load_questions()
            messagebox.showinfo("Deleted", "Question deleted successfully.")

    tk.Button(win, text="Load Questions", command=load_questions).pack()
    tk.Button(win, text="Delete Selected Question", command=delete_selected).pack(pady=5)

def open_admin_dashboard():
    dash = tk.Toplevel()
    dash.title("Admin Dashboard")
    dash.geometry("300x300")

    tk.Label(dash, text="Admin Dashboard", font=("Helvetica", 14)).pack(pady=10)
    tk.Button(dash, text="Add Question", width=25, command=open_add_question).pack(pady=5)
    tk.Button(dash, text="View/Edit/Delete Questions", width=25, command=open_view_edit_delete).pack(pady=5)
    tk.Button(dash, text="Return to Main Menu", width=25, command=dash.destroy).pack(pady=5)

def authenticate(username_entry, password_entry, window):
    if username_entry.get() == "QuizMaster" and password_entry.get() == "123456789":
        window.destroy()
        open_admin_dashboard()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

def open_admin_login():
    login_window = tk.Toplevel()
    login_window.title("Admin Login")
    login_window.geometry("300x200")

    tk.Label(login_window, text="Admin Login", font=("Helvetica", 14)).pack(pady=10)
    tk.Label(login_window, text="Username").pack()
    username_entry = tk.Entry(login_window)
    username_entry.pack()
    tk.Label(login_window, text="Password").pack()
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack()

    tk.Button(login_window, text="Login", command=lambda: authenticate(username_entry, password_entry, login_window)).pack(pady=10)

# ===== MAIN MENU =====

def main():
    root = tk.Tk()
    root.title("Quiz Bowl App")
    root.geometry("400x250")

    tk.Label(root, text="Welcome to the Quiz Bowl App", font=("Helvetica", 16)).pack(pady=30)

    tk.Button(root, text="Admin Login", width=20, height=2, command=open_admin_login).pack(pady=10)
    tk.Button(root, text="Take a Quiz", width=20, height=2, command=open_category_selection).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
