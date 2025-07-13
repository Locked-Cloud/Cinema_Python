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

        Label(root, text="\ud83c\udfac Cinema App Login", font=("Helvetica", 18), fg="white", bg="#2b2b2b").pack(pady=20)

        self.username = Entry(root, font=("Arial", 12), fg="grey")
        self.username.pack(pady=5)
        self.username.insert(0, "Username")
        self.username.bind("<FocusIn>", self.clear_username_placeholder)
        self.username.bind("<FocusOut>", self.restore_username_placeholder)

        self.password = Entry(root, font=("Arial", 12), fg="grey")
        self.password.pack(pady=5)
        self.password.insert(0, "Password")
        self.password.bind("<FocusIn>", self.clear_password_placeholder)
        self.password.bind("<FocusOut>", self.restore_password_placeholder)
        self.show_password = False

        self.show_pwd_btn = Button(root, text="Show Password", command=self.toggle_password, bg="#757575", fg="white", font=("Arial", 10))
        self.show_pwd_btn.pack(pady=2)

        Button(root, text="Login", command=self.login, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=10)
        Button(root, text="Sign Up", command=self.open_signup, bg="#2196F3", fg="white", font=("Arial", 12)).pack()
        Button(root, text="Forgot Password?", command=self.open_reset_password, bg="#FF9800", fg="white", font=("Arial", 10)).pack(pady=5)

    def clear_username_placeholder(self, event):
        if self.username.get() == "Username":
            self.username.delete(0, END)
            self.username.config(fg="black")

    def restore_username_placeholder(self, event):
        if not self.username.get():
            self.username.insert(0, "Username")
            self.username.config(fg="grey")

    def clear_password_placeholder(self, event):
        if self.password.get() == "Password":
            self.password.delete(0, END)
            self.password.config(show="*" if not self.show_password else "")
            self.password.config(fg="black")

    def restore_password_placeholder(self, event):
        if not self.password.get():
            self.password.insert(0, "Password")
            self.password.config(show="")
            self.password.config(fg="grey")

    def toggle_password(self):
        self.show_password = not self.show_password
        if self.show_password:
            if self.password.get() != "Password":
                self.password.config(show="")
            self.show_pwd_btn.config(text="Hide Password")
        else:
            if self.password.get() != "Password":
                self.password.config(show="*")
            self.show_pwd_btn.config(text="Show Password")

    def login(self):
        user = self.username.get()
        pwd = self.password.get()
        if user == "Username" or not user or pwd == "Password" or not pwd:
            messagebox.showerror("Error", "Please enter both username and password.")
            return
        hashed_pwd = hash_password(pwd)
        try:
            with db.connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, role FROM users WHERE username=%s AND password=%s", (user, hashed_pwd))
                result = cursor.fetchone()
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
        except Exception as e:
            messagebox.showerror("Error", f"Login failed: {e}")

    def open_signup(self):
        self.root.destroy()
        root = Tk()
        root.title("Signup")
        root.geometry("400x300")
        SignupPage(root)
        root.mainloop()

    def open_reset_password(self):
        self.root.destroy()
        root = Tk()
        root.title("Reset Password")
        root.geometry("400x300")
        ResetPasswordPage(root)
        root.mainloop()

class ResetPasswordPage:
    def __init__(self, root):
        self.root = root
        root.configure(bg="#2b2b2b")
        from tkinter import Label, Entry, Button, messagebox
        Label(root, text="🔑 Reset Password", font=("Helvetica", 18), fg="white", bg="#2b2b2b").pack(pady=20)
        self.username = Entry(root, font=("Arial", 12))
        self.username.pack(pady=5)
        self.username.insert(0, "Username")
        self.new_password = Entry(root, font=("Arial", 12), show="*")
        self.new_password.pack(pady=5)
        self.new_password.insert(0, "New Password")
        self.confirm_password = Entry(root, font=("Arial", 12), show="*")
        self.confirm_password.pack(pady=5)
        self.confirm_password.insert(0, "Confirm Password")
        Button(root, text="Reset Password", command=self.reset_password, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=10)
    def reset_password(self):
        from utils import hash_password
        import db
        user = self.username.get()
        pwd = self.new_password.get()
        confirm_pwd = self.confirm_password.get()
        if not user or not pwd or not confirm_pwd:
            from tkinter import messagebox
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        if pwd != confirm_pwd:
            from tkinter import messagebox
            messagebox.showerror("Error", "Passwords do not match.")
            return
        if len(pwd) < 6:
            from tkinter import messagebox
            messagebox.showerror("Error", "Password must be at least 6 characters.")
            return
        hashed_pwd = hash_password(pwd)
        try:
            with db.connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET password=%s WHERE username=%s", (hashed_pwd, user))
                if cursor.rowcount == 0:
                    from tkinter import messagebox
                    messagebox.showerror("Error", "Username not found.")
                    return
                conn.commit()
            from tkinter import messagebox
            messagebox.showinfo("Success", "Password reset. Please login.")
            self.root.destroy()
            from login import LoginPage
            root = Tk()
            LoginPage(root)
            root.mainloop()
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Error", f"Failed to reset password: {e}")

if __name__ == "__main__":
    root = Tk()
    LoginPage(root)
    root.mainloop()
