from tkinter import *
from tkinter import messagebox
import db
from utils import hash_password
from signup import SignupPage
from dashboard_admin import open_admin_dashboard
from dashboard_worker import open_worker_dashboard
from dashboard_user import UserDashboard
from datetime import datetime

class LoginPage:
    def __init__(self, root):
        self.root = root
        root.configure(bg="#2b2b2b")

        Label(root, text="🎬 Cinema App Login", font=("Helvetica", 18), fg="white", bg="#2b2b2b").pack(pady=20)

        self.username = Entry(root, font=("Arial", 12))
        self.username.pack(pady=5)
        self.username.insert(0, "Username")

        self.password = Entry(root, font=("Arial", 12), show="*")
        self.password.pack(pady=5)
        self.password.insert(0, "Password")

        Button(root, text="Login", command=self.login, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=10)
        Button(root, text="Sign Up", command=self.open_signup, bg="#2196F3", fg="white", font=("Arial", 12)).pack()

    def login(self):
        user = self.username.get()
        pwd = self.password.get()
        hashed_pwd = hash_password(pwd)

        conn = db.connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, role FROM users WHERE username=%s AND password=%s", (user, hashed_pwd))
        result = cursor.fetchone()
        conn.close()

        if result:
            user_id = result[0] if isinstance(result, (list, tuple)) else result
            role = result[1] if isinstance(result, (list, tuple)) else result
            self.root.destroy()
            if role == "admin":
                open_admin_dashboard()
            elif role == "worker":
                open_worker_dashboard()
            else:
                UserDashboard(user_id)
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def open_signup(self):
        self.root.destroy()
        root = Tk()
        root.title("Signup")
        root.geometry("400x300")
        SignupPage(root)
        root.mainloop()

if __name__ == "__main__":
    root = Tk()
    LoginPage(root)
    root.mainloop()
