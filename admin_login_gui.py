import tkinter as tk
from tkinter import messagebox

# Hardcoded admin credentials
ADMIN_USERNAME = "QuizMaster"
ADMIN_PASSWORD = "123456789"

def open_admin_dashboard():
    messagebox.showinfo("Admin", "Welcome to the Admin Dashboard! (Coming next)")

def authenticate(username_entry, password_entry, window):
    username = username_entry.get()
    password = password_entry.get()
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
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

    login_button = tk.Button(login_window, text="Login", command=lambda: authenticate(username_entry, password_entry, login_window))
    login_button.pack(pady=10)

# Main Menu Launcher
def main():
    root = tk.Tk()
    root.title("Quiz Bowl App")
    root.geometry("400x250")

    tk.Label(root, text="Welcome to the Quiz Bowl App", font=("Helvetica", 16)).pack(pady=30)

    tk.Button(root, text="Admin Login", width=20, height=2,
              command=open_admin_login).pack(pady=10)

    tk.Button(root, text="Take a Quiz", width=20, height=2,
              command=lambda: messagebox.showinfo("Quiz", "Quiz interface coming soon!")).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
