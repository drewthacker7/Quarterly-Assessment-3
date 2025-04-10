import tkinter as tk
from tkinter import messagebox
import sqlite3
import random

def load_questions(category):
    conn = sqlite3.connect("quiz_bowl.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT question, option_a, option_b, option_c, option_d, correct_option FROM {category}")
    questions = cursor.fetchall()
    conn.close()
    random.shuffle(questions)
    return questions

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

# Category selection window
def get_categories():
    conn = sqlite3.connect("quiz_bowl.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    categories = [row[0] for row in cursor.fetchall()]
    conn.close()
    return categories

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

# Main menu
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
