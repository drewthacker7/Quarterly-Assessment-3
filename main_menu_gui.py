import tkinter as tk
from tkinter import messagebox

def open_admin():
    messagebox.showinfo("Admin", "Admin interface coming soon!")

def open_user():
    messagebox.showinfo("Quiz Taker", "User quiz interface coming soon!")

# Main window
root = tk.Tk()
root.title("Quiz Bowl App")
root.geometry("400x250")

# Title label
label = tk.Label(root, text="Welcome to the Quiz Bowl App", font=("Helvetica", 16))
label.pack(pady=30)

# Admin Button
admin_button = tk.Button(root, text="Admin Login", width=20, height=2, command=open_admin)
admin_button.pack(pady=10)

# User Button
user_button = tk.Button(root, text="Take a Quiz", width=20, height=2, command=open_user)
user_button.pack(pady=10)

# Run the app
root.mainloop()
