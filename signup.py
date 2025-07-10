from tkinter import *
from tkinter import messagebox
from utils import hash_password
import db
# from login import LoginPage  # REMOVE this import

class SignupPage:
    def __init__(self, root):
        self.root = root
        root.configure(bg="#2b2b2b")

        Label(root, text="📋 Create Account", font=("Helvetica", 18), fg="white", bg="#2b2b2b").pack(pady=20)

        self.username = Entry(root, font=("Arial", 12))
        self.username.pack(pady=5)
        self.username.insert(0, "Username")

        self.password = Entry(root, font=("Arial", 12), show="*")
        self.password.pack(pady=5)
        self.password.insert(0, "Password")

        self.role = StringVar(value="user")
        OptionMenu(root, self.role, "admin", "worker", "user").pack(pady=10)

        Button(root, text="Sign Up", command=self.signup, bg="#FF5722", fg="white", font=("Arial", 12)).pack(pady=10)

    def signup(self):
        user = self.username.get()
        pwd = self.password.get()
        role = self.role.get()

        if not user or not pwd:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        hashed_pwd = hash_password(pwd)
        try:
            conn = db.connect_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (user, hashed_pwd, role))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Account created.")
            self.root.destroy()
            root = Tk()
            root.geometry("400x300")
            from login import LoginPage  # <-- moved import here
            LoginPage(root)
            root.mainloop()
        except:
            messagebox.showerror("Error", "Username already exists.")
