from tkinter import *
from tkinter import messagebox
from utils import hash_password
import db
# from login import LoginPage  # REMOVE this import

class SignupPage:
    def __init__(self, root):
        self.root = root
        root.configure(bg="#2b2b2b")

        Label(root, text="\ud83d\udccb Create Account", font=("Helvetica", 18), fg="white", bg="#2b2b2b").pack(pady=20)

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

        self.confirm_password = Entry(root, font=("Arial", 12), fg="grey")
        self.confirm_password.pack(pady=5)
        self.confirm_password.insert(0, "Confirm Password")
        self.confirm_password.bind("<FocusIn>", self.clear_confirm_password_placeholder)
        self.confirm_password.bind("<FocusOut>", self.restore_confirm_password_placeholder)

        self.show_pwd_btn = Button(root, text="Show Passwords", command=self.toggle_password, bg="#757575", fg="white", font=("Arial", 10))
        self.show_pwd_btn.pack(pady=2)

        self.role = StringVar(value="user")
        OptionMenu(root, self.role, "admin", "worker", "user").pack(pady=10)

        Button(root, text="Sign Up", command=self.signup, bg="#FF5722", fg="white", font=("Arial", 12)).pack(pady=10)

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
            self.password.config(show="*" if self.show_password else "")
            self.password.config(fg="black")

    def restore_password_placeholder(self, event):
        if not self.password.get():
            self.password.insert(0, "Password")
            self.password.config(show="")
            self.password.config(fg="grey")

    def clear_confirm_password_placeholder(self, event):
        if self.confirm_password.get() == "Confirm Password":
            self.confirm_password.delete(0, END)
            self.confirm_password.config(show="*" if self.show_password else "")
            self.confirm_password.config(fg="black")

    def restore_confirm_password_placeholder(self, event):
        if not self.confirm_password.get():
            self.confirm_password.insert(0, "Confirm Password")
            self.confirm_password.config(show="")
            self.confirm_password.config(fg="grey")

    def toggle_password(self):
        self.show_password = not self.show_password
        if self.show_password:
            if self.password.get() != "Password":
                self.password.config(show="")
            if self.confirm_password.get() != "Confirm Password":
                self.confirm_password.config(show="")
            self.show_pwd_btn.config(text="Hide Passwords")
        else:
            if self.password.get() != "Password":
                self.password.config(show="*")
            if self.confirm_password.get() != "Confirm Password":
                self.confirm_password.config(show="*")
            self.show_pwd_btn.config(text="Show Passwords")

    def is_valid_username(self, username):
        return len(username) >= 3 and username.isalnum()

    def is_strong_password(self, password):
        import re
        if len(password) < 6:
            return False
        if not re.search(r"[A-Z]", password):
            return False
        if not re.search(r"[a-z]", password):
            return False
        if not re.search(r"[0-9]", password):
            return False
        if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\",.<>/?]", password):
            return False
        return True

    def signup(self):
        user = self.username.get()
        pwd = self.password.get()
        confirm_pwd = self.confirm_password.get()
        role = self.role.get()

        if user == "Username" or not user or pwd == "Password" or not pwd or confirm_pwd == "Confirm Password" or not confirm_pwd:
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        if not self.is_valid_username(user):
            messagebox.showerror("Error", "Username must be at least 3 characters and alphanumeric.")
            return
        if not self.is_strong_password(pwd):
            messagebox.showerror("Error", "Password must be at least 6 characters, include uppercase, lowercase, number, and special character.")
            return
        if pwd != confirm_pwd:
            messagebox.showerror("Error", "Passwords do not match.")
            return
        hashed_pwd = hash_password(pwd)
        try:
            with db.connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (user, hashed_pwd, role))
                conn.commit()
            messagebox.showinfo("Success", "Account created.")
            self.root.destroy()
            root = Tk()
            root.geometry("400x300")
            from login import LoginPage  # <-- moved import here
            LoginPage(root)
            root.mainloop()
        except Exception as e:
            if 'unique' in str(e).lower() or 'duplicate' in str(e).lower():
                messagebox.showerror("Error", "Username already exists.")
            else:
                messagebox.showerror("Error", f"Signup failed: {e}")
